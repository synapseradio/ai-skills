# Templates

Copy-and-adapt templates for the three situations. These require `effect` and
`@effect/typeclass` as dependencies of the consuming project — they type-check
inside such a project, not in isolation.

## Contents

1. Brands — for unary, two-parameter, and input/output type constructors
2. Instances — implementing `@effect/typeclass` interfaces for a custom type
3. Custom typeclass — defining a new typeclass when the catalog lacks it

## 1. Brands (`TypeLambda`)

A brand is an interface that `extends TypeLambda` and supplies a `type` member:
the data type applied to the lambda's parameter slots. `Kind` fills the slots
in. Pick slots by role — `Target`/`Out1`/`Out2` for produced (covariant) types,
`In` for a consumed (contravariant) type.

```typescript
import type { Kind, TypeLambda } from "effect/HKT"

// ── Unary type constructor: MyBox<A> ───────────────────────────────────────
// Only the covariant `Target` slot is used.
export type MyBox<A> = { readonly value: A }

export interface MyBoxTypeLambda extends TypeLambda {
  readonly type: MyBox<this["Target"]>
}

// Verify: this alias should resolve to MyBox<string>.
export type _CheckBox = Kind<MyBoxTypeLambda, never, never, never, string>

// ── Two type parameters: MyResult<E, A> ────────────────────────────────────
// Both produced, so both go in covariant slots: E in Out1, A in Target.
export type MyResult<E, A> =
  | { readonly _tag: "Failure"; readonly error: E }
  | { readonly _tag: "Success"; readonly value: A }

export interface MyResultTypeLambda extends TypeLambda {
  readonly type: MyResult<this["Out1"], this["Target"]>
}

// Verify: should resolve to MyResult<Error, number>.
export type _CheckResult = Kind<MyResultTypeLambda, never, never, Error, number>

// ── Input + output: MyParser<In, A> ────────────────────────────────────────
// `In` is consumed (contravariant) → the `In` slot. `A` is produced → Target.
export type MyParser<In, A> = (input: In) => MyResult<string, A>

export interface MyParserTypeLambda extends TypeLambda {
  readonly type: MyParser<this["In"], this["Target"]>
}

// Verify: should resolve to MyParser<string, number>.
export type _CheckParser = Kind<MyParserTypeLambda, string, never, never, number>
```

## 2. Instances (Situation B)

An instance is a plain value: a dictionary of functions satisfying the typeclass
interface, parameterised by the type's brand. Implement only the core operation
of each typeclass; let Effect's combinators derive the rest. The example is a
from-scratch `Maybe` so `map`, `of`, and `flatMap` are each meaningful.

```typescript
import type { TypeLambda } from "effect/HKT"
import type { Covariant } from "@effect/typeclass/Covariant"
import * as covariant from "@effect/typeclass/Covariant"
import type { Of } from "@effect/typeclass/Of"
import type { FlatMap } from "@effect/typeclass/FlatMap"
import type { Monad } from "@effect/typeclass/Monad"

// ── The data type and its brand ────────────────────────────────────────────
export type Maybe<A> =
  | { readonly _tag: "Just"; readonly value: A }
  | { readonly _tag: "Nothing" }

export interface MaybeTypeLambda extends TypeLambda {
  readonly type: Maybe<this["Target"]>
}

const just = <A>(value: A): Maybe<A> => ({ _tag: "Just", value })
const nothing: Maybe<never> = { _tag: "Nothing" }

// ── Covariant (Functor): core operation `map` ──────────────────────────────
// `imap` is derived from `map` with `covariant.imap` — do not hand-write it.
export const MaybeCovariant: Covariant<MaybeTypeLambda> = {
  imap: covariant.imap<MaybeTypeLambda>((self, f) => MaybeCovariant.map(self, f)),
  map: (self, f) => (self._tag === "Just" ? just(f(self.value)) : nothing),
}

// ── Of: core operation `of` ────────────────────────────────────────────────
export const MaybeOf: Of<MaybeTypeLambda> = {
  of: just,
}

// ── FlatMap: core operation `flatMap` ──────────────────────────────────────
export const MaybeFlatMap: FlatMap<MaybeTypeLambda> = {
  flatMap: (self, f) => (self._tag === "Just" ? f(self.value) : nothing),
}

// ── Monad: composed from the cores above ───────────────────────────────────
// Monad = Covariant + Of + FlatMap. The operations are already implemented.
export const MaybeMonad: Monad<MaybeTypeLambda> = {
  imap: MaybeCovariant.imap,
  map: MaybeCovariant.map,
  of: MaybeOf.of,
  flatMap: MaybeFlatMap.flatMap,
}
```

Verify against the laws — encode them as property tests where the project
supports it:

```text
Functor identity:        map(fa, x => x)          === fa
Functor composition:     map(fa, x => g(f(x)))    === map(map(fa, f), g)
Monad left identity:     flatMap(of(a), f)        === f(a)
Monad right identity:    flatMap(fa, of)          === fa
Monad associativity:     flatMap(flatMap(fa,f),g) === flatMap(fa, a => flatMap(f(a), g))
```

## 3. Custom typeclass (Situation C)

Use this only after confirming `@effect/typeclass` genuinely lacks the
abstraction — check `typeclass-catalog.md` first. A typeclass is an interface
generic over a brand `F extends TypeLambda`; its operations take and return
`Kind<F, ...>`. Mirror the shape of Effect's own interfaces so instances and
combinators compose with the ecosystem.

```typescript
import type { Kind, TypeLambda } from "effect/HKT"

// ── The typeclass interface ────────────────────────────────────────────────
// Example: `Zippable` — combine two structures element-wise with a function.
// (Illustrative; in practice prefer SemiApplicative from @effect/typeclass.)
export interface Zippable<F extends TypeLambda> {
  readonly zipWith: <R, O, E, A, B, C>(
    self: Kind<F, R, O, E, A>,
    that: Kind<F, R, O, E, B>,
    f: (a: A, b: B) => C,
  ) => Kind<F, R, O, E, C>
}

// Keep the four slot parameters generic across the operation, as
// @effect/typeclass does. A unary instance ignores R, O, E — they never appear
// in its result.

// ── An instance of the custom typeclass ────────────────────────────────────
type Pair<A> = readonly [A, A]

interface PairTypeLambda extends TypeLambda {
  readonly type: Pair<this["Target"]>
}

export const PairZippable: Zippable<PairTypeLambda> = {
  zipWith: (self, that, f) => [f(self[0], that[0]), f(self[1], that[1])],
}

// ── Combinators built on the typeclass ─────────────────────────────────────
// Generic over any `Zippable<F>` — this is where the abstraction pays off:
// `F` is genuinely unknown here, filled in by the caller.
export const zip = <F extends TypeLambda>(Z: Zippable<F>) =>
  <R, O, E, A, B>(
    self: Kind<F, R, O, E, A>,
    that: Kind<F, R, O, E, B>,
  ): Kind<F, R, O, E, readonly [A, B]> =>
    Z.zipWith(self, that, (a, b) => [a, b] as const)
```
