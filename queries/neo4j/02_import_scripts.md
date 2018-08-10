### Import Scripts
<br>

#### 1. TITLES


##### 1.1. Import articles and titles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/TITLES_vs_articles.csv" AS eachRow
    CREATE (n:Article)
    SET n = eachRow
```


##### 1.2. Index article uris
```cypher
    CREATE INDEX ON :Article(wosArticleUri)
```
<br>

#### 2. YEARS


##### 2.1. Import 'years'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/years_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
   SET article.publicationYear = eachRow.publicationYear
```
<br>

#### 3. EMAILS


##### 3.1. Import 'emails'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/emails_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceEmail = eachRow.articleEmail
```
<br>

#### 4. ADDRESSES


##### 4.1. Import 'addresses'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/addresses_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.correspondenceAddress = eachRow.articleAddress
```
<br>

#### 5. AUTHORS (NAMES)


##### 5.1.1. Import 'authors' (names)
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/AUTHOR_NAMES.csv" AS eachRow
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
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/authors_vs_articles_pX.csv" AS eachRow
    CREATE (n:AuthorInstance)
    SET n.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri,
        n.authorName = eachRow.authorName
```


##### 5.2.2. Index author wos compound uris in author instances
```cypher
    CREATE INDEX ON :AuthorInstance(wosAuthorCompoundUri)
```


##### 5.2.3. Index authorNames in author instances
```cypher
    CREATE INDEX ON :AuthorInstance(authorName)
```


##### 5.2.4. Connect 'author instances' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/authors_vs_articles_pX.csv" AS eachRow
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
<br>

#### 6. JOURNALS


##### 6.1. Import 'journals'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/JOURNALS.csv" AS eachRow
    CREATE (n:Journal {name:eachRow.journal})
```


##### 6.2. Index journal names
```cypher
    CREATE INDEX ON :Journal(name)
```


##### 6.3. Connect journals with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/journals_vs_articles.csv" AS eachRow
    MATCH (article:Article), (journal:Journal)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //wosArticleUri must be indexed
          journal.name = eachRow.journal  //journal.name must be indexed
    CREATE (article)-[:IS_PUBLISHED_ON]->(journal)
```
<br>

#### 7. DOIs


##### 7.1. Import dois
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/dois_vs_articles.csv" AS eachRow
    MATCH (article:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri
    SET article.doi = eachRow.doi
```


##### 7.2. Index dois
```cypher
    CREATE INDEX ON :Article(doi)
```
<br>

#### 8. CITATIONS


##### 8.1. Import citations and connect articles via 'dois'

In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/citations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (articleThatIsCited:Article)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //:Article(wosArticleUri) must have been indexed before
          articleThatIsCited.doi = eachRow.hasCitedArticle_withDoi  //:Article(doi) must have been indexed before
    CREATE (article)-[:HAS_CITED]->(articleThatIsCited)
```
<br>

#### 9. AUTHOR KEYWORDS


##### 9.1. Import 'author keywords'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/AUTHOR_KEYWORDS.csv" AS eachRow
    CREATE (n:AuthorKeyword {authorKeyword:eachRow.authorKeyword})
```


##### 9.2. Index 'author keywords'
```cypher
    CREATE INDEX ON :AuthorKeyword(authorKeyword)
```


##### 9.3. Connect 'author keywords' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/authorKeywords_vs_articles.csv" AS eachRow
    MATCH (article:Article), (authorKeyword:AuthorKeyword)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // wosArticleUri must be indexed 
          authorKeyword.authorKeyword = eachRow.authorKeyword  // AuthorKeyword.authorKeyword must be indexed
    CREATE (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)
```
<br>

#### 10. ANNOTATIONS


##### 10.1. Import 'annotations'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/ANNOTATIONS.csv" AS eachRow
    CREATE (n:Annotation {annotation:eachRow.annotation})
```


##### 10.2. Index 'annotations'
```cypher
    CREATE INDEX ON :Annotation(annotation)
```


##### 10.3. Connect 'annotations' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/annotations_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (annotation:Annotation)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          annotation.annotation = eachRow.annotation  // 'annotation' must already be indexed before
    CREATE (article)-[:HAS_ANNOTATION]->(annotation)
```
<br>

#### 11. KEYWORDS PLUS


##### 11.1. Import 'keywordsPlus'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/KEYWORDS_PLUS.csv" AS eachRow
    CREATE (n:KeywordPlus {keywordPlus: eachRow.keywordsPlus})
```


##### 11.2. Index 'keywordPlus'
```cypher
    CREATE INDEX ON :KeywordPlus(keywordPlus)
```


##### 11.3. Connect 'keywordPlus' with articles
In the following query, 'pX' should be replaced with 'p1', 'p2' etc (for each part of the data).
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/keywordsPlus_vs_articles_pX.csv" AS eachRow
    MATCH (article:Article), (keywordPlus:KeywordPlus)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          keywordPlus.keywordPlus = eachRow.keywordsPlus  // 'keywordPlus' must already be indexed before
    CREATE (article)-[:HAS_KEYWORD_PLUS]->(keywordPlus)
