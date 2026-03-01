---
name: apache-age
description: Apache AGE graph database extension for PostgreSQL — Cypher query syntax, agtype data types, hybrid SQL+Cypher patterns (CTEs, JOINs, parameter passing), graph schema modeling (vertices, edges, labels, properties), and performance optimization (indexing, EXPLAIN, batch loading). Use when writing Cypher queries, designing graph schemas, combining graph traversal with relational SQL, or optimizing AGE query performance — all within PostgreSQL via the AGE extension.
---

# Apache AGE

## Quick Start

```sql
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
SELECT create_graph('my_graph');

SELECT * FROM cypher('my_graph', $$
  CREATE (a:Person {name: 'Alice'})-[:KNOWS]->(b:Person {name: 'Bob'})
  RETURN a, b
$$) AS (a agtype, b agtype);
```

## Reference Loading

| Task | Reference | Use for |
|------|-----------|---------|
| Data types and casting | [references/data-types.md](references/data-types.md) | agtype, vertex/edge structure, casting to SQL types, null semantics |
| Cypher syntax | [references/cypher-syntax.md](references/cypher-syntax.md) | MATCH, CREATE, MERGE, SET, DELETE, WHERE, WITH, UNWIND, operators, functions |
| SQL+Cypher integration | [references/hybrid-patterns.md](references/hybrid-patterns.md) | CTEs, JOINs, subqueries, parameter passing, mutation guards, multi-graph |
| Graph schema design | [references/graph-modeling.md](references/graph-modeling.md) | Labels, properties, edge design, common patterns, anti-patterns, hybrid decisions |
| Performance | [references/performance.md](references/performance.md) | Indexing (GIN/BTREE), EXPLAIN, query optimization, batch loading |

## Critical Gotchas

### 1. Always define a column list

`cypher()` returns `SETOF record` — PostgreSQL requires an explicit column list:

```sql
-- Required: AS (col agtype)
SELECT * FROM cypher('g', $$ MATCH (n) RETURN n $$) AS (n agtype);
```

### 2. Terminal clauses need a dummy column

CREATE, SET, DELETE at the end of a query return no rows, but the column list is still mandatory:

```sql
SELECT * FROM cypher('g', $$
  CREATE (:Person {name: 'Alice'})
$$) AS (v agtype);
-- Returns 0 rows
```

### 3. SET = replaces all properties; use += to merge

```cypher
-- Replaces ALL properties with just {age: 30}
SET n = {age: 30}

-- Merges {age: 30} into existing properties
SET n += {age: 30}
```

### 4. CREATE/SET/REMOVE not allowed in JOINs

Mutations inside a JOIN cause errors. Wrap in a CTE instead:

```sql
-- Bad: mutation in JOIN
SELECT * FROM users u JOIN cypher('g', $$ CREATE (:Person) $$) AS (v agtype) ON true;

-- Good: mutation in CTE
WITH new_vertex AS (
  SELECT * FROM cypher('g', $$ CREATE (p:Person {name: 'Alice'}) RETURN p $$) AS (v agtype)
)
SELECT * FROM new_vertex;
```

### 5. No list comprehensions or reduce — use UNWIND + collect()

AGE does not support `[x IN list WHERE ...]` or `reduce()`. Workaround:

```cypher
-- Instead of: RETURN [x IN collect(n.name) WHERE x STARTS WITH 'A']
MATCH (n:Person)
WITH collect(n.name) AS names
UNWIND names AS name
WITH name WHERE name STARTS WITH 'A'
RETURN collect(name)
```

### 6. Indexes must be created manually

AGE creates no indexes by default. Add them on label tables:

```sql
-- GIN for inline property filters like {name: 'Alice'}
CREATE INDEX ON my_graph."Person" USING GIN (properties);

-- BTREE for WHERE clause filters on specific properties
CREATE INDEX ON my_graph."Person"
  USING BTREE (agtype_access_operator(VARIADIC ARRAY[properties, '"name"'::agtype]));

-- BTREE on edge endpoints for traversal performance
CREATE INDEX ON my_graph."KNOWS" USING BTREE (start_id);
CREATE INDEX ON my_graph."KNOWS" USING BTREE (end_id);
```

### 7. search_path must include ag_catalog

Without it, `cypher()` and AGE functions are not found:

```sql
SET search_path = ag_catalog, "$user", public;
-- Or fully qualify: SELECT * FROM ag_catalog.cypher(...)
```
