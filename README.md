# **Tamil Nadu 2026 Assembly Election Analysis**
**BY : NIRMIT GUPTA**

Uncover the 3 most interesting stories in the 2026 Tamil Nadu Assembly election data, grounded only in ECI data.

### 1. **The Vote Share Story** - Where did TVK's votes come from?
- TVK is a completely new entrant in 2026 (didn't exist in 2021)
- TVK captured significant vote share by pulling votes from traditional parties
- This is the **disruption story** - a new political force reshaping the electorate

### 2. **The Geographic Story** - Which regions shifted toward which parties?
- Analyzed seat distribution across 6 regions: Chennai Metro, North, Central, Kongu, Delta, South
- Shows where TVK made inroads and where DMK/AIADMK lost ground
- Regional patterns reveal the **geographic contours** of political change

### 3. **The Margin of Victory Story** - Did mandates get stronger or weaker?
- Compared victory margins between 2021 and 2026
- Analyzed what % of winners got 50%+ vs <35% of vote share
- Shows whether 2026 saw **stronger mandates** (clear verdicts) or **weaker ones** (fragmentation)


## **File Structure**

- election-analysis/
- ├── analysis_code.py                 # Main analysis script
- ├── TN_2026_Election_Analysis.pptx   # Presentation
- ├── app.py                           # streamlit web app code
- ├── requirements.txt                 # Python dependencies
- ├── README.md                        # This file
- ├── analysis.md                      # summary of analysis
- ├── app_working.mp4                  # demo of streamlit dashboard app
- ├── data/                            # Data folder
- │    ├── tn_2021_results.csv
- │    ├── tn_2026_results.csv
- │    └── constituency_master.csv
- └── results/                         # Output folder
-      ├── 01_vote_share_shift.png
-      ├── 02_regional_seats.png
-      ├── 03_margin_distribution.png
-      └── 04_mandate_strength.png

## **Streamlit app dashboard**

The dashboard is deployed on streamlit and can be found using 
**https://election-analysis-tamil-nadu.streamlit.app/**
and the demo can be seen in 'app_working.mp4'

## **Video Walkthrough**
the Video walkthrough is available at the following link 
https://drive.google.com/drive/folders/1ftX2Or8_9leEVPZTm7FXAKzvEOvPi1Aw?usp=sharing


## **Data set**

**Taken from the official code basics RPC website**
**CSV Format Requirements:**

**Ensure that the file names are correct and are saved in a folder named "data" at the same location with the script**

Column Description for tn_2021_results.csv and tn_2026_results.csv:
1. constituency: The name of the Assembly Constituency in Tamil Nadu.
2. ac_number: The official Election Commission AC number (1 to 234). Use this as the primary key when joining files.
3. candidate: The name of the candidate as recorded by the ECI.
4. party: Standardized party abbreviation (DMK, AIADMK, TVK, INC, BJP, PMK, VCK, NTK, CPI, CPI(M), IND, NOTA, etc.).
5. votes: Total votes received by the candidate in that constituency.
6. turnout: Constituency-level voter turnout percentage. This is the same value for every row in a given constituency.
8. region: Editorial six-region grouping (Chennai Metro, North, Central, Kongu, Delta, South).

Column Description for constituency_master.csv:
1. ac_number: Official ECI AC number (1 to 234).
2. constituency: AC name.
3. district: Administrative district the constituency belongs to.
4. region: Six-region editorial grouping (Chennai Metro, North, Central, Kongu, Delta, South).
5. reserved: GEN, SC, or ST.


## **Requirements**

pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
requests>=2.28.0
streamlit>=1.28.0


## **Methodology**

- read the read me file carefully 
- clone this repository 
- install requirements
- ensure the data set is available in data folder
- run the analysis code 
- check terminal and results folder made for analysis
- run the app
- observe the analysis in the app or the documentation 
- analysis.md / presentation / results 


## **Run Locally**


- git clone https://github.com/NIRMIT-GUPTA/election-analysis.git

- cd tn-election-analysis

- pip install -r requirements.txt

- python tn_election_analysis.py

- streamlit run app.py

- Press `Ctrl + C` in your terminal to stop


read the terminal or the app or the domcumentation provided for the detailed analysis 


## **Features**

### Main Classes

1. **DataManager** - Handles data loading/creation
   - `download_eci_data()` - Loads existing CSVs or creates sample data

2. **ElectionAnalyzer** - Core analysis engine
   - `analyze_tvk_vote_source()` - RQ1: Vote share shifts
   - `analyze_geographic_shift()` - RQ2: Regional patterns
   - `analyze_margin_of_victory()` - RQ3: Mandate strength

3. **Visualizer** - Creates publication-ready charts
   - `plot_vote_share_shift()` - RQ1 visualization
   - `plot_regional_seats()` - RQ2 visualization
   - `plot_margin_distribution()` - RQ3 visualization (part 1)
   - `plot_mandate_strength()` - RQ3 visualization (part 2)

### Key Statistics Calculated

- **Vote share by party** - State-wide and regional breakdowns
- **Seat distribution** - Winners by party and region
- **Victory margins** - Vote difference between winner and runner-up
- **Winner vote share** - What % of votes did the winner get
- **Mandate strength** - % of winners with 50%+ vs less than 35 percent vote share

## **Documentation**

check the terminal / presentation / analysis.md / results for detailed analysis 

## **Outputs**

Along with the anlaysis presented in the terminal (can also be viewed in the presentation / streamlit web app / analysis.md file provided) The script generates 4 publication-ready charts Saved in a folder named results at the same loaction where your data set folder and code scripts are saved.

1. **01_vote_share_shift.png** - Bar chart showing party vote share changes
2. **02_regional_seats.png** - Regional seat distribution across parties (2021 vs 2026)
3. **03_margin_distribution.png** - Distribution of victory margins
4. **04_mandate_strength.png** - Winners by vote share category
