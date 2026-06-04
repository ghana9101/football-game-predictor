import pandas as pd

# Load the data
matches = pd.read_csv("data/results.csv", parse_dates=["date"])

# Check what tournaments exist
print("All unique tournaments in the dataset:")
print(matches["tournament"].unique())
print(f"\nTotal unique tournaments: {matches['tournament'].nunique()}")

# Check for World Cup qualification matches
wc_qual_mask = matches["tournament"] == "Soccer World Cup qualification"
print(f"\nMatches with 'Soccer World Cup qualification': {wc_qual_mask.sum()}")

# Try alternative names
alt_names = [
    "FIFA World Cup qualification",
    "World Cup qualification", 
    "FIFA World Cup Qualification",
    "WC qualification"
]

for name in alt_names:
    count = (matches["tournament"] == name).sum()
    if count > 0:
        print(f"Matches with '{name}': {count}")

# Get teams from World Cup qualification
if wc_qual_mask.sum() > 0:
    soccer_teams = set(matches.loc[wc_qual_mask, "home_team"]) | set(matches.loc[wc_qual_mask, "away_team"])
    print(f"\nTeams in Soccer World Cup qualification: {len(soccer_teams)}")
    print("Sample teams:", sorted(list(soccer_teams))[:10])
    
    # Check teams with enough matches
    teams_with_enough_matches = []
    for team in soccer_teams:
        home_matches = matches[matches["home_team"] == team]
        away_matches = matches[matches["away_team"] == team]
        total_matches = len(home_matches) + len(away_matches)
        if total_matches >= 30:
            teams_with_enough_matches.append((team, total_matches))
    
    print(f"\nTeams with ≥30 total matches: {len(teams_with_enough_matches)}")
    if teams_with_enough_matches:
        print("Top 10 teams by match count:")
        for team, count in sorted(teams_with_enough_matches, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {team}: {count} matches")

# Made with Bob
