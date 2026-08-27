---
title: "Rolling Into Colemak-DH"
date: 2026-08-26
draft: true
tags: ["keyboards", "ergonomics"]
---

From my understanding, a lot of people are drawn to Colemak (and the many variations upon it) for its ergonomic benefits as a preventative measure for some wrist-trouble, or something like that. I do experience some minor shoulder pain (on the left side), but I do not find it to be a make-or-break issue for my productivity. And to be completely honest, I have no complaints with QWERTY and I can touch-type just fine; so this is a rather poor advertisement for adopting any new keyboard layouts. Yet, learning something new and looking like an odd-ball while doing it is always a joy. They often ask: "who even uses Colemak anyways?" and the answer is almost always "not somebody who needs to," and that includes me.

I switched to **Colemak-DH** in the spring. The first month took me to roughly 50 WPM, which was an unpleasant start, yet I kept pushing. Now, three or four months on I sit at ~90 to ~100. My QWERTY is 120. I am still measurably slower on this keyboard than I am on an ordinary one. But I have no intention of going back. I'll explain why shortly.

This whole process was kicked off by a purchase: I bought a [Cornix LP](https://jezailfunder.jp/products/cornix-lp-keyboard) from JezailFunder (a pretty silver-cased 40% wireless split @ ¥29,500) and then took the opportunity to relearn how to type along with the new column-staggered hand placement. Loving the board also brought a love for adjusting the layout beyond Colemak. It was the process of going from 104 keys to 42 that forced me to consider how to most effectively *design* a keymap tailored to my needs. The maturity of the ecosystem is amazing (*I love Vial, it rocks*).

---

## Why Colemak-DH

Below I've got **(3)** different heatmaps which show off the difference between **QWERTY**, **Colemak**, and **Colemak-DH** in order to best illustrate the keypress distributions for each:

{{< figure src="/images/colemak/heatmap.svg" width="610" height="678" alt="Keypress heatmaps for QWERTY, Colemak and Colemak-DH over the same body of text" caption="**NOTE**: *Stretch* is the share landing in the two inner columns, the ones an index finger reaches by splaying sideways." >}}

QWERTY puts a third of my keypresses on the home row; either Colemak puts about two thirds of them there. Same-finger bigrams (one finger asked to hit two keys in a row, which is the most irritating thing a layout can do) fall from ~4.6% to ~1.3%. The clearest example is one you type constantly without noticing: on QWERTY every regular past-tense verb ends by making your left middle finger hop from `E` on the top row down to `D` on the home row. On either Colemak those two letters are on opposite hands.

On both of those measures, though, stock Colemak and Colemak-DH are indistinguishable. The mod is fractionally *worse* on home row and identical on same-finger bigrams. Its entire case is the third number. `D` and `H` are frequent letters, and stock Colemak parks them in the two inner columns, the ones an index finger reaches by splaying sideways rather than curling under. Mod-DH swaps them for the far rarer `G` and `M`, and the share of my typing that needs that sideways reach drops from 13% to 8%. That is the whole modification. It comes in two flavours depending on whether your rows are staggered like a typewriter or stacked in columns; a column-staggered board like the Cornix takes the **matrix** version, which is the one above.

And this is where the rolling comes from, which is the part I find genuinely difficult to describe without sounding like I have had some sort of religious experience or something. `ST` is left middle to left index, two adjacent fingers on two adjacent keys, one motion rather than two. `NE` is the same on the right hand. `ARST` and `NEIO` are the whole home row under four fingers in order. Typing starts feeling like the keys are [falling over in like a sequence of dominos](https://youtu.be/7ff3UQUPdio?si=2m54kvv-5I7vfJG8&t=107). It is an indescibable pleasure which does not grow old.

My only complaint is that my right pinky went from ~2.7% of keypresses to ~7.9%, because `O` and `;` now live in its row. That is nearly triple, but I really do not find it that bad. Everything else improves, though.

---

## Learning It

|                                        | WPM      | Share of QWERTY |
| -------------------------------------- | -------- | --------------- |
| QWERTY, then and still                 | 120      | N/A             |
| Colemak-DH, after one month            | ~50      | 42%             |
| Colemak-DH, after three to four months | 90 – 100 | 75 – 83%        |

The first fortnight is genuinely bad, and no amount of forewarning prepares you for the specific indignity of it. You do not merely type slowly; you lose the ability to think and type at the same time, because the part of your brain that used to handle spelling has been dragged into finding the letters in a big mental space which holds the keymap in your mind. Prose gets shorter. Replies get curter. I would not choose to do it during a week that mattered.

~50 WPM at a month is roughly the point where the layout stops being the bottleneck and your thinking becomes the bottleneck again (which is the only threshold that actually matters. Everything after that has been a slow accumulation. Despite not running through daily typing drills the number keeps drifting up on its own.

I have been asked if I ended up losing QWERTY in this transition, and the answer is that I did not. Losing QWERTY is too high of a cost to bother with this at all if that were actually the trade being made, nobody wants to permanently handicap themselves for what could end up being almost no benefit, but I digress. I did not shed even a bit of my current WPM of it and this is thanks to an active logical separation I maintain between the physical keyboard styles and the key layouts that I use with them. I've written my Cornix keymap into the board's flash memory (see: [Vial.rocks](https://vial.rocks/)), so there is no required config and/or per-machine setup. The flip side is that the layout does not travel: my laptop keyboard is QWERTY, and every other generic borrowed keyboard is QWERTY.

This could sound like a limitation, maybe, but I maintain that it is the opposite. MacOS ships with Colemak pre-installed but not Colemak-DH, so doing this in software would mean maintaining a custom layout on every machine I touch and then, like, hastily swapping out the keymap configuration to QWERTY and like stumbling around the settings with my cursor like a fool, if anybody tries to use my machine (I also maintain a toggleable layer on my Cornix which provides QWERTY input for anyone who needs it). Thus, really, keeping it within the hardware is less work by a massive margin.

{{< quote cite="–stevep99, some guy on the Colemak forums" url="https://forum.colemak.com/topic/2817-help-on-how-to-keep-both-colemakdh-and-qwerty/" >}}
"People have reported success in […] maintaining both layouts. I've heard of people using psychological hacks to assist with the context switching, for example, using Qwerty on a traditional row-staggered board, and Colemak(-DH) exclusively on an ortholinear. Or, using one layout at home and one at work."
{{< /quote >}}

If anyone is worried about the confusion that might come along with knowing multiple layouts, listen to this: my hands seem to mentally compartmentalize each (QWERTY/Colemak-DH) with the *keyboard* rather than under one slot marked "typing" (it is very similar to knowing multiple languages. If someone spoke to you in French, you wouldn't respond in Chinese). I have never once had to think about the changeover, and maybe you won't need to either.

---

## The Keyboard

The Cornix LP is a 40% split — 6063 aluminium, sandblasted and anodised, an FR4 plate, Kailh Choc V2 switches, a rotary encoder on each half, a 650 mAh cell in each half, and Bluetooth for up to three devices with USB-C when I would rather not think about batteries. It ships on LAK PBT caps, which are perfectly good and which I replaced anyway with a set of [LCK Liquid Silver](https://jezailfunder.jp/products/lck-liquid-silver) at ¥4,900. They are low-profile with a dished centre and a genuinely metallic finish, and against the silver case the whole thing looks like a piece of equipment rather than a hobby. *(Both the caps and the board have been drifting in and out of stock, so temper your expectations before you click.)*

{{< figure src="/images/colemak/cornix-keycaps.webp" width="1400" height="520" alt="Top-down view of both halves of a silver split keyboard with dished metallic silver keycaps" caption="The Liquid Silver caps on the silver case. The knob on each half is a rotary encoder, and the clear window beside it shows the wireless module." >}}

The detail I did not know to want is that **the tenting folds out of the board itself**. Two machined struts under each half, four notched positions — 6°, 12°, 18°, 24° — and nothing to buy. On most splits, tenting is an aftermarket problem you solve with pucks, printed wedges, or a camera tripod and some optimism, and because it costs money and effort you pick an angle early and then spend a year defending that decision. Being able to change it in ten seconds meant I spent the first fortnight actually experimenting instead of committing.

{{< figure src="/images/colemak/cornix-tenting.webp" width="1400" height="534" alt="Side-on view of the keyboard, the left half raised steeply on its fold-out strut and the right half sitting flat" caption="The struts fold out from underneath. The left half is near the top of its range here and the right is flat, which is roughly how the first fortnight went." >}}

---

## The Layer Underneath

Forty-two keys is not enough keys. That is not a complaint, it is the entire mechanism: there is no number row to fall back on, so every digit, bracket, arrow and function key has to be *somewhere you decided*, and the keyboard stops being a thing you buy and starts being a thing you configure.

Which would be tedious if the firmware were tedious. The Cornix runs **[Vial](https://get.vial.today/)**, a QMK fork with a GUI that talks to the keyboard while it is running. There is a [web version](https://vial.rocks/) that needs nothing installed. You change a key, and it changes — no compile, no flash, no unplugging, no twenty-minute round trip to discover you have put the bracket somewhere your hand refuses to go. Iteration cost falling to nearly zero is the difference between a keymap you designed and a keymap you settled for.

### Home Row Mods

Every key on the home row does two jobs: tap it for the letter, hold it for a modifier. So `A R S T` and `N E I O` are also GUI, Alt, Shift and Ctrl, mirrored outward from the index fingers. `Ctrl+C` becomes index finger and middle finger, both hands, both already at rest. Nothing reaches for a corner; nothing pins my left pinky to the bottom-left of the board for the hundredth time that hour.

This is a **mod-tap** in QMK's vocabulary, and Vial exposes it directly. The whole difficulty is timing — how long a hold counts as a hold, what happens when you roll from a modifier into a letter faster than the firmware expected — and it is a solved problem you should not try to solve yourself. Precondition's [guide to home row mods](https://precondition.github.io/home-row-mods) is the reference; it is long, it is worth it, and reading it first will save you a fortnight of wondering why your keyboard occasionally types in capitals.

### Combos

Vial calls chords **combos**: press two keys at the same time, get a third thing. Mine is `H` and `,` for backspace.

The choice of pair is not arbitrary, and I only understood why after a few bad ones. On Colemak-DH, `H` and `,` sit next to each other on the bottom row under the right index and right middle fingers — same row, adjacent columns, *different fingers*. That combination can be pressed as a single motion, the way you would tap two adjacent piano keys. Pairs on the same finger are impossible; pairs spread across rows or hands are just two keys pressed carefully, which is slower than the thing you were trying to avoid. Adjacent, different-fingered, same-row is the whole recipe.

Backspace earns the slot because a 40% has nowhere natural to put it and because it is, after the letters and space, very probably the key I hit most. It never leaves the home position now. Once a combo becomes automatic it stops registering as a chord at all and simply becomes what backspace is.

---

## The Trackball in the Middle

The other thing a split gets you is a hole in the middle of your keyboard, and I put a silver Kensington SlimBlade in it.

This is the dividend nobody advertises. On a normal keyboard the mouse lives past the number pad, so using it means picking up your whole right hand, moving it eight inches, and then finding home row again by feel afterwards. With the halves pushed apart, the pointer sits *inside* the keyboard, roughly where `G` and `H` used to be. My hands barely move.

{{< figure src="/images/colemak/cornix-trackball.webp" width="1400" height="588" alt="Top-down view of the two keyboard halves spread apart with a Kensington SlimBlade trackball centred between them" caption="The SlimBlade sitting where a number pad would be on anything else. This is before the keycap swap — those are the stock caps, and their orange digits and green modifiers are a fair map of everything a 40% has to find room for on a layer." >}}

And because a trackball is a sphere rather than a moulded right-handed shape, it does not care which hand is on it. I use it with either, more or less at random, which spreads a load that used to be entirely one wrist's problem. This was not a plan. I bought the thing because it was silver and it matched.

---

## Resources Worth Bookmarking

- **[Colemak Mod-DH](https://colemakmods.github.io/mod-dh/)** — the source of truth for the mod, including the matrix and angle variants and the reasoning behind each.
- **[A guide to home row mods](https://precondition.github.io/home-row-mods)** — Precondition's guide, and the only one you need. Read it before you configure anything.
- **[Vial](https://get.vial.today/)** — the firmware and GUI; the [combos manual](https://get.vial.today/manual/combos.html) is short and worth ten minutes.
- **[keybr](https://keybr.com/)** — teaches a new layout letter by letter rather than throwing the whole alphabet at you on day one. This is the one that got me to 50.
- **[Monkeytype](https://monkeytype.com/)** — for measuring, once you can bear to look.

### Takeaway

I am still twenty words a minute slower on the Cornix than I am on my laptop and I have stopped caring, which surprised me more than any of the rest of it. Speed was simply the thing I could measure, so it became the thing I measured. What actually changed is that my hands no longer go anywhere — two thirds of my keypresses land where my fingers already are, backspace is a twitch, `Ctrl` is under my index finger, and the mouse is between my wrists instead of across the desk.

The layout gets top billing because it is the part with a name and a partisan internet following. But I could have kept QWERTY on this board and still gained most of it. What did the work was forty-two keys, firmware that let me change my mind for free, and a couple of months of being patient with myself. Colemak-DH is lovely and I will not be giving it up. It is also, I think, the smallest thing that happened here.
