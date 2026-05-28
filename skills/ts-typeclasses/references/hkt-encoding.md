# The HKT encoding: why it exists and how it works

This reference explains the encoding the skill applies. Read it to understand or
explain *why* the `TypeLambda`/`Kind` machinery is shaped the way it is, or to
debug it below the surface.

## Contents

1. Kinds, and why TypeScript is first-order
2. Defunctionalization — the value-level original
3. Type defunctionalization — lifting the trick to types
4. Effect's encoding: `TypeLambda` and `Kind`
5. The four slots and variance
6. Sources

## 1. Kinds, and why TypeScript is first-order

A *type* classifies values. A *kind* classifies types. The kind `*` ("star") is
the kind of every complete type — `string`, `number`, `Tree<string>`. A type
constructor that still needs an argument has an arrow kind: `Array` alone has
kind `* -> *`, because applied to a type it yields a type.

A *higher-kinded type variable* is a variable whose kind is an arrow kind — one
that ranges over type constructors, not over complete types. Haskell writes it
`f :: * -> *`; Scala writes `F[_]`.

TypeScript has no such variable. Every type parameter — every `<T>` — ranges
over complete types of kind `*`. You can quantify over a type (`<T>` in a
generic), but not over a type constructor. Writing `F<A>` for a type parameter
`F` is rejected:

```typescript
interface Functor<F> {
  map: <A, B>(fa: F<A>, f: (a: A) => B) => F<B>
  //          ~~~~  Type 'F' is not generic. ts(2315)
}
```

TypeScript is also more restricted than ML here: a generic type alias cannot
even be *named* without its arguments — `type Bad = Array` fails with
`ts(2314)`. A type constructor is not a first-class entity that can be held,
passed, or stored.

This is a deliberate design boundary, tracked as `microsoft/TypeScript#1213`.
Native HKTs would demand a substantially more powerful unifier. The deep reason
is the *alias problem*: in a structural system with type aliases, unifying a
higher-kinded variable loses the most general unifier. Given `'a 'f ~ (int * int)
list`, the obvious solution unifies `'f` with `list` — but if aliases
`type 'a plist = ('a * 'a) list` and `type 'a iplist = (int * int) list` are in
scope, `'f` could equally be `plist` or `iplist`, and no solution is most
general. Brands sidestep this: a brand is an atomic name with no aliases, so
first-order unification suffices.

## 2. Defunctionalization — the value-level original

The encoding is an application of *defunctionalization*, introduced by John
Reynolds in 1972 to translate higher-order programs into first-order ones.

Defunctionalization replaces each function value with a *tag* — a data
constructor — and replaces every call with one dispatch function, `apply`, that
pattern-matches the tag. A closure becomes inert data: the tag carries the
captured variables as its payload. The function type `A -> B` becomes a single
first-order datatype of tags; `apply : Fn -> A -> B` interprets them.

```ocaml
(* higher-order *)
let adder k = fun n -> n + k

(* defunctionalized: the closure becomes a tag carrying the captured k *)
type fn = Adder of int
let apply (f : fn) (x : int) : int = match f with Adder k -> x + k
let add3 = Adder 3   (* apply add3 10 = 13 *)
```

The intuition: in a first-order world you cannot pass a function, so you pass a
*name* for it and keep one interpreter that knows what each name means.

## 3. Type defunctionalization — lifting the trick to types

Yallop and White's "Lightweight Higher-Kinded Polymorphism" (FLOPS 2014) applies
the same transform one level up — to type constructors. Each row below is a
literal lift of the previous section:

| Value level                  | Type level                          |
|-------------------------------|--------------------------------------|
| a function value / closure    | a type constructor (`Array`, `Tree`)  |
| the function type `A -> B`     | the higher-kinded position            |
| a tag naming a function       | a **brand** naming a constructor       |
| the datatype of all tags      | the abstract type `app`               |
| `apply : Fn -> A -> B`         | the `app` application operation        |

A **brand** is an uninhabited, opaque type that names a constructor. The paper
represents `'a list` as `('a, List.t) app`, where `List.t` is the brand for
`list`. The key move: a brand is itself an ordinary type of kind `*`, so you
*can* quantify over it — `∀'f` over brands is legal first-order quantification,
unlike `∀f` over the kind-`(* -> *)` constructor. Wherever you would write the
forbidden `'a 'f`, you write `('a, 'f) app` instead. `app` is one fixed
two-argument type, which the type system handles without trouble.

