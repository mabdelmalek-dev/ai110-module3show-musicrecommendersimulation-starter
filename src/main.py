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
                          label: str = "", index: int = 0, mode_name: str = "balanced",
                          artist_penalty: float = 2.0, genre_penalty: float = 0.5) -> None:
    mode     = SCORING_MODES[mode_name]
    genre    = user_prefs["favorite_genre"].capitalize()
    mood     = user_prefs["favorite_mood"].capitalize()
    energy   = user_prefs["target_energy"]
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    diversity = f"artist -{artist_penalty:.0f}  genre -{genre_penalty:.1f}" if (artist_penalty or genre_penalty) else "OFF"

    W = 66
    print("\n" + "#" * W)
    print(f"  PROFILE {index}  |  {label}".center(W))
    print("#" * W)
    print(f"  Mode     : {mode.name}")
    print(f"  Diversity: {diversity}")
    print(f"  Prefs    : {genre} · {mood} · Energy {energy} · Acoustic {acoustic}")
    print("-" * W)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = max(0, round((score / mode.max_score) * 20))
        bar_empty  = 20 - bar_filled
        score_bar  = "[" + "#" * bar_filled + "-" * bar_empty + "]"
        print(f"\n  {rank}.  {song['title']}  --  {song['artist']}")
        print(f"       {score_bar}  {score:.2f} / {mode.max_score:.1f}")
        for reason in explanation.split("; "):
            tag = "!" if "diversity penalty" in reason else "-"
            print(f"         {tag} {reason}")

    print("\n" + "-" * W)


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

# Each entry: (display_label, user_prefs_dict, mode_key, artist_penalty, genre_penalty)
# artist_penalty — score deduction per duplicate artist already in results (default 2.0)
# genre_penalty  — score deduction per duplicate genre already in results  (default 0.5)
# Set both to 0.0 to disable diversity enforcement for that profile.
_LOFI_PREFS = {
    "favorite_genre":       "lofi",
    "favorite_mood":        "chill",
    "target_energy":        0.35,
    "likes_acoustic":       True,
    "preferred_popularity": None,
    "preferred_decade":     2020,
    "preferred_tags":       ["calm", "cozy", "focused"],
    "likes_instrumental":   True,
    "wants_live_feel":      False,
}

PROFILES = [
    #  label,  user_prefs,  mode_key,  artist_penalty,  genre_penalty
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
        "balanced", 2.0, 0.5,
    ),
    (
        "Chill Lofi  (NO diversity — shows filter bubble)",
        _LOFI_PREFS,
        "mood_first", 0.0, 0.0,   # diversity OFF — same artist/genre can dominate
    ),
    (
        "Chill Lofi  (WITH diversity — compare above)",
        _LOFI_PREFS,
        "mood_first", 2.0, 0.5,   # diversity ON  — artist+genre penalty applied
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
        "genre_first", 2.0, 0.5,
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
        "energy_focused", 2.0, 0.5,
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
        "discovery", 2.0, 1.0,    # stronger genre penalty for wider discovery
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    k = 5

    for i, (label, user_prefs, mode_name, ap, gp) in enumerate(PROFILES, start=1):
        mode = SCORING_MODES[mode_name]
        recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode,
                                          artist_penalty=ap, genre_penalty=gp)
        print_recommendations(recommendations, user_prefs, k,
                              label=label, index=i, mode_name=mode_name,
                              artist_penalty=ap, genre_penalty=gp)


if __name__ == "__main__":
    main()
