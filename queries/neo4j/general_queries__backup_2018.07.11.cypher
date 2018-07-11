//System status
:sysinfo


// DELETE relationship
MATCH ()-[r:RELNAME]-() 
DETACH
DELETE r


// DELETE all
MATCH (n) 
DETACH
DELETE n


// DELETE iteratively
MATCH (n)
OPTIONAL MATCH (n)-[r]-()
WITH n,r LIMIT 250000
DETACH DELETE n,r
RETURN count(n) as deletedNodesCount


// Return all
MATCH (n) 
RETURN n


// List indexes
CALL db.indexes
