---
name: ts-typeclasses
description: >-
  Implement typeclasses and their instances in TypeScript — Functor,
  Applicative, Monad, Traversable, Foldable — and the higher-kinded type (HKT)
  encoding they require. Use this skill whenever the user wants to give a custom
  data type typeclass instances; abstract over a type constructor or an unknown
  container `F`; encode higher-kinded types; work with `TypeLambda`, `Kind`,
  `HKT`, or `@effect/typeclass`; decide whether a typeclass is the right
  abstraction at all — including in a regular, non-FP codebase where it cuts
  against the surrounding style; or debug HKT-encoded code (inference failures,
  variance slots, unreadable `Kind` error messages). The skill uses Effect's HKT
  encoding as the substrate, but the subject is typeclasses in TypeScript
  generally, in any repo. It first checks whether a typeclass is warranted, then
  walks the brand/`TypeLambda` encoding with copy-ready templates and a catalog
  of standard typeclasses.
---

# TypeScript Typeclasses

This skill builds typeclass abstractions in TypeScript on Effect's higher-kinded
type encoding. A typeclass — `Functor`, `Monad`, `Traversable` — is an interface
abstracted over a *type constructor* (`Array`, `Option`, a custom `Tree`), not
over a plain type. TypeScript cannot quantify over type constructors directly,
so the abstraction is recovered through an encoding: a *brand* (Effect calls it
a `TypeLambda`) names the constructor, and `Kind` applies it. The background and
the theory live in `references/hkt-encoding.md`; this file is the workflow.

The work splits into four steps, preceded by a gate. Do not skip the gate — most
requests for "HKTs" do not actually need them, and the encoding has a real cost.

## Step 0 — Gate: are HKTs needed at all?

The encoding is a powerful tool with a standing cost: every call site that
routes through `Kind` pays an inference-annotation tax and surfaces dense error
messages (see `references/troubleshooting.md`). Adopt it only when it earns its
place.

Apply this single test:

> **Does a real call site exist where the type constructor `F` is genuinely
> unknown — a parameter the caller fills in — rather than a concrete type the
> code can name?**

- **No call site has an unknown `F`.** Do not encode HKTs. Write concrete code
  against the named types, even if that means some duplication. Duplicated
  concrete code is better engineering here than an abstraction nobody calls
  generically. Stop.
- **The user only consumes Effect's own types** (`Option`, `Either`, `Array`,
  `Chunk`, `Effect`, …) and wants typeclass-generic behavior. The instances
  already exist — go to Situation A in Step 1. No encoding work.
- **`F` is genuinely a variable at a real call site** — for example a `traverse`
  that must work for any applicative the caller picks, or a custom type that
  must plug into typeclass-generic code. Proceed.

State the gate's outcome to the user before continuing. If the answer is "no",
say so plainly and recommend the concrete-code path rather than building the
encoding anyway.

## Step 1 — Identify the situation

Three situations, decreasing in frequency. Route to the one that fits.

```
Is the data type one of Effect's built-ins (Option, Either, Array, Chunk, ...)?
├─ yes → Situation A: import existing instances. No encoding work.
└─ no  → Do you own the data type, and does @effect/typeclass already
         define the typeclass you need (Functor, Monad, Traversable, ...)?
         ├─ yes → Situation B: brand the type, implement Effect's typeclass
         │         interfaces. This is the common workflow.
         └─ no  → Situation C: the typeclass itself is missing from
                   @effect/typeclass. Define a new typeclass over
                   `F extends TypeLambda`, then instances. Rare — first
                   re-check the catalog, the abstraction usually exists.
```

### Situation A — consuming Effect's built-in types

Effect's data types already have brands and typeclass instances. Do not
re-encode them. Instances live in `@effect/typeclass/data/<Type>`:

```typescript
import * as ArrayInstances from "@effect/typeclass/data/Array"
import * as OptionInstances from "@effect/typeclass/data/Option"

// ArrayInstances.Monad, OptionInstances.Covariant, etc. are ready to use.
```

`@effect/typeclass/data/` ships instance modules for `Array`, `Either`,
`Option`, `Effect`, `Record`, `Tuple`, `Identity`, and more. The brands
themselves (`OptionTypeLambda`, `ReadonlyArrayTypeLambda`, …) are exported from
each type's own module in `effect`. Confirm the exact export against the
installed version — see `references/typeclass-catalog.md`.

### Situation B — a custom type that needs typeclass support

This is the main workflow. Go to Step 2.

### Situation C — a typeclass `@effect/typeclass` does not provide

Before committing, open `references/typeclass-catalog.md` and confirm the
abstraction is genuinely absent. Effect's catalog is wide — `Covariant`,
`Invariant`, `Contravariant`, `Of`, `Pointed`, `Applicative`, `Monad`,
`Foldable`, `Traversable`, `Filterable`, `Alternative`, and the `Semi*`
variants. A "new" typeclass is usually one of these under a different name. If
it truly is missing, define it over `F extends TypeLambda` using the custom
typeclass template in `references/templates.md`, then proceed to Step 2 for
instances.

## Step 2 — Define the data type and its brand

The brand is a `TypeLambda`: an interface whose `type` member is the data type
applied to `this["Target"]`. `this["Target"]` is the lambda's parameter; `Kind`
fills it in.

The templates below import `TypeLambda` and `Kind` from `effect/HKT`, which
assumes `effect` is a dependency of the repo. In a plain TypeScript codebase
with no FP libraries it usually is not, and the import will not resolve. Do not
improvise an encoding inline when that happens. Decide where the encoding comes
from first: `references/non-effect-repos.md` covers the choice between adding
`effect` and vendoring a verbatim minimal encoding, and supplies the vendorable
code. The rest of this skill is identical either way — only the import path
changes.

