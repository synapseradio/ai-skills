# Typeclass catalog

A catalog of the typeclasses `@effect/typeclass` defines, so an instance reuses
the existing abstraction instead of reinventing it. Each entry gives the core
operation, what it abstracts, the laws, and the package module.

Before defining anything new, scan this list. A "new" typeclass is almost always
one of these under a different name.

> Package: `@effect/typeclass`. Typeclass interfaces live at
> `@effect/typeclass/<Name>`; ready-made instances for Effect's built-in types
> live at `@effect/typeclass/data/<Type>`. The `extends` relationships below
> describe the general hierarchy — confirm the exact clauses against the
> installed version's source, since Effect refines this between releases. [?]

## How to read an instance's requirements

An instance only needs to supply the *core* operation(s) of a typeclass.
Everything a parent typeclass adds is either inherited or derived by an Effect
combinator. Implement the smallest core, then compose upward. The derivation
graph at the end of this file shows what builds on what.

## HKT-requiring typeclasses

These abstract over a type constructor `F extends TypeLambda`. They need the
encoding.

### Invariant — `@effect/typeclass/Invariant`

- **Core operation**: `imap` — map with functions both ways,
  `(self: Kind<F, A>, to: (a: A) => B, from: (b: B) => A) => Kind<F, B>`.
- **Abstracts**: structures where `A` appears in both input and output
  position, so a one-way `map` is not enough.
- **Role**: the root of the mapping hierarchy. `Covariant` and `Contravariant`
  both extend it.

### Covariant — `@effect/typeclass/Covariant`

- **Core operation**: `map` — `(self: Kind<F, A>, f: (a: A) => B) => Kind<F, B>`.
- **Abstracts**: a "container" or "context" whose contents can be transformed.
  This is the classic `Functor`.
- **Extends**: `Invariant` (and supplies `imap` from `map` via
  `covariant.imap`).
- **Laws**:
    - Identity: `map(fa, x => x)` equals `fa`.
    - Composition: `map(fa, x => g(f(x)))` equals `map(map(fa, f), g)`.

### Contravariant — `@effect/typeclass/Contravariant`

- **Core operation**: `contramap` —
  `(self: Kind<F, A>, f: (b: B) => A) => Kind<F, B>`.
- **Abstracts**: structures that *consume* `A` rather than produce it —
  predicates, comparators, serializers. The brand puts the consumed type in the
  contravariant `In` slot.
- **Extends**: `Invariant`.

### Bicovariant — `@effect/typeclass/Bicovariant`

- **Core operation**: `bimap` — map over *both* type parameters of a
  two-parameter constructor, e.g. `Either<E, A>`.
- **Abstracts**: types with two independently mappable positions.

### Of — `@effect/typeclass/Of`

- **Core operation**: `of` — `(a: A) => Kind<F, A>`. Lift a single value into
  the structure.
- **Abstracts**: the ability to construct a minimal `F<A>` from an `A`.

### Pointed — `@effect/typeclass/Pointed`

- **Composed of**: `Covariant` + `Of`. No new core operation.

### SemiProduct / Product — `@effect/typeclass/SemiProduct`, `.../Product`

- **Core operation**: `product` —
  `(self: Kind<F, A>, that: Kind<F, B>) => Kind<F, [A, B]>`. Combine two
  independent structures into one of pairs.
- **`Product`** adds `of` (via `Of`), giving an empty/unit element and
  n-ary `productAll`.
- **Abstracts**: zipping or pairing independent effects.

### SemiApplicative / Applicative — `.../SemiApplicative`, `.../Applicative`

- **Composed of**: `SemiApplicative` is `Covariant` + `SemiProduct`;
  `Applicative` is `SemiApplicative` + `Product` (so also `Pointed`).
- **Abstracts**: applying a function inside the structure to an argument inside
  the structure — independent, non-sequential composition of effects.
