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

@dataclass(frozen=True)
class ScoringStrategy:
    """Define the weights used by one recommendation ranking mode."""
    genre_weight: float
    mood_weight: float
    energy_weight: float


SCORING_STRATEGIES = {
    "genre-first": ScoringStrategy(genre_weight=1.5, mood_weight=0.75, energy_weight=1.5),
    "mood-first": ScoringStrategy(genre_weight=0.75, mood_weight=1.5, energy_weight=1.5),
    "energy-focused": ScoringStrategy(genre_weight=0.5, mood_weight=0.5, energy_weight=2.0),
}

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

def score_song(
    user_prefs: Dict, song: Dict, mode: str = "genre-first"
) -> Tuple[float, List[str]]:
    """Score one song with the selected ranking strategy."""
    score = 0.0
    reasons = []
    try:
        strategy = SCORING_STRATEGIES[mode]
    except KeyError as error:
        valid_modes = ", ".join(sorted(SCORING_STRATEGIES))
        raise ValueError(f"Unknown scoring mode '{mode}'. Choose: {valid_modes}") from error

    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))

    if song["genre"] == favorite_genre:
        score += strategy.genre_weight
        reasons.append(f"genre match (+{strategy.genre_weight:.2f})")

    if song["mood"] == favorite_mood:
        score += strategy.mood_weight
        reasons.append(f"mood match (+{strategy.mood_weight:.2f})")

    if target_energy is not None:
        energy_similarity = max(
            0.0, min(1.0, 1.0 - abs(float(song["energy"]) - float(target_energy)))
        )
        energy_points = strategy.energy_weight * energy_similarity
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

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "genre-first",
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked with diversity penalties."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored_songs.append((song, score, reasons))

    recommendations = []
    selected_artists = set()
    selected_genres = set()

    while scored_songs and len(recommendations) < k:
        adjusted_scores = []
        for song, score, reasons in scored_songs:
            diversity_penalty = 0.0
            penalty_reasons = []

            if song["artist"] in selected_artists:
                diversity_penalty += 1.0
                penalty_reasons.append("repeat artist penalty (-1.0)")
            if song["genre"] in selected_genres:
                diversity_penalty += 0.25
                penalty_reasons.append("repeat genre penalty (-0.25)")

            adjusted_scores.append(
                (song, score - diversity_penalty, reasons, penalty_reasons)
            )

        song, adjusted_score, reasons, penalty_reasons = max(
            adjusted_scores, key=lambda result: result[1]
        )
        explanation_parts = reasons + penalty_reasons
        explanation = ", ".join(explanation_parts) or "no preference matches"
        recommendations.append((song, adjusted_score, explanation))
        selected_artists.add(song["artist"])
        selected_genres.add(song["genre"])
        scored_songs = [
            result for result in scored_songs if result[0] is not song
        ]

    return recommendations
