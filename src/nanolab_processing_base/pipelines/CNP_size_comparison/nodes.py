"""
This is a boilerplate pipeline 'CNP_size_comparison'
generated using Kedro 0.19.11
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for headless execution
import matplotlib.pyplot as plt
import nanoplot as nplt
import pandas as pd

nplt.apply()

# Maximum absolute delta CNP gate voltage (V) to include in plots (filter outliers)
DELTA_CNP_OUTLIER_THRESHOLD = 40

# Size groupings: pairs of sample letters that correspond to the same chip size
# A & B = size 1, C & D = size 2, E & F = size 3, G & H = size 4, I & J = size 5
SIZE_GROUPS = {
    "Size 1 (A,B)": ["A", "B"],
    "Size 2 (C,D)": ["C", "D"],
    "Size 3 (E,F)": ["E", "F"],
    "Size 4 (G,H)": ["G", "H"],
    "Size 5 (I,J)": ["I", "J"],
}


def create_mean_shift_by_size_plot(
    *all_props: pd.DataFrame,
    chip1_samples: list[str],
    chip3_samples: list[str],
    chip4_samples: list[str],
) -> plt.Figure:
    """
    Create a line plot showing mean CNP shift vs stress voltage for each chip size.
    Each line represents one size group (A&B, C&D, E&F, G&H, I&J).

    Args:
        *all_props: All DataFrames in order: CHIP1 samples, then CHIP3 samples, then CHIP4 samples.
        chip1_samples: List of sample letters for CHIP1.
        chip3_samples: List of sample letters for CHIP3.
        chip4_samples: List of sample letters for CHIP4.

    Returns:
        matplotlib Figure object with the line plot.
    """
    # Build mapping from sample letter to dataframe
    all_samples = chip1_samples + chip3_samples + chip4_samples
    sample_to_df = {}
    
    chip1_count = len(chip1_samples)
    chip3_count = len(chip3_samples)
    
    for i, sample in enumerate(chip1_samples):
        sample_to_df[f"CHIP1{sample}"] = all_props[i]
    for i, sample in enumerate(chip3_samples):
        sample_to_df[f"CHIP3{sample}"] = all_props[chip1_count + i]
    for i, sample in enumerate(chip4_samples):
        sample_to_df[f"CHIP4{sample}"] = all_props[chip1_count + chip3_count + i]

    # Combine all data to get unique VG values
    all_data = pd.concat(all_props, ignore_index=True)
    all_data = all_data[
        all_data["delta_CNP_gate_voltage_forward"].abs() <= DELTA_CNP_OUTLIER_THRESHOLD
    ]
    all_vg = sorted(all_data["VG"].dropna().unique())

    fig, ax = plt.subplots()

    # Colors for each size group
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    for (size_name, letters), color in zip(SIZE_GROUPS.items(), colors):
        # Collect data for all samples matching these letters across all chips
        size_data = []
        for letter in letters:
            for chip in ["CHIP1", "CHIP3", "CHIP4"]:
                key = f"{chip}{letter}"
                if key in sample_to_df:
                    df = sample_to_df[key]
                    # Filter outliers
                    df = df[
                        df["delta_CNP_gate_voltage_forward"].abs()
                        <= DELTA_CNP_OUTLIER_THRESHOLD
                    ]
                    size_data.append(df)

        if not size_data:
            continue

        combined = pd.concat(size_data, ignore_index=True)

        # Calculate mean for each VG
        means = []
        for vg in all_vg:
            vg_data = combined[combined["VG"] == vg]["delta_CNP_gate_voltage_forward"].dropna()
            if len(vg_data) > 0:
                means.append(vg_data.mean())
            else:
                means.append(float("nan"))

        ax.plot(all_vg, means, marker="o", label=size_name, color=color)

    ax.set_xlabel(r"Stress $V_G$ (V)")
    ax.set_ylabel(r"Mean $\Delta$ CNP forward $V_G$ (V)")
    ax.legend()
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)

    return fig
