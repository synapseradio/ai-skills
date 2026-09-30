# tutor: what a derivative is, for a cook

- skill: tutor, from commit 0c9258f
- subject: Learning what a derivative is, from a learner who only knows cooking.
- kind: staged conversation (the user side played by a second agent)

## Prompt

/tutor Learning what a derivative is, from a learner who only knows cooking.

## Run

**Skill:** Before we start, three quick questions so I teach the way that suits you. (1) Do you want detailed explanations, or concise ones? (2) Do you prefer analogies from things you know, or precise definitions? (3) Do you want a broad wander through the idea, or a specific goal, such as being able to say what a derivative is in your own words?

**User (played):** Concise, please, and I'd rather have comparisons from the kitchen than definitions. As for a goal, I'd like to be able to explain what a derivative is to my sister over a cup of tea, in my own words.

**Skill:** Concise, kitchen comparisons, and a goal of explaining it to your sister over tea. That is what we will aim for.

What I know versus what I checked: the idea of a derivative is well settled, and I confirmed the standard definition against a calculus text (a derivative is the instantaneous rate of change, the slope of the tangent line: <https://math.libretexts.org/Courses/Mount_Royal_University/Calculus_for_Scientists_I/3%3A_Derivatives/3.0%3A_Tangent_lines_and_Rates_of_change>). The oven numbers below are made up for teaching, not measured. My plan is five layers, each true on its own: (1) rate of change, (2) rate over a shrinking window, (3) the picture as a slope, (4) the rate at every moment as its own curve, (5) what flat spots tell you.

Layer 1. You put a cold oven on to preheat. At minute 0 it is 20 degrees. At minute 40 it is 180. How fast did it heat up, in one number you could say to your sister?

Whatever you work out, that number is a "rate of change": how much one thing changed for each step of another.

Here is my check question. Suppose the oven took a while to get going, then raced, then crept up near 180. Would your one number describe minute 5 as well as it describes minute 35? Say what you think in your own words.

**User (played):** Going from 20 to 180 in 40 minutes is 160 degrees over 40 minutes, so 4 degrees a minute. That's like saying a roast loses so much weight per hour. It's a fair average.

But no, that one number wouldn't describe minute 5 as well as minute 35. If the oven is slow to start, minute 5 might only be gaining 1 degree a minute. Then it races, maybe 8 a minute. Then it creeps at the end. The 4 is just the whole trip averaged out, like saying a car journey took 50 miles an hour when it sat in traffic and then flew down the motorway.

**Skill:** Yes, and your car journey is the same idea: 50 miles an hour is the whole trip averaged, while the speedometer tells you the speed at one instant. You have just named the gap this whole subject is about.

Layer 2. How would you find the oven's speed at exactly minute 5? You could read the thermometer at minute 5 and again at minute 6, and take that one-minute average. Say it reads 40.0 degrees at minute 5 and 41.5 at minute 6, so 1.5 degrees a minute. A shorter window is better: minute 5 to 5 and a half reads 40.7, so 1.4 a minute. Shorter again, minute 5 to six seconds later, reads about 1.31 a minute. (These numbers are invented, but they behave the way a real oven would.)

Notice that as the window shrinks, the average stops jumping around and settles toward one number, about 1.3. That settled number is the oven's speed at minute 5 itself, and it has a name: the derivative of temperature with respect to time, at minute 5.

Check question: in your own words, why does shrinking the window get you closer to "the speed at minute 5" than the one-minute average did? And what would that 1.3 mean if your sister asked?

**User (played):** A short window gets you closer because the oven has less time to change its pace. Over a whole minute it might speed up partway through, so the average mixes slow and fast. Over a few seconds it's basically going one speed, so the average is nearly the true speed at that moment. It's like tasting a sauce with a tiny spoon instead of a ladle from the whole pot.

If my sister asked, I'd say the 1.3 means that right at minute 5, the oven is heating at about one and a third degrees every minute. I'm not sure whether "if it kept going at that pace" belongs in there, because it won't actually keep going that pace, will it?

**Skill:** The tiny spoon against the ladle is a good way to put it. And your doubt is the right one. You are correct that the oven will not keep that pace. So the 1.3 is best said as "the speed right at minute 5". Your phrase "if it kept going at that pace" is a useful way to picture it, and it leads straight into the next layer.

Layer 3. Draw the oven's story: time along the bottom, temperature up the side, one curve. Where the oven races, the curve climbs steeply. Where it creeps, the curve flattens out. Now imagine the oven kept its minute-5 pace forever. That would be a straight, tilted line laid against the curve so that it just touches it at minute 5 and does not cross it there. This line is called the tangent. Its steepness, the slope, is 1.3 degrees a minute. So the derivative at a point is the steepness of the curve at that point.

Check question: near minute 40, the oven is creeping up to 180 and finally holds there. On your drawing, is the touching line at that spot steeper or flatter than the one at minute 5? And once the oven sits at 180 and stays there, what would the derivative be?

**User (played):** Flatter, I think. Near minute 40 the curve is nearly level, so a line touching it there would barely tilt, much flatter than at minute 5, when the oven was gaining well.

Once it sits at 180 and holds, the line would be perfectly flat, so the derivative would be zero. It isn't gaining any degrees a minute, the way a roast resting on the counter has stopped cooking. Is zero the answer, or does "zero" mean something different from "nothing happening"?

**Skill:** Zero is the answer, and your second question is the sharp part of it. Zero means "not changing", not "nothing happening". The oven is still on and working hard to hold 180. The derivative only reports how fast the temperature is moving, never how hot it is. A pot at 100 degrees and a pot at 20 both have a derivative of zero if neither is changing.

Layer 4. So far you have found the speed at one moment. Do it at every minute and you get a whole list: a slow speed at minute 2, a fast one at minute 15, nearly zero at minute 38, zero at minute 45. Plot that list against time and you get a second curve, built from the first. It starts low, rises to a hump while the oven races, then falls back to zero. This second curve is what mathematicians call "the derivative" of the first, a curve that says how steep the first curve is at each moment.

Check question: the hump of the speed curve is the busiest moment of the preheat. Where is that moment on the original temperature curve: at the flat start, the flat end, or somewhere on the climb? Say why.

**User (played):** Somewhere on the climb, in the steepest part. The hump is where the oven is gaining the most degrees a minute, and that's exactly where the temperature curve is climbing hardest. The flat start and flat end are the slow bits, so they'd sit low on the speed curve, near zero at the end.

So the second curve is like a record of how hard the oven is working at each minute, not how hot it is. Is that fair to tell my sister, that it's a "how fast is it changing" chart drawn from the "how hot is it" chart?

**Skill:** Yes, that is fair to tell your sister. "How fast is it changing" drawn from "how much is there" is the derivative in one sentence. And you placed the hump on the steepest part of the climb correctly.

Layer 5, the last one. The derivative can go below zero. If you switch the oven off, the temperature falls, the touching line tilts downward, and the derivative is negative: it is still a speed, now pointing down.

That gives you a use. Picture a dough proving. Its volume rises, the rise slows, it reaches a top, and if you leave it too long it collapses. At the very top the touching line is flat, so the derivative is zero, and just before it the derivative is positive and just after it is negative. A cook who watches for the moment the rise stops is watching for the derivative to hit zero. Mathematicians use exactly this to find peaks and lowest points of anything.

Now your own goal. Pretend I am your sister with the cup of tea, and I ask "what is a derivative?" Answer me in your own words, using whatever kitchen comparison you like.

**User (played):** A derivative is how fast something is changing, right at one moment. It isn't how much of it there is, or how it changed on average. Say you're preheating the oven. The thermometer tells you how hot it is. The derivative tells you how quickly it's climbing at this very minute. You get it by looking at shorter and shorter stretches of time until the average settles on one number, like tasting with a tiny spoon instead of a ladle.

If you drew the temperature as a curve, the derivative is how steep the curve is at that spot. It's zero when the oven holds steady, and negative when it's cooling. And when my dough stops rising, that's the derivative hitting zero, which is how you spot the top of the rise before it collapses.

Was that close? I'm still a bit hazy on how you'd actually work out the number without a thermometer, if all you had was a recipe for the curve.

**Skill:** That was close to complete. Your sister has "how fast, right now, not how much and not on average", the shrinking window, the steepness of the curve, and the zero at the top of the rise. Nothing there needs fixing.

Your last question is where the ground gets new, so I will follow it. With a recipe for the curve, you run the same shrinking-window trick with arithmetic instead of a thermometer.

Take a toy dough whose height in centimetres is the number of hours squared: at 3 hours it is 9 cm. Speed at hour 3, by shrinking the window:

- hour 3 to 4: height goes 9 to 16, so 7 cm an hour
- hour 3 to 3.1: height goes 9 to 9.61, so 6.1 cm an hour
- hour 3 to 3.01: height goes 9 to 9.0601, so 6.01 cm an hour

It settles at 6. Now work the same trick at hour 2: the height there is 4, and the windows give 5, then 4.1, then 4.01, settling at 4. So the speed at hour 2 is 4 and at hour 3 is 6.

Check question: I will not give you the rule, so guess it. What do you think the speed is at hour 5, and what is the pattern you are using?

**User (played):** Ten, I think. At hour 2 the speed was 4, and at hour 3 it was 6, so it looks like double the hour number. Hour 5 would be 10.

I only spotted that by comparing the two answers, so I'm not certain it holds for every hour. It's like scaling a recipe. If two loaves need 4 and three need 6, I'd guess five need 10, but I'd want to try a bigger batch before trusting it. Should I test it at hour 5 with the shrinking window, the way you did for 2 and 3?

**Skill:** Yes, test it. Your instinct to try a bigger batch before trusting the pattern is the right habit, and it is how the rule gets checked in practice.

Hour 5, where the height is 25:

- hour 5 to 6: 25 to 36, so 11 cm an hour
- hour 5 to 5.1: 25 to 26.01, so 10.1 cm an hour
- hour 5 to 5.01: 25 to 25.1001, so 10.01 cm an hour

It settles at 10, so your guess held. For this dough, where the height is the hour squared, the speed at any hour is twice the hour. That rule is the derivative of "hours squared". It is a second recipe, this time for the speed curve, and with it you never need to shrink the window by hand again for this dough.

What would you like to do next: try another toy dough, such as height equal to the hour cubed, to see whether a pattern shows up there too, or is there a different part of this you want to firm up first?

**User (played):** I'd like to try the cubed one. Squared gave me "twice the hour", so I'm curious whether cubed gives some other tidy rule or whether it's messier. Can we do hour 2 and hour 3, like before? Then I can guess the rule before you tell me.

The 10 held, which pleases me. It's like a recipe scaling up the way I hoped.