```
<br>

#### 12. SUBJECT CATEGORIES


##### 12.1. Import 'subjectCategories'
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/SUBJECT_CATEGORIES.csv" AS eachRow
    CREATE (n:SubjectCategory {subjectCategory: eachRow.subjectCategory})
```


##### 12.2. Index 'subjectCategories'
```cypher
    CREATE INDEX ON :SubjectCategory(subjectCategory)
```


##### 12.3. Connect 'subjectCategories' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "file:///wos_csv_files/subjectCategories_vs_articles.csv" AS eachRow
    MATCH (article:Article), (subjectCategory:SubjectCategory)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
          subjectCategory.subjectCategory = eachRow.subjectCategory  // 'subjectCategory' must already be indexed before
    CREATE (article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory)
```
<br>

#### 13. WEB OF SCIENCE CATEGORIES


##### 13.1. Import 'wosCategories'
```cypher
    LOAD CSV WITH HEADERS FROM "http://clokman.com/hosting/kfir/wos_csvs/WOS_CATEGORIES_v2.csv" AS eachRow
    CREATE (n:WosCategory {wosCategory:eachRow.wosCategory})
```


##### 13.2. Index 'wosCategories'
```cypher
CREATE INDEX ON :WosCategory(wosCategory)
```

##### 13.3. Connect 'wosCategories' with articles
```cypher
    LOAD CSV WITH HEADERS FROM "http://clokman.com/hosting/kfir/wos_csvs/wos_categories_vs_articles_v2.csv" AS eachRow
    MATCH (article:Article), (wosCategory:WosCategory)
    WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // wosArticleUri must be indexed 
    wosCategory.wosCategory = eachRow.wosCategory  // WosCategory.wosCategory must be indexed
    CREATE (article)-[:HAS_WOS_CATEGORY]->(wosCategory)
```
<br>

#### 14. AUTHOR-TOPIC RELATIONSHIPS


##### 14.1. Connect authors with annotations
```cypher
    CALL apoc.periodic.iterate(
        "MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_ANNOTATION]->(annotation:Annotation) WHERE NOT (author)-[:HAS_RESEARCHED]->(annotation) RETURN author, annotation",
        "MERGE (author)-[:HAS_RESEARCHED]->(annotation)", {batchSize:100}
    )
    YIELD batches, total, timeTaken
    RETURN batches, total, timeTaken
```


##### 14.2. Connect authors with keywords plus
```cypher
    CALL apoc.periodic.iterate(
        "MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_KEYWORD_PLUS]->(keywordPlus:KeywordPlus) WHERE NOT (author)-[:HAS_RESEARCHED]->(keywordPlus) RETURN author, keywordPlus",
        "MERGE (author)-[:HAS_RESEARCHED]->(keywordPlus)", {batchSize:100}
    )
    YIELD batches, total, timeTaken
    RETURN batches, total, timeTaken
```


##### 14.3. Connect authors with author keywords
```cypher
    CALL apoc.periodic.iterate(
        "MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword:AuthorKeyword) WHERE NOT (author)-[:HAS_RESEARCHED]->(authorKeyword) RETURN author, authorKeyword",
        "MERGE (author)-[:HAS_RESEARCHED]->(authorKeyword)", {batchSize:100}
    )
    YIELD batches, total, timeTaken
    RETURN batches, total, timeTaken
```


##### 14.4. Connect authors with subject categories
```cypher
    CALL apoc.periodic.iterate(
        "MATCH (author:Author)-[:HAS_INSTANCE]->(authorInstance:AuthorInstance)-[:IS_AUTHOR_OF]->(article:Article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory:SubjectCategory) WHERE NOT (author)-[:HAS_RESEARCHED]->(subjectCategory) RETURN author, subjectCategory",
        "MERGE (author)-[:HAS_RESEARCHED]->(subjectCategory)", {batchSize:100}
    )
    YIELD batches, total, timeTaken
    RETURN batches, total, timeTaken
```
<br>

#### 15. JOURNAL-TOPIC RELATIONSHIPS


##### 15.1. Connect journals with annotations
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_ANNOTATION]->(annotation:Annotation)
    MERGE (journal)-[:IS_ABOUT]->(annotation)
```


##### 15.2. Connect journals with keywords plus
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_KEYWORD_PLUS]->(keywordPlus:KeywordPlus)
    MERGE (journal)-[:IS_ABOUT]->(keywordPlus)
```


##### 15.3. Connect journals with author keywords
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword:AuthorKeyword)
    MERGE (journal)-[:IS_ABOUT]->(authorKeyword)
```


##### 15.4. Connect journals with subject categories
```cypher
    MATCH (journal:Journal)<-[:IS_PUBLISHED_ON]-(article:Article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory:SubjectCategory)
    MERGE (journal)-[:IS_ABOUT]->(subjectCategory)
```
