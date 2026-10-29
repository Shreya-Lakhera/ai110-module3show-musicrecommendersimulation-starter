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
`valence`, `danceability`, and `acousticness` (along with identifying
information such as title and artist). The profile stores the preferences
that are most useful for distinguishing contrasting songs:

```python
user_prefs = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,
    "likes_acoustic": False,
}
```

This profile should clearly separate an intense rock song from a chill lofi
song: the genre and mood matches receive points, and the high target energy
favors energetic tracks. It is intentionally specific enough to make those
differences visible without requiring every song to match exactly.

### Algorithm Recipe

For every song, the scoring loop starts at zero and applies these rules:

1. Add **2.0 points** when `song["genre"]` matches `favorite_genre`.
2. Add **1.0 point** when `song["mood"]` matches `favorite_mood`.
3. Add an energy-similarity score of
   `1.0 - abs(song["energy"] - target_energy)`. This gives a song closer to
   the target energy more points while keeping the contribution between zero
   and one for the dataset's normalized energy values.
4. Add **0.5 points** when the user's acoustic preference agrees with the
   song's acousticness: an acoustic preference matches an acousticness of at
   least `0.6`, while a non-acoustic preference matches a value below `0.6`.
5. Sort songs by score from highest to lowest and return the top `k`
   recommendations. The explanation for each result lists the matching
   features that contributed to its score.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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