```typescript
import type { TypeLambda } from "effect/HKT"

// The custom data type — a unary type constructor.
export type Tree<A> =
  | { readonly _tag: "Leaf"; readonly value: A }
  | { readonly _tag: "Branch"; readonly left: Tree<A>; readonly right: Tree<A> }

// The brand. `type` is Tree applied to the lambda parameter.
export interface TreeTypeLambda extends TypeLambda {
  readonly type: Tree<this["Target"]>
}
```

`TypeLambda` has four parameter slots, used by `Kind<F, In, Out2, Out1, Target>`.
Pick slots by *variance and position*, not by counting left to right:

| Slot     | Variance      | Typical use                                   |
|----------|---------------|------------------------------------------------|
| `Target` | covariant     | the main output type — the `A` in `Tree<A>`     |
| `Out1`   | covariant     | a second output — the `E` in `Either<E, A>`     |
| `Out2`   | covariant     | a third output                                  |
| `In`     | contravariant | an input requirement — the `R` in `Effect<R,E,A>` |

A unary type uses only `Target`. A two-parameter type like `Result<E, A>` uses
`Out1` for `E` and `Target` for `A`:

```typescript
export interface ResultTypeLambda extends TypeLambda {
  readonly type: Result<this["Out1"], this["Target"]>
}
```

Brand templates for common arities are in `references/templates.md`.

## Step 3 — Implement the instances

An instance is a plain value: a dictionary of functions satisfying a typeclass
interface. **Reuse before writing.** `@effect/typeclass` derives most of a
typeclass from a smaller one — implement the minimal core, then let Effect build
the rest.

For Situation B, implement Effect's typeclass interfaces, parameterised by the
brand. These interfaces come from `@effect/typeclass`, a separate package from
`effect` — a repo can depend on one without the other. If `@effect/typeclass`
is not installed, hand-write the small interface the task needs, following
`references/non-effect-repos.md`, with `references/typeclass-catalog.md` as the
spec for its operations and laws. Do not improvise it.

```typescript
import type { Covariant } from "@effect/typeclass/Covariant"

export const TreeCovariant: Covariant<TreeTypeLambda> = {
  imap: (self, to, _from) => TreeCovariant.map(self, to),
  map: (self, f) =>
    self._tag === "Leaf"
      ? { _tag: "Leaf", value: f(self.value) }
      : {
          _tag: "Branch",
          left: TreeCovariant.map(self.left, f),
          right: TreeCovariant.map(self.right, f),
        },
}
```

Inside `map`, `self` has type `Kind<TreeTypeLambda, ..., A>`. Because the brand
is concrete there, `Kind` reduces immediately to `Tree<A>`, so the `_tag`
discriminates normally.

Effect provides combinators that derive instances. For example `Covariant`
exposes `imap` as a derivation from `map`, and `Monad` can be assembled from
`FlatMap` plus `Of`. Reach for these rather than re-deriving by hand — see
`references/typeclass-catalog.md` for the dependency graph and the minimal core
each typeclass needs. Full instance templates are in `references/templates.md`.

For Situation C, define the typeclass first (custom typeclass template in
`references/templates.md`), then write instances the same way.

## Step 4 — Verify

Three checks, cheapest first.

1. **Type-level reduction.** Confirm the brand applies correctly. Hover or
   `tsc`-check this alias:

   ```typescript
   import type { Kind } from "effect/HKT"
   type _TreeOfString = Kind<TreeTypeLambda, never, never, never, string>
   //   should resolve to Tree<string>
   ```

2. **Compilation.** Run the project's type-checker. The instance is correct at
   the type level only if `tsc` accepts the dictionary against the typeclass
   interface. Do not trust a hand-traced reduction over the compiler.

3. **Laws.** Every typeclass carries laws — `Functor` must preserve identity and
   composition, `Monad` must satisfy left identity, right identity, and
   associativity. An instance that type-checks but breaks its laws is still
   wrong. The laws for each typeclass are in `references/typeclass-catalog.md`;
   encode them as property tests where the project supports it.

## Principle: reuse the prior art

Effect and `@effect/typeclass` encode a large amount of already-solved design.
Before defining a brand, check whether the type is an Effect built-in
(Situation A). Before defining a typeclass, check the catalog (Situation C
guard). Before writing an instance method, check whether a combinator derives it
from a smaller one. Hand-rolling is the last resort, reserved for genuinely
novel types and abstractions — and even then, it should mirror the shape of the
Effect interfaces so the result composes with the rest of the ecosystem.

## References

Read these as the task requires — do not load them all upfront.

- **`references/hkt-encoding.md`** — why TypeScript has no native HKTs, how
  defunctionalization and brands recover them, and how `Kind` works
  mechanically. Read when explaining the encoding or debugging it at depth.
- **`references/typeclass-catalog.md`** — every `@effect/typeclass` typeclass:
  what it abstracts, its core operation, its laws, its derivation graph, and
  whether it needs an HKT. Read when picking or implementing a specific
  typeclass.
- **`references/troubleshooting.md`** — inference failures, variance-slot
  mistakes, decoding `Kind` error messages, the `this`-resolution stall. Read
  when something does not compile.
- **`references/templates.md`** — copy-and-adapt templates for brands,
  instances, and custom typeclasses. Read when writing the actual code.
- **`references/non-effect-repos.md`** — getting typeclasses into a repo that
  does not depend on Effect: the choice between adding `effect` /
  `@effect/typeclass` and vendoring a minimal encoding plus hand-written
  interfaces, with the vendorable code. Read when `effect` or
  `@effect/typeclass` is not already installed.
