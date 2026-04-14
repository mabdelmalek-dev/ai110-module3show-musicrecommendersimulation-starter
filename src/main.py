"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

MAX_SCORE = 7.0  # genre(2) + mood(2) + energy(2) + acousticness(1)


def print_recommendations(recommendations, user_prefs: dict, k: int) -> None:
    genre  = user_prefs["favorite_genre"].capitalize()
    mood   = user_prefs["favorite_mood"].capitalize()
    energy = user_prefs["target_energy"]
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"

    width = 60
    print()
    print("=" * width)
    print(f"  Music Recommender — Top {k} Results".center(width))
    print("=" * width)
    print(f"  Profile: {genre} · {mood} · Energy {energy} · Acoustic {acoustic}")
    print("-" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']}  —  {song['artist']}")
        print(f"     Score  : {score:.2f} / {MAX_SCORE:.1f}")
        # Print each reason on its own indented line for readability
        for reason in explanation.split("; "):
            print(f"     • {reason}")

    print()
    print("=" * width)
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Default "pop / happy" profile — keys must match score_song expectations
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.8,
        "likes_acoustic": False,
    }

    k = 5
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print_recommendations(recommendations, user_prefs, k)


if __name__ == "__main__":
    main()
