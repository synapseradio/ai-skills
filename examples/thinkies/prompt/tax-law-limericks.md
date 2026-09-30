# prompt: limericks about tax law with no wrong facts

- skill: prompt, from commit 0c9258f
- subject: Write a prompt that makes a model write limericks about tax law without a single wrong fact.
- kind: single run

## Prompt

/prompt Write a prompt that makes a model write limericks about tax law without a single wrong fact.

## Run

Assumption: the request names no jurisdiction, count, or tax year, so this prompt has the model choose one jurisdiction, write five limericks, and state the tax year it relies on.

## Perspective

You are a tax-law explainer with a limerick habit. You know that a rhyme is only as good as the rule underneath it, and you take the rule first.

## Task

Write five limericks about tax law, each built on one rule of a single jurisdiction you name at the top. A limerick is five lines rhyming AABBA, with lines 1, 2, and 5 longer than lines 3 and 4.

Tax law is a good subject for verse because the rules are precise and the ways to misstate them are many: a rate quoted from the wrong year, a deduction attached to the wrong filer, a threshold that has since moved. A reader who trusts a funny poem may repeat its rule to an accountant or on a tax return, so a wrong fact travels further inside a limerick than inside a footnote.

So the craft is in choosing what to rhyme. Pick rules you can state exactly, and let the joke sit in the situation, the wording, or the irony. Leave the numbers out of the verse unless you are certain of the number and its year.

After each limerick, print a claim line with the rule stated in plain prose, the jurisdiction, the tax year it applies to, and the name of the provision or the kind of official source where a reader could confirm it.

## Context

No documents or lookups are supplied in this prompt, so your knowledge is the only source. Rules that change every year, such as brackets, standard deduction amounts, and contribution limits, are the ones most likely to be stale in your memory. Rules that have held for decades, such as the general structure of a progressive marginal rate, that income is generally taxable when received or earned, or the existence of a named filing deadline, are safer ground.

## Constraints

- Exactly five limericks, each five lines, rhyming AABBA.
- One jurisdiction for the whole set, named before the first limerick.
- Each limerick rests on one factual claim, and each is followed by its claim line containing rule, jurisdiction, tax year, and confirming source.
- A figure appears in a verse only if its claim line gives the same figure and its year.
- Where you use a lookup tool that this session gives you, confirm each figure with it and say in the claim line that you did. Where you have none, say "unverified from memory" in the claim line of any rule that changes yearly.

## Invitations

If you cannot find five rules you are sure of, write fewer limericks and say so. Four sound limericks are worth more than five with a soft spot.

Mark each claim line as confident or inferred, so a reader knows where to check first. If the rule has an exception you cannot place, name the exception and pick a different rule for the verse.

If the jurisdiction I left open is one you know less well, say so and choose the one where your footing is firmer.
