"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

MAX_SCORE = 8.0  # EXPERIMENT: genre(1) + mood(2) + energy(4) + acousticness(1)


def print_recommendations(recommendations, user_prefs: dict, k: int, label: str = "", index: int = 0) -> None:
    genre    = user_prefs["favorite_genre"].capitalize()
    mood     = user_prefs["favorite_mood"].capitalize()
    energy   = user_prefs["target_energy"]
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"

    W = 62
    # Profile banner
    print("\n" + "#" * W)
    print(f"  PROFILE {index}  |  {label}".center(W))
    print("#" * W)
    print(f"  Genre: {genre}  |  Mood: {mood}  |  Energy: {energy}  |  Acoustic: {acoustic}")
    print("-" * W)

    # Results
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled  = round((score / MAX_SCORE) * 20)
        bar_empty   = 20 - bar_filled
        score_bar   = "[" + "#" * bar_filled + "-" * bar_empty + "]"
        print(f"\n  {rank}.  {song['title']}  --  {song['artist']}")
        print(f"       {score_bar}  {score:.2f} / {MAX_SCORE:.1f}")
        for reason in explanation.split("; "):
            print(f"         - {reason}")

    print("\n" + "-" * W)


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = [
    # --- Standard profiles ---------------------------------------------------
    (
        "High-Energy Pop",
        {
            "favorite_genre": "pop",
            "favorite_mood":  "happy",
            "target_energy":  0.9,
            "likes_acoustic": False,
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre": "lofi",
            "favorite_mood":  "chill",
            "target_energy":  0.35,
            "likes_acoustic": True,
        },
    ),
    (
        "Intense Rock",
        {
            "favorite_genre": "rock",
            "favorite_mood":  "intense",
            "target_energy":  0.9,
            "likes_acoustic": False,
        },
    ),
    # --- Adversarial / edge-case profiles ------------------------------------
    (
        "EDGE: Ghost Genre (k-pop not in catalog)",
        # No song will ever match the genre — the +2.0 genre bonus never fires.
        # Reveals how tightly scores compress when only energy + acousticness score.
        {
            "favorite_genre": "k-pop",
            "favorite_mood":  "happy",
            "target_energy":  0.8,
            "likes_acoustic": False,
        },
    ),
    (
        "EDGE: High-Energy + Melancholic (conflicting signals)",
        # 'melancholic' only exists on low-energy classical/blues songs.
        # Tests whether the rock genre bonus on Storm Runner overrides the mood mismatch.
        {
            "favorite_genre": "rock",
            "favorite_mood":  "melancholic",
            "target_energy":  0.9,
            "likes_acoustic": False,
        },
    ),
    (
        "EDGE: Acoustic Metal Fan (preference punishes the perfect match)",
        # Iron Fist (metal/aggressive, energy 0.97) is a perfect genre+mood+energy match
        # but has acousticness 0.05 — likes_acoustic:True awards only +0.05 to it,
        # while highly acoustic songs it should never surface gain up to +1.0.
        {
            "favorite_genre": "metal",
            "favorite_mood":  "aggressive",
            "target_energy":  0.97,
            "likes_acoustic": True,
        },
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    k = 5

    for i, (label, user_prefs) in enumerate(PROFILES, start=1):
        recommendations = recommend_songs(user_prefs, songs, k=k)
        print_recommendations(recommendations, user_prefs, k, label=label, index=i)


if __name__ == "__main__":
    main()
