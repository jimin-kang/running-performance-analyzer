################################
# Constant values used throughout utility functions and main entrypoint
################################
from pathlib import Path

WEEKLY_MILEAGE_PLOT_TICK_FREQUENCY = 5
FIG_SIZE = (12, 8)
RACE_TYPES = [
    "400m",
    "1/2 mile",
    "1K",
    "1 mile",
    "2 mile",
    "5K",
    "10K",
    "15K",
    "10 mile",
    "20K",
    "Half-Marathon",
    "Marathon"
]
WEEK_FREQ = "W-MON"
DATE_FORMAT = "%Y-W%U"
KM_TO_METERS = 1000
MILE_TO_METERS = 1609.344
DATA_DIR = "strava_data"
ACTIVITIES_FILE = "activities"
PR_FILE = "personal_records"
OUTPUT_DIR = Path("reports") 
RACE_LINE_PLOT_COLOR = 'red'