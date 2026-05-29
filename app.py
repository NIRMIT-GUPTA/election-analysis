"""
Streamlit Dashboard for TN 2026 Assembly Election Analysis
Interactive dashboard supporting the AtliQ Media data storytelling project
Author: Data Analyst
Date: 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TN 2026 Election Analysis",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLING ====================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    """Load election data with caching"""
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / 'data'
    data_dir.mkdir(exist_ok=True)    
    try:
        results_2021 = pd.read_csv(data_dir / 'tn_2021_results.csv')
        results_2026 = pd.read_csv(data_dir / 'tn_2026_results.csv')
        constituency = pd.read_csv(data_dir / 'constituency_master.csv')
        return results_2021, results_2026, constituency
    except FileNotFoundError:
        st.error("Data files not found. Please run tn_election_analysis.py first.")
        st.stop()

# ==================== ANALYSIS FUNCTIONS ====================
def get_winners(results_df):
    """Get winning candidates per constituency"""
    return results_df.loc[results_df.groupby('ac_number')['votes'].idxmax()]

def analyze_vote_share(results_2021, results_2026):
    """Analyze vote share changes between elections"""
    state_votes_2021 = results_2021.groupby('party')['votes'].sum()
    state_votes_2026 = results_2026.groupby('party')['votes'].sum()
    
    state_share_2021 = (state_votes_2021 / state_votes_2021.sum() * 100).round(2)
    state_share_2026 = (state_votes_2026 / state_votes_2026.sum() * 100).round(2)
    
    vote_share_comp = pd.DataFrame({
        '2021 (%)': state_share_2021,
        '2026 (%)': state_share_2026.reindex(state_share_2021.index, fill_value=0),
        'Change (pp)': state_share_2026.reindex(state_share_2021.index, fill_value=0) - state_share_2021
    }).round(2).sort_values('2026 (%)', ascending=False)
    vote_share_comp = vote_share_comp.loc[~((vote_share_comp['2021 (%)'] == 0) & (vote_share_comp['2026 (%)'] == 0))]
    
    return vote_share_comp

def analyze_regional_seats(results_2021, results_2026):
    """Analyze seat distribution by region"""
    winners_2021 = get_winners(results_2021)
    winners_2026 = get_winners(results_2026)
    
    seats_2021 = winners_2021[winners_2021['party'].isin(['DMK','AIADMK', 'TVK'])].groupby(['region', 'party']).size().unstack(fill_value=0)
    seats_2026 = winners_2026[winners_2026['party'].isin(['DMK','AIADMK', 'TVK'])].groupby(['region', 'party']).size().unstack(fill_value=0)    
    return seats_2021, seats_2026

def analyze_margins(results_df):
    """Analyze victory margins"""
    margins_data = []
    for ac in results_df['ac_number'].unique():
        const_data = results_df[results_df['ac_number'] == ac].nlargest(2, 'votes')
        if len(const_data) >= 2:
            winner = const_data.iloc[0]
            runner_up = const_data.iloc[1]
            total_votes = results_df[results_df['ac_number'] == ac]['votes'].sum()
            
            margin = winner['votes'] - runner_up['votes']
            winner_share = (winner['votes'] / total_votes * 100) if total_votes > 0 else 0
            
            margins_data.append({
                'ac_number': ac,
                'margin': margin,
                'winner_share': winner_share,
                'winner_party': winner['party'],
                'region': winner.get('region', 'Unknown'),
                'reserved': winner.get('reserved', 'Unknown')
            })
    
    return pd.DataFrame(margins_data)

# ==================== PAGE LAYOUT ====================
# Sidebar Navigation
st.sidebar.markdown("# 🗳️ TN 2026 Election Dashboard")
page = st.sidebar.radio(
    "Navigate to:",
    ["📊 Overview", "🎯 Vote Share Story", "🗺️ Geographic Story", "📈 Margin Story", "📋 Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About This Analysis
- **Data Source:** Election Commission of India
- **Elections Analyzed:** 2021 vs 2026
- **Focus:** Fact-based storytelling for AtliQ Media
- **Research Questions:** 3 connected stories about TN's political transformation
""")

