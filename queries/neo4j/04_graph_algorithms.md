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


## 1.1. Construct `KeywordPlus` graph
Connect keywords plus nodes to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (keywordPlus1:KeywordPlus)<-[:HAS_KEYWORD_PLUS]-(:Article)-[:HAS_KEYWORD_PLUS]->(keywordPlus2:KeywordPlus) WHERE id(keywordPlus1) < id(keywordPlus2) RETURN keywordPlus1, keywordPlus2, count(*) as times",
                "MERGE (keywordPlus1)-[coOccurredWith:CO_OCCURRED_WITH]->(keywordPlus2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 1.2. Construct `AuthorKeyword` graph
Connect author keywords to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (authorKeyword1:AuthorKeyword)<-[:HAS_AUTHOR_KEYWORD]-(:Article)-[:HAS_AUTHOR_KEYWORD]->(authorKeyword2:AuthorKeyword) WHERE id(authorKeyword1) < id(authorKeyword2) RETURN authorKeyword1, authorKeyword2, count(*) as times",
                "MERGE (authorKeyword1)-[coOccurredWith:CO_OCCURRED_WITH]->(authorKeyword2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 1.3. Construct `Annotation` graph
Connect annotations to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (annotation1:Annotation)<-[:HAS_ANNOTATION]-(:Article)-[:HAS_ANNOTATION]->(annotation2:Annotation) WHERE id(annotation1) < id(annotation2) RETURN annotation1, annotation2, count(*) as times",
                "MERGE (annotation1)-[coOccurredWith:CO_OCCURRED_WITH]->(annotation2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 1.4. Construct `SubjectCategory` graph
Connect ISI subject categories to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (subjectCategory1:SubjectCategory)<-[:HAS_SUBJECT_CATEGORY]-(:Article)-[:HAS_SUBJECT_CATEGORY]->(subjectCategory2:SubjectCategory) WHERE id(subjectCategory1) < id(subjectCategory2) RETURN subjectCategory1, subjectCategory2, count(*) as times",
                "MERGE (subjectCategory1)-[coOccurredWith:CO_OCCURRED_WITH]->(subjectCategory2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken


## 1.5. Construct `WosCategory` graph
Connect Web of Science categories to each other using articles as intermediaries:

        CALL apoc.periodic.iterate(
                "MATCH (wosCategory1:WosCategory)<-[:HAS_WOS_CATEGORY]-(:Article)-[:HAS_WOS_CATEGORY]->(wosCategory2:WosCategory) WHERE id(wosCategory1) < id(wosCategory2) RETURN wosCategory1, wosCategory2, count(*) as times",
                "MERGE (wosCategory1)-[coOccurredWith:CO_OCCURRED_WITH]->(wosCategory2) ON CREATE SET coOccurredWith.times = times ON MATCH SET coOccurredWith.times = coOccurredWith.times + times",
                {batchSize:1000, iterateList:true}
        )
        YIELD batches, total, timeTaken
        RETURN batches, total, timeTaken
        

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

## 3.1. Calculate betweenness centralities in **keywords plus** graph:

**Stream betweenness centrality scores for `KeywordPlus`**:

        CALL algo.betweenness.stream('KeywordPlusGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (keywordPlus:KeywordPlus) WHERE id(keywordPlus) = nodeId
        RETURN keywordPlus.keywordPlus AS keywordPlus, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores for `KeywordPlus`** to nodes:

        CALL algo.betweenness('KeywordPlusGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'keywordPlusGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

## 3.2. Calculate betweenness centralities in **author keywords** graph:

**Stream betweenness centrality scores for `AuthorKeyword`**:

        CALL algo.betweenness.stream('AuthorKeywordGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (authorKeyword:AuthorKeyword) WHERE id(authorKeyword) = nodeId
        RETURN authorKeyword.authorKeyword AS authorKeyword, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores for `AuthorKeyword`** to nodes:

        CALL algo.betweenness('AuthorKeywordGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'authorKeywordGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


## 3.3. Calculate betweenness centralities in **annotation** graph:

**Stream betweenness centrality scores for `Annotation`**:

        CALL algo.betweenness.stream('AnnotationGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (annotation:Annotation) WHERE id(annotation) = nodeId
        RETURN annotation.annotation AS annotation, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores for `Annotation`** to nodes:

        CALL algo.betweenness('AnnotationGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'annotationGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis

This query took 2,1 hours to complete

## 3.4. Calculate betweenness centralities in **subject categories** graph:

**Stream betweenness centrality scores for `SubjectCategory`**:

        CALL algo.betweenness.stream('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (subjectCategory:SubjectCategory) WHERE id(subjectCategory) = nodeId
        RETURN subjectCategory.subjectCategory AS subjectCategory, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores for `SubjectCategory`** to nodes:

        CALL algo.betweenness('SubjectCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'subjectCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


## 3.5. Calculate betweenness centralities in **Web of Science categories** graph:

**Stream betweenness centrality scores for `WosCategory`**:

        CALL algo.betweenness.stream('WosCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both'})
        YIELD nodeId, centrality
        MATCH (wosCategory:WosCategory) WHERE id(wosCategory) = nodeId
        RETURN wosCategory.wosCategory AS wosCategory, centrality AS betweennessCentrality
        ORDER BY centrality DESC

**Write betweenness centrality scores for `WosCategory`** to nodes:

        CALL algo.betweenness('WosCategoryGraphMainComponentNode', 'CO_OCCURRED_WITH', {direction:'both', write:true, writeProperty:'wosCategoryGraphBetweennessCentrality'})
        YIELD nodes, minCentrality, maxCentrality, sumCentrality, loadMillis, computeMillis, writeMillis


# 4. COMMUNITY DETECTION

## 4.1. Detecting communities in KeywordPlus graph

**Stream** keywordPlus communities using:

        CALL algo.louvain.stream('KeywordPlus', 'CO_OCCURRED_WITH', {})
        YIELD nodeId, community

        MATCH (keywordPlus:KeywordPlus) WHERE id(keywordPlus) = nodeId

        RETURN keywordPlus.keywordPlus AS keywordPlus, community
        ORDER BY community


**Write** keywordPlus communities to nodes:

        CALL algo.louvain('KeywordPlus', 'CO_OCCURRED_WITH', {write:true, writeProperty:'keywordPlusSubGraphCommunity'})
        YIELD nodes, communityCount, iterations, loadMillis, computeMillis, writeMillis;


















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












