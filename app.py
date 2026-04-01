# ============================================
# NBA Analytics Dashboard
# Day 6 - Polished Dashboard
# ============================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# STEP 1 - PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="NBA Analytics Dashboard",
    page_icon="🏀",
    layout="wide"
)

# ============================================
# STEP 2 - CUSTOM CSS STYLING
# ============================================

# st.markdown with unsafe_allow_html lets us inject
# real CSS into the dashboard to style it our way
# This is how you go from "default" to "professional"
st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Metric cards styling */
    [data-testid="stMetric"] {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 15px;
    }

    /* Metric label color */
    [data-testid="stMetricLabel"] {
        color: #a0aec0 !important;
        font-size: 14px !important;
    }

    /* Metric value color */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1f2e;
        border-right: 1px solid #2d3748;
    }

    /* Chart container styling */
    [data-testid="stPlotlyChart"] {
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 10px;
        background-color: #1a1f2e;
    }

    /* Header styling */
    h1 {
        color: #ffffff !important;
        font-size: 36px !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #e2e8f0 !important;
    }

    /* Divider color */
    hr {
        border-color: #2d3748;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# STEP 3 - CONNECT TO DATABASE
# ============================================

@st.cache_resource
def get_connection():
    return sqlite3.connect('data/nba.db', check_same_thread=False)

conn = get_connection()

# ============================================
# STEP 4 - LOAD DATA
# ============================================

@st.cache_data
def load_data():
    df = pd.read_sql("""
        SELECT PLAYER, TEAM, GP, PTS, AST, REB, STL, BLK,
        ROUND(PTS + AST + REB, 1) AS EFFICIENCY
        FROM player_stats
    """, get_connection())
    return df

df = load_data()

# ============================================
# STEP 5 - SIDEBAR
# ============================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/0/03/National_Basketball_Association_logo.svg/200px-National_Basketball_Association_logo.svg.png",
    width=100
)

st.sidebar.title("🏀 NBA Dashboard")
st.sidebar.markdown("**2025/26 Season**")
st.sidebar.markdown("---")

# Navigation section
st.sidebar.markdown("### 📊 Filters")

all_teams = sorted(df['TEAM'].unique())

selected_teams = st.sidebar.multiselect(
    "Filter by Team",
    options=all_teams,
    default=all_teams
)

min_games = st.sidebar.slider(
    "Minimum Games Played",
    min_value=1,
    max_value=int(df['GP'].max()),
    value=10
)

st.sidebar.markdown("---")

# Stat selector - lets user pick which stat to focus on
stat_focus = st.sidebar.selectbox(
    "📈 Focus Stat for Top 10 Chart",
    options={
        'PTS': 'Points Per Game',
        'AST': 'Assists Per Game',
        'REB': 'Rebounds Per Game',
        'STL': 'Steals Per Game',
        'BLK': 'Blocks Per Game'
    }.keys(),
    format_func=lambda x: {
        'PTS': 'Points Per Game',
        'AST': 'Assists Per Game',
        'REB': 'Rebounds Per Game',
        'STL': 'Steals Per Game',
        'BLK': 'Blocks Per Game'
    }[x]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 About")
st.sidebar.markdown("""
Built by **Zayd Hannan**  
ITI Student @ Rutgers University  

**Tools Used:**
- Python & Pandas
- SQLite & SQL
- Plotly & Streamlit
- NBA Stats API
""")

# ============================================
# STEP 6 - FILTER DATA
# ============================================

filtered_df = df[
    (df['TEAM'].isin(selected_teams)) &
    (df['GP'] >= min_games)
]

# ============================================
# STEP 7 - DASHBOARD HEADER
# ============================================

# Two columns for header - title on left, description on right
header_left, header_right = st.columns([2, 1])

with header_left:
    st.title("🏀 NBA Analytics Dashboard")
    st.markdown("Real-time player and team statistics for the **2025/26 NBA Season**")

with header_right:
    st.markdown("###")
    st.info("💡 Use the sidebar filters to explore different teams and stats")

st.markdown("---")

# ============================================
# STEP 8 - METRIC CARDS
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏀 Total Players",
        value=len(filtered_df)
    )