# ==================== PAGE: OVERVIEW ====================
if page == "📊 Overview":
    st.markdown('<h1 class="main-header">2026: The TVK Disruption</h1>', unsafe_allow_html=True)
    st.markdown("### Tamil Nadu Assembly Election Analysis for AtliQ Media")
    
    results_2021, results_2026, constituency = load_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Constituencies", "234", help="234 assembly seats in Tamil Nadu")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        winners_2026 = get_winners(results_2026)
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Number of Parties", len(winners_2026['party'].unique()), help="Unique parties that won seats")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Average Turnout 2026", "85.1%", help="State record turnout")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("""
    ### The Story: Political Disruption
    
    **2026 was not about who won, but who emerged.**
    
    Tamil Nadu's political landscape transformed. A completely new entrant disrupted the traditional two-party contest. 
    Regional patterns shifted. Victory margins changed. Mandates became clearer.
    
    This dashboard explores three connected research questions that reveal the transformation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 3 Research Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **RQ1: The Vote Share Story**
        Where did TVK come from ? 
        Compare party vote share state-wide and by region in 2021 vs 2026. 
        Did TVK pull from DMK, AIADMK, both, or from previously non-voting populations?
        """)
    
    with col2:
        st.markdown("""
        **RQ2: The Geographic Story**
        How did the seat distribution shift across Tamil Nadu's six regions 
        (Chennai Metro, North, Central, Kongu, Delta, South) between 2021 and 2026? 
        Where did each major formation gain or lose ground?
        """)
    
    with col3:
        st.markdown("""
        **RQ3: The Margin Story**
        Strength of Mandates How did the average margin of victory change between 2021 and 2026? 
        In how many constituencies did the winning candidate secure more than 50 percent of the valid votes polled? 
        In how many did the winning candidate receive less than 35 percent of the valid votes polled?
        """)

