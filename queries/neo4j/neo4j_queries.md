<br>
### Description 
These slides contain the cypher scripts for importing Web of Science database from CSV files (which are exported from a triple store) into Neo4j.

### Format and Notation
The .csv files may serve as a list of **instances** (e.g., a list of all unique titles, which would be imported as nodes in Neo4j), as **join datasets** (e.g., a list of relationships between two titles and article IDs), or both.

The names of .csv files that contain unique instances (nodes) are written in capitals (e.g., "TITLES.csv", which contains a list of unique titles that can be used to populate the graph with nodes).

---

<br>
### Import Scripts
#### 1. Titles
##### 1.1. Import articles and titles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///TITLES_vs_articles.csv" AS eachRow
    CREATE (n:Article)
    SET n = eachRow
```

##### 1.2. Index article uris
```cypher
    CREATE INDEX ON :Article(wosArticleUri)
```

#### 2. Years
Import 'years'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///years_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
   SET article.publicationYear = eachRow.publicationYear
```

#### 3. Emails
Import 'emails'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///emails_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceEmail = eachRow.articleEmail
```

#### 4. Addresses
Import 'addresses'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///addresses_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceAddress = eachRow.articleAddress
```

#### 5. Authors (names)

##### 5.1.1. Import 'authors' (names)
```cypher
    LOAD CSV WITH HEADERS FROM "file:///AUTHOR_NAMES.csv" AS eachRow
    CREATE (n:Author)
    SET n.name = eachRow.authorName
```

##### 5.1.2. Index 'author' names
```cypher
    CREATE INDEX ON :Author(name)
```

##### 5.2.1. Import author instances
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles_pX.csv" AS eachRow
    CREATE (n:AuthorInstance)
    SET n.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri,
        n.authorName = eachRow.authorName
```

##### 5.2.2. Index author wos compound uris in author instances
```cypher
    CREATE INDEX ON :AuthorInstance(wosAuthorCompoundUri)
```

##### 5.2.3. Connect 'author instances' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (authorInstance:AuthorInstance)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND 
          authorInstance.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri
    CREATE (authorInstance)-[:IS_AUTHOR_OF]->(article)
```

##### 5.3. Connect 'author instances' with 'authors'
This script is currently a preview; ran for 1 million connections.
```cypher
    MATCH (author:Author), (authorInstance:AuthorInstance)
    WHERE author.name = authorInstance.authorName
    WITH author, authorInstance LIMIT 1000000
    MERGE (author)-[:HAS_INSTANCE]->(authorInstance)
```
#### 6. Journals
##### 6.1. Import 'journals'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///JOURNALS.csv" AS eachRow
    CREATE (n:Journal {name:eachRow.journal})
```

##### 6.2. Index journal names
```cypher
    CREATE INDEX ON :Journal(name)
```

##### 6.3. Connect journals with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///journals_vs_articles.csv" AS eachRow
    MATCH (article:Article), (journal:Journal)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //wosArticleUri must be indexed
          journal.name = eachRow.journal  //journal.name must be indexed
    CREATE (article)-[:IS_PUBLISHED_ON]->(journal)
```
#### 7. DOIs
##### 7.1. Import dois
```cypher
    LOAD CSV WITH HEADERS FROM "file:///dois_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.doi = eachRow.doi
```

##### 7.2. Index dois
```cypher
    CREATE INDEX ON :Article(doi)
```

#### 8. Citations
Import citations and connect articles via 'dois'

In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///citations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (articleThatIsCited:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //:Article(wosArticleUri) must have been indexed before
          articleThatIsCited.doi = eachRow.hasCitedArticle_withDoi  //:Article(doi) must have been indexed before
    CREATE (article)-[:HAS_CITED]->(articleThatIsCited)
```

#### 9. Author Keywords
##### 9.1. Import 'author keywords'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///AUTHOR_KEYWORDS.csv" AS eachRow
    CREATE (n:AuthorKeyword {authorKeyword:eachRow.authorKeyword})
```

##### 9.2. Index 'author keywords'
```cypher
    CREATE INDEX ON :AuthorKeyword(authorKeyword)
```

