#!/usr/bin/env python3
"""
Space Debris Altitude Distribution Visualization
Generates altitude distribution plot from satellite catalog CSV data
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def classify_debris_type(row):
    """Classify debris based on object type"""
    obj_type = str(row['OBJECT_TYPE']).upper()
    
    if obj_type == 'PAYLOAD':
        return 'Spacecraft'
    elif obj_type == 'ROCKET BODY':
        return 'Rocket Bodies'
    elif obj_type == 'DEBRIS':
        return 'Fragmentation Debris'
    else:
        return 'Mission Debris'

def calculate_altitude(semimajor_axis, apoapsis, periapsis):
    """Calculate orbital altitude from TLE data"""
    # Use apoapsis and periapsis to get mean altitude
    # semimajor_axis is in km, apoapsis/periapsis are altitudes above Earth surface
    if pd.notna(apoapsis) and pd.notna(periapsis):
        return (float(apoapsis) + float(periapsis)) / 2
    elif pd.notna(semimajor_axis):
        # semimajor_axis is from Earth center, subtract Earth radius (6371 km)
        return float(semimajor_axis) - 6371
    else:
        return None

def load_and_process_data(csv_file):
    """Load CSV data and extract altitude information"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Calculate altitudes
        df['altitude'] = df.apply(
            lambda row: calculate_altitude(
                row['SEMIMAJOR_AXIS'], 
                row['APOAPSIS'], 
                row['PERIAPSIS']
            ), 
            axis=1
        )
        
        # Classify debris types
        df['debris_type'] = df.apply(classify_debris_type, axis=1)
        
        # Filter valid altitudes (remove NaN and unrealistic values)
        df = df[df['altitude'].notna()]
        df = df[(df['altitude'] > 0) & (df['altitude'] < 50000)]
        
        return df
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        print("Please ensure your CSV file is in the same directory as this script.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_altitude_distribution_plot(df, output_file='altitude_distribution.png'):
    """Create altitude distribution visualization"""
    
    # Set up the plot style for academic papers
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'figure.figsize': (12, 7),
        'figure.dpi': 300,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
    })
    
    # Color scheme for debris types
    colors = {
        'Spacecraft': '#2E86AB',
        'Rocket Bodies': '#A23B72',
        'Mission Debris': '#F18F01',
        'Fragmentation Debris': '#C73E1D'
    }
    
    # Create figure
    fig, ax = plt.subplots()
    
    # Create logarithmic bins for altitude
    bins = np.logspace(np.log10(200), np.log10(40000), 60)
    
    # Prepare data by type
    debris_types = ['Spacecraft', 'Rocket Bodies', 'Mission Debris', 'Fragmentation Debris']
    data_by_type = {}
    
    for debris_type in debris_types:
        mask = df['debris_type'] == debris_type
        data_by_type[debris_type] = df[mask]['altitude'].values
    
    # Calculate LEO statistics
    leo_mask = df['altitude'] < 2000
    leo_percentage = (leo_mask.sum() / len(df)) * 100
    
    # Add LEO region highlight
    ax.fill_between([200, 2000], 0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 20000,
                     color='red', alpha=0.1, zorder=0)
    
    # Create stacked histogram
    bottom = np.zeros(len(bins) - 1)
    
    for debris_type in debris_types:
        if len(data_by_type[debris_type]) > 0:
            hist, _ = np.histogram(data_by_type[debris_type], bins=bins)
            ax.bar(bins[:-1], hist, width=np.diff(bins),
                  bottom=bottom, color=colors[debris_type],
                  alpha=0.8, align='edge', linewidth=0,
                  label=debris_type)
            bottom += hist
    
    # Add LEO region annotation
    ax.text(0.02, 0.98, 
            f'LEO Region (160-2000 km)\n{leo_percentage:.1f}% of all objects',
            transform=ax.transAxes, fontsize=9,
            bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, pad=8),
            va='top')
    
    # Add reference lines
    ax.axvline(400, color='darkred', linestyle='--', alpha=0.6, linewidth=1.5, label='ISS Orbit (400 km)')
    
    # Formatting
    ax.set_xscale('log')
    ax.set_xlabel('Altitude (km)', fontsize=11, labelpad=10)
    ax.set_ylabel('Number of Objects', fontsize=11, labelpad=10)
    ax.set_title('Space Debris Altitude Distribution', fontsize=12, fontweight='bold', pad=15)
    
    # Format tick labels
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{int(y):,}'))
    
    # Legend
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95, edgecolor='gray')
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Plot saved to: {output_file}")
    
    # Show plot
    plt.show()
    
    return fig

def main():
    """Main execution function"""
    print("=" * 70)
    print("SPACE DEBRIS ALTITUDE DISTRIBUTION VISUALIZATION")
    print("=" * 70)
    print()
    
    # Ask for CSV file name
    csv_file = input("Enter CSV filename (or press Enter for 'satellite_data.csv'): ").strip()
    if not csv_file:
        csv_file = 'satellite_data.csv'
    
    print(f"\nLoading data from: {csv_file}")
    
    # Load and process data
    df = load_and_process_data(csv_file)
    
    if df is None:
        return
    
    print(f"Loaded {len(df):,} objects with valid altitude data")
    print(f"\nDebris breakdown:")
    for debris_type in df['debris_type'].unique():
        count = (df['debris_type'] == debris_type).sum()
        percentage = (count / len(df)) * 100
        print(f"  - {debris_type}: {count:,} ({percentage:.1f}%)")
    
    print(f"\nCreating visualization...")
    
    # Create visualization
    create_altitude_distribution_plot(df)
    
    print("\nVisualization complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()