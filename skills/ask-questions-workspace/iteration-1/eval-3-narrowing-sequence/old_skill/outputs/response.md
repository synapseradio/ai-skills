Here's an ordered set that funnels from "slow" down to something you can reproduce and fix. Each question only makes sense once the previous one's answered, so ask them in sequence rather than all at once — and let each answer shape how you phrase the next.

1. **"When you say slow — is that all the time, or does it happen at certain moments?"**
   Splits "general sluggishness" (perf/device issue) from "specific moments" (a particular action or screen) before you go further.

2. **"What were you doing right when it felt slow — which screen, and what action?"**
   Pins the location: a page load, a button click, a search, a save.

3. **"Can you walk me through the exact steps, in order, from opening the app to noticing the slowness?"**
   This is the one that turns a memory into a reproduction recipe — get the sequence of clicks/taps, not just the destination.

4. **"How slow did it feel — a couple seconds' pause, or did it seem stuck/frozen?"**
   Distinguishes latency from a hang, which points at very different root causes.

5. **"Does it happen every time you do that, or only sometimes?"**
   Tells you if you're chasing something deterministic or intermittent (network, cache state, data volume).

6. **"Did you notice this just today, or has it been building for a while — and did anything change around when it started (update, new device, different network)?"**
   Surfaces a possible triggering change instead of assuming it's always been this way.

7. **"What device and connection were you on — and are you able to reproduce it again right now?"**
   Gets you the environment variables and, ideally, a live repro you (or they) can capture with a screen recording or timestamped log.

8. **"Anything else about it that stood out, even if it seems unrelated?"**
   Closes the door open — catches the detail you didn't think to ask about.

By the end you should have: a specific screen/action, an exact step sequence, a rough time cost, a frequency (always/sometimes), a possible trigger, and an environment — enough to either reproduce it yourself or hand it to engineering as a real bug report instead of "slow."