##### 9.3. Connect 'author keywords' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authorKeywords_vs_articles.csv" AS eachRow
    MATCH (article:Article), (authorKeyword:AuthorKeyword)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // wosArticleUri must be indexed 
          authorKeyword.authorKeyword = eachRow.authorKeyword  // authorKeyword.authorKeyword must be indexed
    CREATE (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
```

#### 10. Annotations
##### 10.1. Import 'annotations'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///ANNOTATIONS.csv" AS eachRow
    CREATE (n:Annotation {annotation:eachRow.annotation})
```

##### 10.2. Index 'annotations'
```cypher
    CREATE INDEX ON :Annotation(annotation)
```

##### 10.3. Connect 'annotations' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///annotations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (annotation:Annotation)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          annotation.annotation = eachRow.annotation  // 'annotation' must already be indexed before
    CREATE (article)-[:HAS_ANNOTATION]->(annotation)
```

#### 11. Keywords Plus
##### 11.1. Import 'keywordsPlus'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///KEYWORDS_PLUS.csv" AS eachRow
    CREATE (n:KeywordPlus {keywordPlus: eachRow.keywordsPlus})
```

##### 11.2. Index 'keywordPlus'
```cypher
    CREATE INDEX ON :KeywordPlus(keywordPlus)
```

##### 11.3. Connect 'keywordPlus' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///keywordsPlus_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (keywordPlus:KeywordPlus)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          keywordPlus.keywordPlus = eachRow.keywordsPlus  // 'keywordPlus' must already be indexed before
    CREATE (article)-[:HAS_KEYWORD_PLUS]->(keywordPlus)
```

#### 12. Subject Categories
##### 12.1. Import 'subjectCategories'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///SUBJECT_CATEGORIES.csv" AS eachRow
    CREATE (n:SubjectCategory {subjectCategory: eachRow.subjectCategory})
```

##### 12.2. Index 'subjectCategories'
```cypher
    CREATE INDEX ON :SubjectCategory(subjectCategory)
```

##### 12.3. Connect 'subjectCategories' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///subjectCategories_vs_articles.csv" AS eachRow
    MATCH (article:Article), (subjectCategory:SubjectCategory)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          subjectCategory.subjectCategory = eachRow.subjectCategory  // 'subjectCategory' must already be indexed before
    CREATE (article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory)
```

#### 13. Authors to all Topics
##### Connect authors with annotations, keywordsPlus, author keywords, subject categories
Currently is preview with limit: 10K
```cypher 
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_ANNOTATION |:HAS_KEYWORD_PLUS |:HAS_AUTHOR_KEYWORD |:HAS_SUBJECT_CATEGORY]->(topic)
    MERGE (author)-[:HAS_RESEARCHED]->(topic)
    RETURN author, topic
    LIMIT 10000
```

#### 14. Journals to all Topics
##### Connect journals with annotations, keywordsPlus, author keywords, subject categories 
Currently is preview with limit: 10K
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_ANNOTATION |:HAS_KEYWORD_PLUS |:HAS_AUTHOR_KEYWORD |:HAS_SUBJECT_CATEGORY]->(topic)
    MERGE (journal)-[:IS_ABOUT]->(topic)
    RETURN journal, topic
    LIMIT 10000
```


---


### Example Queries
#### Articles from Netherlands
```cypher
    MATCH(n)
    WHERE n.correspondenceAddress CONTAINS 'Netherlands' OR
          n.correspondenceAddress CONTAINS 'NETHERLANDS'
    RETURN n  LIMIT 10
```

#### Articles from VU and VUMC
```cypher
    MATCH (article:Article)
    WHERE article.correspondenceEmail ENDS WITH '@vumc.nl' OR
          article.correspondenceEmail ENDS WITH '@vu.nl'
    RETURN article  LIMIT 100
```

#### Articles about 'neuropsychology'
```cypher
    MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
    WHERE toLower(authorKeyword.authorKeyword) = 'neuropsychology'
    RETURN article, authorKeyword
```

#### Authors who published on topic 'neuropsychology'
```cypher
    MATCH (author:AuthorInstance)-[:IS_AUTHOR_OF]->(article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
    WHERE authorKeyword.authorKeyword = 'neuropsychology'
    RETURN author, article, authorKeyword
    LIMIT 25
```

#### Authors and author instances
```cypher
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)
    RETURN author, authorInstance
    LIMIT 10
```

#### Topic cloud of a journal
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_SUBJECT_CATEGORY|:HAS_ANNOTATION|:HAS_KEYWORD_PLUS|:HAS_AUTHOR_KEYWORD]->(keyword)
    WHERE journal.name = 'Biosystems'
    RETURN journal, article, keyword
    LIMIT 100
```

#### Topic cloud of an author
```cypher
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_SUBJECT_CATEGORY|:HAS_ANNOTATION|:HAS_KEYWORD_PLUS|:HAS_AUTHOR_KEYWORD]->(keyword)
    WHERE author.name = 'Jakobs, C'
    RETURN author, authorInstance, article, keyword
    LIMIT 75
```

#### Topics related to 'neuropsychology'
```cypher
    MATCH (article)-[:HAS_AUTHOR_KEYWORD]->(targetAuthorKeyword),
          (article)-[:HAS_AUTHOR_KEYWORD]->(otherAuthorKeywords) 
    WHERE targetAuthorKeyword.authorKeyword = 'neuropsychology'
    RETURN article, targetAuthorKeyword, otherAuthorKeywords
    LIMIT 100
```

#### Journal annotation cloud
```cypher
    MATCH (journal)-[:IS_ABOUT]->(topic:Annotation)
    RETURN journal, topic
    LIMIT 250
```

#### Journal cloud of all topics
```cypher
MATCH (journal)-[:IS_ABOUT]->(topic)
RETURN journal, topic
LIMIT 300
```

#### Author annotation cloud
```cypher
    MATCH (author:Author)-[:HAS_RESEARCHED]->(topic:Annotation)
    RETURN author, topic
    LIMIT 250
```