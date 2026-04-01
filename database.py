# NBA Analytics Dashboard - Database Setup & SQL Queries
# ============================================

import sqlite3

# pandas to read our CSV file
import pandas as pd

# ============================================
# STEP 1 - Load Our CSV Into pandas
# ============================================

print("Loading player stats from CSV...")

# Read the CSV we saved yesterday into a DataFrame
df_players = pd.read_csv('data/player_stats.csv')

print(f"Loaded {len(df_players)} players successfully!")

# ============================================
# STEP 2 - Create a SQLite Database
# ============================================

print("\nCreating database...")

# This creates a database file called nba.db in our data/ folder
# Think of it like creating a new Excel workbook
# If the file already exists, it just connects to it
conn = sqlite3.connect('data/nba.db')

# A cursor is like a pen that writes to the database
# We use it to execute SQL commands
cursor = conn.cursor()

print("Database created!")

# ============================================
# STEP 3 - Load DataFrame Into Database
# ============================================

# This takes our pandas DataFrame and saves it as a 
# table called 'player_stats' inside the database
# if_exists='replace' means if the table already exists,
# overwrite it with fresh data
df_players.to_sql('player_stats', conn, if_exists='replace', index=False)

print("Player stats loaded into database!")

# ============================================
# STEP 4 - Run SQL Queries
# ============================================

print("\n--- TOP 10 SCORERS ---")

# pd.read_sql lets us run a SQL query and get back a DataFrame
# This is exactly how data analysts query databases in real jobs
top_scorers = pd.read_sql("""
    SELECT 
        PLAYER,
        TEAM,
        GP,
        PTS,
        AST,
        REB
    FROM player_stats
    ORDER BY PTS DESC
    LIMIT 10
""", conn)

print(top_scorers)

# ============================================

print("\n--- MOST EFFICIENT PLAYERS (MIN 20 GAMES) ---")

# Here we filter players who have played at least 20 games
# and rank them by a simple efficiency score
efficient_players = pd.read_sql("""
    SELECT 
        PLAYER,
        TEAM,
        GP,
        PTS,
        AST,
        REB,
        (PTS + AST + REB) AS EFFICIENCY
    FROM player_stats
    WHERE GP >= 20
    ORDER BY EFFICIENCY DESC
    LIMIT 10
""", conn)

print(efficient_players)

# ============================================

print("\n--- TEAM SCORING AVERAGES ---")

# Here we GROUP BY team to get average stats per team
# GROUP BY is one of the most important SQL concepts
team_averages = pd.read_sql("""
    SELECT
        TEAM,
        COUNT(PLAYER) AS NUM_PLAYERS,
        ROUND(AVG(PTS), 1) AS AVG_PTS,
        ROUND(AVG(AST), 1) AS AVG_AST,
        ROUND(AVG(REB), 1) AS AVG_REB
    FROM player_stats
    GROUP BY TEAM
    ORDER BY AVG_PTS DESC
""", conn)

print(team_averages)

# ============================================
# STEP 5 - Save Queries to queries.sql
# ============================================

# We save our SQL queries to queries.sql so recruiters
# can see your SQL skills clearly on GitHub
sql_content = """
-- NBA Analytics Dashboard
-- SQL Queries

-- Top 10 Scorers
SELECT PLAYER, TEAM, GP, PTS, AST, REB
FROM player_stats
ORDER BY PTS DESC
LIMIT 10;

-- Most Efficient Players (Min 20 Games)
SELECT 
    PLAYER, TEAM, GP, PTS, AST, REB,
    (PTS + AST + REB) AS EFFICIENCY
FROM player_stats
WHERE GP >= 20
ORDER BY EFFICIENCY DESC
LIMIT 10;

-- Team Scoring Averages
SELECT
    TEAM,
    COUNT(PLAYER) AS NUM_PLAYERS,
    ROUND(AVG(PTS), 1) AS AVG_PTS,
    ROUND(AVG(AST), 1) AS AVG_AST,
    ROUND(AVG(REB), 1) AS AVG_REB
FROM player_stats
GROUP BY TEAM
ORDER BY AVG_PTS DESC;
"""

with open('queries.sql', 'w') as f:
    f.write(sql_content)

print("\nSQL queries saved to queries.sql!")

# ============================================
# STEP 6 - Close the Connection
# ============================================

# Always close your database connection when done
# Like closing a file after you're done reading it
conn.close()

print("\nAll done! Database is ready.")