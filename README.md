# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The recommender compares each song in `data/songs.csv` with one user's
taste profile. Each song includes its `genre`, `mood`, `energy`, `tempo_bpm`,
`valence`, `danceability`, `acousticness`, `popularity`, `release_decade`,
`mood_tags`, `lyrical_complexity`, and `instrumentalness` (along with
identifying information such as title and artist). The profile stores the preferences
that are most useful for distinguishing contrasting songs:

```python
user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}
```

This profile should clearly separate an upbeat pop song from a chill lofi
song: the genre and mood matches receive points, and the high target energy
favors energetic tracks. It is intentionally specific enough to make those
differences visible without requiring every song to match exactly.

### Algorithm Recipe

For every song, the scoring loop starts at zero and applies these rules:

1. Add **1.0 point** when `song["genre"]` matches `favorite_genre`.
2. Add **1.0 point** when `song["mood"]` matches `favorite_mood`.
3. Add an energy-similarity score of
   `1.0 - abs(song["energy"] - target_energy)`. This gives a song closer to
   the target energy more points. The experiment doubles this similarity
   contribution, so energy contributes between zero and two points.
4. Add **0.5 points** when the user's acoustic preference agrees with the
   song's acousticness: an acoustic preference matches an acousticness of at
   least `0.6`, while a non-acoustic preference matches a value below `0.6`.
5. Add up to **0.5 points** for popularity similarity, **0.5 points** for a
   preferred release decade, and **0.5 points** for a preferred detailed mood
   tag.
6. Add up to **0.5 points** for lyrical-complexity similarity and **0.5
   points** when instrumentalness agrees with the user's preference.
7. Sort songs by score from highest to lowest and return the top `k`
   recommendations. The explanation for each result lists the matching
   features that contributed to its score.

The implementation uses Python's `sorted()` rather than `.sort()`.
`sorted()` returns a new ranked list and leaves the original song catalog
unchanged; `.sort()` would reorder the catalog in place.

The data flow is:

```text
Input: user_prefs
          |
          v
Process: load songs -> score every song -> record reasons
          |
          v
Output: sort by score -> return top k recommendations
```

### Expected Biases

This rule may over-prioritize genre because a genre match is worth twice as
much as a mood match. It may also favor high-energy songs for this particular
profile and overlook a great song with a different genre or mood. The small
ten-song catalog, hand-selected features, and single fixed profile can make
the results less representative than a real user's preferences.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

The current High-Energy Pop profile produces:

```
Loaded songs: 10

Top recommendations:

Sunrise City - Score: 6.82
Because: genre match (+1.0), mood match (+1.0), energy similarity (+1.84), acoustic preference match (+0.5), popularity similarity (+0.48), release decade match (+0.5), detailed mood tag match (+0.5), lyrical complexity similarity (+0.49), instrumental preference match (+0.5)

Gym Hero - Score: 5.89
Because: genre match (+1.0), energy similarity (+1.94), acoustic preference match (+0.5), popularity similarity (+0.46), release decade match (+0.5), detailed mood tag match (+0.5), lyrical complexity similarity (+0.49), instrumental preference match (+0.5)

Rooftop Lights - Score: 4.67
Because: mood match (+1.0), energy similarity (+1.72), acoustic preference match (+0.5), popularity similarity (+0.49), lyrical complexity similarity (+0.46), instrumental preference match (+0.5)

Storm Runner - Score: 3.88
Because: energy similarity (+1.98), acoustic preference match (+0.5), popularity similarity (+0.48), lyrical complexity similarity (+0.42), instrumental preference match (+0.5)

Night Drive Loop - Score: 3.60
Because: energy similarity (+1.70), acoustic preference match (+0.5), popularity similarity (+0.47), detailed mood tag match (+0.5), lyrical complexity similarity (+0.43)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
