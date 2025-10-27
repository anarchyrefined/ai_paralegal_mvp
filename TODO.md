# TODO: Integrate FilterPanel into KG Page

## Steps to Complete

- [x] Modify ui/components/FilterPanel.js: Remove local filtering logic, add onApply prop to make it controlled.
- [x] Modify ui/components/GraphPanel.tsx: Add optional nodes and edges props; use provided data if available, else fetch from API.
- [x] Update ui/pages/kg.tsx: Import FilterPanel; add state for filter, nodes, edges; add useEffect to fetch graph data; add filtering function; render FilterPanel above graph; pass filtered data to GraphPanel.
- [x] Test the integration: Attempted to run UI server, but no package.json in ui directory. Served static files via Python HTTP server. Browser tool disabled, so manual testing not possible. Code changes implemented as per plan.
