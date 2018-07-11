// (1) Connect authors with author keywords
MATCH (author:Author)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword:AuthorKeyword)
CREATE (author)-[:HAS_PUBLISHED_ON_AUTHOR_KEYWORD]->(authorKeyword)
RETURN author, article, authorKeyword


// (1x) DELETE author-authorKeyword relationships
MATCH ()-[r:HAS_PUBLISHED_ON_AUTHOR_KEYWORD]-() 
DETACH
DELETE r