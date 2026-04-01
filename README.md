# 🏀 NBA Analytics Dashboard

A real-time NBA analytics dashboard built with Python, SQL, and Streamlit.
Live data is pulled directly from the NBA Stats API and visualized
through interactive charts and filters.

## 🔗 Live Demo
👉 [https://nba-analytics-dashboard-zaydh.streamlit.app/]
## 📊 Features

- **Top 10 Players** — Switchable between Points, Assists, Rebounds, Steals and Blocks
- **Team Star Players** — Each team's highest scoring player visualized
- **Player Efficiency Map** — Scatter plot comparing points, assists and rebounds
- **Live Filters** — Filter by team and minimum games played
- **Player Search** — Search any player by name in the full stats table
- **KPI Cards** — Top scorer, assists leader and rebound leader at a glance

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| nba_api | Pulls live data from NBA Stats API |
| Pandas | Data cleaning and transformation |
| SQLite | Local database storage |
| SQL | Data querying and aggregation |
| Plotly | Interactive chart visualizations |
| Streamlit | Web app framework |

## 📁 Project Structure
```
nba-analytics-dashboard/
├── data/               # Raw data and SQLite database
├── notebooks/          # Exploratory analysis
├── app.py              # Main Streamlit dashboard
├── database.py         # Database setup and SQL queries
├── charts.py           # Chart building scripts
├── queries.sql         # SQL queries reference
└── README.md           # Project documentation
```

## 🚀 Run Locally

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/nba-analytics-dashboard.git
cd nba-analytics-dashboard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Pull fresh NBA data
```bash
python app.py
python database.py
```

4. Launch the dashboard
```bash
streamlit run app.py
```

## 💡 Key Skills Demonstrated

- End-to-end data pipeline from API to visualization
- SQL database design and querying including subqueries and GROUP BY
- Interactive dashboard development
- Real-world data cleaning and transformation
- Professional project structure and documentation

## 👨‍💻 Built By

**Zayd Hannan** — ITI Student @ Rutgers University  
[GitHub](ZaydH23)
