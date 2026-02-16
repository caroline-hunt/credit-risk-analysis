import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Read the cleaned data
df = pd.read_csv('output/delinquency_data_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])

# Calculate period-over-period changes
df['pct_change'] = df['value'].pct_change() * 100
df['abs_change'] = df['value'].diff()

# Identify sharp increases (threshold: >1% increase or >0.03 percentage points)
sharp_increase_threshold_pct = 1.0  # 1% increase
sharp_increase_threshold_abs = 0.03  # 0.03 percentage points
df['sharp_increase'] = ((df['pct_change'] > sharp_increase_threshold_pct) |
                        (df['abs_change'] > sharp_increase_threshold_abs))

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the main line
ax.plot(df['date'], df['value'], marker='o', linewidth=2, markersize=8,
        color='#2E86AB', label='Delinquency Rate')

# Highlight sharp increases
sharp_increases = df[df['sharp_increase'] == True]
if not sharp_increases.empty:
    ax.scatter(sharp_increases['date'], sharp_increases['value'],
              color='#E63946', s=200, zorder=5, label='Sharp Increase',
              marker='^', edgecolors='darkred', linewidth=2)

    # Add annotations for sharp increases
    for idx, row in sharp_increases.iterrows():
        ax.annotate(f'+{row["abs_change"]:.2f}pp\n({row["pct_change"]:.1f}%)',
                   xy=(row['date'], row['value']),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='#E63946', alpha=0.7),
                   color='white', fontweight='bold', fontsize=9,
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0',
                                 color='#E63946', lw=2))

# Formatting
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Delinquency Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Credit Card Delinquency Rate Over Time (2024-2025)',
            fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='best', fontsize=10)

# Format y-axis to show percentage
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}%'))

# Rotate x-axis labels
plt.xticks(rotation=45, ha='right')

plt.tight_layout()

# Save the plot
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)
plt.savefig('output/delinquency_trends.png', dpi=300, bbox_inches='tight')
print("Plot saved to: output/delinquency_trends.png")

# Generate summary statistics
print("\n" + "="*70)
print("SUMMARY STATISTICS - Credit Card Delinquency Rate")
print("="*70)

summary_stats = df['value'].describe()
print(f"\nBasic Statistics:")
print(f"  Count:          {summary_stats['count']:.0f} observations")
print(f"  Mean:           {summary_stats['mean']:.2f}%")
print(f"  Std Dev:        {summary_stats['std']:.2f}%")
print(f"  Min:            {summary_stats['min']:.2f}%")
print(f"  25th percentile: {summary_stats['25%']:.2f}%")
print(f"  Median (50th):  {summary_stats['50%']:.2f}%")
print(f"  75th percentile: {summary_stats['75%']:.2f}%")
print(f"  Max:            {summary_stats['max']:.2f}%")

print(f"\nTrend Analysis:")
print(f"  Date Range:     {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
print(f"  Overall Change: {df['value'].iloc[-1] - df['value'].iloc[0]:.2f} percentage points")
print(f"  Overall % Change: {((df['value'].iloc[-1] / df['value'].iloc[0]) - 1) * 100:.2f}%")
print(f"  Peak Rate:      {df['value'].max():.2f}% on {df[df['value'] == df['value'].max()]['date'].iloc[0].strftime('%Y-%m-%d')}")
print(f"  Lowest Rate:    {df['value'].min():.2f}% on {df[df['value'] == df['value'].min()]['date'].iloc[0].strftime('%Y-%m-%d')}")

print(f"\nPeriod-over-Period Changes:")
changes_df = df[['date', 'value', 'abs_change', 'pct_change']].copy()
changes_df['date'] = changes_df['date'].dt.strftime('%Y-%m-%d')
print(changes_df.to_string(index=False))

if not sharp_increases.empty:
    print(f"\n⚠️  Sharp Increases Detected: {len(sharp_increases)}")
    for idx, row in sharp_increases.iterrows():
        print(f"  • {row['date'].strftime('%Y-%m-%d')}: {row['value']:.2f}% "
              f"(+{row['abs_change']:.2f}pp, +{row['pct_change']:.1f}%)")
else:
    print(f"\n✓ No sharp increases detected (threshold: >{sharp_increase_threshold_abs}pp or >{sharp_increase_threshold_pct}%)")

print("\n" + "="*70)

# Create summary statistics DataFrame for export
summary_df = pd.DataFrame({
    'Metric': ['Count', 'Mean', 'Std Dev', 'Min', '25th Percentile',
               'Median', '75th Percentile', 'Max', 'Range', 'Overall Change'],
    'Value': [
        f"{summary_stats['count']:.0f}",
        f"{summary_stats['mean']:.2f}%",
        f"{summary_stats['std']:.2f}%",
        f"{summary_stats['min']:.2f}%",
        f"{summary_stats['25%']:.2f}%",
        f"{summary_stats['50%']:.2f}%",
        f"{summary_stats['75%']:.2f}%",
        f"{summary_stats['max']:.2f}%",
        f"{summary_stats['max'] - summary_stats['min']:.2f}%",
        f"{df['value'].iloc[-1] - df['value'].iloc[0]:.2f}pp"
    ]
})

summary_df.to_csv('output/summary_statistics.csv', index=False)
print("\nSummary statistics saved to: output/summary_statistics.csv")
