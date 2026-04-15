"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

MAX_SCORE = 14.0  # genre(1)+mood(2)+energy(4)+acoustic(1)+popularity(1)+era(1.5)+tags(2)+instru(1)+live(0.5)


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
    # --- Standard profiles (now include all new preference fields) -----------
    (
        "High-Energy Pop",
        {
            "favorite_genre":       "pop",
            "favorite_mood":        "happy",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": "mainstream",  # reward well-known tracks
            "preferred_decade":     2020,           # wants current-era songs
            "preferred_tags":       ["euphoric", "dancefloor", "uplifting"],
            "likes_instrumental":   False,          # wants vocals
            "wants_live_feel":      False,          # prefers studio-clean
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre":       "lofi",
            "favorite_mood":        "chill",
            "target_energy":        0.35,
            "likes_acoustic":       True,
            "preferred_popularity": None,           # popularity doesn't matter
            "preferred_decade":     2020,
            "preferred_tags":       ["calm", "cozy", "focused"],
            "likes_instrumental":   True,           # prefers no vocals
            "wants_live_feel":      False,
        },
    ),
    (
        "Intense Rock",
        {
            "favorite_genre":       "rock",
            "favorite_mood":        "intense",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": None,
            "preferred_decade":     2010,           # prefers 2010s rock era
            "preferred_tags":       ["aggressive", "powerful", "adrenaline"],
            "likes_instrumental":   False,
            "wants_live_feel":      True,           # wants that live-gig energy
        },
    ),
    # --- New profile: exercises all 5 new attributes -------------------------
    (
        "Nostalgic Vinyl Fan",
        # Wants obscure, acoustic, vocal blues from the 2000s with a live feel.
        # Tests era match, obscure popularity, soulful tag overlap, and liveness.
        {
            "favorite_genre":       "blues",
            "favorite_mood":        "melancholic",
            "target_energy":        0.4,
            "likes_acoustic":       True,
            "preferred_popularity": "obscure",      # prefers under-the-radar songs
            "preferred_decade":     2000,           # wants 2000s or adjacent era
            "preferred_tags":       ["nostalgic", "melancholic", "soulful"],
            "likes_instrumental":   False,          # wants vocal-led songs
            "wants_live_feel":      True,           # wants live recording warmth
        },
    ),
    # --- Adversarial / edge-case profiles ------------------------------------
    (
        "EDGE: Ghost Genre (k-pop not in catalog)",
        {
            "favorite_genre":       "k-pop",
            "favorite_mood":        "happy",
            "target_energy":        0.8,
            "likes_acoustic":       False,
            "preferred_popularity": "mainstream",
            "preferred_decade":     2020,
            "preferred_tags":       ["euphoric", "dancefloor"],
            "likes_instrumental":   False,
            "wants_live_feel":      False,
        },
    ),
    (
        "EDGE: High-Energy + Melancholic (conflicting signals)",
        {
            "favorite_genre":       "rock",
            "favorite_mood":        "melancholic",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": None,
            "preferred_decade":     2010,
            "preferred_tags":       ["melancholic", "powerful"],
            "likes_instrumental":   False,
            "wants_live_feel":      True,
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
