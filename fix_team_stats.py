# Fixed version of Task 7: Save the model and team statistics
from pathlib import Path
import joblib
import pandas as pd

# Load the data
matches = pd.read_csv("data/results.csv", parse_dates=["date"])

# Create models directory
Path("models").mkdir(exist_ok=True)

# Build set of FIFA World Cup qualification teams (CORRECTED NAME)
wc_qual_mask = matches["tournament"] == "FIFA World Cup qualification"
soccer_teams = set(matches.loc[wc_qual_mask, "home_team"]) | set(matches.loc[wc_qual_mask, "away_team"])

print(f"Found {len(soccer_teams)} teams in FIFA World Cup qualification")

# Calculate team statistics
team_stats = {}

for team in soccer_teams:
    # Get all matches for this team
    home_matches = matches[matches["home_team"] == team]
    away_matches = matches[matches["away_team"] == team]
    
    total_matches = len(home_matches) + len(away_matches)
    
    # Skip teams with fewer than 30 matches
    if total_matches < 30:
        continue
    
    # Calculate wins
    home_wins = (home_matches["home_score"] > home_matches["away_score"]).sum()
    away_wins = (away_matches["away_score"] > away_matches["home_score"]).sum()
    total_wins = home_wins + away_wins
    winrate = total_wins / total_matches
    
    # Calculate goal average
    home_goals = home_matches["home_score"].sum()
    away_goals = away_matches["away_score"].sum()
    total_goals = home_goals + away_goals
    goal_avg = total_goals / total_matches
    
    # Calculate recent form (last 10 matches by date)
    all_team_matches = pd.concat([
        home_matches.assign(team_score=home_matches["home_score"], opp_score=home_matches["away_score"]),
        away_matches.assign(team_score=away_matches["away_score"], opp_score=away_matches["home_score"])
    ]).sort_values("date")
    
    if len(all_team_matches) < 10:
        recent_form = 0.5
    else:
        last_10 = all_team_matches.tail(10)
        recent_wins = (last_10["team_score"] > last_10["opp_score"]).sum()
        recent_form = recent_wins / 10
    
    team_stats[team] = {
        "winrate": float(winrate),
        "goal_avg": float(goal_avg),
        "recent_form": float(recent_form),
        "matches_played": int(total_matches)
    }

# Load the model (assuming it was already trained)
try:
    model = joblib.load("models/match_predictor.pkl")
    feature_cols = ["team_a_winrate", "team_b_winrate", "team_a_goal_avg", "team_b_goal_avg", 
                    "team_a_recent_form", "team_b_recent_form", "is_neutral", "is_major_tournament"]
    
    # Save updated team data
    joblib.dump({"team_stats": team_stats, "feature_cols": feature_cols}, "models/team_data.pkl")
    
    print(f"\n✓ Successfully saved {len(team_stats)} teams to models/team_data.pkl")
    
    # Print statistics
    print(f"\nNumber of teams stored: {len(team_stats)}")
    print("\nTop 5 teams by winrate (≥100 matches):")
    top_teams = [(team, stats["winrate"]) for team, stats in team_stats.items() if stats["matches_played"] >= 100]
    top_teams.sort(key=lambda x: x[1], reverse=True)
    for i, (team, wr) in enumerate(top_teams[:5], 1):
        matches_played = team_stats[team]["matches_played"]
        print(f"{i}. {team}: {wr:.4f} ({matches_played} matches)")
    
    # Show some available teams
    print("\nSample of available teams (first 20 alphabetically):")
    for team in sorted(list(team_stats.keys()))[:20]:
        print(f"  - {team}")
        
except FileNotFoundError:
    print("\n⚠ Warning: Model file not found. Please run Task 6 first to train the model.")
    print("Saving team_stats anyway for reference...")
    joblib.dump({"team_stats": team_stats, "feature_cols": []}, "models/team_data.pkl")

# Made with Bob
