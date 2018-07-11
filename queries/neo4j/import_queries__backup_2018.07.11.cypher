// (1.1) Import articles and titles
LOAD CSV WITH HEADERS FROM "file:///titles_vs_articles.csv" AS eachRow
CREATE (n:Article)
SET n = eachRow


// (1.2) Index article uris
CREATE INDEX ON :Article(wosArticleUri)


// (2) Import 'years'
LOAD CSV WITH HEADERS FROM "file:///years_vs_articles.csv" AS eachRow
MATCH (article:Article)
WHERE article.wosArticleUri = eachRow.wosArticleUri
SET article.publicationYear = eachRow.publicationYear


// (3) Import 'emails'
LOAD CSV WITH HEADERS FROM "file:///emails_vs_articles.csv" AS eachRow
MATCH (article:Article)
WHERE article.wosArticleUri = eachRow.wosArticleUri
SET article.correspondenceEmail = eachRow.articleEmail


// (4) Import 'addresses'
LOAD CSV WITH HEADERS FROM "file:///addresses_vs_articles.csv" AS eachRow
MATCH (article:Article)
WHERE article.wosArticleUri = eachRow.wosArticleUri
SET article.correspondenceAddress = eachRow.articleAddress


// (5.1.1) Import 'authors' (names)
LOAD CSV WITH HEADERS FROM "file:///list_of_authorNames.csv" AS eachRow
CREATE (n:Author)
SET n.name = eachRow.authorName


// (5.1.2) Index 'author' names
CREATE INDEX ON :Author(name)


// (5.2.1) Import author instances
LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles.csv" AS eachRow
CREATE (n:AuthorInstance)
SET n.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri,
    n.authorName = eachRow.authorName


// (5.2.2) Index author wos compound uris in author instances
CREATE INDEX ON :AuthorInstance(wosAuthorCompoundUri)


// (5.2.3) Connect 'author instances' with articles
LOAD CSV WITH HEADERS FROM "file:///authors_vs_articles.csv" AS eachRow
MATCH (article:Article), (authorInstance:AuthorInstance)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND 
	  authorInstance.wosAuthorCompoundUri = eachRow.wosAuthorCompoundUri
CREATE (authorInstance)-[:IS_AUTHOR_OF]->(article)


// (5.3) [until 1M] Connect 'author instances' with 'authors'
MATCH (author:Author), (authorInstance:AuthorInstance)
WHERE author.name = authorInstance.authorName
WITH author, authorInstance LIMIT 1000000
MERGE (author)-[:HAS_INSTANCE]->(authorInstance)


// (6.1) Import 'journals'
LOAD CSV WITH HEADERS FROM "file:///list_of_journals.csv" AS eachRow
CREATE (n:Journal {name:eachRow.journal})


// (6.2) Index journal names
CREATE INDEX ON :Journal(name)


// (6.3) Connect journals with articles
LOAD CSV WITH HEADERS FROM "file:///journals_vs_articles.csv" AS eachRow
MATCH (article:Article), (journal:Journal)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //wosArticleUri must be indexed
	  journal.name = eachRow.journal  //journal.name must be indexed
CREATE (article)-[:IS_PUBLISHED_ON]->(journal)


// (7.1) Import dois
LOAD CSV WITH HEADERS FROM "file:///dois_vs_articles.csv" AS eachRow
MATCH (article:Article)
WHERE article.wosArticleUri = eachRow.wosArticleUri
SET article.doi = eachRow.doi


// (7.2) Index dois
CREATE INDEX ON :Article(doi)


// (8) Import citations and connect articles via 'dois'
LOAD CSV WITH HEADERS FROM "file:///citations_vs_articles.csv" AS eachRow
MATCH (article:Article), (articleThatIsCited:Article)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  //:Article(wosArticleUri) must have been indexed before
	  articleThatIsCited.doi = eachRow.hasCitedArticle_withDoi  //:Article(doi) must have been indexed before
CREATE (article)-[:HAS_CITED]->(articleThatIsCited)


// (9.1) Import 'author keywords'
LOAD CSV WITH HEADERS FROM "file:///AUTHOR_KEYWORDS.csv" AS eachRow
CREATE (n:AuthorKeyword {authorKeyword:eachRow.authorKeyword})


// (9.2) Index 'author keywords'
CREATE INDEX ON :AuthorKeyword(authorKeyword)


// (9.3) Connect 'author keywords' with articles
LOAD CSV WITH HEADERS FROM "file:///authorKeywords_vs_articles.csv" AS eachRow
MATCH (article:Article), (authorKeyword:AuthorKeyword)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // wosArticleUri must be indexed 
      authorKeyword.authorKeyword = eachRow.authorKeyword  // authorKeyword.authorKeyword must be indexed
CREATE (article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword)


// (10.1) Import 'annotations'
LOAD CSV WITH HEADERS FROM "file:///ANNOTATIONS.csv" AS eachRow
CREATE (n:Annotation {annotation:eachRow.annotation})


// (10.2) Index 'annotations'
CREATE INDEX ON :Annotation(annotation)


// (10.3) Connect 'annotations' with articles
LOAD CSV WITH HEADERS FROM "file:///annotations_vs_articles.csv" AS eachRow
MATCH (article:Article), (annotation:Annotation)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
      annotation.annotation = eachRow.annotation  // 'annotation' must already be indexed before
CREATE (article)-[:HAS_ANNOTATION]->(annotation)


// (11.1) Import 'keywordsPlus'
LOAD CSV WITH HEADERS FROM "file:///KEYWORDS_PLUS.csv" AS eachRow
CREATE (n:KeywordPlus {keywordPlus: eachRow.keywordsPlus})


// (11.2) Index 'keywordPlus'
CREATE INDEX ON :KeywordPlus(keywordPlus)


// (11.3) Connect 'keywordPlus' with articles
LOAD CSV WITH HEADERS FROM "file:///keywordsPlus_vs_articles.csv" AS eachRow
MATCH (article:Article), (keywordPlus:KeywordPlus)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
      keywordPlus.keywordPlus = eachRow.keywordsPlus  // 'keywordPlus' must already be indexed before
CREATE (article)-[:HAS_KEYWORD_PLUS]->(keywordPlus)


// (12.1) Import 'subjectCategories'
LOAD CSV WITH HEADERS FROM "file:///SUBJECT_CATEGORIES.csv" AS eachRow
CREATE (n:SubjectCategory {subjectCategory: eachRow.subjectCategory})


// (12.2) Index 'subjectCategories'
CREATE INDEX ON :SubjectCategory(subjectCategory)


// (12.3) Connect 'subjectCategories' with articles
LOAD CSV WITH HEADERS FROM "file:///subjectCategories_vs_articles.csv" AS eachRow
MATCH (article:Article), (subjectCategory:SubjectCategory)
WHERE article.wosArticleUri = eachRow.wosArticleUri AND  // 'wosArticleUri' must already be indexed before
      subjectCategory.subjectCategory = eachRow.subjectCategory  // 'subjectCategory' must already be indexed before
CREATE (article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory)