# Graph Report - c:/Users/dibya/OneDrive/Desktop/Excellence/DATA SCIENCE/Git-Hub project analysis RAG project  (2026-04-18)

## Corpus Check
- Corpus is ~3,465 words - fits in a single context window. You may not need a graph.

## Summary
- 19 nodes · 15 edges · 6 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 1,200 input · 400 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `Chat Interface` - 3 edges
2. `get_github_docs()` - 2 edges
3. `ChatRequest` - 2 edges
4. `get_repos()` - 2 edges
5. `Welcome Interface` - 1 edges
6. `Marked.js` - 1 edges
7. `Highlight.js` - 1 edges

## Surprising Connections (you probably didn't know these)
- `get_github_docs()` --calls--> `get_repos()`  [INFERRED]
  github_fetch.py → main.py
- `Welcome Interface` --conceptually_related_to--> `Chat Interface`  [INFERRED]
  index.html → chat.html

## Communities

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (0): 

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (4): Chat Interface, Highlight.js, Welcome Interface, Marked.js

### Community 2 - "Community 2"
Cohesion: 0.67
Nodes (2): get_github_docs(), get_repos()

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): BaseModel, ChatRequest

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (0): 

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **3 isolated node(s):** `Welcome Interface`, `Marked.js`, `Highlight.js`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 3`** (2 nodes): `BaseModel`, `ChatRequest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (2 nodes): `format_docs()`, `rag_chain.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 5`** (1 nodes): `embed_store.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_repos()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `ChatRequest` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **What connects `Welcome Interface`, `Marked.js`, `Highlight.js` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._