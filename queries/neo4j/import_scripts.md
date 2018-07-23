### Import Scripts
<br>
#### 1. Titles
<br>
##### 1.1. Import articles and titles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///TITLES_vs_articles.csv" AS eachRow
    CREATE (n:Article)
    SET n = eachRow
```
<br>
##### 1.2. Index article uris
```cypher
    CREATE INDEX ON :Article(wosArticleUri)
```
<br>
#### 2. Years
<br>
Import 'years'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///years_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
   SET article.publicationYear = eachRow.publicationYear
```
<br>
#### 3. Emails
<br>
Import 'emails'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///emails_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceEmail = eachRow.articleEmail
```
<br>
#### 4. Addresses
<br>
Import 'addresses'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///addresses_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceAddress = eachRow.articleAddress
```
<br>
#### 5. Authors (names)
<br>
##### 5.1.1. Import 'authors' (names)
```cypher
    LOAD CSV WITH HEADERS FROM "file:///AUTHOR_NAMES.csv" AS eachRow
    CREATE (n:Author)
    SET n.name = eachRow.authorName
```
<br>
##### 5.1.2. Index 'author' names
```cypher
    CREATE INDEX ON :Author(name)
```
<br>
##### 5.2.1. Import author instances
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles_pX.csv" AS eachRow
    CREATE (n:AuthorInstance)
    SET n.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri,
        n.authorName = eachRow.authorName
```
<br>
##### 5.2.2. Index author wos compound uris in author instances
```cypher
    CREATE INDEX ON :AuthorInstance(wosAuthorCompoundUri)
```
<br>
##### 5.2.3. Connect 'author instances' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (authorInstance:AuthorInstance)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND 
          authorInstance.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri
    CREATE (authorInstance)-[:IS_AUTHOR_OF]->(article)
```
<br>
##### 5.3. Connect 'author instances' with 'authors'
This script is currently a preview; ran for 1 million connections.
```cypher
    MATCH (author:Author), (authorInstance:AuthorInstance)
    WHERE author.name = authorInstance.authorName
    WITH author, authorInstance LIMIT 1000000
    MERGE (author)-[:HAS_INSTANCE]->(authorInstance)
```
<br>
#### 6. Journals
<br>
##### 6.1. Import 'journals'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///JOURNALS.csv" AS eachRow
    CREATE (n:Journal {name:eachRow.journal})
```
<br>
##### 6.2. Index journal names
```cypher
    CREATE INDEX ON :Journal(name)
```
<br>
##### 6.3. Connect journals with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///journals_vs_articles.csv" AS eachRow
    MATCH (article:Article), (journal:Journal)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //wosArticleUri must be indexed
          journal.name = eachRow.journal  //journal.name must be indexed
    CREATE (article)-[:IS_PUBLISHED_ON]->(journal)
```
<br>
#### 7. DOIs
<br>
##### 7.1. Import dois
```cypher
    LOAD CSV WITH HEADERS FROM "file:///dois_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.doi = eachRow.doi
```
<br>
##### 7.2. Index dois
```cypher
    CREATE INDEX ON :Article(doi)
```
<br>
#### 8. Citations
Import citations and connect articles via 'dois'
<br>
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///citations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (articleThatIsCited:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //:Article(wosArticleUri) must have been indexed before
          articleThatIsCited.doi = eachRow.hasCitedArticle_withDoi  //:Article(doi) must have been indexed before
    CREATE (article)-[:HAS_CITED]->(articleThatIsCited)
```
<br>
#### 9. Author Keywords
<br>
##### 9.1. Import 'author keywords'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///AUTHOR_KEYWORDS.csv" AS eachRow
    CREATE (n:AuthorKeyword {authorKeyword:eachRow.authorKeyword})
```
<br>
##### 9.2. Index 'author keywords'
```cypher
    CREATE INDEX ON :AuthorKeyword(authorKeyword)
```
<br>
##### 9.3. Connect 'author keywords' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///authorKeywords_vs_articles.csv" AS eachRow
    MATCH (article:Article), (authorKeyword:AuthorKeyword)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // wosArticleUri must be indexed 
          authorKeyword.authorKeyword = eachRow.authorKeyword  // authorKeyword.authorKeyword must be indexed
    CREATE (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
```
<br>
#### 10. Annotations
<br>
##### 10.1. Import 'annotations'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///ANNOTATIONS.csv" AS eachRow
    CREATE (n:Annotation {annotation:eachRow.annotation})
```
<br>
##### 10.2. Index 'annotations'
```cypher
    CREATE INDEX ON :Annotation(annotation)
```
<br>
##### 10.3. Connect 'annotations' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///annotations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (annotation:Annotation)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          annotation.annotation = eachRow.annotation  // 'annotation' must already be indexed before
    CREATE (article)-[:HAS_ANNOTATION]->(annotation)
```
<br>
#### 11. Keywords Plus
<br>
##### 11.1. Import 'keywordsPlus'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///KEYWORDS_PLUS.csv" AS eachRow
    CREATE (n:KeywordPlus {keywordPlus: eachRow.keywordsPlus})
```
<br>
##### 11.2. Index 'keywordPlus'
```cypher
    CREATE INDEX ON :KeywordPlus(keywordPlus)
```
<br>
##### 11.3. Connect 'keywordPlus' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///keywordsPlus_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (keywordPlus:KeywordPlus)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          keywordPlus.keywordPlus = eachRow.keywordsPlus  // 'keywordPlus' must already be indexed before
    CREATE (article)-[:HAS_KEYWORD_PLUS]->(keywordPlus)
```
<br>
#### 12. Subject Categories
<br>
##### 12.1. Import 'subjectCategories'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///SUBJECT_CATEGORIES.csv" AS eachRow
    CREATE (n:SubjectCategory {subjectCategory: eachRow.subjectCategory})
```
<br>
##### 12.2. Index 'subjectCategories'
```cypher
    CREATE INDEX ON :SubjectCategory(subjectCategory)
```
<br>
##### 12.3. Connect 'subjectCategories' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///subjectCategories_vs_articles.csv" AS eachRow
    MATCH (article:Article), (subjectCategory:SubjectCategory)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          subjectCategory.subjectCategory = eachRow.subjectCategory  // 'subjectCategory' must already be indexed before
    CREATE (article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory)
```
<br>
#### 13. Authors to all Topics
<br>
##### Connect authors with annotations, keywordsPlus, author keywords, subject categories
Currently is preview with limit: 10K
```cypher 
    MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_ANNOTATION |:HAS_KEYWORD_PLUS |:HAS_AUTHOR_KEYWORD |:HAS_SUBJECT_CATEGORY]->(topic)
    MERGE (author)-[:HAS_RESEARCHED]->(topic)
    RETURN author, topic
    LIMIT 10000
```

<br>

#### 14. Journals to all Topics
<br>
##### Connect journals with annotations, keywordsPlus, author keywords, subject categories 
Currently is preview with limit: 10K
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_ANNOTATION |:HAS_KEYWORD_PLUS |:HAS_AUTHOR_KEYWORD |:HAS_SUBJECT_CATEGORY]->(topic)
    MERGE (journal)-[:IS_ABOUT]->(topic)
    RETURN journal, topic
    LIMIT 10000
```
<br>
