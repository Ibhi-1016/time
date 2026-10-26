"""
World Clock - Get the current time from any place in the world.

Usage:
    python world_clock.py                  # Interactive mode
    python world_clock.py "New York"       # Get time for a specific place
    python world_clock.py --list           # List all supported timezones
"""

import sys
from datetime import datetime, timezone, timedelta

# ──────────────────────────────────────────────────────────────
# Mapping of common place / city names to their UTC offsets
# ──────────────────────────────────────────────────────────────
TIMEZONE_MAP = {
    # Asia
    "india":            {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "new delhi":        {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "mumbai":           {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "kolkata":          {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "chennai":          {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "bangalore":        {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "hyderabad":        {"offset":  5.5,  "tz": "IST",  "full": "India Standard Time"},
    "tokyo":            {"offset":  9,    "tz": "JST",  "full": "Japan Standard Time"},
    "japan":            {"offset":  9,    "tz": "JST",  "full": "Japan Standard Time"},
    "beijing":          {"offset":  8,    "tz": "CST",  "full": "China Standard Time"},
    "shanghai":         {"offset":  8,    "tz": "CST",  "full": "China Standard Time"},
    "china":            {"offset":  8,    "tz": "CST",  "full": "China Standard Time"},
    "hong kong":        {"offset":  8,    "tz": "HKT",  "full": "Hong Kong Time"},
    "singapore":        {"offset":  8,    "tz": "SGT",  "full": "Singapore Time"},
    "dubai":            {"offset":  4,    "tz": "GST",  "full": "Gulf Standard Time"},
    "abu dhabi":        {"offset":  4,    "tz": "GST",  "full": "Gulf Standard Time"},
    "bangkok":          {"offset":  7,    "tz": "ICT",  "full": "Indochina Time"},
    "jakarta":          {"offset":  7,    "tz": "WIB",  "full": "Western Indonesia Time"},
    "seoul":            {"offset":  9,    "tz": "KST",  "full": "Korea Standard Time"},
    "south korea":      {"offset":  9,    "tz": "KST",  "full": "Korea Standard Time"},
    "karachi":          {"offset":  5,    "tz": "PKT",  "full": "Pakistan Standard Time"},
    "pakistan":          {"offset":  5,    "tz": "PKT",  "full": "Pakistan Standard Time"},
    "dhaka":            {"offset":  6,    "tz": "BST",  "full": "Bangladesh Standard Time"},
    "bangladesh":       {"offset":  6,    "tz": "BST",  "full": "Bangladesh Standard Time"},
    "kathmandu":        {"offset":  5.75, "tz": "NPT",  "full": "Nepal Time"},
    "nepal":            {"offset":  5.75, "tz": "NPT",  "full": "Nepal Time"},
    "colombo":          {"offset":  5.5,  "tz": "SLST", "full": "Sri Lanka Standard Time"},
    "sri lanka":        {"offset":  5.5,  "tz": "SLST", "full": "Sri Lanka Standard Time"},
    "kuala lumpur":     {"offset":  8,    "tz": "MYT",  "full": "Malaysia Time"},
    "malaysia":         {"offset":  8,    "tz": "MYT",  "full": "Malaysia Time"},
    "taipei":           {"offset":  8,    "tz": "CST",  "full": "China Standard Time"},
    "taiwan":           {"offset":  8,    "tz": "CST",  "full": "China Standard Time"},

    # Europe
    "london":           {"offset":  0,    "tz": "GMT",  "full": "Greenwich Mean Time"},
    "uk":               {"offset":  0,    "tz": "GMT",  "full": "Greenwich Mean Time"},
    "england":          {"offset":  0,    "tz": "GMT",  "full": "Greenwich Mean Time"},
    "paris":            {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "france":           {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "berlin":           {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "germany":          {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "rome":             {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "italy":            {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "madrid":           {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "spain":            {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "amsterdam":        {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "moscow":           {"offset":  3,    "tz": "MSK",  "full": "Moscow Standard Time"},
    "russia":           {"offset":  3,    "tz": "MSK",  "full": "Moscow Standard Time"},
    "istanbul":         {"offset":  3,    "tz": "TRT",  "full": "Turkey Time"},
    "turkey":           {"offset":  3,    "tz": "TRT",  "full": "Turkey Time"},
    "athens":           {"offset":  2,    "tz": "EET",  "full": "Eastern European Time"},
    "greece":           {"offset":  2,    "tz": "EET",  "full": "Eastern European Time"},
    "zurich":           {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "switzerland":      {"offset":  1,    "tz": "CET",  "full": "Central European Time"},

    # Americas
    "new york":         {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "washington":       {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "boston":            {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "miami":            {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "chicago":          {"offset": -6,    "tz": "CST",  "full": "Central Standard Time"},
    "houston":          {"offset": -6,    "tz": "CST",  "full": "Central Standard Time"},
    "dallas":           {"offset": -6,    "tz": "CST",  "full": "Central Standard Time"},
    "denver":           {"offset": -7,    "tz": "MST",  "full": "Mountain Standard Time"},
    "los angeles":      {"offset": -8,    "tz": "PST",  "full": "Pacific Standard Time"},
    "san francisco":    {"offset": -8,    "tz": "PST",  "full": "Pacific Standard Time"},
    "seattle":          {"offset": -8,    "tz": "PST",  "full": "Pacific Standard Time"},
    "toronto":          {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "canada":           {"offset": -5,    "tz": "EST",  "full": "Eastern Standard Time"},
    "vancouver":        {"offset": -8,    "tz": "PST",  "full": "Pacific Standard Time"},
    "mexico city":      {"offset": -6,    "tz": "CST",  "full": "Central Standard Time"},
    "mexico":           {"offset": -6,    "tz": "CST",  "full": "Central Standard Time"},
    "sao paulo":        {"offset": -3,    "tz": "BRT",  "full": "Brasilia Time"},
    "brazil":           {"offset": -3,    "tz": "BRT",  "full": "Brasilia Time"},
    "buenos aires":     {"offset": -3,    "tz": "ART",  "full": "Argentina Time"},
    "argentina":        {"offset": -3,    "tz": "ART",  "full": "Argentina Time"},
    "bogota":           {"offset": -5,    "tz": "COT",  "full": "Colombia Time"},
    "lima":             {"offset": -5,    "tz": "PET",  "full": "Peru Time"},

    # Oceania
    "sydney":           {"offset":  10,   "tz": "AEST", "full": "Australian Eastern Standard Time"},
    "australia":        {"offset":  10,   "tz": "AEST", "full": "Australian Eastern Standard Time"},
    "melbourne":        {"offset":  10,   "tz": "AEST", "full": "Australian Eastern Standard Time"},
    "perth":            {"offset":  8,    "tz": "AWST", "full": "Australian Western Standard Time"},
    "auckland":         {"offset":  12,   "tz": "NZST", "full": "New Zealand Standard Time"},
    "new zealand":      {"offset":  12,   "tz": "NZST", "full": "New Zealand Standard Time"},

    # Africa
    "cairo":            {"offset":  2,    "tz": "EET",  "full": "Eastern European Time"},
    "egypt":            {"offset":  2,    "tz": "EET",  "full": "Eastern European Time"},
    "lagos":            {"offset":  1,    "tz": "WAT",  "full": "West Africa Time"},
    "nigeria":          {"offset":  1,    "tz": "WAT",  "full": "West Africa Time"},
    "nairobi":          {"offset":  3,    "tz": "EAT",  "full": "East Africa Time"},
    "kenya":            {"offset":  3,    "tz": "EAT",  "full": "East Africa Time"},
    "johannesburg":     {"offset":  2,    "tz": "SAST", "full": "South Africa Standard Time"},
    "south africa":     {"offset":  2,    "tz": "SAST", "full": "South Africa Standard Time"},
    "casablanca":       {"offset":  1,    "tz": "CET",  "full": "Central European Time"},
    "morocco":          {"offset":  1,    "tz": "CET",  "full": "Central European Time"},

    # Special
    "utc":              {"offset":  0,    "tz": "UTC",  "full": "Coordinated Universal Time"},
    "gmt":              {"offset":  0,    "tz": "GMT",  "full": "Greenwich Mean Time"},
}


def format_offset(hours):
    """Format a UTC offset (in hours) as a string like UTC+05:30."""
    sign = "+" if hours >= 0 else "-"
    hours = abs(hours)
    h = int(hours)
    m = int((hours - h) * 60)
    return f"UTC{sign}{h:02d}:{m:02d}"


def get_time_for_place(place_name):
    """
    Return a formatted string with the current date & time
    for the given place name.
    """
    key = place_name.strip().lower()
    if key not in TIMEZONE_MAP:
        return None

    info = TIMEZONE_MAP[key]
    offset_hours = info["offset"]
    tz = timezone(timedelta(hours=offset_hours))
    now = datetime.now(tz)

    offset_str = format_offset(offset_hours)

    lines = [
        f"╔══════════════════════════════════════════════╗",
        f"║  🌍  World Clock                             ║",
        f"╠══════════════════════════════════════════════╣",
        f"║  Place    : {place_name.title():<33}║",
        f"║  Timezone : {info['tz']} ({info['full']})",
        f"║  Offset   : {offset_str:<33}║",
        f"╠══════════════════════════════════════════════╣",
        f"║  Date     : {now.strftime('%A, %d %B %Y'):<33}║",
        f"║  Time     : {now.strftime('%I:%M:%S %p'):<33}║",
        f"╚══════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def list_all_places():
    """Print all supported places grouped by region."""
    seen = set()
    places = []
    for name, info in TIMEZONE_MAP.items():
        label = f"{name.title()} ({info['tz']}, {format_offset(info['offset'])})"
        if label not in seen:
            seen.add(label)
            places.append(label)
    places.sort()

    print("\n📋  Supported Places & Timezones\n" + "─" * 45)
    for p in places:
        print(f"   • {p}")
    print(f"\n   Total: {len(places)} entries\n")


def interactive_mode():
    """Run the program in interactive (loop) mode."""
    print("\n🌐  World Clock — Interactive Mode")
    print("─" * 45)
    print("Type a city or country name to get the current time.")
    print("Type 'list' to see all supported places.")
    print("Type 'quit' or 'exit' to leave.\n")

    while True:
        try:
            place = input("🔎  Enter a place: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            break

        if not place:
            continue
        if place.lower() in ("quit", "exit", "q"):
            print("Goodbye! 👋")
            break
        if place.lower() == "list":
            list_all_places()
            continue

        result = get_time_for_place(place)
        if result:
            print(f"\n{result}\n")
        else:
            print(f"\n❌  '{place}' not found. Type 'list' to see supported places.\n")


def main():
    args = sys.argv[1:]

    if not args:
        interactive_mode()
        return

    if args[0] in ("--list", "-l"):
        list_all_places()
        return

    if args[0] in ("--help", "-h"):
        print(__doc__)
        return

    place = " ".join(args)
    result = get_time_for_place(place)
    if result:
        print(f"\n{result}\n")
    else:
        print(f"\n❌  '{place}' not found.")
        print("Use --list to see all supported places.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
