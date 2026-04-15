from typing import List, Dict, Tuple, Optional
import csv
from dataclasses import dataclass, field

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    print(f"Loading songs from {csv_path}...")
    try:
        with open(csv_path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                # convert numeric fields
                try:
                    song_id = int(row.get('id', '').strip()) if row.get('id', '').strip() != '' else None
                except Exception:
                    song_id = None

                def to_float(key: str) -> Optional[float]:
                    v = row.get(key, '')
                    if v is None:
                        return None
                    v = v.strip()
                    if v == '':
                        return None
                    try:
                        return float(v)
                    except Exception:
                        return None

                def to_int(key: str) -> Optional[int]:
                    v = row.get(key, '')
                    if v is None:
                        return None
                    v = v.strip()
                    if v == '':
                        return None
                    try:
                        return int(v)
                    except Exception:
                        return None

                raw_tags = row.get('mood_tags', '').strip().strip('"')
                mood_tags = [t.strip() for t in raw_tags.split(',') if t.strip()] if raw_tags else []

                song = {
                    'id': song_id,
                    'title': row.get('title', '').strip(),
                    'artist': row.get('artist', '').strip(),
                    'genre': row.get('genre', '').strip(),
                    'mood': row.get('mood', '').strip(),
                    'energy': to_float('energy'),
                    'tempo_bpm': to_float('tempo_bpm'),
                    'valence': to_float('valence'),
                    'danceability': to_float('danceability'),
                    'acousticness': to_float('acousticness'),
                    # --- new attributes ---
                    'popularity':      to_int('popularity'),
                    'release_decade':  to_int('release_decade'),
                    'mood_tags':       mood_tags,
                    'instrumentalness': to_float('instrumentalness'),
                    'liveness':        to_float('liveness'),
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: file not found: {csv_path}")
    except Exception as exc:
        print(f"Error reading {csv_path}: {exc}")

    print(f"Loaded songs: {len(songs)}")
    return songs

# ---------------------------------------------------------------------------
# Scoring Strategy — dataclass carrying all signal weights for one mode.
# Swap the mode object to change ranking behaviour without touching any
# scoring logic.  Each weight scales the raw signal value for that feature.
# ---------------------------------------------------------------------------

@dataclass
class ScoringMode:
    """
    Holds the weight multipliers for every scoring signal.
    Pass a different ScoringMode instance to score_song / recommend_songs
    to switch ranking strategy without changing any scoring logic.
    """
    name:        str
    description: str
    # categorical signals
    genre_w:    float = 1.0   # flat bonus for exact genre match
    mood_w:     float = 2.0   # flat bonus for exact mood match
    # continuous signals
    energy_w:   float = 4.0   # (1 - |target - song|) × energy_w
    acoustic_w: float = 1.0   # acousticness or (1-acousticness) × acoustic_w
    popular_w:  float = 1.0   # (pop/100) or ((100-pop)/100) × popular_w
    era_w:      float = 1.5   # exact decade = era_w; adjacent = era_w × 0.5
    tag_w:      float = 0.5   # +tag_w per matching mood tag (max 4 tags)
    instru_w:   float = 1.0   # instrumentalness or (1-instrumentalness) × instru_w
    live_w:     float = 0.5   # liveness or (1-liveness) × live_w

    @property
    def max_score(self) -> float:
        """Theoretical maximum achievable under this mode."""
        return (self.genre_w + self.mood_w + self.energy_w + self.acoustic_w +
                self.popular_w + self.era_w + self.tag_w * 4 +
                self.instru_w + self.live_w)


# ---------------------------------------------------------------------------
# Built-in mode presets — import SCORING_MODES in main.py to switch modes.
# ---------------------------------------------------------------------------

SCORING_MODES: Dict[str, ScoringMode] = {
    "balanced": ScoringMode(
        name="Balanced",
        description="All signals weighted evenly. Good general-purpose default.",
        genre_w=1.0, mood_w=2.0, energy_w=4.0, acoustic_w=1.0,
        popular_w=1.0, era_w=1.5, tag_w=0.5, instru_w=1.0, live_w=0.5,
    ),
    "genre_first": ScoringMode(
        name="Genre-First",
        description="Genre match worth 5× everything else. Use when catalog identity matters most.",
        genre_w=5.0, mood_w=1.0, energy_w=1.5, acoustic_w=0.5,
        popular_w=0.5, era_w=0.5, tag_w=0.25, instru_w=0.5, live_w=0.25,
    ),
    "mood_first": ScoringMode(
        name="Mood-First",
        description="Emotional feel and tag overlap dominate. Genre is just a tiebreaker.",
        genre_w=0.5, mood_w=5.0, energy_w=1.5, acoustic_w=0.5,
        popular_w=0.5, era_w=0.5, tag_w=1.5, instru_w=0.5, live_w=0.25,
    ),
    "energy_focused": ScoringMode(
        name="Energy-Focused",
        description="BPM and intensity dominate. Great for workout or activity playlists.",
        genre_w=0.5, mood_w=0.5, energy_w=8.0, acoustic_w=1.0,
        popular_w=0.5, era_w=0.5, tag_w=0.25, instru_w=0.5, live_w=0.25,
    ),
    "discovery": ScoringMode(
        name="Discovery",
        description="Rewards obscure songs, live recordings, and era specificity. Finds hidden gems.",
        genre_w=0.5, mood_w=1.0, energy_w=2.0, acoustic_w=1.0,
        popular_w=3.0, era_w=2.0, tag_w=1.0, instru_w=1.0, live_w=2.0,
    ),
}

DEFAULT_MODE = SCORING_MODES["balanced"]


def score_song(user_prefs: Dict, song: Dict,
               mode: ScoringMode = DEFAULT_MODE) -> Tuple[float, List[str]]:
    """Score a song against user preferences using the given ScoringMode's weights."""
    score = 0.0
    reasons: List[str] = []

    # Genre match — binary
    if song.get('genre', '').lower() == user_prefs.get('favorite_genre', '').lower():
        score += mode.genre_w
        reasons.append(f"genre match (+{mode.genre_w:.1f})")

    # Mood match — binary
    if song.get('mood', '').lower() == user_prefs.get('favorite_mood', '').lower():
        score += mode.mood_w
        reasons.append(f"mood match (+{mode.mood_w:.1f})")

    # Energy proximity — continuous, max = mode.energy_w
    target_energy = user_prefs.get('target_energy')
    song_energy   = song.get('energy')
    if target_energy is not None and song_energy is not None:
        points = (1.0 - abs(target_energy - song_energy)) * mode.energy_w
        score += points
        reasons.append(f"energy proximity (+{points:.2f})")

    # Acousticness preference — continuous, max = mode.acoustic_w
    acousticness = song.get('acousticness')
    if acousticness is not None:
        points = (acousticness if user_prefs.get('likes_acoustic') else (1.0 - acousticness)) * mode.acoustic_w
        score += points
        reasons.append(f"acousticness (+{points:.2f})")

    # Popularity — direction set by user_prefs, magnitude scaled by mode.popular_w
    pop_pref   = user_prefs.get('preferred_popularity')
    popularity = song.get('popularity')
    if pop_pref is not None and popularity is not None:
        raw    = (popularity / 100.0) if pop_pref == 'mainstream' else ((100 - popularity) / 100.0)
        points = raw * mode.popular_w
        score += points
        reasons.append(f"{pop_pref} popularity (+{points:.2f})")

    # Era match — exact decade = mode.era_w; adjacent = mode.era_w × 0.5
    pref_decade = user_prefs.get('preferred_decade')
    song_decade = song.get('release_decade')
    if pref_decade is not None and song_decade is not None:
        gap = abs(pref_decade - song_decade)
        if gap == 0:
            points = mode.era_w
            reasons.append(f"era match {song_decade}s (+{points:.2f})")
        elif gap == 10:
            points = mode.era_w * 0.5
            reasons.append(f"adjacent era {song_decade}s (+{points:.2f})")
        else:
            points = 0.0
        score += points

    # Mood tags — +mode.tag_w per overlapping tag, capped at 4
    pref_tags = user_prefs.get('preferred_tags') or []
    song_tags = song.get('mood_tags') or []
    if pref_tags and song_tags:
        matches = [t for t in pref_tags if t in song_tags][:4]
        if matches:
            points = len(matches) * mode.tag_w
            score += points
            reasons.append(f"tag overlap {matches} (+{points:.2f})")

    # Instrumentalness — continuous, max = mode.instru_w
    instru_pref      = user_prefs.get('likes_instrumental')
    instrumentalness = song.get('instrumentalness')
    if instru_pref is not None and instrumentalness is not None:
        points = (instrumentalness if instru_pref else (1.0 - instrumentalness)) * mode.instru_w
        score += points
        reasons.append(f"instrumentalness (+{points:.2f})")

    # Liveness — continuous, max = mode.live_w
    live_pref = user_prefs.get('wants_live_feel')
    liveness  = song.get('liveness')
    if live_pref is not None and liveness is not None:
        points = (liveness if live_pref else (1.0 - liveness)) * mode.live_w
        score += points
        reasons.append(f"liveness (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    mode: ScoringMode = DEFAULT_MODE,
                    artist_penalty: float = 2.0,
                    genre_penalty: float = 0.5) -> List[Tuple[Dict, float, str]]:
    """
    Return the top-k songs ranked by score_song under the given ScoringMode.

    Diversity penalty (applied at selection time, not scoring time):
      - Each time an artist is already in the selected list, every remaining
        song by that artist loses `artist_penalty` points from its effective score.
      - Each time a genre is already in the selected list, every remaining
        song in that genre loses `genre_penalty` points.
    This prevents the same artist or genre from monopolising the top results.
    Set both penalties to 0.0 to disable diversity enforcement.
    """
    # Step 1 — score every song independently (no diversity concern here)
    candidates: List[Dict] = []
    for song in songs:
        raw_score, reasons = score_song(user_prefs, song, mode)
        candidates.append({
            "song":      song,
            "raw_score": raw_score,
            "reasons":   reasons,
        })

    # Step 2 — greedy selection with running diversity penalty
    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}
    genre_counts:  Dict[str, int] = {}

    while len(selected) < k and candidates:
        # Find the candidate with the highest *effective* score after penalties
        best_idx      = 0
        best_effective = float('-inf')

        for i, entry in enumerate(candidates):
            artist  = entry["song"].get("artist", "")
            genre   = entry["song"].get("genre", "")
            penalty = (artist_counts.get(artist, 0) * artist_penalty +
                       genre_counts.get(genre,  0) * genre_penalty)
            effective = entry["raw_score"] - penalty
            if effective > best_effective:
                best_effective = effective
                best_idx = i

        chosen  = candidates.pop(best_idx)
        artist  = chosen["song"].get("artist", "")
        genre   = chosen["song"].get("genre",  "")

        # Build explanation — append penalty line if one was applied
        penalty_applied = (artist_counts.get(artist, 0) * artist_penalty +
                           genre_counts.get(genre,  0) * genre_penalty)
        reasons = list(chosen["reasons"])
        if penalty_applied > 0:
            reasons.append(f"diversity penalty (-{penalty_applied:.1f})")

        explanation = "; ".join(reasons) if reasons else "No strong matches found."
        selected.append((chosen["song"], best_effective, explanation))

        # Update counts so later picks are penalised accordingly
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
        genre_counts[genre]   = genre_counts.get(genre,  0) + 1

    return selected
