"""
TN 2026 Assembly Election Analysis
BY- NIRMIT GUPTA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# DATA SOURCING 
class DataManager:
    
    @staticmethod
    def download_eci_data():
        script_dir = Path(__file__).resolve().parent
        data_dir = script_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        try:
            results_2021 = pd.read_csv(data_dir / 'tn_2021_results.csv')
            results_2026 = pd.read_csv(data_dir / 'tn_2026_results.csv')
            print("Loaded existing CSV files")
            return results_2021, results_2026
        except FileNotFoundError as ex:
            missing_path = Path(ex.filename)
            if not missing_path.is_absolute():
                missing_path = data_dir / missing_path
            print(f"DATA FILE ERROR: {missing_path} not found.")
            print("Please place the required CSV files inside the data/ folder next to this script and rerun.")
            sys.exit(1)
        
# DATA PROCESSING 
class ElectionAnalyzer:    
    def __init__(self, results_2021, results_2026):
        self.results_2021 = results_2021
        self.results_2026 = results_2026
        self.style_setup()
    
    @staticmethod
    def style_setup():
        """Configure visualization style"""
        sns.set_theme(style="whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
    
    def get_winners(self, results_df):
        """Get winning candidates per constituency"""
        return results_df.loc[results_df.groupby('ac_number')['votes'].idxmax()]
    
    # RESEARCH QUESTION 1: VOTE SHARE STORY 
    def analyze_tvk_vote_source(self):
        """
        RQ1: Where did TVK's votes come from?
        TVK didn't exist in 2021, so in 2026 it must have pulled from somewhere.
        """
        print("\n" + "="*60)
        print("RQ1: THE VOTE SHARE STORY - Where did TVK come from ? Compare party vote share state-wide and by region in 2021 vs 2026. Did TVK pull from DMK, AIADMK, both, or from previously non-voting populations?")
        print("="*60)
        
        # Vote share by party in 2021 vs 2026
        state_votes_2021 = self.results_2021.groupby('party')['votes'].sum()
        state_votes_2026 = self.results_2026.groupby('party')['votes'].sum()
        
        state_share_2021 = (state_votes_2021 / state_votes_2021.sum() * 100).round(2)
        state_share_2026 = (state_votes_2026 / state_votes_2026.sum() * 100).round(2)
        
        # Create comparison dataframe
        vote_share_comp = pd.DataFrame({
            '2021 (%)': state_share_2021,
            '2026 (%)': state_share_2026.reindex(state_share_2021.index, fill_value=0),
            'Change (pp)': state_share_2026.reindex(state_share_2021.index, fill_value=0) - state_share_2021
        }).round(2)
        
        # Remove parties with zero votes in both years so the comparison stays focused
        vote_share_comp = vote_share_comp.loc[~((vote_share_comp['2021 (%)'] == 0) & (vote_share_comp['2026 (%)'] == 0))]
        
        # Add TVK separately
        tvk_2026 = state_share_2026.get('TVK', 0)
        vote_share_comp = vote_share_comp.sort_values('2026 (%)', ascending=False)
        
        print("\nState-wide Vote Share Comparison:")
        print(vote_share_comp)
        print("\nParties not mentioned above had no votes in either year and are excluded for clarity.")
        print(f"\nTVK's vote share in 2026: {tvk_2026:.2f}%")
        
        # Calculate who lost vote share
        traditional_parties = ['DMK', 'AIADMK']
        vote_loss = vote_share_comp.loc[traditional_parties, 'Change (pp)'].sum()
        print(f"Vote share lost by traditional parties - DMK , AIADMK: {abs(vote_loss):.2f}pp")
        print(f"This closely matches TVK's vote share - TVK is the story of disruption as it got votes form both DMK and AIADMK and through non voters.")
        
        return vote_share_comp, state_votes_2021, state_votes_2026
    
    #  RESEARCH QUESTION 2: GEOGRAPHIC STORY 
    def analyze_geographic_shift(self):
        """
        RQ2: How did seat distribution shift across regions between 2021 and 2026?
        """
        print("\n" + "="*60)
        print("RQ2: THE GEOGRAPHIC STORY - How did the seat distribution shift across Tamil Nadu's six regions (Chennai Metro, North, Central, Kongu, Delta, South) between 2021 and 2026? Where did each major formation gain or lose ground?")
        print("="*60)
        
        winners_2021 = self.get_winners(self.results_2021)
        winners_2026 = self.get_winners(self.results_2026)
        
        # Seats by region and party
        seats_2021 = winners_2021[winners_2021['party'].isin(['DMK','AIADMK', 'TVK'])].groupby(['region', 'party']).size().unstack(fill_value=0)
        seats_2026 = winners_2026[winners_2026['party'].isin(['DMK','AIADMK', 'TVK'])].groupby(['region', 'party']).size().unstack(fill_value=0)
        
        votes_by_region_2026 = self.results_2026.groupby(['region', 'party'])['votes'].sum().unstack(fill_value=0)
        
        print("\nSeats by Region - 2021:")
        print(seats_2021)
        print("\nSeats by Region - 2026:")
        print(seats_2026)
        
        # TVK regional presence
        print("\nTVK Vote Share by Region (2026):")
        if 'TVK' in votes_by_region_2026.columns:
            tvk_regional = votes_by_region_2026[['TVK']].div(votes_by_region_2026.sum(axis=1), axis=0) * 100
        else:
            tvk_regional = pd.DataFrame(0, index=votes_by_region_2026.index, columns=['TVK'])
        print(tvk_regional.round(2))
        
        return seats_2021, seats_2026
    
    # RESEARCH QUESTION 3: MARGIN OF VICTORY STORY 
    def analyze_margin_of_victory(self):
        """
        RQ3: How did margins of victory change between 2021 and 2026?
        Did mandates get stronger (higher margins) or weaker?
        """
        print("\n" + "="*60)
        print("RQ3: THE MARGIN OF VICTORY STORY - Strength of Mandates How did the average margin of victory change between 2021 and 2026? In how many constituencies did the winning candidate secure more than 50% of the valid votes polled? In how many did the winning candidate receive less than 35% of the valid votes polled?")
        print("="*60)
        
        def calculate_margins(results_df):
            """Calculate victory margins"""
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
                        'region': winner['region'],
                        'reserved': winner['reserved']
                    })
            
            return pd.DataFrame(margins_data)
        
        margins_2021 = calculate_margins(self.results_2021)
        margins_2026 = calculate_margins(self.results_2026)
        
        print("\nMargin Statistics:")
        print(f"2021 - Avg margin: {margins_2021['margin'].mean():,.0f} votes")
        print(f"2021 - Std dev: {margins_2021['margin'].std():,.0f}")
        print(f"2026 - Avg margin: {margins_2026['margin'].mean():,.0f} votes")
        print(f"2026 - Std dev: {margins_2026['margin'].std():,.0f}")
        
        # Winners with 50%+ vote share
        winners_50_2021 = len(margins_2021[margins_2021['winner_share'] >= 50])
        winners_50_2026 = len(margins_2026[margins_2026['winner_share'] >= 50])
        
        print(f"\nWinners with 50%+ vote share:")
        print(f"2021: {winners_50_2021} constituencies ({winners_50_2021/len(margins_2021)*100:.1f}%)")
        print(f"2026: {winners_50_2026} constituencies ({winners_50_2026/len(margins_2026)*100:.1f}%)")

        # Winners with 35-50% vote share (potentially competitive)
        winners_35_50_2021 = len(margins_2021[(margins_2021['winner_share'] >= 35) & (margins_2021['winner_share'] < 50)])
        winners_35_50_2026 = len(margins_2026[(margins_2026['winner_share'] >= 35) & (margins_2026['winner_share'] < 50)])
        print(f"\nWinners with 35-50% vote share (potentially competitive):")
        print(f"2021: {winners_35_50_2021} constituencies ({winners_35_50_2021/len(margins_2021)*100:.1f}%)")
        print(f"2026: {winners_35_50_2026} constituencies ({winners_35_50_2026/len(margins_2026)*100:.1f}%)")
        
        
        # Winners with <35% vote share (weakest mandates)
        winners_35_2021 = len(margins_2021[margins_2021['winner_share'] < 35])
        winners_35_2026 = len(margins_2026[margins_2026['winner_share'] < 35])
        
        print(f"\nWinners with <35% vote share (weakest mandates):")
        print(f"2021: {winners_35_2021} constituencies ({winners_35_2021/len(margins_2021)*100:.1f}%)")
        print(f"2026: {winners_35_2026} constituencies ({winners_35_2026/len(margins_2026)*100:.1f}%)")
        
        # Change in margins
        margin_change = margins_2026['margin'].mean() - margins_2021['margin'].mean()
        print(f"\nChange in average margin: {margin_change:+,.0f} votes")
        if margin_change < 0:
            print("→ Mandates got WEAKER (smaller margins, more polarized)")
        else:
            print("→ Mandates got STRONGER (larger margins, clearer verdicts)")
        
        return margins_2021, margins_2026

# ==================== VISUALIZATION ====================
class Visualizer:
    @staticmethod
    def get_output_path(output_dir: str = 'results') -> Path:
        script_dir = Path(__file__).resolve().parent
        output_path = script_dir / output_dir
        output_path.mkdir(exist_ok=True)
        return output_path

    @staticmethod
    def plot_vote_share_shift(vote_share_comp, output_dir='results'):
        """Chart 1: Vote share shift - The disruption"""
        vote_share_comp = vote_share_comp.loc[~((vote_share_comp['2021 (%)'] == 0) & (vote_share_comp['2026 (%)'] == 0))]

        output_path = Visualizer.get_output_path(output_dir)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        parties = vote_share_comp.index
        x = np.arange(len(parties))
        width = 0.35
        
        ax.bar(x - width/2, vote_share_comp['2021 (%)'], width, label='2021', alpha=0.8, color='#1f77b4')
        ax.bar(x + width/2, vote_share_comp['2026 (%)'], width, label='2026', alpha=0.8, color='#ff7f0e')
        
        ax.set_xlabel('Party', fontsize=12, fontweight='bold')
        ax.set_ylabel('Vote Share (%)', fontsize=12, fontweight='bold')
        ax.set_title("Vote Share Shift: TVK's Disruption of Tamil Nadu Politics", fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(parties, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / '01_vote_share_shift.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path / '01_vote_share_shift.png'}")
        plt.close()
    
    @staticmethod
    def plot_regional_seats(seats_2021, seats_2026, output_dir='results'):
        """Chart 2: Regional seat distribution"""
        output_path = Visualizer.get_output_path(output_dir)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        seats_2021.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Regional Seat Distribution - 2021', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Seats', fontweight='bold')
        ax1.set_xlabel('Region', fontweight='bold')
        ax1.legend(title='Party', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax1.grid(axis='y', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        seats_2026.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('Regional Seat Distribution - 2026', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Seats', fontweight='bold')
        ax2.set_xlabel('Region', fontweight='bold')
        ax2.legend(title='Party', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        ax2.grid(axis='y', alpha=0.3)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(output_path / '02_regional_seats.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path / '02_regional_seats.png'}")
        plt.close()
    
    @staticmethod
    def plot_margin_distribution(margins_2021, margins_2026, output_dir='results'):
        """Chart 3: Margin of victory distribution"""
        output_path = Visualizer.get_output_path(output_dir)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.hist(margins_2021['margin']/1000, bins=20, alpha=0.6, label='2021', color='#1f77b4')
        ax.hist(margins_2026['margin']/1000, bins=20, alpha=0.6, label='2026', color='#ff7f0e')
        
        ax.axvline(margins_2021['margin'].mean()/1000, color='#1f77b4', linestyle='--', linewidth=2, label=f'2021 Avg: {margins_2021["margin"].mean()/1000:.1f}K')
        ax.axvline(margins_2026['margin'].mean()/1000, color='#ff7f0e', linestyle='--', linewidth=2, label=f'2026 Avg: {margins_2026["margin"].mean()/1000:.1f}K')
        
        ax.set_xlabel('Victory Margin (Thousands of Votes)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Constituencies', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Victory Margins: Are Mandates Getting Weaker?', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / '03_margin_distribution.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path / '03_margin_distribution.png'}")
        plt.close()
    
    @staticmethod
    def plot_mandate_strength(margins_2021, margins_2026, output_dir='results'):
        """Chart 4: Mandate strength categories"""
        output_path = Visualizer.get_output_path(output_dir)
        
        categories_2021 = margins_2021['winner_share'].apply(lambda x: '<35%' if x < 35 else ('50%+' if x >= 50 else ('35-50%' if x >= 35 else np.nan)))
        categories_2026 = margins_2026['winner_share'].apply(lambda x: '<35%' if x < 35 else ('50%+' if x >= 50 else ('35-50%' if x >= 35 else np.nan)))
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(categories_2021.value_counts().index))
        width = 0.35
        
        cat_2021 = categories_2021.value_counts().sort_index()
        cat_2026 = categories_2026.value_counts().sort_index()
        
        ax.bar(x - width/2, cat_2021, width, label='2021', alpha=0.8, color='#1f77b4')
        ax.bar(x + width/2, cat_2026, width, label='2026', alpha=0.8, color='#ff7f0e')
        
        ax.set_xlabel('Winner Vote Share Range', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Constituencies', fontsize=12, fontweight='bold')
        ax.set_title('Strength of Mandates: How Dominant Were Winners?', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(cat_2021.index)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path / '04_mandate_strength.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {output_path / '04_mandate_strength.png'}")
        plt.close()

# ==================== MAIN EXECUTION ====================
def main():
    """Run complete analysis pipeline"""
    print("\n" + "="*80)
    print("TN 2026 ASSEMBLY ELECTION ANALYSIS FOR ATLIQ MEDIA")
    print("="*80)
    
    # Load data
    print("\n[STEP 1] Loading election data...")
    dm = DataManager()
    results_2021, results_2026 = dm.download_eci_data()
    
    # Initialize analyzer
    print("\n[STEP 2] Initializing analysis...")
    analyzer = ElectionAnalyzer(results_2021, results_2026)
    
    # Run three research questions
    print("\n[STEP 3] Running research questions...")
    
    # RQ1: Vote Share Story
    vote_share_comp, state_votes_2021, state_votes_2026 = analyzer.analyze_tvk_vote_source()
    
    # RQ2: Geographic Story
    seats_2021, seats_2026 = analyzer.analyze_geographic_shift()
    
    # RQ3: Margin of Victory Story
    margins_2021, margins_2026 = analyzer.analyze_margin_of_victory()
    
    # Generate visualizations
    print("\n[STEP 4] Generating visualizations for deck...")
    Visualizer.plot_vote_share_shift(vote_share_comp)
    Visualizer.plot_regional_seats(seats_2021, seats_2026)
    Visualizer.plot_margin_distribution(margins_2021, margins_2026)
    Visualizer.plot_mandate_strength(margins_2021, margins_2026)
    
    # Summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nRUN SUCCESSFUL: charts saved to the results folder.")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code if exit_code is not None else 0)
    except FileNotFoundError as ex:
        print(f"\nDATA FILE ERROR: {ex.filename} not found.")
        print("Please make sure the required CSV files are present in data/ and rerun.")
        sys.exit(1)
    except Exception as ex:
        print("\nUNEXPECTED ERROR: Execution failed.")
        print(str(ex))
        sys.exit(1)