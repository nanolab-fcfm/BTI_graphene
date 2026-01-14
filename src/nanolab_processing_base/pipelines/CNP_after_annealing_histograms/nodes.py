"""
This is a boilerplate pipeline 'CNP_after_annealing_histograms'
generated using Kedro 0.19.11
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for headless execution
import matplotlib.pyplot as plt
import nanoplot as nplt
import numpy as np
import pandas as pd

nplt.apply()


def get_after_annealing_cnps(props: pd.DataFrame) -> pd.DataFrame:
    """
    Extract CNP values from VVg experiments that occur just before stress.
    These are the experiments "after annealing" - the baseline measurements
    before each stress cycle.

    Args:
        props: DataFrame with CNP calculations (properties_project_CHIPXY_with_CNPs).

    Returns:
        DataFrame containing only the VVg rows immediately before stress experiments.
    """
    props = props.sort_values(by="Start time").reset_index(drop=True).copy()
    props["VG"] = props["VG"].ffill()

    # Find indices where "Procedure type" is "Stress"
    stress_idx = props.index[props["Procedure type"] == "Stress"]

    # Get the row index just before each "Stress" (these are VVg after annealing)
    previous_idx = [i - 1 for i in stress_idx if (i - 1) in props.index]

    # Select only those rows
    after_annealing = props.loc[previous_idx].copy()

    return after_annealing


def create_cnp_histogram(
    props: pd.DataFrame,
    sample_name: str,
) -> plt.Figure:
    """
    Create a histogram of CNP gate voltage values for experiments after annealing.

    Args:
        props: DataFrame with CNP calculations (properties_project_CHIPXY_with_CNPs).
        sample_name: Name of the sample (e.g., "CHIP1A") for the plot title.

    Returns:
        matplotlib Figure object with the histogram.
    """
    # Get only the after-annealing experiments
    after_annealing = get_after_annealing_cnps(props)

    # Get CNP forward values
    cnp_values = after_annealing["CNP_gate_voltage_forward"].dropna()

    fig, ax = plt.subplots()

    if len(cnp_values) > 0:
        ax.hist(cnp_values, bins="auto", edgecolor="black", alpha=0.7)
        ax.axvline(
            cnp_values.mean(),
            color="red",
            linestyle="--",
            label=f"Mean: {cnp_values.mean():.2f} V",
        )
        ax.legend()

    ax.set_xlabel(r"CNP forward $V_G$ (V)")
    ax.set_ylabel("Count")

    return fig


def create_cnp_deviation_summary(
    *all_props: pd.DataFrame,
    sample_names: list[str],
) -> plt.Figure:
    """
    Create a summary plot showing the deviation from mean (min and max) for each sample.
    X-axis: sample letters, Y-axis: deviation from mean (min and max as error bars).
    Background is shaded by chip color.

    Args:
        *all_props: All DataFrames with CNP calculations for each sample.
        sample_names: List of sample names in the same order as all_props.

    Returns:
        matplotlib Figure object with the summary plot.
    """
    # Colors for each chip (same as boxplot comparison)
    chip_colors = {
        "CHIP1": "#1f77b4",
        "CHIP3": "#ff7f0e",
        "CHIP4": "#2ca02c",
    }

    means = []
    mins = []
    maxs = []
    valid_sample_names = []
    chips = []

    for props, sample_name in zip(all_props, sample_names):
        after_annealing = get_after_annealing_cnps(props)
        cnp_values = after_annealing["CNP_gate_voltage_forward"].dropna()

        if len(cnp_values) > 0:
            mean_val = cnp_values.mean()
            min_val = cnp_values.min()
            max_val = cnp_values.max()

            means.append(mean_val)
            mins.append(mean_val - min_val)  # deviation below mean
            maxs.append(max_val - mean_val)  # deviation above mean
            valid_sample_names.append(sample_name)
            # Extract chip name (e.g., "CHIP1" from "CHIP1A")
            chip = sample_name[:-1]
            chips.append(chip)

    fig, ax = plt.subplots()

    x = list(range(len(valid_sample_names)))

    # Draw shaded background regions for each chip
    current_chip = None
    region_start = 0
    for i, chip in enumerate(chips + [None]):  # Add None to close last region
        if chip != current_chip:
            if current_chip is not None:
                # Draw shaded region for the previous chip
                ax.axvspan(
                    region_start - 0.5,
                    i - 0.5,
                    alpha=0.2,
                    color=chip_colors.get(current_chip, "gray"),
                    label=current_chip,
                )
            region_start = i
            current_chip = chip

    # Plot error bars showing min/max deviation from mean (centered at 0)
    # All samples are centered at y=0, showing only their deviation range
    zeros = [0] * len(valid_sample_names)
    ax.errorbar(
        x,
        zeros,
        yerr=[mins, maxs],
        fmt="o",
        color="black",
    )

    # Extract just the sample letter for x-tick labels
    letters = [name[-1] for name in valid_sample_names]
    ax.set_xticks(x)
    ax.set_xticklabels(letters)
    ax.set_xlabel("Sample")
    ax.set_ylabel(r"CNP deviation from mean (V)")

    # Create legend for chip colors
    legend_patches = [
        plt.Line2D([0], [0], color=chip_colors["CHIP1"], lw=10, alpha=0.2, label="CHIP1"),
        plt.Line2D([0], [0], color=chip_colors["CHIP3"], lw=10, alpha=0.2, label="CHIP3"),
        plt.Line2D([0], [0], color=chip_colors["CHIP4"], lw=10, alpha=0.2, label="CHIP4"),
    ]
    ax.legend(handles=legend_patches)

    return fig


def create_cnp_deviation_histograms(
    *all_props: pd.DataFrame,
    sample_names: list[str],
) -> plt.Figure:
    """
    Create histograms of min deviation, max deviation, and standard deviation
    from mean CNP values across all samples.

    Args:
        *all_props: All DataFrames with CNP calculations for each sample.
        sample_names: List of sample names in the same order as all_props.

    Returns:
        matplotlib Figure object with three overlapping histograms.
    """
    min_devs = []
    max_devs = []
    std_devs = []

    for props, sample_name in zip(all_props, sample_names):
        after_annealing = get_after_annealing_cnps(props)
        cnp_values = after_annealing["CNP_gate_voltage_forward"].dropna()

        if len(cnp_values) > 0:
            mean_val = cnp_values.mean()
            min_devs.append(cnp_values.min() - mean_val)  # negative deviation (below mean)
            max_devs.append(cnp_values.max() - mean_val)  # positive deviation (above mean)
            std_devs.append(cnp_values.std())

    fig, ax = plt.subplots()

    # Combine all data to determine common bin edges
    all_data = min_devs + max_devs + std_devs
    bins = np.linspace(min(all_data), max(all_data), 30)

    ax.hist(min_devs, bins=bins, alpha=0.7, label="Min deviation")
    ax.hist(max_devs, bins=bins, alpha=0.7, label="Max deviation")
    ax.hist(std_devs, bins=bins, alpha=0.7, label="Standard deviation")

    ax.set_xlabel("Deviation (V)")
    ax.set_ylabel("Count")
    ax.legend()

    return fig
