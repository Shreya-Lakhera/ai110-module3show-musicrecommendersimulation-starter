# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender starts with a user's favorite genre, favorite mood, target
energy level, and acoustic preference. It looks at every song in the catalog
and gives it points when its genre matches the favorite genre and when its
mood matches the favorite mood. A genre match is worth 2 points and a mood
match is worth 1 point.

The model also compares the song's energy with the user's target. Songs closer
to the target receive more similarity points, up to 1 point. A song receives
another 0.5 points when its acousticness agrees with the user's acoustic
preference. After all songs are scored, the model sorts them from highest to
lowest and displays the top results in the command-line interface, along with
the reasons for each score. This replaces the starter behavior, which did not
calculate scores or produce ranked recommendations.

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The weight-shift experiment reduced the genre bonus to 1 point and doubled
the energy contribution to a maximum of 2 points. This makes the system more
sensitive to numerical energy differences, so a song in the preferred genre
can lose to a song with a closer energy level. The energy gap still assumes
that a user's taste can be represented by one normalized target, which may
ignore people who enjoy both calm and intense music. Because the catalog has
only ten hand-selected songs, these weights can also amplify the
over-representation of particular energy levels or moods.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

### Weight-Shift Experiment

The original scoring used a 2-point genre match and up to 1 energy point. In
this experiment, genre is worth 1 point and energy similarity is doubled to a
maximum of 2 points. The change kept the same top song for each tested
profile, but it changed the scores and made close-energy songs more
competitive. For example, in the High-Energy Pop profile, Rooftop Lights
moved from 2.36 to 3.22 because its energy similarity increased from 0.86 to
1.72, while the genre match became less important. The result is more
responsive to energy, but not necessarily more accurate: it can recommend a
song with the right energy even when its genre or mood is less suitable.

## 7. Evaluation  

I evaluated four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock,
and a conflicting High-Energy Sad profile. The first three profiles produced
recommendations that generally matched their names. The conflicting profile
was an edge case because the catalog has no song with a `sad` mood, so its
ranking was driven by the rock genre, high-energy target, and non-acoustic
preference instead of a mood match.

The CLI evaluation output before the weight-shift experiment was:

### High-Energy Pop

```text
Sunrise City - Score: 4.42
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.92), acoustic preference match (+0.5)

Gym Hero - Score: 3.47
Because: genre match (+2.0), energy similarity (+0.97), acoustic preference match (+0.5)

Rooftop Lights - Score: 2.36
Because: mood match (+1.0), energy similarity (+0.86), acoustic preference match (+0.5)

Storm Runner - Score: 1.49
Because: energy similarity (+0.99), acoustic preference match (+0.5)

Night Drive Loop - Score: 1.35
Because: energy similarity (+0.85), acoustic preference match (+0.5)
```

### Chill Lofi

```text
Midnight Coding - Score: 4.48
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98), acoustic preference match (+0.5)

Library Rain - Score: 4.45
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.95), acoustic preference match (+0.5)

Focus Flow - Score: 3.50
Because: genre match (+2.0), energy similarity (+1.00), acoustic preference match (+0.5)

Spacewalk Thoughts - Score: 2.38
Because: mood match (+1.0), energy similarity (+0.88), acoustic preference match (+0.5)

Coffee Shop Stories - Score: 1.47
Because: energy similarity (+0.97), acoustic preference match (+0.5)
```

### Deep Intense Rock

```text
Storm Runner - Score: 4.49
Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.99), acoustic preference match (+0.5)

Gym Hero - Score: 2.47
Because: mood match (+1.0), energy similarity (+0.97), acoustic preference match (+0.5)

Sunrise City - Score: 1.42
Because: energy similarity (+0.92), acoustic preference match (+0.5)

Rooftop Lights - Score: 1.36
Because: energy similarity (+0.86), acoustic preference match (+0.5)

Night Drive Loop - Score: 1.35
Because: energy similarity (+0.85), acoustic preference match (+0.5)
```

