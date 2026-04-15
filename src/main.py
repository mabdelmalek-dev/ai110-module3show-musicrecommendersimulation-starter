"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, SCORING_MODES


def print_recommendations(recommendations, user_prefs: dict, k: int,
                          label: str = "", index: int = 0, mode_name: str = "balanced") -> None:
    mode     = SCORING_MODES[mode_name]
    genre    = user_prefs["favorite_genre"].capitalize()
    mood     = user_prefs["favorite_mood"].capitalize()
    energy   = user_prefs["target_energy"]
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"

    W = 66
    print("\n" + "#" * W)
    print(f"  PROFILE {index}  |  {label}".center(W))
    print("#" * W)
    print(f"  Mode : {mode.name} — {mode.description}")
    print(f"  Prefs: {genre} · {mood} · Energy {energy} · Acoustic {acoustic}")
    print("-" * W)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = round((score / mode.max_score) * 20)
        bar_empty  = 20 - bar_filled
        score_bar  = "[" + "#" * bar_filled + "-" * bar_empty + "]"
        print(f"\n  {rank}.  {song['title']}  --  {song['artist']}")
        print(f"       {score_bar}  {score:.2f} / {mode.max_score:.1f}")
        for reason in explanation.split("; "):
            print(f"         - {reason}")

    print("\n" + "-" * W)


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

# Each entry: (display_label, user_prefs_dict, mode_key)
# Change the mode_key string to switch ranking strategy for that profile.
# Available modes: "balanced" | "genre_first" | "mood_first" | "energy_focused" | "discovery"
PROFILES = [
    (
        "High-Energy Pop",
        {
            "favorite_genre":       "pop",
            "favorite_mood":        "happy",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": "mainstream",
            "preferred_decade":     2020,
            "preferred_tags":       ["euphoric", "dancefloor", "uplifting"],
            "likes_instrumental":   False,
            "wants_live_feel":      False,
        },
        "balanced",       # <-- swap to any mode key to re-rank
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre":       "lofi",
            "favorite_mood":        "chill",
            "target_energy":        0.35,
            "likes_acoustic":       True,
            "preferred_popularity": None,
            "preferred_decade":     2020,
            "preferred_tags":       ["calm", "cozy", "focused"],
            "likes_instrumental":   True,
            "wants_live_feel":      False,
        },
        "mood_first",     # mood + tags dominate for a vibe-driven listener
    ),
    (
        "Intense Rock",
        {
            "favorite_genre":       "rock",
            "favorite_mood":        "intense",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": None,
            "preferred_decade":     2010,
            "preferred_tags":       ["aggressive", "powerful", "adrenaline"],
            "likes_instrumental":   False,
            "wants_live_feel":      True,
        },
        "genre_first",    # only true rock should rank highly
    ),
    (
        "Workout Playlist",
        {
            "favorite_genre":       "pop",
            "favorite_mood":        "intense",
            "target_energy":        0.95,
            "likes_acoustic":       False,
            "preferred_popularity": "mainstream",
            "preferred_decade":     2020,
            "preferred_tags":       ["energetic", "motivational", "adrenaline"],
            "likes_instrumental":   False,
            "wants_live_feel":      False,
        },
        "energy_focused", # BPM and intensity above all else
    ),
    (
        "Nostalgic Vinyl Fan",
        {
            "favorite_genre":       "blues",
            "favorite_mood":        "melancholic",
            "target_energy":        0.4,
            "likes_acoustic":       True,
            "preferred_popularity": "obscure",
            "preferred_decade":     2000,
            "preferred_tags":       ["nostalgic", "melancholic", "soulful"],
            "likes_instrumental":   False,
            "wants_live_feel":      True,
        },
        "discovery",      # obscure + live + era signals boosted
    ),
    (
        "EDGE: Same Profile, Different Mode (High-Energy Pop / Genre-First)",
        # Identical prefs to profile 1 — shows how mode alone reshuffles ranks
        {
            "favorite_genre":       "pop",
            "favorite_mood":        "happy",
            "target_energy":        0.9,
            "likes_acoustic":       False,
            "preferred_popularity": "mainstream",
            "preferred_decade":     2020,
            "preferred_tags":       ["euphoric", "dancefloor", "uplifting"],
            "likes_instrumental":   False,
            "wants_live_feel":      False,
        },
        "genre_first",    # same listener, strict genre filter — compare with profile 1
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    k = 5

    for i, (label, user_prefs, mode_name) in enumerate(PROFILES, start=1):
        mode = SCORING_MODES[mode_name]
        recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode)
        print_recommendations(recommendations, user_prefs, k,
                              label=label, index=i, mode_name=mode_name)


if __name__ == "__main__":
    main()
