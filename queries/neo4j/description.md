### Description 
These slides contain the cypher scripts for importing Web of Science database from CSV files (which are exported from a triple store) into Neo4j.

### Format and Notation
The .csv files may serve as a list of **instances** (e.g., a list of all unique titles, which would be imported as nodes in Neo4j), as **join datasets** (e.g., a list of relationships between two titles and article IDs), or both.

The names of .csv files that contain unique instances (nodes) are written in capitals (e.g., "TITLES.csv", which contains a list of unique titles that can be used to populate the graph with nodes).
