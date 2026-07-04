import argparse
from datetime import datetime
import json
from constants import *    
from utils import parse_date, validate_input_arguments, get_activities_and_prs, validate_pr_map, generate_reports       

def main():
    # 1. Define CLI args and validate them
    parser = argparse.ArgumentParser(description="Strava Analyzer: visualize the relationship between your training & running performance!")
    parser.add_argument("-d", "--distance", type=str, required=True, choices=RACE_TYPES, help="The race distance you want to analyze (ex: 1 mile, 5K, 10K, Half Marathon, Marathon).")
    parser.add_argument("-n", "--num-races", type=int, default=5, help="The fastest N races you want to analyze for the distance (default: 5).")
    parser.add_argument("--start-date", type=parse_date, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=parse_date, help="End date (YYYY-MM-DD)")
    parser.add_argument("--use-cached", action='store_true', help="Fetch activity & PR data from local JSON files instead of the Strava API (default: False).")
    parser.add_argument("-o", "--output", type=str, help="Filename of the analysis (default: {distance}_analysis_{timestamp}.pdf/.xlsx).")
    args = parser.parse_args()   
    
    validate_input_arguments(args, parser)

    # Determine file name for reports
    RACE_TYPE = args.distance
    TOP_N = args.num_races 
    if args.output is None:
        day_timestamp = datetime.now().strftime("%Y%m%d")
        OUTPUT_FILE = f"{args.distance}_analysis_{day_timestamp}"
    else:
        OUTPUT_FILE = args.output
    
    # 2. Load activity & race data
    if not args.use_cached:
        # Load data from the Strava API, if not operating in cached mode
        activities_map, pr_map = get_activities_and_prs(args.start_date, args.end_date, TOP_N)
    else:
        # Otherwise, load activities & races from local JSON files.
        # If the files don't exist or don't contain sufficient PR data (i.e. less than TOP_N PRs per race distance), then we'll load activities from the Strava API
        print(f"Loading activities & PRs from JSON files in '{DATA_DIR}'...")
        try:
            with open(f"{DATA_DIR}/{ACTIVITIES_FILE}.json") as f:
                activities_map = json.load(f)
            with open(f"{DATA_DIR}/{PR_FILE}.json") as f:
                pr_map = json.load(f)
            
            if not validate_pr_map(pr_map, TOP_N):
                print("Local PR data doesn't contain sufficient data, calling Strava API to fetch all activities.")
                activities_map, pr_map = get_activities_and_prs(args.start_date, args.end_date, TOP_N)
            
        except FileNotFoundError as e:
            print(f"Activity data not found from local JSON files: {e}.")
            print("Loading data from Strava API instead!")
            activities_map, pr_map = get_activities_and_prs(args.start_date, args.end_date, TOP_N)

    # 3. Create the reports (PDF & Excel)
    generate_reports(activities_map, pr_map, RACE_TYPE, OUTPUT_FILE)
    

if __name__ == "__main__":
    main()
    