with col2:
    top_scorer = filtered_df.loc[filtered_df['PTS'].idxmax(), 'PLAYER']
    top_pts = filtered_df['PTS'].max()
    st.metric(
        label="👑 Top Scorer",
        value=top_scorer,
        delta=f"{top_pts} PPG"
    )

with col3:
    top_assist = filtered_df.loc[filtered_df['AST'].idxmax(), 'PLAYER']
    top_ast = filtered_df['AST'].max()
    st.metric(
        label="🎯 Top Assists",
        value=top_assist,
        delta=f"{top_ast} APG"
    )

with col4:
    top_rebounder = filtered_df.loc[filtered_df['REB'].idxmax(), 'PLAYER']
    top_reb = filtered_df['REB'].max()
    st.metric(
        label="💪 Top Rebounder",
        value=top_rebounder,
        delta=f"{top_reb} RPG"
    )

st.markdown("---")

# ============================================
# STEP 9 - CHARTS ROW 1
# ============================================

col_left, col_right = st.columns(2)

with col_left:
    # Dynamic title based on stat selected in sidebar
    stat_labels = {
        'PTS': 'Points', 'AST': 'Assists',
        'REB': 'Rebounds', 'STL': 'Steals', 'BLK': 'Blocks'
    }
    st.subheader(f"🏆 Top 10 Players by {stat_labels[stat_focus]}")
    st.caption("Use the sidebar to switch between different stats")

    top_10 = filtered_df.nlargest(10, stat_focus)

    fig1 = px.bar(
        top_10,
        x='PLAYER',
        y=stat_focus,
        color='TEAM',
        labels={
            stat_focus: f"{stat_labels[stat_focus]} Per Game",
            'PLAYER': 'Player'
        },
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig1.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("⭐ Each Team's Best Scorer")
    st.caption("The highest scoring player on each team")

    star_players = filtered_df.loc[
        filtered_df.groupby('TEAM')['PTS'].idxmax()
    ].sort_values('PTS', ascending=False)

    fig3 = px.bar(
        star_players,
        x='TEAM',
        y='PTS',
        color='PTS',
        labels={'PTS': 'Points Per Game', 'TEAM': 'Team'},
        template='plotly_dark',
        text='PLAYER',
        color_continuous_scale='Blues'
    )
    fig3.update_traces(
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Player: %{text}<br>Points: %{y}<extra></extra>"
    )
    fig3.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        margin=dict(t=20)
    )
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# STEP 10 - SCATTER PLOT
# ============================================

st.markdown("---")
st.subheader("🔵 Player Efficiency Map")
st.caption("Each bubble is a player. Bigger bubble = more rebounds. Brighter color = higher efficiency score.")

fig2 = px.scatter(
    filtered_df,
    x='PTS',
    y='AST',
    size='REB',
    color='EFFICIENCY',
    hover_name='PLAYER',
    hover_data={'TEAM': True, 'GP': True, 'REB': True},
    labels={
        'PTS': 'Points Per Game',
        'AST': 'Assists Per Game',
        'EFFICIENCY': 'Efficiency Score',
        'GP': 'Games Played',
        'REB': 'Rebounds'
    },
    template='plotly_dark',
    color_continuous_scale='Viridis'
)
fig2.update_layout(
    height=550,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# STEP 11 - PLAYER STATS TABLE
# ============================================

st.markdown("---")
st.subheader("📋 Full Player Stats Table")
st.caption("Search for any player or browse all stats")

search = st.text_input("🔍 Search player by name")

if search:
    table_df = filtered_df[
        filtered_df['PLAYER'].str.contains(search, case=False)
    ]
else:
    table_df = filtered_df

st.dataframe(
    table_df.sort_values('PTS', ascending=False).head(50)[[
        'PLAYER', 'TEAM', 'GP', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'EFFICIENCY'
    ]],
    use_container_width=True,
    hide_index=True
)

# ============================================
# STEP 12 - FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 20px;'>
    🏀 NBA Analytics Dashboard • Built with Python, Streamlit & Plotly • Data from NBA Stats API
</div>
""", unsafe_allow_html=True)
