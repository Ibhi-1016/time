# 🌍 World Clock — Python

A simple Python program to get the **current time** from any place in the world.

## Features

- **90+ cities & countries** supported across all continents
- **Interactive mode** — just run the script and type a place name
- **Command-line mode** — pass a place name as an argument
- **No external dependencies** — uses only Python's standard library

## Usage

### Interactive Mode
```bash
python world_clock.py
```
You'll be prompted to enter a city or country name.

### Command-Line Mode
```bash
python world_clock.py "New York"
python world_clock.py Tokyo
python world_clock.py India
```

### List All Supported Places
```bash
python world_clock.py --list
```

## Example Output

```
╔══════════════════════════════════════════════╗
║  🌍  World Clock                             ║
╠══════════════════════════════════════════════╣
║  Place    : New York                         ║
║  Timezone : EST (Eastern Standard Time)
║  Offset   : UTC-05:00                        ║
╠══════════════════════════════════════════════╣
║  Date     : Monday, 26 October 2026          ║
║  Time     : 10:57:04 AM                      ║
╚══════════════════════════════════════════════╝
```

## Requirements

- Python 3.6+
