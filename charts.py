# NBA Analytics Dashboard - Building Charts with Plotly
# ============================================

import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# STEP 1 - Connect to Our Database
# ============================================

# We connect to the same database we built yesterday
# This is the power of a database - any script can access it
conn = sqlite3.connect('data/nba.db')

# ============================================
# STEP 2 - Pull Data for Our Charts
# ============================================

# Top 10 scorers for our bar chart
top_scorers = pd.read_sql("""
    SELECT PLAYER, TEAM, PTS, AST, REB
    FROM player_stats
    ORDER BY PTS DESC
    LIMIT 10
""", conn)

# All players with 20+ games for our scatter plot
all_players = pd.read_sql("""
    SELECT PLAYER, TEAM, PTS, AST, REB, GP,
    (PTS + AST + REB) AS EFFICIENCY
    FROM player_stats
    WHERE GP >= 20
""", conn)

# Team averages for our team chart
# Each team's best scorer
star_players = pd.read_sql("""
    SELECT 
        p.TEAM,
        p.PLAYER,
        p.PTS,
        p.AST,
        p.REB
    FROM player_stats p
    INNER JOIN (
        SELECT TEAM, MAX(PTS) AS MAX_PTS
        FROM player_stats
        GROUP BY TEAM
    ) AS best
    ON p.TEAM = best.TEAM 
    AND p.PTS = best.MAX_PTS
    ORDER BY p.PTS DESC
""", conn)

# ============================================
# STEP 3 - Chart 1: Top 10 Scorers Bar Chart
# ============================================

print("Building Chart 1 - Top 10 Scorers...")

# px.bar creates a bar chart
# x = what goes on the horizontal axis
# y = what goes on the vertical axis
# color = what determines the bar color
# title = chart title
fig1 = px.bar(
    top_scorers,
    x='PLAYER',
    y='PTS',
    color='TEAM',
    title='🏀 Top 10 NBA Scorers - 2025/26 Season',
    labels={'PTS': 'Points Per Game', 'PLAYER': 'Player'},
    template='plotly_dark'  # Dark theme looks sleek
)

# This adds hover text so when you mouse over a bar
# you see the player's full stats
fig1.update_traces(
    hovertemplate="<b>%{x}</b><br>Points: %{y}<extra></extra>"
)

fig1.update_layout(
    xaxis_tickangle=-45,  # Angle the player names so they dont overlap
    showlegend=True
)

# Save the chart as an HTML file
# HTML means it stays interactive - not a flat image
fig1.write_html('data/chart_top_scorers.html')
print("Chart 1 saved!")

# ============================================
# STEP 4 - Chart 2: Points vs Assists Scatter Plot
# ============================================

print("Building Chart 2 - Points vs Assists...")

# A scatter plot shows the relationship between two stats
# Each dot = one player
# x axis = points, y axis = assists
# size of dot = rebounds (bigger dot = more rebounds)
fig2 = px.scatter(
    all_players,
    x='PTS',
    y='AST',
    size='REB',             # Dot size based on rebounds
    color='EFFICIENCY',     # Dot color based on efficiency
    hover_name='PLAYER',    # Show player name on hover
    title='🏀 Points vs Assists (Bubble size = Rebounds)',
    labels={
        'PTS': 'Total Points ',
        'AST': 'Total Assists ',
        'EFFICIENCY': 'Efficiency Score '
    },
    template='plotly_dark',
    color_continuous_scale='Viridis'  # Color gradient
)

fig2.write_html('data/chart_scatter.html')
print("Chart 2 saved!")

# ============================================
# STEP 5 - Chart 3: Team Scoring Averages
# ============================================

print("Building Chart 3 - Each Team's Best Scorer...")

fig3 = px.bar(
    star_players,
    x='TEAM',
    y='PTS',
    color='PLAYER',
    title="🏀 Each Team's Best Scorer - 2025/26 Season",
    labels={
        'PTS': 'Points Per Game',
        'TEAM': 'Team',
        'PLAYER': 'Star Player'
    },
    template='plotly_dark',
    text='PLAYER'
)

fig3.update_traces(
    textposition='inside',
    hovertemplate="<b>%{x}</b><br>Player: %{text}<br>Points: %{y}<extra></extra>"
)

fig3.update_layout(
    xaxis_tickangle=-45,
    showlegend=False,
)

fig3.write_html('data/chart_team_averages.html')
print("Chart 3 saved!")

# ============================================
# STEP 6 - Close Database Connection
# ============================================

conn.close()

print("\nAll 3 charts built and saved to data/ folder!")
print("Open the .html files in your browser to see them!")