# Reflection: What the Profiles Taught Me

## The Six Profiles I Tested

I ran the recommender against six user profiles — three "normal" listeners and three designed to expose weaknesses.

| # | Name | What it represents |
|---|---|---|
| 1 | High-Energy Pop | A mainstream listener who wants upbeat pop at high volume |
| 2 | Chill Lofi | A study-session listener who wants quiet, acoustic background music |
| 3 | Intense Rock | A workout listener who wants loud, driving guitar music |
| 4 | Ghost Genre (k-pop) | A listener whose favourite genre does not exist in the catalog |
| 5 | High-Energy + Melancholic | A listener with conflicting preferences — sad mood, high energy |
| 6 | Acoustic Metal Fan | A listener who loves heavy music but also wants acoustic texture |

---

## Pair 1 — High-Energy Pop vs Chill Lofi

**What changed:** These two profiles produced almost completely opposite song lists.
The Pop profile surfaced Sunrise City, Gym Hero, and Rooftop Lights — all fast, punchy, non-acoustic.
The Lofi profile surfaced Library Rain, Midnight Coding, and Spacewalk Thoughts — all quiet, slow, and acoustic.

**Why it makes sense:** Think of it like two different rooms in a house. The Pop listener is in the gym with the speakers loud. The Lofi listener is in a library with headphones on. The scoring system is responding correctly here — energy and acousticness are pulling the results in completely opposite directions. Library Rain scored a near-perfect 6.86/7.0 for the Lofi profile because it matched on every single signal at once: right genre, right mood, almost identical energy, and high acousticness.

**What surprised me:** The gap between rank 1 and rank 5 was much bigger for the Lofi profile (6.86 down to 2.85) than for the Pop profile (6.66 down to 2.86). That means the catalog contains a tight cluster of songs that suit a chill listener very well, while the pop listener's top results thin out quickly after rank 2. Lofi listeners are actually better served by this catalog than pop listeners.

---

## Pair 2 — High-Energy Pop vs Intense Rock

**What changed:** Both profiles ask for high energy (0.9) and no acousticness. The only difference is genre (pop vs rock) and mood (happy vs intense). Despite that, the top-5 lists are almost completely different.

**Why it makes sense:** The genre and mood bonuses act like hard filters at the top. Sunrise City (pop/happy) and Storm Runner (rock/intense) are each a near-perfect match for their respective profiles and land at #1 with scores around 6.6–6.9. Below rank 2, the lists start to look similar — songs like Club Pulse and Iron Fist appear in both because they score well on energy even without a genre or mood match.

**What surprised me:** Gym Hero (pop/intense) appears at rank 2 for both profiles with nearly the same score (4.89). For the Pop listener, it gets there via genre match. For the Rock listener, it gets there via mood match. The *same song earns its position through a completely different combination of reasons* depending on who is listening — the number looks identical but the explanation is different. This is a good reminder that a score alone does not tell the full story.

---

## Pair 3 — High-Energy Pop vs Ghost Genre (k-pop)

**What changed:** The k-pop profile is almost identical to the Pop profile (same mood, similar energy) except the genre does not exist in the catalog.

**Why it makes sense:** Removing the genre match is like removing the most important filter. The k-pop listener still sees Sunrise City at rank 1 — but only because it happens to be happy and high-energy, not because it is the right genre. The system is essentially saying "I cannot find what you really want, so here is the closest thing by feel."

**The plain-language explanation for Gym Hero:** Gym Hero keeps appearing for Happy Pop listeners because the scoring system grades songs on four separate report cards — genre, mood, energy, and acousticness — and adds them up. Gym Hero is a pop song, so it passes the genre test. It is very high energy (0.93), so it nearly aces the energy test. And it is not acoustic, which is what a non-acoustic pop listener wants. It only fails the mood test (it is "intense" not "happy"). But three passes out of four is still a good total score, so it lands at rank 2. The system has no way to know that "intense gym energy" and "happy dancefloor energy" feel completely different to an actual listener — to the math, they are both just "pop + high energy."

---

## Pair 4 — Intense Rock vs High-Energy + Melancholic

**What changed:** Both profiles want rock at high energy (0.9), but one wants "intense" mood and the other wants "melancholic."

**Why it makes sense:** Storm Runner (rock/intense) dominates both lists at rank 1. For Intense Rock it scores 6.88 — a near-perfect match. For High-Energy + Melancholic it scores 4.88 — still rank 1, but significantly lower, because it gets no mood points. The gap at the top opened up and the bottom of the list filled in with random high-energy songs (Gym Hero, Club Pulse) that have nothing to do with rock or melancholy.

**What surprised me:** Blue Midnight (blues/melancholic, energy 0.38) was the *only song in the entire catalog* that matched the melancholic mood for a high-energy listener. It appeared at rank 2 with 3.16 points — but it got there almost entirely on its mood bonus alone, because its energy is so far from the target (0.9) that the energy score collapsed to near zero. The system found the right emotional match but had to drag it up by the mood bonus against a wall of energy-penalty. This is the clearest example of the catalog's bias: "melancholic" and "high energy" are never paired together in the data, so the system effectively treats that combination as an impossible request.

---

## Pair 5 — Intense Rock vs Acoustic Metal Fan

**What changed:** Both profiles want aggressive, high-energy music, but the Acoustic Metal Fan adds `likes_acoustic: True` — preferring textured, acoustic sound.

**Why it makes sense:** Iron Fist (metal/aggressive, energy 0.97) wins for both profiles. But look at its score: 6.88 for Intense Rock, only 6.05 for Acoustic Metal Fan — even though Iron Fist is a perfect genre + mood + energy match for both. The reason is acousticness: Iron Fist has an acousticness score of 0.05 (very non-acoustic). The acoustic preference awards it only +0.05 instead of +0.95. The system is penalising its best match for not being acoustic enough.

**What surprised me:** The gap between rank 1 (6.05) and rank 2 (1.98) for the Acoustic Metal Fan is nearly 4 full points — the largest gap of any profile. This means Iron Fist is the only remotely valid result; ranks 2–5 are garbage filler. The Acoustic Metal Fan preference is essentially self-contradicting given this catalog — there are no acoustic metal songs in the data, so the system cannot satisfy both halves of the request at once. It correctly defaults to the one song that nails three out of four signals, but the acoustic preference becomes meaningless noise.

---

## Overall Takeaway

The recommender works well when a listener's preferences are consistent with the patterns already in the catalog — upbeat pop users and chill lofi users are both served well because those genres have multiple songs that cluster together. The system struggles when a listener's preferences cross the hidden assumptions baked into the data, like wanting melancholy at high energy or acoustic texture in metal. In those cases, the scores still produce a ranked list — but the top results are either a lucky accident or a compromise that no real listener would actually enjoy.
