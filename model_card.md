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

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**Process Flow**

```mermaid
flowchart TD
	A[User Preferences (profile)] --> B[Load songs.csv]
	B --> C{For each song}
	C --> D[Parse song attributes]
	D --> E[Compute genre_score (+2.0 if match)]
	D --> F[Compute mood_score (+1.0 if match)]
	D --> G[Compute energy_score (up to +2.0, decays with distance)]
	D --> H[Compute acoustic_score (+1.0 or 1-acousticness)]
	D --> I[Compute tempo_score (up to +0.5)]
	D --> J[Compute valence_score (up to +0.5)]
	D --> K[Compute dance_score (up to +0.3)]
	E --> L[Sum weighted scores -> raw_score]
	F --> L
	G --> L
	H --> L
	I --> L
	J --> L
	K --> L
	L --> M[Normalize score -> final_score; build explanation]
	M --> N[Add (song, final_score, explanation) to scored_list]
	N --> C
	N --> O[After all songs]
	O --> P[Sort scored_list by final_score desc]
	P --> Q[Apply tie-breakers (popularity, diversity penalties)]
	Q --> R[Select Top K]
	R --> S[Output: Ranked recommendations (+ explanations)]
```

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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

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
