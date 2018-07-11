// Articles from Netherlands
MATCH(n)
WHERE n.correspondenceAddress CONTAINS 'Netherlands' OR
	  n.correspondenceAddress CONTAINS 'NETHERLANDS'
RETURN n  LIMIT 100


// Articles from VU and VUMC
MATCH (n)
WHERE n.correspondenceEmail ENDS WITH '@vumc.nl' OR
	  n.correspondenceEmail ENDS WITH '@vu.nl'
RETURN n  LIMIT 100


// Articles about 'neuropsychology'
MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
WHERE authorKeyword.authorKeyword = 'neuropsychology'
RETURN article


// Authors who published on topic 'neuropsychology'
MATCH (author:Author)-[:IS_AUTHOR_OF]->(article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
WHERE authorKeyword.authorKeyword = 'neuropsychology'
RETURN author, article, authorKeyword


// Authors who published on 'neuropsychology' + constellation
MATCH (author:Author)-[:IS_AUTHOR_OF]->(article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)-[*1..3]-(thing)
WHERE authorKeyword.authorKeyword = 'neuropsychology'
RETURN author, article, authorKeyword, thing


// Constellation of 'neuropsychology'
MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)-[*1..4]-(contellationKeyword:AuthorKeyword)
WHERE authorKeyword.authorKeyword = 'neuropsychology'
RETURN article, authorKeyword, contellationKeyword


// Author-topic map
MATCH (author:Author)-[:HAS_PUBLISHED_ON_AUTHOR_KEYWORD]->(authorKeyword)
RETURN author,authorKeyword


// Author-topic-article map
MATCH (author:Author)-[:HAS_PUBLISHED_ON_AUTHOR_KEYWORD]->(authorKeyword)<-[:HAS_AUTHOR_KEYWORD]-(article:Article)
RETURN author,authorKeyword, article


// Author topic constellation: of 'Jakobs, C'
MATCH (author)-[:HAS_PUBLISHED_ON_AUTHOR_KEYWORD]->(authorKeyword)-[*1..2]-(constellationKeyword:AuthorKeyword)
WHERE author.authorName = 'Jakobs, C'
RETURN author, authorKeyword, constellationKeyword