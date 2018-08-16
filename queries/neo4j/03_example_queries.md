
### Example Queries
<br>
#### Articles from Netherlands
```cypher
    MATCH(n)
    WHERE n.correspondenceAddress CONTAINS 'Netherlands' OR
          n.correspondenceAddress CONTAINS 'NETHERLANDS'
    RETURN n  LIMIT 10
```
<br>
#### Articles from VU and VUMC
```cypher
    MATCH (article:Article)
    WHERE article.correspondenceEmail ENDS WITH '@vumc.nl' OR
          article.correspondenceEmail ENDS WITH '@vu.nl'
    RETURN article  LIMIT 100
```
<br>
#### Articles about 'neuropsychology'
```cypher
    MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
    WHERE toLower(authorKeyword.authorKeyword) = 'neuropsychology'
    RETURN article, authorKeyword
```
<br>
#### Authors who published on topic 'neuropsychology'
```cypher
    MATCH (author:AuthorInstance)-[:IS_AUTHOR_OF]->(article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
    WHERE authorKeyword.authorKeyword = 'neuropsychology'
    RETURN author, article, authorKeyword
    LIMIT 25
```
<br>
#### Authors and author instances
```cypher
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)
    RETURN author, authorInstance
    LIMIT 10
```
<br>
#### Topic cloud of a journal
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_SUBJECT_CATEGORY|:HAS_ANNOTATION|:HAS_KEYWORD_PLUS|:HAS_AUTHOR_KEYWORD]->(keyword)
    WHERE journal.name = 'Biosystems'
    RETURN journal, article, keyword
    LIMIT 100
```
<br>
#### Topic cloud of an author
```cypher
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_SUBJECT_CATEGORY|:HAS_ANNOTATION|:HAS_KEYWORD_PLUS|:HAS_AUTHOR_KEYWORD]->(keyword)
    WHERE author.name = 'Jakobs, C'
    RETURN author, authorInstance, article, keyword
    LIMIT 75
```
<br>
#### Topics related to 'neuropsychology'
```cypher
    MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(targetAuthorKeyword),
          (article)-[:HAS_AUTHOR_KEYWORD]->(otherAuthorKeywords) 
    WHERE targetAuthorKeyword.authorKeyword = 'neuropsychology'
    RETURN article, targetAuthorKeyword, otherAuthorKeywords
    LIMIT 100
```
<br>
#### Journal annotation cloud
```cypher
    MATCH (journal)-[:IS_ABOUT]->(topic:Annotation)
    RETURN journal, topic
    LIMIT 250
```
<br>
#### Journal cloud of all topics
```cypher
MATCH (journal)-[:IS_ABOUT]->(topic)
RETURN journal, topic
LIMIT 300
```
<br>
#### Author annotation cloud
```cypher
    MATCH (author:Author)-[:HAS_RESEARCHED]->(topic:Annotation)
    RETURN author, topic
    LIMIT 250
```
<br>
#### WoS categoeries and supercategories
Return the WoS supercategory 'Literature'
```cypher
    MATCH (wc:WosCategory)--(ws:wosSupercategory {wosSupercategory: 'Literature'})
    RETURN wc, ws LIMIT 10
```

Return some journals with their WoS supercategories
```cypher
    MATCH(journal:Journal)-[:IS_ABOUT]->(wosSupercategory:WosSupercategory)
    RETURN journal, wosSupercategory LIMIT 100
```
