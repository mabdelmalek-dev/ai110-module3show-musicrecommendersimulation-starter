from typing import List, Dict, Tuple, Optional
import csv
from dataclasses import dataclass

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences; return (total_score, reason_strings) with max 14.0."""
    # --- weights (original 8.0 budget) ---
    GENRE_W     = 1.0
    MOOD_W      = 2.0
    ENERGY_W    = 4.0
    ACOUSTIC_W  = 1.0
    # --- new attribute weights (6.0 budget, total max = 14.0) ---
    POPULAR_W   = 1.0   # mainstream or obscure preference
    ERA_W       = 1.5   # exact decade match; 0.5× for adjacent decade
    TAG_W       = 0.5   # per overlapping mood tag, capped at 4 matches (+2.0)
    INSTRU_W    = 1.0   # instrumental vs vocal preference
    LIVE_W      = 0.5   # live-feel preference

    score = 0.0
    reasons: List[str] = []

    # --- original signals ---

    # Genre match — binary
    if song.get('genre', '').lower() == user_prefs.get('favorite_genre', '').lower():
        score += GENRE_W
        reasons.append(f"genre match (+{GENRE_W:.1f})")

    # Mood match — binary
    if song.get('mood', '').lower() == user_prefs.get('favorite_mood', '').lower():
        score += MOOD_W
        reasons.append(f"mood match (+{MOOD_W:.1f})")

    # Energy proximity — continuous, max = ENERGY_W
    target_energy = user_prefs.get('target_energy')
    song_energy = song.get('energy')
    if target_energy is not None and song_energy is not None:
        points = (1.0 - abs(target_energy - song_energy)) * ENERGY_W
        score += points
        reasons.append(f"energy proximity (+{points:.2f})")

    # Acousticness preference — continuous, max = ACOUSTIC_W
    acousticness = song.get('acousticness')
    if acousticness is not None:
        points = (acousticness if user_prefs.get('likes_acoustic') else (1.0 - acousticness)) * ACOUSTIC_W
        score += points
        reasons.append(f"acousticness preference (+{points:.2f})")

    # --- new signals ---

    # Popularity: "mainstream" rewards popular songs; "obscure" rewards hidden gems
    pop_pref   = user_prefs.get('preferred_popularity')
    popularity = song.get('popularity')
    if pop_pref is not None and popularity is not None:
        if pop_pref == 'mainstream':
            points = (popularity / 100.0) * POPULAR_W
        else:  # 'obscure'
            points = ((100 - popularity) / 100.0) * POPULAR_W
        score += points
        reasons.append(f"{pop_pref} popularity (+{points:.2f})")

    # Era match: exact decade = ERA_W; one decade away = ERA_W × 0.5
    pref_decade  = user_prefs.get('preferred_decade')
    song_decade  = song.get('release_decade')
    if pref_decade is not None and song_decade is not None:
        gap = abs(pref_decade - song_decade)
        if gap == 0:
            points = ERA_W
            reasons.append(f"era match {song_decade}s (+{points:.2f})")
        elif gap == 10:
            points = ERA_W * 0.5
            reasons.append(f"adjacent era {song_decade}s (+{points:.2f})")
        else:
            points = 0.0
        score += points

    # Mood tags: +TAG_W per overlapping tag, max 4 matches
    pref_tags = user_prefs.get('preferred_tags') or []
    song_tags = song.get('mood_tags') or []
    if pref_tags and song_tags:
        matches = [t for t in pref_tags if t in song_tags][:4]
        if matches:
            points = len(matches) * TAG_W
            score += points
            reasons.append(f"tag overlap {matches} (+{points:.2f})")

    # Instrumentalness: reward instrumental or vocal tracks based on preference
    instru_pref   = user_prefs.get('likes_instrumental')
    instrumentalness = song.get('instrumentalness')
    if instru_pref is not None and instrumentalness is not None:
        points = (instrumentalness if instru_pref else (1.0 - instrumentalness)) * INSTRU_W
        score += points
        reasons.append(f"instrumentalness preference (+{points:.2f})")

    # Liveness: reward live-feel or studio-clean based on preference
    live_pref = user_prefs.get('wants_live_feel')
    liveness  = song.get('liveness')
    if live_pref is not None and liveness is not None:
        points = (liveness if live_pref else (1.0 - liveness)) * LIVE_W
        score += points
        reasons.append(f"liveness preference (+{points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs from the catalog ranked by score_song, highest score first."""
    def to_entry(song: Dict) -> Tuple[Dict, float, str]:
        """Pack a song into a (song, score, explanation) tuple using score_song."""
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong matches found."
        return (song, score, explanation)

    scored = [to_entry(song) for song in songs]
    return sorted(scored, key=lambda entry: entry[1], reverse=True)[:k]