- **Laws**: identity, homomorphism, interchange, composition (the standard
  applicative laws).

### FlatMap / Chainable / Monad — `.../FlatMap`, `.../Chainable`, `.../Monad`

- **Core operation**: `flatMap` —
  `(self: Kind<F, A>, f: (a: A) => Kind<F, B>) => Kind<F, B>`. Sequence a
  computation that depends on a previous result.
- **`Chainable`** = `Covariant` + `FlatMap`. **`Monad`** = `Chainable` + `Of`
  (equivalently `Pointed` + `FlatMap`).
- **Abstracts**: dependent sequencing — the second step needs the first step's
  value.
- **Monad laws**:
    - Left identity: `flatMap(of(a), f)` equals `f(a)`.
    - Right identity: `flatMap(fa, of)` equals `fa`.
    - Associativity: `flatMap(flatMap(fa, f), g)` equals
    `flatMap(fa, a => flatMap(f(a), g))`.

### Foldable — `@effect/typeclass/Foldable`

- **Core operation**: `reduce` —
  `(self: Kind<F, A>, b: B, f: (b: B, a: A) => B) => B`.
- **Abstracts**: collapsing a structure to a summary value.

### Traversable — `@effect/typeclass/Traversable`

- **Core operation**: `traverse` — walk a structure, running an applicative
  effect at each element, and collect the results inside that applicative:
  `(F: Applicative<G>) => (self: Kind<T, A>, f: (a: A) => Kind<G, B>) =>
  Kind<G, Kind<T, B>>`.
- **Abstracts**: effectful iteration that preserves shape — the single most
  common reason to genuinely need HKTs, since `G` is universally quantified.

### Filterable / TraversableFilterable — `.../Filterable`, `.../TraversableFilterable`

- **Core operation**: `partitionMap` / `filterMap` — map and drop or split in
  one pass, typically over `Option` or `Either` results.

### SemiCoproduct / Coproduct — `.../SemiCoproduct`, `.../Coproduct`

- **Core operation**: `coproduct` — combine two structures by choice rather than
  by pairing. `Coproduct` adds an identity element (an empty structure).

### SemiAlternative / Alternative — `.../SemiAlternative`, `.../Alternative`

- **Composed of**: `Covariant` plus `SemiCoproduct` / `Coproduct`.
- **Abstracts**: choice with a failure/empty case — parsers, validations that
  fall back.

## Non-HKT typeclasses

These abstract over a plain type of kind `*`, not a type constructor. They do
**not** need the encoding — no brand, no `Kind`. They are included because they
often appear alongside HKT typeclasses.

- **Semigroup** — `@effect/typeclass/Semigroup`: `combine: (a: A, a: A) => A`,
  an associative binary operation.
- **Monoid** — `@effect/typeclass/Monoid`: `Semigroup` plus an identity element
  `empty`.
- **Bounded** — `@effect/typeclass/Bounded`: an ordered type with `maxBound` and
  `minBound`.

If the abstraction is over a plain type — "how do I combine two of these" — it
is one of these, and the HKT machinery is unnecessary.

## Derivation graph

Implement the core at the bottom; the rest is inherited or composed.

```
Invariant
  └─ Covariant ──────────────┐
       └─ Pointed            │
   Contravariant             │
                             ├─ SemiApplicative ─ Applicative
   Of ───────────────────────┘        │
   SemiProduct ─ Product ──────────────┘
   FlatMap
     └─ Chainable
          └─ Monad   (= Chainable + Of)
   Foldable
   Traversable
   SemiCoproduct ─ Coproduct ─ (Semi)Alternative
```

Reuse the composition helpers Effect ships — for example deriving `imap` from
`map` with `covariant.imap`, or assembling a `Monad` from a `FlatMap` and an
`Of`. Hand-write only the genuine core operations.

## Source

`@effect/typeclass` modules:
<https://github.com/Effect-TS/effect/tree/main/packages/typeclass/src>
