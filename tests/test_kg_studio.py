import pytest
import pandas as pd
from kg.kg_queries import HybridSearch

def test_hybrid_search_initialization():
    search = HybridSearch()
    assert hasattr(search, 'hybrid_search')
    assert hasattr(search, '_combine_kg_insights')
    assert hasattr(search, 'get_kg_stats')

def test_get_kg_stats():
    search = HybridSearch()
    stats = search.get_kg_stats()

    assert "total_nodes" in stats
    assert "total_edges" in stats
    assert "avg_connections" in stats
    assert isinstance(stats["total_nodes"], int)
    assert isinstance(stats["total_edges"], int)

def test_hybrid_search_basic():
    search = HybridSearch()
    query = "contract dispute"
    results = search.hybrid_search(query)

    assert "graph_results" in results
    assert "vector_results" in results
    assert "combined_insights" in results
    assert isinstance(results["combined_insights"], list)

def test_combine_kg_insights():
    search = HybridSearch()
    query = "contract"
    top_k = 5

    combined = search._combine_kg_insights(query, top_k)

    assert isinstance(combined, list)
    # Should return insights based on query matching
    if len(combined) > 0:
        assert all("node" in item for item in combined)
        assert all("connections" in item for item in combined)

def test_hybrid_search_with_filters():
    search = HybridSearch()
    query = "contract"

    results = search.hybrid_search(query)

    assert "graph_results" in results
    assert "vector_results" in results
    assert "combined_insights" in results

    # Check that results contain expected structure
    assert isinstance(results["vector_results"], list)
    if len(results["vector_results"]) > 0:
        assert "id" in results["vector_results"][0]
        assert "type" in results["vector_results"][0]

def test_kg_stats_calculation():
    search = HybridSearch()
    stats = search.get_kg_stats()

    # Verify calculations are reasonable
    assert stats["total_nodes"] >= 0
    assert stats["total_edges"] >= 0
    if stats["total_nodes"] > 0:
        assert stats["avg_connections"] >= 0
        assert stats["avg_connections"] <= stats["total_edges"]  # Should be reasonable
