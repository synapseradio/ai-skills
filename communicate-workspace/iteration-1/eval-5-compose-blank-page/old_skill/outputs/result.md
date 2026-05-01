## Why User Input Is Untrusted by Default

This library treats every value that originates outside your process as untrusted. That is not a configurable policy — it is the default, and changing it requires explicit opt-in.

The reason is concrete: we kept seeing the same class of bug report. A developer would call an internal API, pass a value from a query parameter or a form field directly, and the library would act on it without question. Sometimes that meant a crafted input could reach a path it was never supposed to reach. Sometimes it meant a downstream service received data it assumed had already been sanitized. In both cases, the developer had not made a deliberate trust decision — they had simply omitted one, and the library had filled the gap with trust.

The default flips that gap. When you pass a value into any API that operates on content, the library assumes the value is hostile until you tell it otherwise. This forces a decision point: you must explicitly mark input as validated before the library treats it as safe. That decision point is where your validation logic should already live.

If you are reading values from a database your own code wrote, you can mark them trusted. If you are reading values from a request, a URL, a cookie, or any external source, leave the default in place. When in doubt, untrusted is the correct call.
