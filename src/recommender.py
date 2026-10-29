import csv
from typing import List, Dict, Tuple, Optional
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

def load_songs(csv_path):
    """Load songs from a CSV file and convert numeric features."""
    songs = []

    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["popularity"] = int(row["popularity"])
            row["release_decade"] = int(row["release_decade"].replace("s", ""))
            row["lyrical_complexity"] = float(row["lyrical_complexity"])
            row["instrumentalness"] = float(row["instrumentalness"])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and explain the result."""
    score = 0.0
    reasons = []

    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))

    if song["genre"] == favorite_genre:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if target_energy is not None:
        energy_similarity = max(
            0.0, min(1.0, 1.0 - abs(float(song["energy"]) - float(target_energy)))
        )
        energy_points = 2.0 * energy_similarity
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        acousticness = float(song["acousticness"])
        acoustic_match = (
            acousticness >= 0.6
            if user_prefs["likes_acoustic"]
            else acousticness < 0.6
        )
        if acoustic_match:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

    if "target_popularity" in user_prefs:
        popularity_similarity = max(
            0.0,
            min(
                1.0,
                1.0
                - abs(
                    float(song["popularity"])
                    - float(user_prefs["target_popularity"])
                )
                / 100.0,
            ),
        )
        popularity_points = 0.5 * popularity_similarity
        score += popularity_points
        reasons.append(f"popularity similarity (+{popularity_points:.2f})")

    if "preferred_release_decade" in user_prefs:
        if song["release_decade"] == int(user_prefs["preferred_release_decade"]):
            score += 0.5
            reasons.append("release decade match (+0.5)")

    if "preferred_mood_tag" in user_prefs:
        mood_tags = song["mood_tags"].split(";")
        if user_prefs["preferred_mood_tag"] in mood_tags:
            score += 0.5
            reasons.append("detailed mood tag match (+0.5)")

    if "target_lyrical_complexity" in user_prefs:
        lyrical_similarity = max(
            0.0,
            min(
                1.0,
                1.0
                - abs(
                    float(song["lyrical_complexity"])
                    - float(user_prefs["target_lyrical_complexity"])
                ),
            ),
        )
        lyrical_points = 0.5 * lyrical_similarity
        score += lyrical_points
        reasons.append(f"lyrical complexity similarity (+{lyrical_points:.2f})")

    if "likes_instrumental" in user_prefs:
        is_instrumental = float(song["instrumentalness"]) >= 0.6
        if is_instrumental == bool(user_prefs["likes_instrumental"]):
            score += 0.5
            reasons.append("instrumental preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked by preference score."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) or "no preference matches"
        scored_songs.append((song, score, explanation))

    return sorted(scored_songs, key=lambda result: result[1], reverse=True)[:k]