The paper gives three implementations of `app`: an unchecked cast guarded by
generative functors, an open (extensible) data type, and Haskell type families —
"extensible type-level functions, which provide exactly the functionality we
need". TypeScript's conditional and mapped types *are* extensible type-level
functions, so the TypeScript encoding follows the type-family approach. And
because TypeScript types are fully erased at runtime, the encoding needs no
value-level `app` and no unsafe cast at all.

## 4. Effect's encoding: `TypeLambda` and `Kind`

Effect's `effect/HKT` module is the `app` machinery for TypeScript. It is about
45 lines. The load-bearing parts:

```typescript
// the brand's shape — Effect's name for a brand is "TypeLambda"
export interface TypeLambda {
  readonly In: unknown
  readonly Out2: unknown
  readonly Out1: unknown
  readonly Target: unknown
}

// the application operation — the paper's `app`/`Apply`
export type Kind<F extends TypeLambda, In, Out2, Out1, Target> =
  F extends { readonly type: unknown }
    ? (F & { readonly In: In; readonly Out2: Out2;
             readonly Out1: Out1; readonly Target: Target })["type"]
    : { /* error fallback for a non-brand F */ }
```

A concrete brand extends `TypeLambda` and supplies a `type` member:

```typescript
export interface OptionTypeLambda extends TypeLambda {
  readonly type: Option<this["Target"]>
}
```

The brand is a genuine type-level lambda: `Target` is its bound parameter,
`this["Target"]` is the parameter reference, and `type` is the body. `Kind`
applies it by beta-reduction. Trace `Kind<OptionTypeLambda, never, never, never,
string>`:

1. `OptionTypeLambda` has a `type` member, so the conditional takes the first
   branch.
2. Intersect: `OptionTypeLambda & { In: never; Out2: never; Out1: never;
   Target: string }`.
3. Index `["type"]`. The body is `Option<this["Target"]>`; inside the
   intersected type, polymorphic `this` makes `this["Target"]` resolve to
   `string`.
4. Result: `Option<string>`.

The fallback branch — taken when `F` has no `type` member — produces a
deliberately unusable type, so passing a non-brand fails to compile.

Effect's design improves on a central registry (the approach `fp-ts` used, where
one global `URItoKind` table mapped string tags to constructors and any two
packages registering the same key collided). Each Effect brand carries its own
application clause in its `type` member, so adding a new HKT never touches
anything central — no registry, no collisions, fully open.

## 5. The four slots and variance

`Kind<F, In, Out2, Out1, Target>` has four argument slots so one encoding can
serve constructors of several arities and variances:

- `Target` — the primary covariant output (`A` in `Option<A>`).
- `Out1`, `Out2` — additional covariant outputs (`E` in `Either<E, A>` goes in
  `Out1`).
- `In` — a contravariant input (`R`, the requirements, in `Effect<R, E, A>`).

A unary type uses only `Target` and ignores the rest; unused slots are passed
`never` and never appear in the result. The slot names encode intent: place a
type parameter by what it *is* (an output the type produces, or an input it
consumes), not by its left-to-right position in the original type.

This fixed four-slot shape is also the encoding's main limit. A constructor with
more independent type-level parameters than the slots accommodate has no clean
home. In practice four slots cover the overwhelming majority of types, including
`Effect<R, E, A>` itself.

## 6. Sources

- Jeremy Yallop and Leo White, "Lightweight Higher-Kinded Polymorphism", FLOPS
  2014. <https://www.cl.cam.ac.uk/~jdy22/papers/lightweight-higher-kinded-polymorphism.pdf>
- John C. Reynolds, "Definitional Interpreters for Higher-Order Programming
  Languages", ACM '72 — the origin of defunctionalization.
- Effect `effect/HKT` source:
  <https://github.com/Effect-TS/effect/blob/main/packages/effect/src/HKT.ts>
- TypeScript HKT tracking issue:
  <https://github.com/microsoft/TypeScript/issues/1213>