### Conflicting High-Energy Sad

```text
Storm Runner - Score: 3.49
Because: genre match (+2.0), energy similarity (+0.99), acoustic preference match (+0.5)

Gym Hero - Score: 1.47
Because: energy similarity (+0.97), acoustic preference match (+0.5)

Sunrise City - Score: 1.42
Because: energy similarity (+0.92), acoustic preference match (+0.5)

Rooftop Lights - Score: 1.36
Because: energy similarity (+0.86), acoustic preference match (+0.5)

Night Drive Loop - Score: 1.35
Because: energy similarity (+0.85), acoustic preference match (+0.5)
```

Storm Runner ranked first for the Deep Intense Rock profile because it earned
the full genre match, mood match, and acoustic-preference points while its
energy of `0.91` was nearly identical to the target of `0.90`. For the
conflicting profile, it still ranked first because the missing `sad` mood
match affected every song equally, leaving its rock match and high energy as
the deciding factors. This result felt intuitive for the rock profile, but it
also showed that the small catalog cannot represent every mood preference.

### Pairwise Comparisons

- **High-Energy Pop vs. Chill Lofi:** High-Energy Pop puts Sunrise City and
  Gym Hero at the top because they are pop songs with high energy. Chill Lofi
  instead favors Midnight Coding and Library Rain because they match both the
  lofi genre and chill mood at lower energy levels. This change makes sense
  because the profiles ask for different genres, moods, and energy ranges.
- **High-Energy Pop vs. Deep Intense Rock:** High-Energy Pop ranks Sunrise
  City first because it matches pop and happy, while Deep Intense Rock ranks
  Storm Runner first because it matches rock and intense. Gym Hero still
  appears near the top for both profiles: it is pop and energetic, so it
  matches the Pop profile's genre and energy, and it matches the Rock
  profile's intense mood and energy. The song is a useful reminder that a
  strong match on two features can keep a track competitive even when one
  feature does not match.
- **High-Energy Pop vs. Conflicting High-Energy Sad:** The profiles share a
  high-energy preference but ask for different genres and moods. High-Energy
  Pop rewards Sunrise City for matching pop and happy, while the conflicting
  profile rewards Storm Runner for matching rock; no song receives a sad mood
  point because the catalog contains no sad song. This makes the conflicting
  results less specific than the profile suggests.
- **Chill Lofi vs. Deep Intense Rock:** Chill Lofi favors the two lofi songs
  because they match both genre and mood, while Deep Intense Rock favors Storm
  Runner because it matches rock and intense. The same scoring rules produce
  very different lists because the profiles reverse the desired energy range
  and descriptive tags.
- **Chill Lofi vs. Conflicting High-Energy Sad:** Chill Lofi produces strong
  scores for Midnight Coding and Library Rain because both requested tags are
  present. The conflicting profile has no mood match anywhere, so its list is
  driven mostly by energy and the one rock match. This shows that a profile
  with preferences missing from the catalog cannot express its intended taste
  very well.
- **Deep Intense Rock vs. Conflicting High-Energy Sad:** Both profiles prefer
  rock and high energy, so Storm Runner remains first for both. Deep Intense
  Rock scores it higher because its intense mood also matches; the conflicting
  profile does not have any sad match. This is a useful sanity check: changing
  only the mood should affect the mood bonus without changing the song's other
  evidence.

Gym Hero can keep showing up for someone who wants Happy Pop even though its
mood is intense because the scoring system rewards its pop genre, high energy,
and non-acoustic sound. It does not need to match every preference to rank
well. In this experiment, energy is worth up to two points and genre is worth
one, so a song that feels energetic and belongs to the requested genre can
outscore a quieter song that matches the mood better. This is understandable
for a user who wants upbeat music, but it also shows why the weights should be
adjusted if mood matters more than energy.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
