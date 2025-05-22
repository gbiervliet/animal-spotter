# Animal Search

A tool for fetching animal observation data from waarneming.nl.

## Python Version

### Requirements
- Python 3.x
- Required packages: `requests`, `beautifulsoup4`

### Installation
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate

# Install dependencies
pip install requests beautifulsoup4
```

### Usage
```bash
# Run with default values
python search.py

# Run with custom parameters
python search.py --end_date 2025-06-30 --distance 10 --species_id 123 --point_coords "5.123456%2051.654321"
```

## JavaScript Version

### Requirements
- Node.js
- npm

# Install dependencies
npm install
```

### Usage
```bash
# Run with default values
node search.js

# Run with custom parameters
node search.js --end_date=2025-06-30 --distance=10 --species_id=123 --point_coords="5.123456%2051.654321"
```

## Parameters

- `--end_date`: End date for observations (format: YYYY-MM-DD)
- `--point_coords`: Point coordinates (format: lon%2Clat)
- `--distance`: Search radius distance in km
- `--species_id`: Species ID to search for 