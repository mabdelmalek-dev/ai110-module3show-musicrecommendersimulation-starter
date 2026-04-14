# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

In production systems, recommenders combine explicit preferences, implicit behavior (listens, skips), collaborative patterns from other users, and content features to balance relevance, novelty, and diversity. This project keeps the design intentionally small and interpretable: we score songs by how closely their attributes (genre, mood, energy, tempo, valence, acousticness, danceability) match a user's stated profile, normalize the scores, and return the Top K tracks with short explanations.

### Algorithm Recipe

- Input: a `user_prefs` dictionary containing at minimum: `favorite_genre` (str), `favorite_mood` (str), `target_energy` (0.0–1.0), and `likes_acoustic` (bool). Optional numeric targets: `target_valence`, `preferred_tempo_range`, and `wants_danceable` (bool).
- For each song in `data/songs.csv` parse attributes: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`.
- Per-song scoring (weights):
  - Genre match: +2.0 if `song.genre == favorite_genre`.
  - Mood match: +1.0 if `song.mood == favorite_mood`.
  - Energy similarity (up to +2.0):
    - energy_tolerance = 0.25
    - energy_score = 2.0 * max(0, 1 - abs(song.energy - target_energy) / energy_tolerance)
  - Acoustic preference (+1.0):
    - if `likes_acoustic`: acoustic_score = 1.0 * song.acousticness
    - else: acoustic_score = 1.0 * (1 - song.acousticness)
  - Tempo proximity (up to +0.5):
    - expected_tempo = 60 + target_energy * 160  # maps 0→60, 1→220
    - tempo_tolerance = 20
    - tempo_score = 0.5 * max(0, 1 - abs(song.tempo_bpm - expected_tempo) / tempo_tolerance)
  - Valence (optional, up to +0.5): valence_score = 0.5 * max(0, 1 - abs(song.valence - target_valence)) if provided.
  - Danceability bonus (optional): dance_score = 0.3 * song.danceability if `wants_danceable`.

- Aggregate:
  - raw_score = sum(all component scores)
  - normalization_denominator = 2.0 + 1.0 + 2.0 + 1.0 + 0.5 + 0.5 + 0.3  # sum of maximums
  - normalized_score = raw_score / normalization_denominator
  - final_score_display = normalized_score * 100

- Tie-breakers and heuristics:
  - Use `popularity_score` (if available) to prefer better-known tracks.
  - Penalize duplicate artists within the same Top-K to increase diversity.
  - Build a concise explanation string listing the top contributing factors (e.g., "genre match, energy close to 0.88").

### Process Flow (visual)

```mermaid
flowchart TD
  A[User Preferences (profile)] --> B[Load songs.csv]
  B --> C{For each song}
  C --> D[Parse song attributes]
  D --> E[Compute genre_score (+2.0 if match)]
  D --> F[Compute mood_score (+1.0 if match)]
  D --> G[Compute energy_score (up to +2.0, decays with distance)]
  D --> H[Compute acoustic_score (+1.0 or 1-acousticness)]
  D --> I[Compute tempo_score (up to +0.5)]
  D --> J[Compute valence_score (up to +0.5)]
  D --> K[Compute dance_score (up to +0.3)]
  E --> L[Sum weighted scores -> raw_score]
  F --> L
  G --> L
  H --> L
  I --> L
  J --> L
  K --> L
  L --> M[Normalize score -> final_score; build explanation]
  M --> N[Add (song, final_score, explanation) to scored_list]
  N --> C
  N --> O[After all songs]
  O --> P[Sort scored_list by final_score desc]
  P --> Q[Apply tie-breakers (popularity, diversity penalties)]
  Q --> R[Select Top K]
  R --> S[Output: Ranked recommendations (+ explanations)]
```

### Potential Biases and Limitations

- Over-prioritizing genre: the +2.0 genre bonus strongly favors same-genre tracks and can hide songs from other genres that better match the user's mood or energy.
- Label noise and granularity: genre and mood are coarse categorical labels; inconsistent labeling or mixed-genre tracks reduce accuracy.
- Popularity bias (if used): favoring popular tracks can reduce discovery of niche or newer artists.
- Numeric target brittleness: a single `target_energy` needs a tolerance; users with broader tastes benefit from range-based preferences or multiple favorite genres.
- Underrepresentation: rare genres in the catalog will be poorly recommended even if they match a user's stated preference.

You can tune weights (genre vs energy vs mood), add preference weights or ranges, or learn weights from interaction data to mitigate these biases over time.

**Process Flow**

```mermaid
flowchart TD
  A[User Preferences (profile)] --> B[Load songs.csv]
  B --> C{For each song}
  C --> D[Parse song attributes]
  D --> E[Compute genre_score (+2.0 if match)]
  D --> F[Compute mood_score (+1.0 if match)]
  D --> G[Compute energy_score (up to +2.0, decays with distance)]
  D --> H[Compute acoustic_score (+1.0 or 1-acousticness)]
  D --> I[Compute tempo_score (up to +0.5)]
  D --> J[Compute valence_score (up to +0.5)]
  D --> K[Compute dance_score (up to +0.3)]
  E --> L[Sum weighted scores -> raw_score]
  F --> L
  G --> L
  H --> L
  I --> L
  J --> L
  K --> L
  L --> M[Normalize score -> final_score; build explanation]
  M --> N[Add (song, final_score, explanation) to scored_list]
  N --> C
  N --> O[After all songs]
  O --> P[Sort scored_list by final_score desc]
  P --> Q[Apply tie-breakers (popularity, diversity penalties)]
  Q --> R[Select Top K]
  R --> S[Output: Ranked recommendations (+ explanations)]
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Output

Running `python -m src.main` with the default Pop · Happy · Energy 0.8 profile:

```
============================================================
              Music Recommender — Top 5 Results
============================================================
  Profile: Pop · Happy · Energy 0.8 · Acoustic no
------------------------------------------------------------

  1. Sunrise City  —  Neon Echo
     Score  : 6.78 / 7.0
     • genre match (+2.0)
     • mood match (+2.0)
     • energy proximity (+1.96)
     • acousticness preference (+0.82)

  2. Gym Hero  —  Max Pulse
     Score  : 4.69 / 7.0
     • genre match (+2.0)
     • energy proximity (+1.74)
     • acousticness preference (+0.95)

  3. Rooftop Lights  —  Indigo Parade
     Score  : 4.57 / 7.0
     • mood match (+2.0)
     • energy proximity (+1.92)
     • acousticness preference (+0.65)

  4. Club Pulse  —  Young Rhyme
     Score  : 2.74 / 7.0
     • energy proximity (+1.84)
     • acousticness preference (+0.90)

  5. Storm Runner  —  Voltline
     Score  : 2.68 / 7.0
     • energy proximity (+1.78)
     • acousticness preference (+0.90)

============================================================
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

