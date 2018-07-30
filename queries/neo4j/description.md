### Description 
These slides contain the cypher scripts for importing Web of Science database from CSV files (which are exported from a triple store) into Neo4j. These slides should be imported to Neo4j as guides by using `:play https://slidewiki.org/neo4jguide/115514/_/115514/754640-41/` in Neo4j Browser. (For this URL to work, it should first be whitelisted in Neo4j database's conf file.) 

### Format and Notation
The .csv files may serve as a list of **instances** (e.g., a list of all unique titles, which would be imported as nodes in Neo4j), as **join datasets** (e.g., a list of relationships between two titles and article IDs), or both.

The names of .csv files that contain unique instances (nodes) are written in capitals (e.g., "TITLES.csv", which contains a list of unique titles that can be used to populate the graph with nodes).
