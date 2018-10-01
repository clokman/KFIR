# X. QUERYING THE CITATION NETWORK

## X.1. (Article) HAS_CITED (Article)

### @sandbox

        CALL algo.unionFind.stream('Character', 'INTERACTS1', {})
        YIELD nodeId, setId
        MATCH (character:Character) WHERE id(u) = nodeId
        RETURN character.name AS character, setId


### @risis

        CALL algo.unionFind.stream('Article', 'HAS_CITED', {})
        YIELD nodeId, setId
        MATCH (article:Article) WHERE id(article) = nodeId
        RETURN article.title AS character, setId


# 1. CREATING TOPIC SUBGRAPHS

## 1.X. Delete Author to author connections

        CALL apoc.periodic.iterate(
                "MATCH (:Author)-[sharesTopicWith:SHARES_TOPIC_WITH]-(:Author)"
                "DELETE sharesTopicWith",
                {batchSize:10000}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 1.0. Test weighted relationship creation in GoT sandbox

Create a weighted relationship by aggregating existing relationships:

        MATCH (character1:Character)-[:INTERACTS1]-(character2:Character)
        // MATCH (character1:Character)-[:INTERACTS2]-(character2:Character)  // uncomment one line (and comment out the previous line) until each commented out line is ran once
        // MATCH (character1:Character)-[:INTERACTS3]-(character2:Character)
        // MATCH (character1:Character)-[:INTERACTS45]-(character2:Character)
        WHERE id(character1) < id(character2)
        WITH character1, character2, count(*) as weight
        MERGE (character1)-[interacts0:INTERACTS0]->(character2)
        ON CREATE SET interacts0.weight = weight
        ON MATCH SET interacts0.weight = interacts0.weight + weight

Note: The above example ignores the exising weight properties in the existing connections.


## 1.1. Construct `KeywordPlus` graph(s)

### 1.1.1. Weighted `KeywordPlus` graph

Connect keywords plus nodes to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (keywordPlus1:KeywordPlus)<-[:HAS_KEYWORD_PLUS]-(:Article)-[:HAS_KEYWORD_PLUS]->(keywordPlus2:KeywordPlus) WHERE id(keywordPlus1) < id(keywordPlus2) RETURN keywordPlus1, keywordPlus2, count(*) as times",
                "MERGE (keywordPlus1)-[coOccurredWith:CO_OCCURRED_WITH]->(keywordPlus2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 1.3.2. Unweighted `KeywordPlus` graph:

Connect topics to each other using articles as intermediaries. Create one relationship per connection:

        CALL apoc.periodic.iterate(
                "MATCH (keywordPlus1:KeywordPlus)<-[:HAS_KEYWORD_PLUS]-(:Article)-[:HAS_KEYWORD_PLUS]->(keywordPlus2:KeywordPlus) WHERE id(keywordPlus1) < id(keywordPlus2) RETURN keywordPlus1, keywordPlus2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (keywordPlus1)-[:CO_OCCURRED_WITH_UNWEIGHTED]->(keywordPlus2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Test if the unweighted relationships are correctly created:

        MATCH (n:KeywordPlus {keywordPlus: 'X'})-[r1:HAS_KEYWORD_PLUS]-(a:Article)-[r2:HAS_KEYWORD_PLUS]-(n2:KeywordPlus {keywordPlus: 'Y'})
        RETURN n, r1, a, r2, n2 LIMIT 100


## 1.2. Construct `AuthorKeyword` graph(s)

### 1.2.1. Weighted `AuthorKeyword` graph
Connect author keywords to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (authorKeyword1:AuthorKeyword)<-[:HAS_AUTHOR_KEYWORD]-(:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword2:AuthorKeyword) WHERE id(authorKeyword1) < id(authorKeyword2) RETURN authorKeyword1, authorKeyword2, count(*) as times",
                "MERGE (authorKeyword1)-[coOccurredWith:CO_OCCURRED_WITH]->(authorKeyword2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 1.2.2. Unweighted `AuthorKeyword` graph:

Connect topics to each other using articles as intermediaries. Create one relationship per connection:

        CALL apoc.periodic.iterate(
                "MATCH (authorKeyword1:AuthorKeyword)<-[:HAS_AUTHOR_KEYWORD]-(:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword2:AuthorKeyword) WHERE id(authorKeyword1) < id(authorKeyword2) RETURN authorKeyword1, authorKeyword2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (authorKeyword1)-[:CO_OCCURRED_WITH_UNWEIGHTED]->(authorKeyword2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Test if the unweighted relationships are correctly created:

        MATCH (n:AuthorKeyword {authorKeyword: 'X'})-[r1:HAS_AUTHOR_KEYWORD]-(a:Article)-[r2:HAS_AUTHOR_KEYWORD]-(n2:AuthorKeyword {authorKeyword: 'Y'})
        RETURN n, r1, a, r2, n2 LIMIT 100


## 1.3. Construct `Annotation` graph(s)

## 1.3.1. Weighted `Annotation` graph

Connect annotations to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (annotation1:Annotation)<-[:HAS_ANNOTATION]-(:Article)-[:HAS_ANNOTATION]->(annotation2:Annotation) WHERE id(annotation1) < id(annotation2) RETURN annotation1, annotation2, count(*) as times",
                "MERGE (annotation1)-[coOccurredWith:CO_OCCURRED_WITH]->(annotation2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 1.3.2. Unweighted `Annotation` graph:

Connect topics to each other using articles as intermediaries. Create one relationship per connection:

        CALL apoc.periodic.iterate(
                "MATCH (annotation1:Annotation)<-[:HAS_ANNOTATION]-(:Article)-[:HAS_ANNOTATION]->(annotation2:Annotation) WHERE id(annotation1) < id(annotation2) RETURN annotation1, annotation2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (annotation1)-[:CO_OCCURRED_WITH_UNWEIGHTED]->(annotation2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Test if the unweighted relationships are correctly created:

        MATCH (n:Annotation {annotation: 'X'})-[r1:HAS_ANNOTATION]-(a:Article)-[r2:HAS_ANNOTATION]-(n2:Annotation {annotation: 'Y'})
        RETURN n, r1, a, r2, n2 LIMIT 100


## 1.4. Construct `SubjectCategory` graph(s)

### 1.4.1. Weighted `SubjectCategory` graph:

Connect ISI subject categories to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (subjectCategory1:SubjectCategory)<-[:HAS_SUBJECT_CATEGORY]-(:Article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory2:SubjectCategory) WHERE id(subjectCategory1) < id(subjectCategory2) RETURN subjectCategory1, subjectCategory2, count(*) as times",
                "MERGE (subjectCategory1)-[coOccurredWith:CO_OCCURRED_WITH]->(subjectCategory2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 1.4.2. Unweighted `SubjectCategory` graph:

Connect topics to each other using articles as intermediaries. Create one relationship per connection:

        CALL apoc.periodic.iterate(
                "MATCH (subjectCategory1:SubjectCategory)<-[:HAS_SUBJECT_CATEGORY]-(:Article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory2:SubjectCategory) WHERE id(subjectCategory1) < id(subjectCategory2) RETURN subjectCategory1, subjectCategory2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (subjectCategory1)-[:CO_OCCURRED_WITH_UNWEIGHTED]->(subjectCategory2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Test if the unweighted relationships are correctly created:

        MATCH (n:SubjectCategory {subjectCategory: 'Film, Radio & Television'})-[r1:HAS_SUBJECT_CATEGORY]-(a:Article)-[r2:HAS_SUBJECT_CATEGORY]-(n2:SubjectCategory {subjectCategory: 'Psychology'})
        RETURN n, r1, a, r2, n2 LIMIT 100


## 1.5. Construct `WosCategory` graph(s)

### 1.5.1. Weighted `WosCategory` graph

Connect Web of Science categories to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (wosCategory1:WosCategory)<-[:HAS_WOS_CATEGORY]-(:Article)-[:HAS_WOS_CATEGORY]->(wosCategory2:WosCategory) WHERE id(wosCategory1) < id(wosCategory2) RETURN wosCategory1, wosCategory2, count(*) as times",
                "MERGE (wosCategory1)-[coOccurredWith:CO_OCCURRED_WITH]->(wosCategory2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken
        

## 1.5.2. Unweighted `WosCategory` graph
Connect topics to each other using articles as intermediaries. Create one relationship per connection:

        CALL apoc.periodic.iterate(
                "MATCH (wosCategory1:WosCategory)<-[:HAS_WOS_CATEGORY]-(:Article)-[:HAS_WOS_CATEGORY]->(wosCategory2:WosCategory) WHERE id(wosCategory1) < id(wosCategory2) RETURN wosCategory1, wosCategory2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (wosCategory1)-[:CO_OCCURRED_WITH_UNWEIGHTED]->(wosCategory2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Test if the unweighted relationships are correctly created:

        MATCH(n:WosCategory {wosCategory: 'Work'})-[r1:HAS_WOS_CATEGORY]-(a:Article)-[r2:HAS_WOS_CATEGORY]-(n2:WosCategory {wosCategory: 'Planning & Development'})
        RETURN n, r1, a, r2, n2 LIMIT 100


# 2. MAPPING THE INNER-CONNECTEDNESS OF GRAPHS

In unionFind, the direction of connections is ignored:
"The direction of the relationships in our graph are ignored - we treat the graph as undirected." (from graph algorithms documentation)


## 2.0. Testing the `unionFind` algorithm in GoT sandbox

**Stream GoT graph components** with `unionFind`:

        CALL algo.unionFind(
        'MATCH (character:Character)-[:INTERACTS1]-() 
        RETURN id(character) AS id',
        'MATCH (character1:Character)-[:INTERACTS1]-(character2)
        WHERE NOT id(character1) = id(character2)
        RETURN id(character1) AS source, id(character2) AS target',
        {graph:'cypher', write:true}
        )
        YIELD nodes, setCount;

The query **above is the equivalent** of this query:

        CALL algo.unionFind('Character', 'INTERACTS1', {write:true})
        YIELD nodes, setCount;


## 2.1. Map the components of the `KeywordPlus` graph

**Stream `KeywordPlus` graph components**:

        CALL algo.unionFind.stream('KeywordPlus', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (keywordPlus:KeywordPlus) WHERE id(keywordPlus) = nodeId
        RETURN keywordPlus.keywordPlus AS keywordPlus, setId
        ORDER BY setId


**Write `KeywordPlus` graph components** to nodes:

        CALL algo.unionFind('KeywordPlus', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'keywordPlusSubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (keywordPlus:KeywordPlus)
        UNWIND keywordPlus.keywordPlusSubGraphComponent as keywordPlusSubGraphComponent
        WITH keywordPlusSubGraphComponent, COUNT(keywordPlus) as count
        ORDER BY (count) DESC
        RETURN keywordPlusSubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(keywordPlusSubGraphComponent) as mainSetId
        // RETURN mainSetId

The most frequent mainSetId (i.e., the main graph component) is '82571'.


**Write `KeywordPlusGraphMainComponentNode` label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (keywordPlus:KeywordPlus) WHERE keywordPlus.keywordPlusSubGraphComponent = 82571 RETURN keywordPlus",
          "SET keywordPlus:KeywordPlusGraphMainComponentNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 2.2. Map the components of the `AuthorKeyword` graph

**Stream `AuthorKeyword` graph components**:

        CALL algo.unionFind.stream('AuthorKeyword', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (authorKeyword:AuthorKeyword) WHERE id(authorKeyword) = nodeId
        RETURN authorKeyword.authorKeyword AS authorKeyword, setId
        ORDER BY setId


**Write `AuthorKeyword` graph components** to nodes:

                CALL algo.unionFind('AuthorKeyword', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'authorKeywordSubGraphComponent'})
                YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (authorKeyword:AuthorKeyword)
        UNWIND authorKeyword.authorKeywordSubGraphComponent as authorKeywordSubGraphComponent
        WITH authorKeywordSubGraphComponent, COUNT(authorKeyword) as count
        ORDER BY (count) DESC
        RETURN authorKeywordSubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(authorKeywordSubGraphComponent) as mainSetId
        // RETURN mainSetId

The most frequent mainSetId (i.e., the main graph component) is '98756'.


**Write `AuthorKeywordGraphMainComponentNode` label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (authorKeyword:AuthorKeyword) WHERE authorKeyword.authorKeywordSubGraphComponent = 98756 RETURN authorKeyword",
          "SET authorKeyword:AuthorKeywordGraphMainComponentNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 2.3. Map the components of the `Annotation` graph

**Stream `Annotation` graph components**:

        CALL algo.unionFind.stream('Annotation', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (annotation:Annotation) WHERE id(annotation) = nodeId
        RETURN annotation.annotation AS annotation, setId
        ORDER BY setId


**Write `Annotation` graph components** to nodes:

        CALL algo.unionFind('Annotation', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'annotationSubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (annotation:Annotation)
        UNWIND annotation.annotationSubGraphComponent as annotationSubGraphComponent
        WITH annotationSubGraphComponent, COUNT(annotation) as count
        ORDER BY (count) DESC
        RETURN annotationSubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(annotationSubGraphComponent) as mainSetId
        // RETURN mainSetId

The most frequent mainSetId (i.e., the main graph component) is '50898'.


**Write `AnnotationGraphMainComponentNode` label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (annotation:Annotation) WHERE annotation.annotationSubGraphComponent = 50898 RETURN annotation",
          "SET annotation:AnnotationGraphMainComponentNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 2.4. Map the components of the `SubjectCategory` graph

**Stream `SubjectCategory` graph components**:

        CALL algo.unionFind.stream('SubjectCategory', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (subjectCategory:SubjectCategory) WHERE id(subjectCategory) = nodeId
        RETURN subjectCategory.subjectCategory AS subjectCategory, setId
        ORDER BY setId


**Write `SubjectCategory` graph components** to nodes:

        CALL algo.unionFind('SubjectCategory', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'subjectCategorySubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (subjectCategory:SubjectCategory)
        UNWIND subjectCategory.subjectCategorySubGraphComponent as subjectCategorySubGraphComponent
        WITH subjectCategorySubGraphComponent, COUNT(subjectCategory) as count
        ORDER BY (count) DESC
        RETURN subjectCategorySubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(subjectCategorySubGraphComponent) as mainSetId
        // RETURN mainSetId

The most frequent mainSetId (i.e., the main graph component) is '1'.


**Write `SubjectCategoryGraphMainComponentNode` label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (subjectCategory:SubjectCategory) WHERE subjectCategory.subjectCategorySubGraphComponent = 1 RETURN subjectCategory",
          "SET subjectCategory:SubjectCategoryGraphMainComponentNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 2.5. Map the components of the `WosCategory` graph

**Stream `WosCategory` graph components**:

        CALL algo.unionFind.stream('WosCategory', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (wosCategory:WosCategory) WHERE id(wosCategory) = nodeId
        RETURN wosCategory.wosCategory AS wosCategory, setId
        ORDER BY setId


**Write `WosCategory` graph components** to nodes:

        CALL algo.unionFind('WosCategory', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'wosCategorySubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (wosCategory:WosCategory)
        UNWIND wosCategory.wosCategorySubGraphComponent as wosCategorySubGraphComponent
        WITH wosCategorySubGraphComponent, COUNT(wosCategory) as count
        ORDER BY (count) DESC
        RETURN wosCategorySubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(wosCategorySubGraphComponent) as mainSetId
        // RETURN mainSetId

The most frequent mainSetId (i.e., the main graph component) is '3'.


**Write `WosCategoryGraphMainComponentNode` label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (wosCategory:WosCategory) WHERE wosCategory.wosCategorySubGraphComponent = 3 RETURN wosCategory",
          "SET wosCategory:WosCategoryGraphMainComponentNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken



# 3. BETWEENNESS CENTRALITY

## 3.1. Betweenness centralities in **keywords plus** graph:

### 3.1.1. Calculate betweenness centralities

**Stream betweenness centrality scores for `KeywordPlus`**:

        CALL algo.betweenness.stream('KeywordPlusGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (keywordPlus:KeywordPlus) WHERE id(keywordPlus) = nodeId
        RETURN keywordPlus.keywordPlus AS keywordPlus, centrality AS betweennessCentrality
        ORDER BY centrality DESC
        
**Write betweenness centrality scores to `KeywordPlus`** nodes that connect via **`CO_OCCURRED_WITH`**:

        CALL algo.betweenness('KeywordPlusGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'keywordPlusGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

**Write betweenness centrality scores to `KeywordPlus`** nodes that connect via **`CO_OCCURRED_WITH_UNWEIGHTED`**:

        CALL algo.betweenness('KeywordPlusGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedKeywordPlusGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


### 3.1.2. Normalize betweenness centralities

**Stream normalized** `unweightedKeywordPlusGraphBetweennessCentrality` scores:

        MATCH(n:KeywordPlus)
	WHERE EXISTS (n.unweightedKeywordPlusGraphBetweennessCentrality)
	WITH COLLECT (n.unweightedKeywordPlusGraphBetweennessCentrality) as absoluteCentralities, max(n.unweightedKeywordPlusGraphBetweennessCentrality) as maxCentrality, min(n.unweightedKeywordPlusGraphBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC

Get **minimum and maximum centralities**:

        MATCH (n:KeywordPlus)
	WHERE EXISTS (n.unweightedKeywordPlusGraphBetweennessCentrality)
        UNWIND (n.unweightedKeywordPlusGraphBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | 576489938.8534923     |

**Write normalized** `unweightedKeywordPlusGraphBetweennessCentrality` scores to nodes:

        MATCH (n:KeywordPlus)
	WHERE EXISTS (n.unweightedKeywordPlusGraphBetweennessCentrality)
	SET n.normalizedUnweightedKeywordPlusGraphBetweennessCentrality = (n.unweightedKeywordPlusGraphBetweennessCentrality - 0) / (576489938.8534923 - 0)


## 3.2. Betweenness centralities in **author keywords** graph:

### 3.2.1. Calculate betweenness centralities

**Stream betweenness centrality scores for `AuthorKeyword`**:

        CALL algo.betweenness.stream('AuthorKeywordGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (authorKeyword:AuthorKeyword) WHERE id(authorKeyword) = nodeId
        RETURN authorKeyword.authorKeyword AS authorKeyword, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores to `AuthorKeyword`** nodes that connect via **`CO_OCCURRED_WITH`**:

        CALL algo.betweenness('AuthorKeywordGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'authorKeywordGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

**Write betweenness centrality scores to `AuthorKeyword`** nodes that connect via **`CO_OCCURRED_WITH_UNWEIGHTED`**:

        CALL algo.betweenness('AuthorKeywordGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedAuthorKeywordGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


### 3.2.2. Normalize betweenness centralities

**Stream normalized** `unweightedAuthorKeywordGraphBetweennessCentrality` scores:

        MATCH(n:AuthorKeyword)
	WHERE EXISTS (n.unweightedAuthorKeywordGraphBetweennessCentrality)
	WITH COLLECT (n.unweightedAuthorKeywordGraphBetweennessCentrality) as absoluteCentralities, max(n.unweightedAuthorKeywordGraphBetweennessCentrality) as maxCentrality, min(n.unweightedAuthorKeywordGraphBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC

Get **minimum and maximum centralities**:

        MATCH (n:AuthorKeyword)
	WHERE EXISTS (n.unweightedAuthorKeywordGraphBetweennessCentrality)
        UNWIND (n.unweightedAuthorKeywordGraphBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | 482046793.90087616     |

**Write normalized** `unweightedAuthorKeywordGraphBetweennessCentrality` scores to nodes:

        MATCH (n:AuthorKeyword)
	WHERE EXISTS (n.unweightedAuthorKeywordGraphBetweennessCentrality)
	SET n.normalizedUnweightedAuthorKeywordGraphBetweennessCentrality = (n.unweightedAuthorKeywordGraphBetweennessCentrality - 0) / (482046793.90087616 - 0)


## 3.3. Betweenness centralities in **annotation** graph:

### 3.3.1. Calculate betweenness centralities

**Stream betweenness centrality scores for `Annotation`**:

        CALL algo.betweenness.stream('AnnotationGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (annotation:Annotation) WHERE id(annotation) = nodeId
        RETURN annotation.annotation AS annotation, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores to `Annotation`** nodes that connect via **`CO_OCCURRED_WITH`**:

        CALL algo.betweenness('AnnotationGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'annotationGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

This query took 2,1 hours to complete

**Write betweenness centrality scores to `Annotation`** nodes that connect via **`CO_OCCURRED_WITH_UNWEIGHTED`**:

        CALL algo.betweenness('AnnotationGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedAnnotationGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


### 3.3.2. Normalize betweenness centralities

**Stream normalized** `unweightedAnnotationGraphBetweennessCentrality` scores:

        MATCH(n:Annotation)
	WHERE EXISTS (n.unweightedAnnotationGraphBetweennessCentrality)
	WITH COLLECT (n.unweightedAnnotationGraphBetweennessCentrality) as absoluteCentralities, max(n.unweightedAnnotationGraphBetweennessCentrality) as maxCentrality, min(n.unweightedAnnotationGraphBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC

Get **minimum and maximum centralities**:

        MATCH (n:Annotation)
	WHERE EXISTS (n.unweightedAnnotationGraphBetweennessCentrality)
        UNWIND (n.unweightedAnnotationGraphBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | 274731992.4064494     |

**Write normalized** `unweightedAnnotationGraphBetweennessCentrality` scores to nodes:

        MATCH (n:Annotation)
	WHERE EXISTS (n.unweightedAnnotationGraphBetweennessCentrality)
	SET n.normalizedUnweightedAnnotationGraphBetweennessCentrality = (n.unweightedAnnotationGraphBetweennessCentrality - 0) / (274731992.4064494 - 0)        

        
## 3.4. Betweenness centralities in **subject categories** graph:

### 3.4.1. Calculate betweenness centralities

**Stream betweenness centrality scores for `SubjectCategory`**:

        CALL algo.betweenness.stream('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (subjectCategory:SubjectCategory) WHERE id(subjectCategory) = nodeId
        RETURN subjectCategory.subjectCategory AS subjectCategory, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores to `SubjectCategory`** nodes that connect via **`CO_OCCURRED_WITH`**:

        CALL algo.betweenness('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'subjectCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

**Write betweenness centrality scores to `SubjectCategory`** nodes that connect via **`CO_OCCURRED_WITH_UNWEIGHTED`**:

        CALL algo.betweenness('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedSubjectCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

### 3.4.2. Normalize betweenness centralities

**Stream normalized** `unweightedSubjectCategoryGraphBetweennessCentrality` scores:

        MATCH(n:SubjectCategory)
	WHERE EXISTS (n.unweightedSubjectCategoryGraphBetweennessCentrality)
	WITH COLLECT (n.unweightedSubjectCategoryGraphBetweennessCentrality) as absoluteCentralities, max(n.unweightedSubjectCategoryGraphBetweennessCentrality) as maxCentrality, min(n.unweightedSubjectCategoryGraphBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC

Get **minimum and maximum centralities**:

        MATCH (n:SubjectCategory)
	WHERE EXISTS (n.unweightedSubjectCategoryGraphBetweennessCentrality)
        UNWIND (n.unweightedSubjectCategoryGraphBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | 1309.6523634772705     |

**Write normalized** `unweightedSubjectCategoryGraphBetweennessCentrality` scores to nodes:

        MATCH (n:SubjectCategory)
	WHERE EXISTS (n.unweightedSubjectCategoryGraphBetweennessCentrality)
	SET n.normalizedUnweightedSubjectCategoryGraphBetweennessCentrality = (n.unweightedSubjectCategoryGraphBetweennessCentrality - 0) / (1309.6523634772705 - 0)        


## 3.5. Betweenness centralities in **Web of Science categories** graph:

### 3.5.1. Calculate betweenness centralities

**Stream betweenness centrality scores for `WosCategory`**:

        CALL algo.betweenness.stream('WosCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (wosCategory:WosCategory) WHERE id(wosCategory) = nodeId
        RETURN wosCategory.wosCategory AS wosCategory, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores to `WosCategory`** nodes that connect via **`CO_OCCURRED_WITH`**:

        CALL algo.betweenness('WosCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'wosCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

**Write betweenness centrality scores to `WosCategory`** nodes that connect via **`CO_OCCURRED_WITH_UNWEIGHTED`**:

        CALL algo.betweenness('WosCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedWosCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

### 3.5.2. Normalize betweenness centralities

**Stream normalized** `unweightedWosCategoryGraphBetweennessCentrality` scores:

        MATCH(n:WosCategory)
	WHERE EXISTS (n.unweightedWosCategoryGraphBetweennessCentrality)
	WITH COLLECT (n.unweightedWosCategoryGraphBetweennessCentrality) as absoluteCentralities, max(n.unweightedWosCategoryGraphBetweennessCentrality) as maxCentrality, min(n.unweightedWosCategoryGraphBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC

Get **minimum and maximum centralities**:

        MATCH (n:WosCategory)
	WHERE EXISTS (n.unweightedWosCategoryGraphBetweennessCentrality)
        UNWIND (n.unweightedWosCategoryGraphBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | 5099.378299140871     |

**Write normalized** `unweightedWosCategoryGraphBetweennessCentrality` scores to nodes:

        MATCH (n:WosCategory)
	WHERE EXISTS (n.unweightedWosCategoryGraphBetweennessCentrality)
	SET n.normalizedUnweightedWosCategoryGraphBetweennessCentrality = (n.unweightedWosCategoryGraphBetweennessCentrality - 0) / (5099.378299140871 - 0)        


# 4. COMMUNITY DETECTION

## 4.1. Detecting communities in KeywordPlus graph

**Stream** keywordPlus communities using:

        CALL algo.louvain.stream('KeywordPlus', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, community

        MATCH (keywordPlus:KeywordPlus) WHERE id(keywordPlus) = nodeId

        RETURN keywordPlus.keywordPlus AS keywordPlus, community
        ORDER BY community


**Write** keywordPlus communities to nodes:

        CALL algo.louvain('KeywordPlus', 'CO_OCCURRED_WITH_UNWEIGHTED', {write:true, writeProperty:'keywordPlusSubGraphCommunity'})
        YIELD nodes, communityCount, iterations, loadMillis, computeMillis, writeMillis;

## 4.2. Detecting communities in AuthorKeyword graph
## 4.3. Detecting communities in Annotation graph
## 4.4. Detecting communities in SubjectCategory graph
## 4.5. Detecting communities in WosCategory graph
**Stream** wosCategory communities using:

        CALL algo.louvain.stream('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {})
        YIELD nodeId, community

        MATCH (subjectCategory:SubjectCategoryGraphMainComponentNode) WHERE id(subjectCategory) = nodeId

        RETURN subjectCategory.subjectCategory AS subjectCategory, community
        ORDER BY community


**Write** subjectCategory communities to nodes:

        CALL algo.louvain('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH_UNWEIGHTED', {write:true, writeProperty:'subjectCategorySubGraphCommunity'})
        YIELD nodes, communityCount, iterations, loadMillis, computeMillis, writeMillis;



# 5. REFACTORING

## 5.1. Rename properties from 'n.n' format to 'n.name'

### 5.1.1. Rename `keywordPlus` property to `name`

Change `n.keywordPlus` to `n.name`:

        CALL apoc.periodic.iterate(
                "MATCH (n:KeywordPlus) RETURN n",
                "SET n.name = n.keywordPlus REMOVE n.keywordPlus", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Drop the old index on `n.keywordPlus`:

        DROP INDEX ON :KeywordPlus(keywordPlus)

Create new index on `n.name`:

        CREATE INDEX ON :KeywordPlus(name)


### 5.1.2. Rename `authorKeyword` property to `name`

Change `n.authorKeyword` to `n.name`:

        CALL apoc.periodic.iterate(
                "MATCH (n:AuthorKeyword) RETURN n",
                "SET n.name = n.authorKeyword REMOVE n.authorKeyword", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Drop the old index on `n.authorKeyword`:

        DROP INDEX ON :AuthorKeyword(authorKeyword)

Create new index on `n.name`:

        CREATE INDEX ON :AuthorKeyword(name)


### 5.1.3.  Rename `annotation` property to `name`

Change `n.annotation` to `n.name`:

        CALL apoc.periodic.iterate(
                "MATCH (n:Annotation) RETURN n",
                "SET n.name = n.annotation REMOVE n.annotation", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Drop the old index on `n.annotation`:

        DROP INDEX ON :Annotation(annotation)

Create new index on `n.name`:

        CREATE INDEX ON :Annotation(name)


### 5.1.4.  Rename `subjectCategory` property to `name`

Change `n.subjectCategory` to `n.name`:

        CALL apoc.periodic.iterate(
                "MATCH (n:SubjectCategory) RETURN n",
                "SET n.name = n.subjectCategory REMOVE n.subjectCategory", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Drop the old index on `n.subjectCategory`:

        DROP INDEX ON :SubjectCategory(subjectCategory)

Create new index on `n.name`:

        CREATE INDEX ON :SubjectCategory(name)


### 5.1.5.  Rename `wosCategory` property to `name`

Change `n.wosCategory` to `n.name`:

        CALL apoc.periodic.iterate(
                "MATCH (n:WosCategory) RETURN n",
                "SET n.name = n.wosCategory REMOVE n.wosCategory", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Drop the old index on `n.wosCategory`:

        DROP INDEX ON :WosCategory(wosCategory)

Create new index on `n.name`:

        CREATE INDEX ON :WosCategory(name)


# 6. CONSTRUCTING THE MULTI-LEVEL TOPIC GRAPH

## 6.1. Refactoring: Add `:Topic` label to all topic categories

### 6.1.1. Add `:Topic` to KeywordPlus

        CALL apoc.periodic.iterate(
                "MATCH (n:KeywordPlus) RETURN n",
                "SET n:Topic",
                {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 6.1.2. Add `:Topic` to AuthorKeyword

        CALL apoc.periodic.iterate(
                "MATCH (n:AuthorKeyword) RETURN n",
                "SET n:Topic",
                {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 6.1.3. Add `:Topic` to Annotation

        CALL apoc.periodic.iterate(
                "MATCH (n:Annotation) RETURN n",
                "SET n:Topic",
                {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

### 6.1.4. Add `:Topic` to SubjectCategory

        CALL apoc.periodic.iterate(
                "MATCH (n:SubjectCategory) RETURN n",
                "SET n:Topic",
                {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


### 6.1.5. Add `:Topic` to WosCategory

        CALL apoc.periodic.iterate(
                "MATCH (n:WosCategory) RETURN n",
                "SET n:Topic",
                {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

## 6.2. Construct the multilevel topic graph

## 6.2.1. Construct the *weighted* multi-level graph

Create a weighted connecion between all topics (this is the first time inter-topic-level connections are being made)

        CALL apoc.periodic.iterate(
                "MATCH (topic1:Topic)-[]-(topic2:Topic) WHERE id(topic1) < id(topic2) RETURN topic1, topic2, count(*) as times",
                "MERGE (topic1)-[coOccurredWith:CO_OCCURRED_WITH_MULTILEVEL]->(topic2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 6.2.1. Construct the *unweighted* multi-level graph 

Create one relationship per connection within and between topic levels:

        CALL apoc.periodic.iterate(
                "MATCH (topic1:Topic)-[]-(topic2:Topic) WHERE id(topic1) < id(topic2) RETURN topic1, topic2, count(*) as times",
                "FOREACH (i IN RANGE(1, times) | CREATE (topic1)-[:CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED]->(topic2)) ",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

## 6.3. Map the components of the multi-level graph

**Stream `Topic` graph components**:

        CALL algo.unionFind.stream('Topic', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (topic:Topic) WHERE id(topic) = nodeId
        RETURN topic.name AS topic, setId
        ORDER BY setId


**Write `Topic` graph components** to nodes:

        CALL algo.unionFind('Topic', 'CO_OCCURRED_WITH', {write:true, partitionProperty:'topicSubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


Get the `mainSetId` of the **main component**:

        MATCH (topic:Topic)
        UNWIND topic.topicSubGraphComponent as topicSubGraphComponent
        WITH topicSubGraphComponent, COUNT(topic) as count
        ORDER BY (count) DESC
        RETURN topicSubGraphComponent, count
        // for extracting the most common setId, uncomment the two lines below (and comment out the RETURN statement above)
        // WITH apoc.agg.first(topicSubGraphComponent) as mainSetId
        // RETURN mainSetId


| topicSubGraphComponent | count  |
| ---------------------- | -----  |
| 176206	         | 167354 |
| 325613	         | 155796 |
| 276625	         | 100153 |

The most frequent setIds are `176206`,`325613`, and `276625`.


**Write `TopicGraphMainComponentOneNode`, label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (topic:Topic) WHERE topic.topicSubGraphComponent = 176206 RETURN topic",
          "SET topic:TopicGraphMainComponentOneNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

**Write `TopicGraphMainComponentTwoNode`, label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (topic:Topic) WHERE topic.topicSubGraphComponent = 325613 RETURN topic",
          "SET topic:TopicGraphMainComponentTwoNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

**Write `TopicGraphMainComponentThreeNode`, label** to nodes in the main component:

        CALL apoc.periodic.iterate(
          "MATCH (topic:Topic) WHERE topic.topicSubGraphComponent = 276625 RETURN topic",
          "SET topic:TopicGraphMainComponentThreeNode", {batchSize:10000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

## 6.4. Calculate betweenness centralities for the three main components of the multi-topic graph

### 3.5.1. Calculate betweenness centralities

**Write betweenness centrality scores to `Topic`** nodes in `TopicGraphMainComponentOneNode` that connect via **`CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED`**:

        CALL algo.betweenness('TopicGraphMainComponentOneNode', 'CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedTopicGraphComponentOneBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

**Write betweenness centrality scores to `Topic`** nodes in `TopicGraphMainComponentTwoNode` that connect via **`CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED`**:

        CALL algo.betweenness('TopicGraphMainComponentTwoNode', 'CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedTopicGraphComponentTwoBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


**Write betweenness centrality scores to `Topic`** nodes in `TopicGraphMainComponentThreeNode` that connect via **`CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED`**:

        CALL algo.betweenness('TopicGraphMainComponentThreeNode', 'CO_OCCURRED_WITH_MULTILEVEL_UNWEIGHTED', {direction:'both', write:true, writeProperty:'unweightedTopicGraphComponentThreeBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


### TODO ###
### 3.5.2. Normalize betweenness centralities

#### 3.5.2.0. Preview the operation

**Stream normalized** `unweightedTopicGraphComponentOneBetweennessCentrality` scores (for testing, only for Main Component One):

        MATCH(n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentOneBetweennessCentrality)
	WITH COLLECT (n.unweightedTopicGraphComponentOneBetweennessCentrality) as absoluteCentralities, max(n.unweightedTopicGraphComponentOneBetweennessCentrality) as maxCentrality, min(n.unweightedTopicGraphComponentOneBetweennessCentrality) as minCentrality
	UNWIND absoluteCentralities AS eachAbsoluteCentrality
	RETURN (eachAbsoluteCentrality - minCentrality) / (maxCentrality - minCentrality) AS normalizedBetweennessCentrality, eachAbsoluteCentrality AS absoluteBetweennessCentrality
	ORDER BY normalizedBetweennessCentrality DESC


#### 3.5.2.1. Normalize main component one betweenness centralities 

Get **minimum and maximum centralities** for *main component one*:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentOneBetweennessCentrality)
        UNWIND (n.unweightedTopicGraphComponentOneBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | XXXXXXXXXXXXXXX     |

**Write normalized** `unweightedTopicGraphComponentOneBetweennessCentrality` scores to nodes:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentOneBetweennessCentrality)
	SET n.normalizedUnweightedTopicGraphComponentOneBetweennessCentrality = (n.unweightedTopicGraphComponentOneBetweennessCentrality - 0) / (XXXXXXXXXXXXXXX - 0)        


#### 3.5.2.2. Normalize main component two betweenness centralities

Get **minimum and maximum centralities** for `*main component two*:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentTwoBetweennessCentrality)
        UNWIND (n.unweightedTopicGraphComponentTwoBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | XXXXXXXXXXXXXXX     |

**Write normalized** `unweightedTopicGraphComponentTwoBetweennessCentrality` scores to nodes:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentTwoBetweennessCentrality)
	SET n.normalizedUnweightedTopicGraphComponentTwoBetweennessCentrality = (n.unweightedTopicGraphComponentTwoBetweennessCentrality - 0) / (XXXXXXXXXXXXXXX - 0)        


#### 3.5.2.3. Normalize main component three betweenness centralities

Get **minimum and maximum centralities** for *main component three*:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentThreeBetweennessCentrality)
        UNWIND (n.unweightedTopicGraphComponentThreeBetweennessCentrality) as centralitiesList
	RETURN min(centralitiesList), max(centralitiesList)

This query returns:

| min(centralitiesList) | max(centralitiesList) |
|-----------------------|-----------------------|
| 0.0                   | XXXXXXXXXXXXXXX     |

**Write normalized** `unweightedTopicGraphComponentThreeBetweennessCentrality` scores to nodes:

        MATCH (n:Topic)
	WHERE EXISTS (n.unweightedTopicGraphComponentThreeBetweennessCentrality)
	SET n.normalizedUnweightedTopicGraphComponentThreeBetweennessCentrality = (n.unweightedTopicGraphComponentThreeBetweennessCentrality - 0) / (XXXXXXXXXXXXXXX - 0)        





# 7. GRAPH VISUALIZATION

## A. Gephi graph streaming
https://secdiary.com/streaming-data-from-neo4j-to-gephi/


### Solutions:
Note: Current remote and local IPs can be viewed [here](https://www.whatismyip.com/)

Remote ip address (does not work):

    MATCH path = (:Person)-[:DIRECTED]->(:Movie)<-[:ACTED_IN]-(:Person)
    CALL apoc.gephi.add('http://145.121.16.198:8080','workspace1',path,'weight',['born','name','title', 'released']) yield nodes
    return *
    
    # returns error:
    Neo.ClientError.Procedure.ProcedureCallFailed: Failed to invoke procedure `apoc.gephi.add`: Caused by: java.net.SocketTimeoutException: connect timed out

Local ip address:

    MATCH path = (:Person)-[:DIRECTED]->(:Movie)<-[:ACTED_IN]-(:Person)
    CALL apoc.gephi.add('http://192.168.42.165:8080','workspace1',path,'weight',['born','name','title', 'released']) yield nodes
    return *

    
`localhost:8080`:

    MATCH path = (:Person)-[:DIRECTED]->(:Movie)<-[:ACTED_IN]-(:Person)
    CALL apoc.gephi.add('http://localhost:8080','workspace1',path,'weight',['born','name','title', 'released']) yield nodes
    return *
    
`null` for local

    MATCH path = (:Person)-[:DIRECTED]->(:Movie)<-[:ACTED_IN]-(:Person)
    CALL apoc.gephi.add(null,'workspace1',path,'weight',['born','name','title', 'released']) yield nodes
    return *



## B. Neovis
https://medium.com/neo4j/graph-visualization-with-neo4j-using-neovis-js-a2ecaaa7c379
https://github.com/neo4j-contrib/neovis.js

# X - Demos for meeting

        MATCH (n:WosCategory)
        WHERE EXISTS (n.unweightedWosCategoryGraphBetweennessCentrality)
        RETURN n.wosCategory, n.wosCategoryGraphBetweennessCentrality, n.unweightedWosCategoryGraphBetweennessCentrality , n.normalizedUnweightedWosCategoryGraphBetweennessCentrality
        ORDER BY n.normalizedUnweightedWosCategoryGraphBetweennessCentrality


## 7.1. Stream `keywordPlus` graph to Gephi

Stream to Gephi:

        MATCH path = (:KeywordPlusGraphMainComponentNode)-[:CO_OCCURRED_WITH]->(:KeywordPlusGraphMainComponentNode)
        CALL apoc.gephi.add('http://localhost:8080', 'workspace1', path, 'times', ['keywordPlus', 'normalizedUnweightedKeywordPlusGraphBetweennessCentrality']) yield nodes
        RETURN *


## 7.2. Stream `authorKeyword` graph to Gephi

Stream to Gephi:

        MATCH path = (:AuthorKeywordGraphMainComponentNode)-[:CO_OCCURRED_WITH]->(:AuthorKeywordGraphMainComponentNode)
        CALL apoc.gephi.add('http://localhost:8080', 'workspace1', path, 'times', ['authorKeyword', 'normalizedUnweightedAuthorKeywordGraphBetweennessCentrality']) yield nodes
        RETURN *


## 7.3. Stream `annotation` graph to Gephi

Stream to Gephi:

        MATCH path = (:AnnotationGraphMainComponentNode)-[:CO_OCCURRED_WITH]->(:AnnotationGraphMainComponentNode)
        CALL apoc.gephi.add('http://localhost:8080', 'workspace1', path, 'times', ['annotation', 'normalizedUnweightedAnnotationGraphBetweennessCentrality']) yield nodes
        RETURN *    


## 7.4. Stream `subjectCategory` graph to Gephi

Stream to Gephi:

        MATCH path = (:SubjectCategoryGraphMainComponentNode)-[:CO_OCCURRED_WITH]->(:SubjectCategoryGraphMainComponentNode)
        CALL apoc.gephi.add('http://localhost:8080', 'workspace1', path, 'times', ['subjectCategory', 'normalizedUnweightedSubjectCategoryGraphBetweennessCentrality']) yield nodes
        RETURN *


## 7.5. Stream `wosCategory` graph to Gephi

Stream to Gephi:

        MATCH path = (:WosCategoryGraphMainComponentNode)-[:CO_OCCURRED_WITH]->(:WosCategoryGraphMainComponentNode)
        CALL apoc.gephi.add('http://localhost:8080', 'workspace1', path, 'times', ['wosCategory', 'normalizedUnweightedWosCategoryGraphBetweennessCentrality']) yield nodes
        RETURN *












<!-- 

THE OLD CODE (Author clustering approach)
------------------------------------------------------------------------------------------


## 2.1. Annotations graph

**Create** the annotations graph in batches:

        CALL apoc.periodic.iterate(
          "MATCH (author1:Author)-[:HAS_RESEARCHED]->(annotation:Annotation)<-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN author1, annotation, author2",
          "CREATE (author1)-[:SHARES_TOPIC_WITH {type:'Annotation', topic:annotation.annotation}]->(author2)", {batchSize:100}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

`WHERE id(author1) < id(author2)` statement is for ensuring that all the relationships are one-way.

### Alternative (unused) scripts for reference

**Create** the annotations graph in batches using **new design**:
        TODO: Use incrementation for incrementing numbers weights (`r.weight = r.weight + 1`) and aggregation to append annotations to a list (`r.annotations = r.annotations + annotation.annotation`). However, to be able to run the algorithms on actual connections, each five topic type should still have their own relationship types (+ an additional type for aggregations)

        CALL apoc.periodic.iterate(
          "MATCH (author1:Author)-[:HAS_RESEARCHED]->(annotation:Annotation)<-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN author1, annotation, author2",
          "CREATE (author1)-[:SHARES_ANNOTATION_WITH {annotation:annotation.annotation}]->(author2) CREATE (author1)-[:SHARES_TOPIC_WITH {type:'Annotation', topic:annotation.annotation}]->(author2)", {batchSize:100}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


Create the **annotations graph in one go**:
        
        MATCH (author1:Author)-[:HAS_RESEARCHED]->(annotation:Annotation)<-[:HAS_RESEARCHED]-(author2:Author)
        WHERE id(author1) < id(author2)  // ensure that the relationship is one sided
        CREATE (author1)-[rel:SHARES_TOPIC_WITH {type:'Annotation', topic:annotation.annotation}]->(author2) 
        // RETURN author1, rel, author2 
        // LIMIT 1000

Project the **virtual annotations graph**:
        
        MATCH (author1:Author)-[:HAS_RESEARCHED]-(annotation:Annotation)-[:HAS_RESEARCHED]-(author2:Author)
        WHERE NOT id(author1) = id(author2)
        CALL apoc.create.vRelationship(author1, 'SHARES_TOPIC_WITH', {type:'Annotation', topic:annotation.annotation}, author2) 
        YIELD rel
        RETURN *
        LIMIT 25

## 2.2. Author keywords graph

**Create** the author keywords graph in batches:

        CALL apoc.periodic.iterate(
          "MATCH (author1:Author)-[:HAS_RESEARCHED]->(authorKeyword:AuthorKeyword)<-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN author1, authorKeyword, author2",
          "CREATE (author1)-[:SHARES_TOPIC_WITH {type:'AuthorKeyword', topic:authorKeyword.authorKeyword}]->(author2)", {batchSize:100}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

`WHERE id(author1) < id(author2)` statement is for ensuring that all the relationships are one-way.




## x.x. INDEXING

## 2.3. WoS categories graph

### 2.3.1. Wos categories
**Create** the author keywords graph in batches:

        CALL apoc.periodic.iterate(
          "MATCH (author1:Author)-[:HAS_RESEARCHED]->(wosCategory:WosCategory)<-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN author1, wosCategory, author2",
          "CREATE (author1)-[:SHARES_TOPIC_WITH {type:'WosCategory', topic:wosCategory.wosCategory}]->(author2)", {batchSize:100}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken

`WHERE id(author1) < id(author2)` statement is for ensuring that all the relationships are one-way.


### 2.3.2. Wos supercategories


## 2.4. Subject categories graph

## 2.5. Keywords plus graph


# 3. MAPPING GRAPH CONNECTIVITY

In unionFind, the direction of connections is ignored:
"The direction of the relationships in our graph are ignored - we treat the graph as undirected." (from graph algorithms documentation)


## 3.1. Testing the unionFind algorithm in GoT sandbox

**Stream GoT graph components** with `unionFind`:

        CALL algo.unionFind(
        'MATCH (character:Character)-[:INTERACTS1]-() 
        RETURN id(character) AS id',
        'MATCH (character1:Character)-[:INTERACTS1]-(character2)
        WHERE NOT id(character1) = id(character2)
        RETURN id(character1) AS source, id(character2) AS target',
        {graph:'cypher', write:true}
        )
        YIELD nodes, setCount;

The query **above is the equivalent** of this query:

        CALL algo.unionFind('Character', 'INTERACTS1', {write:true})
        YIELD nodes, setCount;
        

## 3.2. Mapping the components of the combined topic graph

**Stream combined topic graph components** in the **actual** graph using:

        CALL algo.unionFind.stream('Author', 'SHARES_TOPIC_WITH', {})
        YIELD nodeId,setId
        WITH nodeId, setId LIMIT 10000
        MATCH (author:Author) WHERE id(author) = nodeId
        RETURN author.name AS author, setId
        ORDER BY setId DESC


**Write combined topic graph components** to nodes using **actual** relationships:

        CALL algo.unionFind('Author', 'SHARES_TOPIC_WITH', {write:true, partitionProperty:'annotationSubGraphComponent'})
        YIELD nodes, setCount, loadMillis, computeMillis, writeMillis


## 3.3. Mapping the components of the annotation graph

  **Stream annotation graph components** using **virtual** relationships:


        CALL algo.unionFind.stream(
                'MATCH (author:Author)-[:HAS_RESEARCHED]-(:Annotation) RETURN id(author) AS id',
                'MATCH (author1:Author)-[:HAS_RESEARCHED]-(annotation:Annotation)-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN id(author1) AS source, id(author2) AS target',
                {graph:'cypher'}
        )
        YIELD nodeId, setId
        WITH nodeId, setId
        MATCH (author:Author) WHERE id(author) = nodeId
        RETURN author.name AS author, setId
        ORDER BY setId

       
**Write annotation graph components** to nodes using **virtual** relationships:

        CALL algo.unionFind(
                'MATCH (author:Author)-[:HAS_RESEARCHED]-(:Annotation) RETURN id(author) AS id',
                'MATCH (author1:Author)-[:HAS_RESEARCHED]-(annotation:Annotation)-[:HAS_RESEARCHED]-(author2:Author) WHERE id(author1) < id(author2) RETURN id(author1) AS source, id(author2) AS target',
                {graph:'cypher', write:true, partitionProperty:'annotationSubGraphComponent'}
                
        )
        YIELD nodes, setCount;

 -->
