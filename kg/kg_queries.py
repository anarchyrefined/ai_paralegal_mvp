import os
import logging
from typing import List, Dict, Any

os.environ.setdefault("CHROMA_TELEMETRY", "false")
os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")

logger = logging.getLogger(__name__)

try:
    import chromadb
except Exception as exc:  # pragma: no cover - optional dependency
    chromadb = None  # type: ignore
    logger.warning(f"ChromaDB unavailable: {exc}. Vector search disabled.")

import pandas as pd

class HybridSearch:
    def __init__(self, graph_store="falkordb", vector_store_path="./chroma_db"):
        self.chroma_client = None
        self.vector_store = None
        if chromadb:
            try:
                self.chroma_client = chromadb.PersistentClient(path=vector_store_path)
                self.vector_store = self.chroma_client.get_or_create_collection(name="legal_docs")
            except Exception as exc:  # pragma: no cover - telemetry/offline issues
                logger.warning(f"ChromaDB client disabled: {exc}")

        # Placeholder for GraphRAG SDK integration - will be implemented when SDK is available
        self.kg = None  # Placeholder

        self.nodes_df = None
        self.edges_df = None
        self._load_kg_data()

    def _load_kg_data(self):
        """Load knowledge graph data from CSV files."""
        try:
            self.nodes_df = pd.read_csv("kg/nodes_final.csv")
            # Handle empty edges file gracefully
            try:
                self.edges_df = pd.read_csv("kg/edges_final.csv")
                if self.edges_df.empty:
                    self.edges_df = pd.DataFrame(columns=['source', 'target', 'relationship', 'proof'])
            except pd.errors.EmptyDataError:
                self.edges_df = pd.DataFrame(columns=['source', 'target', 'relationship', 'proof'])
            logger.info(f"Loaded KG with {len(self.nodes_df)} nodes and {len(self.edges_df)} edges")
        except FileNotFoundError:
            logger.warning("KG CSV files not found. Run kg/refine_kg.py first.")
            self.nodes_df = pd.DataFrame()
            self.edges_df = pd.DataFrame()

    def hybrid_search(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Perform hybrid search combining graph traversal and vector similarity.
        """
        results = {
            "graph_results": [],
            "vector_results": [],
            "combined_insights": []
        }

        # Graph-based search using KnowledgeGraph (placeholder)
        try:
            if self.kg:
                graph_results = self.kg.query(query, method="graph", top_k=top_k)
                results["graph_results"] = graph_results if graph_results else []
            else:
                results["graph_results"] = []  # Placeholder until GraphRAG SDK is properly integrated
        except Exception as e:
            logger.error(f"Graph search failed: {e}")
            results["graph_results"] = []

        # Simple text-based search on nodes for now (vector store initialization issues)
        try:
            node_matches = self.nodes_df[
                self.nodes_df['name'].str.contains(query, case=False, na=False) |
                self.nodes_df['type'].str.contains(query, case=False, na=False)
            ].head(top_k).to_dict('records')
            results["vector_results"] = node_matches
        except Exception as e:
            logger.error(f"Node search failed: {e}")
            results["vector_results"] = []

        # Combine insights from KG structure
        if not self.nodes_df.empty:
            combined_insights = self._combine_kg_insights(query, top_k)
            results["combined_insights"] = combined_insights

        return results

    def _combine_kg_insights(self, query: str, top_k: int) -> List[Dict]:
        """
        Combine insights from nodes and edges based on query relevance.
        """
        insights = []

        # Find relevant nodes by type and name matching
        query_lower = query.lower()
        relevant_nodes = self.nodes_df[
            self.nodes_df['name'].str.lower().str.contains(query_lower, na=False) |
            self.nodes_df['type'].str.lower().str.contains(query_lower, na=False)
        ].head(top_k)

        for _, node in relevant_nodes.iterrows():
            # Find connected edges
            connected_edges = self.edges_df[
                (self.edges_df['source'] == node['id']) |
                (self.edges_df['target'] == node['id'])
            ]

            insight = {
                "node": {
                    "id": node['id'],
                    "type": node['type'],
                    "name": node['name']
                },
                "connections": len(connected_edges),
                "relationships": connected_edges['relationship'].tolist() if not connected_edges.empty else [],
                "proof_tokens": connected_edges['proof'].tolist() if not connected_edges.empty else []
            }
            insights.append(insight)

        return insights

    def get_kg_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph."""
        if self.nodes_df.empty:
            return {"error": "KG data not loaded"}

        stats = {
            "total_nodes": len(self.nodes_df),
            "total_edges": len(self.edges_df),
            "node_types": self.nodes_df['type'].value_counts().to_dict(),
            "edge_types": self.edges_df['relationship'].value_counts().to_dict() if not self.edges_df.empty else {},
            "avg_connections": self.edges_df.groupby('source').size().mean() if not self.edges_df.empty else 0
        }
        return stats

# Global instance for API use
hybrid_search = HybridSearch()
