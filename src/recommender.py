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
                }
                songs.append(song)
    except FileNotFoundError:
        print(f"Error: file not found: {csv_path}")
    except Exception as exc:
        print(f"Error reading {csv_path}: {exc}")

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences; return (total_score, reason_strings) with max 8.0."""
    # EXPERIMENT: genre halved (2.0 -> 1.0), energy doubled (x2.0 -> x4.0). New max = 8.0.
    # Revert to GENRE_W=2.0 and ENERGY_W=2.0 to restore original weights.
    GENRE_W  = 1.0   # was 2.0
    MOOD_W   = 2.0
    ENERGY_W = 4.0   # was 2.0
    ACOUSTIC_W = 1.0

    score = 0.0
    reasons: List[str] = []

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
