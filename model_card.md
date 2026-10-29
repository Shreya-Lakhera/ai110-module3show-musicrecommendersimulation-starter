# Model Card: VibeMatch 1.0

## 1. Model Name

**VibeMatch 1.0** is a small, explainable music recommender.

## 2. Goal / Task

VibeMatch suggests songs for a user's taste profile.
It ranks songs from the best match to the weakest match.
It also explains why each song received its score.

## 3. Data Used

The system uses a catalog of 10 songs from `data/songs.csv`.
Each song has a title, artist, genre, mood, energy, tempo, valence,
danceability, acousticness, popularity, release decade, detailed mood tags,
lyrical complexity, and instrumentalness.

The dataset includes pop, lofi, rock, ambient, jazz, synthwave, and indie
pop. It includes moods such as happy, chill, intense, relaxed, focused, and
moody.

This is a very small hand-selected dataset. It has no lyrics, listening
history, user ratings, skips, or demographic information. It also has no song
with a `sad` mood, so a user asking for sad music cannot get a direct mood
match.

## 4. Algorithm Summary

The user profile contains a favorite genre, favorite mood, target energy, and
acoustic preference.

The recommender checks every song:

- A genre match adds 1 point.
- A mood match adds 1 point.
- An energy value close to the target adds up to 2 points.
- An acoustic preference match adds 0.5 points.
- A close popularity target adds up to 0.5 points.
- A release decade match adds 0.5 points.
- A detailed mood tag match adds 0.5 points.
- A close lyrical-complexity target adds up to 0.5 points.
- An instrumental preference match adds 0.5 points.

The current weights come from a small experiment. The original recipe gave
genre 2 points and energy up to 1 point. The experiment reduced the genre
weight and doubled the energy weight. The system then sorts all songs and
returns the top five. Each result includes its matching reasons.

## 5. Observed Behavior / Biases

The system favors songs with energy close to the user's target. This can
outweigh a mood mismatch. For example, Gym Hero can rank highly for a Happy
Pop user because it is pop, energetic, and non-acoustic, even though its mood
is intense.

The catalog is too small to represent every taste. The missing `sad` mood
means a conflicting high-energy sad profile receives no mood points at all.
The hand-selected songs may also make some genres and energy levels seem more
common than they are in real music libraries.

## 6. Evaluation Process

I tested four profiles:

- **High-Energy Pop**
- **Chill Lofi**
- **Deep Intense Rock**
- **Conflicting High-Energy Sad**

The first three profiles produced sensible results. High-Energy Pop favored
Sunrise City. Chill Lofi favored Midnight Coding and Library Rain. Deep
Intense Rock favored Storm Runner.

The conflicting profile showed an edge case. No song matched `sad`, so the
results were driven by rock, energy, and acousticness instead.

I also ran a weight-shift experiment. I changed the genre weight from 2 to 1
and doubled the maximum energy contribution from 1 to 2. The top songs usually
stayed the same, but energy-focused songs became more competitive. I compared
each pair of profiles and checked whether the changes matched the requested
preferences.

## 7. Intended Use and Non-Intended Use

This project is intended for classroom learning and small demonstrations.
It is useful for showing how simple scores can create ranked suggestions.
It is also useful because each recommendation has an explanation.

It is not intended for a production music service. It should not be used to
make decisions about people, infer personal traits, or claim that a song is
objectively good. It should not replace real user feedback or larger-scale
recommendation testing.

## 8. Ideas for Improvement

- Add more songs and more balanced genres and moods.
- Let users give several favorite genres, moods, and energy ranges.
- Use listening history, ratings, skips, and diversity rules.

## 9. Personal Reflection

My biggest learning moment was seeing that a few weighted rules can produce
results that feel like real recommendations. The system does not understand
music, but matching genre, mood, and energy still creates a believable order.

AI tools helped me write and explain the scoring logic quickly. I still had
to double-check the score math, the exact terminal output, and the import
behavior when running the program as a module. The evaluation also showed why
small datasets can make simple rules look more confident than they should.

If I continued this project, I would add a larger catalog and let users
adjust the weights themselves. I would also add diversity so the recommender
does not return songs that are all too similar.