# ==================== PAGE: VOTE SHARE ====================
elif page == "🎯 Vote Share Story":
    st.markdown('<h1 class="main-header">Where Did TVK Come From?</h1>', unsafe_allow_html=True)
    st.markdown("### Vote Share Shift Analysis")
    
    results_2021, results_2026, _ = load_data()
    vote_share_comp = analyze_vote_share(results_2021, results_2026)
    #vote_share_comp = vote_share_comp.loc[~((vote_share_comp['2021 (%)'] == 0) & (vote_share_comp['2026 (%)'] == 0))]

    # Display table
    st.dataframe(vote_share_comp, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        parties = vote_share_comp.index
        x = np.arange(len(parties))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, vote_share_comp['2021 (%)'], width, label='2021', alpha=0.8, color='#1f77b4')
        bars2 = ax.bar(x + width/2, vote_share_comp['2026 (%)'], width, label='2026', alpha=0.8, color='#ff7f0e')
        
        ax.set_xlabel('Party', fontsize=12, fontweight='bold')
        ax.set_ylabel('Vote Share (%)', fontsize=12, fontweight='bold')
        ax.set_title("Vote Share Shift: TVK's Disruption", fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(parties, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("""
        ### Key Insights
        
        **TVK's Emergence**
        - 34.92% vote share (did not exist in 2021)
        - Pulled from both DMK and AIADMK majorly 
        
        **Traditional Parties**
        - Combined lost 25.59%
        - Fragmentation of vote
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed stats
    st.markdown("---")
    st.markdown("### Detailed Analysis")
    
    tvk_share_2026 = vote_share_comp.loc['TVK', '2026 (%)'] if 'TVK' in vote_share_comp.index else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TVK Vote Share 2026", "34.92%", "New entrant")
    with col2:
        traditional_loss = vote_share_comp.loc[['DMK', 'AIADMK'], 'Change (pp)'].sum()
        st.metric("Traditional Parties Loss", f"{traditional_loss:.2f}pp", "Combined shift")
    with col3:
        st.metric("Year Emerged", "2026", "First election")

# ==================== PAGE: GEOGRAPHIC ====================
elif page == "🗺️ Geographic Story":
    st.markdown('<h1 class="main-header">Which Regions Shifted?</h1>', unsafe_allow_html=True)
    st.markdown("### Regional Seat Distribution Analysis")
    
    results_2021, results_2026, _ = load_data()
    seats_2021, seats_2026 = analyze_regional_seats(results_2021, results_2026)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 2021 Regional Distribution")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        seats_2021.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Seats by Region - 2021 Major Formations', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Seats')
        ax1.set_xlabel('Region')
        ax1.legend(title='Party', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax1.grid(axis='y', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col2:
        st.markdown("#### 2026 Regional Distribution")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        seats_2026.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('Seats by Region - 2026 Major Formations', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Seats')
        ax2.set_xlabel('Region')
        ax2.legend(title='Party', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax2.grid(axis='y', alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig2)
    
    st.markdown("---")
    st.markdown("### TVK's Regional Presence (2026)")
    
    # TVK vote share by region
    votes_by_region_2026 = results_2026.groupby(['region', 'party'])['votes'].sum().unstack(fill_value=0)
    regional_share_2026 = votes_by_region_2026.div(votes_by_region_2026.sum(axis=1), axis=0) * 100
    
    if 'TVK' in regional_share_2026.columns:
        tvk_regional = regional_share_2026[['TVK']].round(2)
        st.dataframe(tvk_regional, use_container_width=True)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        tvk_regional.plot(kind='barh', ax=ax, color='#ff7f0e', legend=False)
        ax.set_xlabel('Vote Share (%)', fontweight='bold')
        ax.set_ylabel('Region', fontweight='bold')
        ax.set_title('TVK Vote Share by Region (2026)', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

# ==================== PAGE: MARGIN STORY ====================
elif page == "📈 Margin Story":
    st.markdown('<h1 class="main-header">Strength of Mandates</h1>', unsafe_allow_html=True)
    st.markdown("### Victory Margin Analysis")
    
    results_2021, results_2026, _ = load_data()
    margins_2021 = analyze_margins(results_2021)
    margins_2026 = analyze_margins(results_2026)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Margin 2021", f"{margins_2021['margin'].mean()/1000:.1f}K", "votes")
    with col2:
        st.metric("Avg Margin 2026", f"{margins_2026['margin'].mean()/1000:.1f}K", "votes")
    with col3:
        change = margins_2026['margin'].mean() - margins_2021['margin'].mean()
        st.metric("Change", f"{change/1000:+.1f}K", "Mandates " + ("Stronger ↑" if change > 0 else "Weaker ↓"))
    with col4:
        st.metric("Constituencies", len(margins_2026), "analyzed")
    
    st.markdown("---")
    
    # Distribution visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Victory Margin Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(margins_2021['margin']/1000, bins=20, alpha=0.6, label='2021', color='#1f77b4')
        ax.hist(margins_2026['margin']/1000, bins=20, alpha=0.6, label='2026', color='#ff7f0e')
        ax.axvline(margins_2021['margin'].mean()/1000, color='#1f77b4', linestyle='--', linewidth=2, 
                   label=f'2021 Avg: {margins_2021["margin"].mean()/1000:.1f}K')
        ax.axvline(margins_2026['margin'].mean()/1000, color='#ff7f0e', linestyle='--', linewidth=2,
                   label=f'2026 Avg: {margins_2026["margin"].mean()/1000:.1f}K')
        ax.set_xlabel('Victory Margin (Thousands of Votes)', fontweight='bold')
        ax.set_ylabel('Number of Constituencies', fontweight='bold')
        ax.set_title('Victory Margins: Are Mandates Changing?', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("#### Mandate Strength Categories")
        
        categories_2021 = margins_2021['winner_share'].apply(lambda x: '<35%' if x < 35 else ('50%+' if x >= 50 else ('35-50%' if x >= 35 else np.nan)))
        categories_2026 = margins_2026['winner_share'].apply(lambda x: '<35%' if x < 35 else ('50%+' if x >= 50 else ('35-50%' if x >= 35 else np.nan)))
        cat_2021 = categories_2021.value_counts().sort_index()
        cat_2026 = categories_2026.value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(cat_2021.index))
        width = 0.35
        ax.bar(x - width/2, cat_2021, width, label='2021', alpha=0.8, color='#1f77b4')
        ax.bar(x + width/2, cat_2026, width, label='2026', alpha=0.8, color='#ff7f0e')
        ax.set_xlabel('Winner Vote Share Range', fontweight='bold')
        ax.set_ylabel('Number of Constituencies', fontweight='bold')
        ax.set_title('How Strong Were Winners?', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(cat_2021.index)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("### Insight")
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    
    winners_50_2021 = len(margins_2021[margins_2021['winner_share'] >= 50])
    winners_50_2026 = len(margins_2026[margins_2026['winner_share'] >= 50])
    winners_35_2021 = len(margins_2021[margins_2021['winner_share'] < 35])
    winners_35_2026 = len(margins_2026[margins_2026['winner_share'] < 35])
    winners_35_50_2021 = len(margins_2021[(margins_2021['winner_share'] >= 35) & (margins_2021['winner_share'] < 50)])
    winners_35_50_2026 = len(margins_2026[(margins_2026['winner_share'] >= 35) & (margins_2026['winner_share'] < 50)])
    
    st.markdown(f"""
    **Winners with 50%+ vote share:**
    - 2021: {winners_50_2021} ({winners_50_2021/len(margins_2021)*100:.1f}%)
    - 2026: {winners_50_2026} ({winners_50_2026/len(margins_2026)*100:.1f}%)

    **Winners with 35-50% vote share:**
    - 2021: {winners_35_50_2021} ({winners_35_50_2021/len(margins_2021)*100:.1f}%)
    - 2026: {winners_35_50_2026} ({winners_35_50_2026/len(margins_2026)*100:.1f}%)
    
    **Winners with <35% vote share (weakest mandates):**
    - 2021: {winners_35_2021} ({winners_35_2021/len(margins_2021)*100:.1f}%)
    - 2026: {winners_35_2026} ({winners_35_2026/len(margins_2026)*100:.1f}%)
    
    → **Interpretation:** {("Mandates got STRONGER (larger margins, clearer verdicts)" if margins_2026['margin'].mean() > margins_2021['margin'].mean() else "Mandates got WEAKER (smaller margins, more competition)")}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE: DATA EXPLORER ====================
elif page == "📋 Data Explorer":
    st.markdown('<h1 class="main-header">Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Explore the Raw Data")
    
    results_2021, results_2026, constituency = load_data()
    
    st.markdown("#### Choose Year and Data")
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.radio("Select Year:", [2021, 2026])
    
    with col2:
        data_type = st.radio("Select Data:", ["Full Results", "Winners Only", "By Constituency"])
    
    if year == 2021:
        data = results_2021.copy()
    else:
        data = results_2026.copy()
    
    if data_type == "Winners Only":
        data = get_winners(data)
    elif data_type == "By Constituency":
        selected_const = st.selectbox("Select Constituency:", data['constituency'].unique())
        data = data[data['constituency'] == selected_const].sort_values('votes', ascending=False)
    
    # Display
    st.dataframe(data.sort_values('votes', ascending=False), use_container_width=True, height=400)
    
    # Download button
    csv = data.to_csv(index=False)
    st.download_button(
        label=f"Download {year} Data",
        data=csv,
        file_name=f"tn_{year}_results.csv",
        mime="text/csv"
    )

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
    <p><b>Data Source:</b> Election Commission of India</p>
    <p><b>Analysis Period:</b> 2021 vs 2026 Tamil Nadu Assembly Elections</p>
    <p><b>Purpose:</b> Fact-based storytelling for AtliQ Media</p>
    <p>Built for the Codebasics Resume Project Challenge</p>
</div>
""", unsafe_allow_html=True)
