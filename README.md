# Space Debris Altitude Distribution Visualization

A Python tool for visualizing orbital debris distribution from satellite catalog data.

## Requirements

- Python 3.8+
- pandas
- matplotlib
- numpy

## Installation

### 1. Create and activate virtual environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install pandas matplotlib numpy
```

Or use requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python orbital_model.py
```

The script will prompt you for the CSV filename. Enter the path to your data file:

```
debris_analysis_output/space_debris_data.csv
```

### Expected CSV Format

Your CSV file should contain these columns:
- `OBJECT_TYPE` - Type of object (PAYLOAD, ROCKET BODY, DEBRIS)
- `SEMIMAJOR_AXIS` - Semi-major axis in km
- `APOAPSIS` - Apoapsis altitude in km
- `PERIAPSIS` - Periapsis altitude in km

### Output

The script generates:
- **Console output**: Statistics about debris distribution
- **PNG file**: High-resolution (300 DPI) altitude distribution plot
  - File: `altitude_distribution.png`
  - Format: Publication-ready quality

## Quick Command Reference

```bash
# Setup (one-time)
python3 -m venv .venv
source .venv/bin/activate
pip install pandas matplotlib numpy

# Run visualization
python orbital_model.py

# Deactivate environment when done
deactivate
```

## Example Output

The visualization shows:
- Stacked histogram of debris by type (Spacecraft, Rocket Bodies, Mission Debris, Fragmentation Debris)
- LEO region highlighted (160-2000 km)
- ISS orbit reference line (400 km)
- Logarithmic altitude scale for better visualization
- Statistics showing percentage of objects in LEO

## Troubleshooting

### Virtual environment not activating properly

```bash
# Remove old environment
rm -rf .venv

# Create fresh environment
python3 -m venv .venv
source .venv/bin/activate

# Verify activation (should show .venv path)
which python
```

### Module not found errors

```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall packages
pip install pandas matplotlib numpy
```

### Python version issues

Ensure you're using Python 3.8 or higher:

```bash
python --version
```

## For Research Papers

The output is formatted for academic publication with:
- Serif fonts (Times New Roman style)
- 300 DPI resolution
- Clean, professional styling
- Proper axis labels and legends

You can directly include the generated PNG in your LaTeX or Word documents.

## Data Sources

This tool works with satellite catalog data in CCSDS OMM format, typically from:
- Space-Track.org
- NASA Orbital Debris Program Office
- ESA Space Debris Office

## License

For research and educational use.
