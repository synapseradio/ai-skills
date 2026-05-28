# Typeclasses without the `effect` dependency

Every other reference in this skill imports `TypeLambda` and `Kind` from
`effect/HKT` and the typeclass interfaces from `@effect/typeclass`. That assumes
`effect` is a dependency of the repo. In a plain TypeScript codebase — a Node
API, a CLI tool, a frontend with no FP libraries — it usually is not. This file
is the decision and the code for that case.

Reach this file once Step 0's gate has already said the HKT encoding is
warranted. The gate question — is there a real call site where `F` is genuinely
unknown? — does not change with the dependency situation. What changes is only
where the encoding *comes from*.

## The decision: add `effect`, or vendor the encoding

There are two ways to get the encoding into a repo that is not already an Effect
repo.

**Add `effect` as a dependency.** Install it (`bun add effect`, plus
`@effect/typeclass` for the prebuilt typeclass interfaces). You get the
encoding, the full typeclass catalog, the derivation combinators, and
ready-made instances for the built-in types — all maintained upstream. The cost
is a real dependency and a paradigm the rest of the team now has to read.
`effect` is tree-shakeable, so unused modules do not ship, but the conceptual
surface is not tree-shakeable: a reviewer who has never seen `TypeLambda` still
has to learn it to read the file.

**Vendor a minimal encoding.** Copy the encoding below into one local file. You
get `TypeLambda` and `Kind` and nothing else — no dependency, no new package in
the lockfile. The cost is that you hand-write every typeclass interface
(`Covariant`, `Monad`, …) and every derivation yourself, because
`@effect/typeclass` is the part you declined to install.

Decide by counting what the task actually needs:

- **One or two local abstractions, a handful of typeclasses, no need for the
  built-in instances.** Vendor. Hand-writing two or three typeclass interfaces
  is a smaller imposition on the codebase than a new dependency.
- **The catalog, the derivation combinators (`Monad` assembled from `FlatMap`
  and `Of`), or instances for `Array` / `Option` / `Either`.** Add `effect`.
  Re-implementing those by hand is more code and more bugs than the dependency.
- **The team is actively against new dependencies or against the FP paradigm.**
  Vendor, and keep the encoding contained to the module that needs it. The
  vendored file is a local implementation detail, not a codebase-wide
  commitment.

The vendored encoding below is copied verbatim from Effect's own source, so it
is API-compatible with it. If the repo later adopts `effect`, migrating is
deleting the vendored file and changing the import path — nothing else changes.
Vendoring is therefore a reversible decision. For a repo that is not otherwise
an Effect repo, treat it as the low-commitment default and reach for the
dependency only when the counting above points there.

## The minimal vendorable encoding

This is Effect's `TypeLambda` and `Kind`, verbatim, with the three variance
helpers they depend on inlined so the file stands alone. Sources:
`effect/src/HKT.ts` (<https://github.com/Effect-TS/effect/blob/main/packages/effect/src/HKT.ts>)
and `effect/src/Types.ts`
(<https://github.com/Effect-TS/effect/blob/main/packages/effect/src/Types.ts>),
both `@since 2.0.0`.

```typescript
// hkt.ts — minimal higher-kinded-type encoding.
// Verbatim from Effect's `effect/HKT` and `effect/Types`; API-compatible with it.

// Variance phantom helpers. They never hold a real value at runtime; they exist
// only to tell the compiler how each slot varies, which keeps `Kind` sound in
// the branch where `F` is still an unresolved type variable.
type Invariant<A> = (_: A) => A
type Covariant<A> = (_: never) => A
type Contravariant<A> = (_: A) => void

// A `TypeLambda` is the brand: the interface a data type extends to register
// itself as a type constructor. The four slots carry the constructor's
// parameters — see the slot/variance table in SKILL.md Step 2.
export interface TypeLambda {
  readonly In: unknown
  readonly Out2: unknown
  readonly Out1: unknown
  readonly Target: unknown
}

// `Kind` applies a branded constructor `F` to concrete arguments. When `F` is a
// concrete brand it carries a `type` member, and `Kind` reduces to that member
// with the slots substituted in. When `F` is still a type variable there is no
// `type` member, so `Kind` falls back to a variance-tagged record that the
// compiler can still reason about soundly.
export type Kind<F extends TypeLambda, In, Out2, Out1, Target> = F extends {
  readonly type: unknown
} ? (F & {
    readonly In: In
    readonly Out2: Out2
    readonly Out1: Out1
    readonly Target: Target
  })["type"]
  : {
    readonly F: F
    readonly In: Contravariant<In>
    readonly Out2: Covariant<Out2>
    readonly Out1: Covariant<Out1>
    readonly Target: Invariant<Target>
  }
```

That is the whole substrate. Everything in `references/templates.md` works
against it unchanged: a brand is still
`interface FooTypeLambda extends TypeLambda { readonly type: Foo<this["Target"]> }`,
and `Kind<FooTypeLambda, never, never, never, A>` still reduces to `Foo<A>`. The
only edit to the templates is the import — `from "./hkt.js"` instead of
`from "effect/HKT"`.

## Writing typeclass interfaces by hand

With `@effect/typeclass` absent, the typeclass interfaces are yours to write.
They are small. A `Covariant` — the `Functor` — over the vendored encoding:

```typescript
import type { Kind, TypeLambda } from "./hkt.js"

export interface Covariant<F extends TypeLambda> {
  readonly map: <In, Out2, Out1, A, B>(
    self: Kind<F, In, Out2, Out1, A>,
    f: (a: A) => B,
  ) => Kind<F, In, Out2, Out1, B>
}
```

Use `references/typeclass-catalog.md` as the spec for each typeclass's
operations and laws. The catalog describes the abstraction itself, not the
`@effect/typeclass` package, so it is just as valid here. Write only the
typeclasses with a real call site. If the task drifts into hand-porting five or
six of them with their full derivation graph, that is the signal the decision
should have gone the other way — stop and add `effect` rather than rebuilding
`@effect/typeclass` by hand.
