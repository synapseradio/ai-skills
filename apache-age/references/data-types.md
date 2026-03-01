---
title: AGE Data Types (agtype)
description: Complete reference for the agtype data type — AGE's single return type, a superset of JSON and custom implementation of JSONB.
tags: apache-age, agtype, data-types, vertex, edge, path, cypher
---

# AGE Data Types (agtype)

## Table of Contents

1. [Overview](#overview)
2. [Simple Types](#simple-types)
   - [Null](#null)
   - [Integer](#integer)
   - [Float](#float)
   - [Numeric](#numeric)
   - [Boolean](#boolean)
   - [String](#string)
3. [Composite Types](#composite-types)
   - [List](#list)
   - [Map](#map)
4. [Graph Entity Types](#graph-entity-types)
   - [Vertex](#vertex)
   - [Edge](#edge)
   - [Path](#path)
5. [Type Casting](#type-casting)
6. [AGE NULL vs PostgreSQL NULL](#age-null-vs-postgresql-null)
7. [Comparability Notes](#comparability-notes)

---

## Overview

AGE uses a single custom data type called **agtype** for all values returned by Cypher queries. Every column in a `cypher()` result set is declared as `agtype`. Agtype is:

- A superset of JSON
- A custom implementation of PostgreSQL's JSONB
- The only type returned from `cypher()` function calls

All `cypher()` calls follow this pattern:

```sql
SELECT * FROM cypher('graph_name', $$
  <Cypher query here>
$$) AS (col_name agtype);
```

Multiple return columns require one `agtype` declaration per returned value:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)-[:KNOWS]->(f:Person)
  RETURN p.name, f.name
$$) AS (person agtype, friend agtype);
```

---

## Simple Types

### Null

`null` represents a missing or undefined value. A vertex property that does not exist returns `null` when accessed.

Key behaviors:
- `null = null` evaluates to `null`, not `true`
- Most expressions receiving `null` produce `null`
- In `WHERE` predicates, anything not `true` is treated as `false`

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN null
$$) AS (result agtype);
-- result is an empty field (not the string "null")
```

In a list, `null` appears as the word `null`:

```sql
SELECT * FROM cypher('my_graph', $$
  WITH [null, 1, 2] AS lst RETURN lst
$$) AS (lst agtype);
-- [null, 1, 2]
```

### Integer

64-bit signed integer. Range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807.

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN 42
$$) AS (result agtype);
-- 42
```

Integer literals in property values:

```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (:Person {age: 30})
$$) AS (v agtype);
```

### Float

Inexact variable-precision numeric type conforming to IEEE-754. Stored and retrieved values may show slight discrepancies — do not use for monetary values.

Special float values must be quoted and cast:

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN 3.14
$$) AS (result agtype);
-- 3.14

-- Special values require casting:
SELECT * FROM cypher('my_graph', $$
  RETURN 'Infinity'::float
$$) AS (result agtype);
```

Special values: `Infinity`, `-Infinity`, `NaN` (case-insensitive on input).

**Note:** `'NaN'::float = 'NaN'::float` evaluates to `true` in AGE (differs from IEEE-754 strict behavior) to allow correct sorting.

### Numeric

Exact arbitrary-precision decimal type. Use for monetary values or any calculation requiring exactness. Slower than integer or float arithmetic.

The `::numeric` cast annotation is required when writing numeric literals:

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN 1.0::numeric
$$) AS (result agtype);
-- 1.0::numeric
```

Store a numeric property:

```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (:Account {balance: 9999.99::numeric})
$$) AS (v agtype);
```

**Note:** `'NaN'::numeric = 'NaN'::numeric` evaluates to `true` in AGE for consistent sorting behavior.

### Boolean

Three-state: `true`, `false`, and `null` (unknown). Keywords are `TRUE`, `FALSE`, `NULL`.

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN TRUE
$$) AS (result agtype);
-- true  (full word, not 't' like PostgreSQL)
```

In WHERE clauses, `null` is treated as `false`:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (n)
  WHERE n.active = TRUE
  RETURN n
$$) AS (n agtype);
```

### String

String literals use single quotes in Cypher input; output uses double quotes.

Supported escape sequences:

| Sequence | Character      |
|----------|----------------|
| `\t`     | Tab            |
| `\b`     | Backspace      |
| `\n`     | Newline        |
| `\r`     | Carriage Return|
| `\f`     | Form Feed      |
| `\'`     | Single Quote   |
| `\"`     | Double Quote   |
| `\\`     | Backslash      |
| `\uXXXX` | Unicode UTF-16 code point |

```sql
SELECT * FROM cypher('my_graph', $$
  RETURN 'Hello, world!'
$$) AS (result agtype);
-- "Hello, world!"
```

String property example:

```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (:Person {name: 'Alice', bio: 'She said \"hi\".', note: 'Line 1\nLine 2'})
$$) AS (v agtype);
```

---

## Composite Types

### List

Ordered collection of agtype values. Elements are comma-separated inside square brackets. A list may contain mixed types including `null` and nested maps.

```sql
-- Literal list
SELECT * FROM cypher('my_graph', $$
  WITH [1, 2.0, 'three', true, null] AS lst RETURN lst
$$) AS (lst agtype);

-- Access by index (0-based)
WITH [10, 20, 30] AS lst RETURN lst[0]   -- 10
WITH [10, 20, 30] AS lst RETURN lst[-1]  -- 30 (negative: from end)

-- Slice (start inclusive, end exclusive)
WITH [0,1,2,3,4] AS lst RETURN lst[1..3]  -- [1, 2]
WITH [0,1,2,3,4] AS lst RETURN lst[..2]   -- [0, 1]
WITH [0,1,2,3,4] AS lst RETURN lst[2..]   -- [2, 3, 4]
WITH [0,1,2,3,4] AS lst RETURN lst[-2..]  -- [3, 4]
```

Out-of-bound **single element** access returns `null`. Out-of-bound **slices** are truncated.

List with nested maps:

```sql
SELECT * FROM cypher('my_graph', $$
  WITH [{name: 'Alice'}, {name: 'Bob'}] AS people
  RETURN people[0].name
$$) AS (result agtype);
-- "Alice"
```

### Map

Key-value collection. Keys must be strings; values can be any agtype.

```sql
-- Literal map with simple types
SELECT * FROM cypher('my_graph', $$
  WITH {name: 'Alice', age: 30, active: true} AS m
  RETURN m
$$) AS (m agtype);
-- {"name": "Alice", "age": 30, "active": true}

-- Property access
WITH {name: 'Alice', age: 30} AS m RETURN m.name  -- "Alice"

-- Nested map
WITH {address: {city: 'Portland', zip: '97201'}} AS m
RETURN m.address.city  -- "Portland"

-- Map containing a list
WITH {tags: ['graph', 'database'], count: 2} AS m
RETURN m.tags[0]  -- "graph"
```

---

## Graph Entity Types

### Vertex

A vertex is the basic graph entity. It can exist independently. Vertices may have zero or one label, and zero or more properties.

**Wire format:**
```
{"id": <graphid>, "label": "<label>", "properties": {<key>: <value>, ...}}::vertex
```

**Attributes:**

| Attribute    | Description                          |
|--------------|--------------------------------------|
| `id`         | Unique graphid (label_id + sequence) |
| `label`      | Label name (string, may be empty)    |
| `properties` | Map of property key-value pairs      |

Create and retrieve a vertex:

```sql
SELECT * FROM cypher('my_graph', $$
  CREATE (p:Person {name: 'Alice', age: 30})
  RETURN p
$$) AS (p agtype);
-- {"id": 844424930131969, "label": "Person", "properties": {"name": "Alice", "age": 30}}::vertex
```

Access vertex properties in a query:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (p:Person)
  RETURN p.name, p.age
$$) AS (name agtype, age agtype);
```

Type-cast a map literal to a vertex (useful for testing):

```sql
SELECT * FROM cypher('my_graph', $$
  WITH {id: 0, label: "Person", properties: {name: "Alice"}}::vertex AS v
  RETURN v
$$) AS (v agtype);
```

### Edge

An edge encodes a directed connection between exactly two vertices. Edges **must** have exactly one label.

**Wire format:**
```
{"id": <graphid>, "label": "<label>", "start_id": <graphid>, "end_id": <graphid>, "properties": {<key>: <value>, ...}}::edge
```

**Attributes:**

| Attribute    | Description                          |
|--------------|--------------------------------------|
| `id`         | Unique graphid                       |
| `label`      | Edge type label (required)           |
| `start_id`   | graphid of source vertex             |
| `end_id`     | graphid of target vertex             |
| `properties` | Map of property key-value pairs      |

Create and retrieve an edge:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
  CREATE (a)-[r:KNOWS {since: 2020}]->(b)
  RETURN r
$$) AS (r agtype);
-- {"id": ..., "label": "KNOWS", "start_id": ..., "end_id": ..., "properties": {"since": 2020}}::edge
```

**Constraint:** Label names for vertices and edges cannot overlap within the same graph.

### Path

A path is a series of alternating vertices and edges, starting with a vertex. Minimum: one vertex and one edge.

**Wire format:** A list cast to `::path`:
```
[<vertex>::vertex, <edge>::edge, <vertex>::vertex, ...]::path
```

Capture and return a path:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH p = (a:Person {name: 'Alice'})-[:KNOWS*1..3]->(b:Person)
  RETURN p
$$) AS (p agtype);
```

Extract components from a path using path functions:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH p = (a:Person)-[:KNOWS]->(b:Person)
  RETURN nodes(p), relationships(p), length(p)
$$) AS (nodes agtype, rels agtype, len agtype);
```

Type-cast a list to a path (for testing):

```sql
SELECT * FROM cypher('my_graph', $$
  WITH [
    {id: 0, label: "Person", properties: {name: "Alice"}}::vertex,
    {id: 2, start_id: 0, end_id: 1, label: "KNOWS", properties: {}}::edge,
    {id: 1, label: "Person", properties: {name: "Bob"}}::vertex
  ]::path AS p
  RETURN p
$$) AS (p agtype);
```

---

## Type Casting

Use `::` to cast agtype values:

| Cast            | Example                        | Use                          |
|-----------------|--------------------------------|------------------------------|
| `::float`       | `'Infinity'::float`            | Special float literals       |
| `::numeric`     | `1.0::numeric`                 | Exact decimal arithmetic     |
| `::vertex`      | `{id:0, label:"L", properties:{}}::vertex` | Map to vertex |
| `::edge`        | `{id:1, start_id:0, end_id:2, label:"E", properties:{}}::edge` | Map to edge |
| `::path`        | `[v::vertex, e::edge, v2::vertex]::path` | List to path |

Casting is required to use special float/numeric literals in SET clauses:

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (n:Sensor {id: 1})
  SET n.reading = '-Infinity'::float
  RETURN n
$$) AS (n agtype);
```

---

## AGE NULL vs PostgreSQL NULL

AGE's `null` and PostgreSQL's `NULL` are conceptually identical — both represent unknown/missing values. However, they exist in different layers:

- **PostgreSQL NULL**: SQL-level null (a row has no value for a column)
- **AGE null**: agtype-level null (a graph property is absent or unknown)

A `cypher()` column typed as `agtype` will return a PostgreSQL non-NULL row containing an agtype null value when a Cypher `null` is returned. Use agtype-aware functions (not `IS NULL`) to test for Cypher nulls in downstream SQL.

---

## Comparability Notes

| Situation                        | Result  | Notes                                  |
|----------------------------------|---------|----------------------------------------|
| `null = null`                    | `null`  | Unknown equals unknown is unknown      |
| `'NaN'::float = 'NaN'::float`   | `true`  | AGE deviation from IEEE-754 for sorting|
| `'NaN'::numeric = 'NaN'::numeric` | `true` | Same deviation                        |
| `1 = 1.0`                        | `true`  | Integer and float comparison           |
| `1 = 1::numeric`                 | `true`  | Integer and numeric comparison         |
