# Movie4U

🎬 Movie4U – Personalized Movie Recommendation System
Movie4U is a full-stack web application that provides smart, personalized movie recommendations using user-based collaborative filtering. Built with machine learning and deployed on Heroku, the platform delivers accurate suggestions based on user behavior and interaction.

🔍 Overview
Movie4U analyzes users' past movie ratings to find similar users and recommend films accordingly. By comparing rating patterns, it uses collaborative filtering to generate relevant suggestions tailored to each user. The algorithm dynamically updates recommendations with every new rating to ensure freshness and accuracy.

🌟 Key Features
✅ Personalized Recommendations: Based on user similarity and past ratings

🔁 Real-time Updates: ML model refreshes with every user interaction

🔐 User Authentication: Login required; recommendations activate after rating at least one movie

🎞️ Movie Search: Search any movie by title

☁️ Deployed on Heroku: Accessible online

📊 Data-Driven: SQL-backed data storage and efficient querying

🛠️ Tech Stack
| Area           | Technologies                |
| -------------- | --------------------------- |
| **Backend**    | Python, Flask               |
| **Frontend**   | HTML, CSS (Jinja templates) |
| **Database**   | PostgreSQL, SQLite          |
| **ML & Data**  | pandas, scikit-learn        |
| **Deployment** | Heroku                      |

🤖 How It Works
User logs in and rates at least one movie

The system computes similarity between users based on rating patterns

The collaborative filtering algorithm finds similar users

Recommended movies are displayed based on those similar users’ preferences

🧠 ML & Data Science
Collaborative Filtering via user similarity

Cosine Similarity calculated with scikit-learn

Data Preprocessing handled with pandas

Models updated dynamically with every interaction
