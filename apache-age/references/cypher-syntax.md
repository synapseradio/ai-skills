---
title: AGE Cypher Syntax Reference
description: Complete syntax reference for running Cypher queries in Apache AGE, including all major clauses, patterns, and the cypher() function wrapper.
tags: apache-age, cypher, syntax, match, create, merge, where, return, with, set, delete
---

# AGE Cypher Syntax Reference

## Table of Contents

1. [The cypher() Function](#the-cypher-function)
2. [Graph Setup](#graph-setup)
3. [Pattern Syntax](#pattern-syntax)
   - [Vertex Patterns](#vertex-patterns)
   - [Edge Patterns](#edge-patterns)
   - [Variable-Length Edges](#variable-length-edges)
4. [MATCH](#match)
5. [CREATE](#create)
6. [MERGE](#merge)
7. [SET and REMOVE](#set-and-remove)
8. [DELETE and DETACH DELETE](#delete-and-detach-delete)
9. [RETURN](#return)
10. [WHERE](#where)
11. [WITH](#with)
12. [ORDER BY, SKIP, LIMIT](#order-by-skip-limit)
13. [UNWIND](#unwind)
14. [Operators](#operators)
15. [Functions Quick Reference](#functions-quick-reference)
16. [AGE-Specific Gotchas](#age-specific-gotchas)

---

## The cypher() Function

Every Cypher query in AGE runs through the `cypher()` SQL function. This is not optional — there is no standalone Cypher REPL.

**Signature:**
```sql
cypher(graph_name text, query_string text [, params agtype])
  RETURNS SETOF agtype
```

**Minimal form:**
```sql
SELECT * FROM cypher('graph_name', $$
  <Cypher here>
$$) AS (col agtype);
```

**Column list rules:**
- One `agtype` column per value returned by `RETURN`
- Column names are arbitrary — they do not need to match Cypher variable names
- When a terminal `CREATE`/`MERGE`/`DELETE` produces no rows, declare a placeholder column anyway:

```sql
-- Terminal clause — no rows returned, but column list still required
SELECT * FROM cypher('my_graph', $$
  CREATE (:Person {name: 'Alice'})
$$) AS (v agtype);
-- Returns 0 rows
```

**Dollar-quoting:** Use `$$` to avoid escaping single quotes inside the Cypher query body.

**Parameterized queries:** Pass an agtype map as the third argument; reference values with `$param_name`:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: $name})
  RETURN p
$$, '{"name": "Alice"}') AS (p agtype);
```

---

## Graph Setup

Create a graph (must be done before any Cypher queries):

```sql
SELECT create_graph('my_graph');
```

Drop a graph:

```sql
SELECT drop_graph('my_graph', true);  -- true = cascade (drops all data)
```

Load the extension (once per database):

```sql
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
```

The `SET search_path` is required in every session (or set it permanently in `postgresql.conf` / `ALTER DATABASE`):

```sql
ALTER DATABASE mydb SET search_path = ag_catalog, "$user", public;
```

---

## Pattern Syntax

### Vertex Patterns

| Pattern                  | Meaning                              |
|--------------------------|--------------------------------------|
| `(n)`                    | Any vertex, bound to variable `n`    |
| `(:Person)`              | Any vertex with label `Person`       |
| `(n:Person)`             | Vertex with label `Person`, variable `n` |
| `(n:Person {name: 'Alice'})` | Vertex with label and property filter |
| `({name: 'Alice'})`      | Any vertex with property (no label)  |

### Edge Patterns

| Pattern              | Meaning                                      |
|----------------------|----------------------------------------------|
| `-[]-`               | Any edge, any direction                      |
| `-[r]-`              | Any edge, bound to `r`                       |
| `-[:KNOWS]->`        | Outgoing edge with label `KNOWS`             |
| `<-[:KNOWS]-`        | Incoming edge with label `KNOWS`             |
| `-[r:KNOWS]->`       | Outgoing `KNOWS` edge, bound to `r`          |
| `-[r:KNOWS {since: 2020}]->` | Edge with property filter          |

**AGE edge direction syntax** uses `>>` for outgoing and `<<` for incoming in some contexts:

```sql
-- Both forms are valid in AGE:
MATCH (a)-[:KNOWS]->(b)   -- standard
MATCH (a)-[:KNOWS]->>(b)  -- AGE extended form (also valid)
MATCH (a)<<-[:KNOWS]-(b)  -- incoming with AGE extended form
```

**Multiple edges in one pattern:**

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Charlie'})-[:ACTED_IN]->(movie)<-[:DIRECTED]-(director)
  RETURN movie.title, director.name
$$) AS (title agtype, director agtype);
```

### Variable-Length Edges

Match paths of variable depth using `*`:

| Pattern         | Meaning                                     |
|-----------------|---------------------------------------------|
| `-[*]->`        | Any number of hops (unbounded)             |
| `-[*2]->`       | Exactly 2 hops                             |
| `-[*2..5]->`    | Between 2 and 5 hops (inclusive)           |
| `-[*2..]->`     | 2 or more hops                             |
| `-[*..5]->`     | Up to 5 hops                               |

```sql
-- Find friends-of-friends (exactly 2 hops)
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'})-[:KNOWS*2]->(fof:Person)
  RETURN fof.name
$$) AS (name agtype);

-- Find all reachable people within 3 hops
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'})-[:KNOWS*1..3]->(b:Person)
  RETURN b.name
$$) AS (name agtype);

-- Capture the full path
SELECT * FROM cypher('my_graph', $$
  MATCH p = (a:Person {name: 'Alice'})-[:KNOWS*]->(b:Person)
  RETURN p
$$) AS (p agtype);
```

---

## MATCH

MATCH searches the graph for patterns. Results are rows — one per unique pattern match.

**Get all vertices:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (v)
  RETURN v
$$) AS (v agtype);
```

**Get vertices by label:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  RETURN p.name, p.age
$$) AS (name agtype, age agtype);
```

**Get vertices by property:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  RETURN p
$$) AS (p agtype);
```

**Traverse an edge:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person)-[:KNOWS]->(b:Person)
  RETURN a.name AS person, b.name AS knows
$$) AS (person agtype, knows agtype);
```

**Optional match (like LEFT JOIN):**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  OPTIONAL MATCH (p)-[:HAS_PET]->(pet)
  RETURN p.name, pet.name
$$) AS (person agtype, pet agtype);
-- pet.name will be null for people without pets
```

**Multiple MATCH clauses:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'})
  MATCH (b:Person {name: 'Bob'})
  RETURN a, b
$$) AS (a agtype, b agtype);
```

---

## CREATE

CREATE creates new vertices and/or edges. It does not check for existing data.

**Create a single vertex:**
```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (n:Person {name: 'Alice', age: 30})
$$) AS (v agtype);
```

**Create multiple vertices:**
```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (:Person {name: 'Alice'}), (:Person {name: 'Bob'})
$$) AS (v agtype);
```

**Create an edge between existing vertices:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
  CREATE (a)-[:KNOWS {since: 2021}]->(b)
$$) AS (e agtype);
```

**Create and return:**
```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (p:Person {name: 'Charlie', age: 25})
  RETURN p
$$) AS (p agtype);
```

**Create a path in one statement:**
```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (a:Person {name: 'Alice'})-[:KNOWS]->(b:Person {name: 'Bob'})
$$) AS (v agtype);
```

---

## MERGE

MERGE matches an existing pattern or creates it if absent. Use `ON CREATE SET` and `ON MATCH SET` to differentiate behavior.

**Basic MERGE (upsert a vertex):**
```sql
SELECT * FROM cypher('my_graph', $$
  MERGE (p:Person {name: 'Alice'})
  RETURN p
$$) AS (p agtype);
```

**MERGE with ON CREATE / ON MATCH:**
```sql
SELECT * FROM cypher('my_graph', $$
  MERGE (p:Person {name: 'Alice'})
  ON CREATE SET p.created_at = 1706745600, p.login_count = 1
  ON MATCH SET p.login_count = p.login_count + 1
  RETURN p
$$) AS (p agtype);
```

**MERGE an edge:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
  MERGE (a)-[r:KNOWS]->(b)
  ON CREATE SET r.since = 2024
  RETURN r
$$) AS (r agtype);
```

---

## SET and REMOVE

### SET

SET updates or adds properties on existing vertices or edges.

```sql
-- Set a single property
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  SET p.age = 31
  RETURN p
$$) AS (p agtype);

-- Set multiple properties
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  SET p.age = 31, p.email = 'alice@example.com'
  RETURN p
$$) AS (p agtype);

-- Replace all properties with a map
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  SET p = {name: 'Alice', age: 31}
  RETURN p
$$) AS (p agtype);

-- Merge properties (additive, does not remove existing keys)
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  SET p += {age: 31, verified: true}
  RETURN p
$$) AS (p agtype);
```

### REMOVE

REMOVE deletes a property from a vertex or edge.

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  REMOVE p.email
  RETURN p
$$) AS (p agtype);
```

---

## DELETE and DETACH DELETE

DELETE removes vertices or edges. Vertices with edges cannot be deleted without `DETACH`.

**Delete an edge:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (:Person {name: 'Alice'})-[r:KNOWS]->(:Person {name: 'Bob'})
  DELETE r
$$) AS (v agtype);
```

**Delete a vertex (only if it has no edges):**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  DELETE p
$$) AS (v agtype);
```

**Delete a vertex and all its edges:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person {name: 'Alice'})
  DETACH DELETE p
$$) AS (v agtype);
```

---

## RETURN

RETURN specifies what to include in query output. Each expression maps to one `agtype` column in the SQL result.

```sql
-- Return full vertex
RETURN p

-- Return specific properties
RETURN p.name, p.age

-- Alias with AS (alias appears in cypher only; SQL column name comes from the AS() list)
RETURN p.name AS name, p.age AS age

-- Return distinct values
RETURN DISTINCT p.city

-- Return count
RETURN count(p)

-- Return with aggregation
RETURN p.city, count(p) AS residents
```

SQL column list must match the number of RETURN expressions:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  RETURN p.name, p.age, count(p) OVER ()
$$) AS (name agtype, age agtype, total agtype);
```

---

## WHERE

WHERE filters pattern matches. Place it immediately after the MATCH or WITH clause it belongs to.

**Property equality:**
```sql
WHERE p.name = 'Alice'
```

**Comparison operators:**
```sql
WHERE p.age > 25
WHERE p.age >= 18 AND p.age < 65
WHERE p.age IN [25, 30, 35]
```

**String predicates:**
```sql
WHERE p.name STARTS WITH 'Al'
WHERE p.name ENDS WITH 'ice'
WHERE p.name CONTAINS 'li'
WHERE p.name =~ 'Al.*'  -- regex
```

**Null checks:**
```sql
WHERE p.email IS NULL
WHERE p.email IS NOT NULL
```

**NOT:**
```sql
WHERE NOT p.name = 'Alice'
WHERE NOT (p)-[:KNOWS]->(q)
```

**Full example:**
```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  WHERE p.age >= 18 AND p.name STARTS WITH 'A'
  RETURN p.name, p.age
$$) AS (name agtype, age agtype);
```

---

## WITH

WITH pipes results from one query part to the next. It is required to chain clauses like MATCH → aggregate → MATCH.

```sql
-- Aggregate, then filter
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)-[:KNOWS]->(friend)
  WITH p, count(friend) AS friend_count
  WHERE friend_count > 3
  RETURN p.name, friend_count
$$) AS (name agtype, friend_count agtype);

-- Introduce a literal
SELECT * FROM cypher('my_graph', $$
  WITH 'Alice' AS target_name
  MATCH (p:Person {name: target_name})
  RETURN p
$$) AS (p agtype);
```

---

## ORDER BY, SKIP, LIMIT

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  RETURN p.name, p.age
  ORDER BY p.age DESC
  SKIP 10
  LIMIT 5
$$) AS (name agtype, age agtype);
```

- `ORDER BY` accepts multiple expressions: `ORDER BY p.age DESC, p.name ASC`
- `SKIP` and `LIMIT` accept integer literals or parameters

---

## UNWIND

UNWIND expands a list into individual rows — the inverse of aggregation.

```sql
-- Expand a literal list
SELECT * FROM cypher('my_graph', $$
  UNWIND [1, 2, 3] AS n
  RETURN n
$$) AS (n agtype);

-- Expand a property that is a list
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  UNWIND p.tags AS tag
  RETURN p.name, tag
$$) AS (name agtype, tag agtype);
```

---

## Operators

### Comparison

| Operator | Meaning            |
|----------|--------------------|
| `=`      | Equal              |
| `<>`     | Not equal          |
| `<`      | Less than          |
| `<=`     | Less or equal      |
| `>`      | Greater than       |
| `>=`     | Greater or equal   |

### Boolean

| Operator | Meaning |
|----------|---------|
| `AND`    | Logical AND |
| `OR`     | Logical OR  |
| `NOT`    | Logical NOT |
| `XOR`    | Logical XOR |

### String

| Operator        | Meaning                        |
|-----------------|--------------------------------|
| `+`             | Concatenation                  |
| `STARTS WITH`   | Prefix match                   |
| `ENDS WITH`     | Suffix match                   |
| `CONTAINS`      | Substring match                |
| `=~`            | Regular expression match       |

### List

| Operator / Form   | Meaning                            |
|-------------------|------------------------------------|
| `+`               | List concatenation                 |
| `IN`              | Element membership test            |
| `[n]`             | Index access (0-based)             |
| `[a..b]`          | Slice                              |

### Mathematical

`+`, `-`, `*`, `/`, `%` (modulo), `^` (exponentiation)

---

## Functions Quick Reference

### Scalar Functions

| Function             | Returns                               |
|----------------------|---------------------------------------|
| `id(n)`              | Internal graphid of a vertex/edge     |
| `labels(n)`          | List of labels on a vertex            |
| `type(r)`            | Label string of an edge               |
| `properties(n)`      | Map of all properties                 |
| `keys(n)`            | List of property key names            |
| `coalesce(a, b, ...)` | First non-null value                 |
| `length(path)`       | Number of edges in a path            |
| `size(list)`         | Number of elements in a list         |
| `toString(x)`        | Convert to string                     |
| `toInteger(x)`       | Convert to integer                    |
| `toFloat(x)`         | Convert to float                      |
| `toBoolean(x)`       | Convert to boolean                    |

### String Functions

| Function                     | Description                    |
|------------------------------|--------------------------------|
| `left(s, n)`                 | First n characters             |
| `right(s, n)`                | Last n characters              |
| `trim(s)`                    | Remove leading/trailing spaces |
| `lTrim(s)` / `rTrim(s)`     | Trim one side                  |
| `toLower(s)` / `toUpper(s)` | Case conversion                |
| `replace(s, find, repl)`    | Substring replacement          |
| `split(s, delim)`           | Split into list                |
| `substring(s, start [, len])` | Extract substring            |
| `size(s)`                    | String length                  |

### List Functions

| Function              | Description                              |
|-----------------------|------------------------------------------|
| `head(list)`          | First element                            |
| `tail(list)`          | All elements except first                |
| `last(list)`          | Last element                             |
| `size(list)`          | Number of elements                       |
| `reverse(list)`       | Reversed list                            |
| `range(start, end [, step])` | Generate integer list          |
| `keys(map)`           | Keys of a map as a list                  |

### Aggregate Functions

| Function      | Description                          |
|---------------|--------------------------------------|
| `count(*)`    | Count all rows                       |
| `count(expr)` | Count non-null values of expr        |
| `sum(expr)`   | Sum of values                        |
| `avg(expr)`   | Average                              |
| `min(expr)`   | Minimum                              |
| `max(expr)`   | Maximum                              |
| `collect(expr)` | Collect values into a list         |
| `stdev(expr)` | Sample standard deviation            |

### Path Functions

| Function                | Description                           |
|-------------------------|---------------------------------------|
| `nodes(path)`           | List of vertices in path              |
| `relationships(path)`   | List of edges in path                 |
| `length(path)`          | Number of edges in path               |
| `shortestPath((a)-[*]->(b))` | Single shortest path           |

---

## AGE-Specific Gotchas

### 1. SET search_path is required every session

Without it, AGE functions like `cypher()` and `create_graph()` are not found:

```sql
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
```

### 2. Column list in AS() must always be present

Even when a clause produces no rows, the AS column list is mandatory:

```sql
-- Correct
SELECT * FROM cypher('g', $$ CREATE (:N) $$) AS (v agtype);

-- Wrong — will error
SELECT * FROM cypher('g', $$ CREATE (:N) $$);
```

### 3. Vertex and edge labels cannot share names

Within a single graph, `Person` cannot be both a vertex label and an edge label.

### 4. Edges require a label

```sql
-- Wrong — edge has no label
CREATE (a)-[]->(b)

-- Correct
CREATE (a)-[:KNOWS]->(b)
```

### 5. graphid is not globally unique across graphs

IDs are unique within a graph, not across graphs. Do not compare `id(n)` values from different graphs.

### 6. String literals use single quotes in Cypher

Output always uses double quotes. Input must use single quotes:

```sql
MATCH (p:Person {name: 'Alice'})  -- correct input
-- Output will show: "Alice"
```

### 7. Numeric literals require ::numeric cast

```sql
-- Wrong — this is a float
RETURN 1.5

-- Correct for exact arithmetic
RETURN 1.5::numeric
```

### 8. MATCH produces one row per unique pattern match

If Alice knows both Bob and Carol, `MATCH (a:Person {name: 'Alice'})-[:KNOWS]->(b)` returns two rows. Always account for fanout when traversing edges.
