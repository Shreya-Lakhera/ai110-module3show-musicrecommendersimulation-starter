"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "target_popularity": 85,
            "preferred_release_decade": 2020,
            "preferred_mood_tag": "euphoric",
            "target_lyrical_complexity": 0.6,
            "likes_instrumental": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "likes_acoustic": True,
            "target_popularity": 70,
            "preferred_release_decade": 2020,
            "preferred_mood_tag": "nostalgic",
            "target_lyrical_complexity": 0.5,
            "likes_instrumental": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "target_popularity": 80,
            "preferred_release_decade": 2010,
            "preferred_mood_tag": "aggressive",
            "target_lyrical_complexity": 0.75,
            "likes_instrumental": False,
        },
        "Conflicting High-Energy Sad": {
            "favorite_genre": "rock",
            "favorite_mood": "sad",
            "target_energy": 0.9,
            "likes_acoustic": False,
            "target_popularity": 80,
            "preferred_release_decade": 2010,
            "preferred_mood_tag": "aggressive",
            "target_lyrical_complexity": 0.75,
            "likes_instrumental": False,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name}\n")
        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
