"""
This is a boilerplate pipeline 'CNP_visualizations'
generated using Kedro 0.19.11
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for headless execution
import matplotlib.pyplot as plt
import pandas as pd

# Maximum absolute delta CNP gate voltage (V) to include in plots (filter outliers)
DELTA_CNP_OUTLIER_THRESHOLD = 40


def create_forward_cnp_boxplot_chip(
    *sample_props: pd.DataFrame,
    chip_name: str,
) -> plt.Figure:
    """
    Create a boxplot showing Forward CNP Shift vs Stress Voltage for a chip,
    combining data from all samples (A, B, C, etc.) of that chip.

    Args:
        *sample_props: DataFrames with CNP calculations after stress for each sample.
        chip_name: Name of the chip (e.g., "CHIP1") for the plot title.

    Returns:
        matplotlib Figure object with the boxplot.
    """
    # Concatenate all samples from the same chip
    combined_props = pd.concat(sample_props, ignore_index=True)

    # Filter out outliers where delta exceeds threshold
    combined_props = combined_props[
        combined_props["delta_CNP_gate_voltage_forward"].abs()
        <= DELTA_CNP_OUTLIER_THRESHOLD
    ]

    fig, ax = plt.subplots(figsize=(9, 5))

    groups = combined_props.groupby("VG")
    data = [g["delta_CNP_gate_voltage_forward"].dropna() for _, g in groups]
    labels = [vg for vg, _ in groups]

    ax.boxplot(
        data,
        tick_labels=labels,
        showfliers=True,
    )

    ax.set_xlabel(r"Stress $V_G$ (V)", fontsize=12)
    ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)", fontsize=12)
    ax.set_title(f"Forward CNP Shift vs Stress Voltage - {chip_name}", fontsize=14)

    ax.grid(True, axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig


def create_forward_cnp_boxplot_comparison(
    *all_props: pd.DataFrame,
    chip1_count: int,
    chip3_count: int,
) -> plt.Figure:
    """
    Create a boxplot comparing Forward CNP Shift across all 3 chips for each gate voltage.
    Each gate voltage has 3 boxes (one per chip) with different colors.

    Args:
        *all_props: All DataFrames in order: CHIP1 samples, then CHIP3 samples, then CHIP4 samples.
        chip1_count: Number of CHIP1 samples.
        chip3_count: Number of CHIP3 samples.

    Returns:
        matplotlib Figure object with the comparison boxplot.
    """
    # Split the flat list into chip groups
    chip1_props = all_props[:chip1_count]
    chip3_props = all_props[chip1_count : chip1_count + chip3_count]
    chip4_props = all_props[chip1_count + chip3_count :]

    # Concatenate all samples for each chip
    chip1_data = pd.concat(chip1_props, ignore_index=True)
    chip3_data = pd.concat(chip3_props, ignore_index=True)
    chip4_data = pd.concat(chip4_props, ignore_index=True)

    # Filter out outliers where delta exceeds threshold
    chip1_data = chip1_data[
        chip1_data["delta_CNP_gate_voltage_forward"].abs()
        <= DELTA_CNP_OUTLIER_THRESHOLD
    ]
    chip3_data = chip3_data[
        chip3_data["delta_CNP_gate_voltage_forward"].abs()
        <= DELTA_CNP_OUTLIER_THRESHOLD
    ]
    chip4_data = chip4_data[
        chip4_data["delta_CNP_gate_voltage_forward"].abs()
        <= DELTA_CNP_OUTLIER_THRESHOLD
    ]

    # Get unique VG values across all chips
    all_vg = sorted(
        set(chip1_data["VG"].dropna())
        | set(chip3_data["VG"].dropna())
        | set(chip4_data["VG"].dropna())
    )

    # Wider figure for better separation
    fig, ax = plt.subplots(figsize=(20, 6))

    # Colors for each chip
    colors = {"CHIP1": "#1f77b4", "CHIP3": "#ff7f0e", "CHIP4": "#2ca02c"}

    # Width of each box and spacing between VG groups
    box_width = 0.15  # Thinner boxes
    group_spacing = 1.5  # More space between VG groups
    positions_chip1 = []
    positions_chip3 = []
    positions_chip4 = []

    # Prepare data and positions for each VG
    data_chip1 = []
    data_chip3 = []
    data_chip4 = []

    for i, vg in enumerate(all_vg):
        base_pos = (
            i * group_spacing
        )  # Base position for this VG group with wider spacing

        # CHIP1
        chip1_vg_data = chip1_data[chip1_data["VG"] == vg][
            "delta_CNP_gate_voltage_forward"
        ].dropna()
        data_chip1.append(chip1_vg_data.values if len(chip1_vg_data) > 0 else [])
        positions_chip1.append(base_pos - box_width * 1.2)

        # CHIP3
        chip3_vg_data = chip3_data[chip3_data["VG"] == vg][
            "delta_CNP_gate_voltage_forward"
        ].dropna()
        data_chip3.append(chip3_vg_data.values if len(chip3_vg_data) > 0 else [])
        positions_chip3.append(base_pos)

        # CHIP4
        chip4_vg_data = chip4_data[chip4_data["VG"] == vg][
            "delta_CNP_gate_voltage_forward"
        ].dropna()
        data_chip4.append(chip4_vg_data.values if len(chip4_vg_data) > 0 else [])
        positions_chip4.append(base_pos + box_width * 1.2)

    # Create boxplots for each chip
    bp1 = ax.boxplot(
        data_chip1,
        positions=positions_chip1,
        widths=box_width,
        patch_artist=True,
        showfliers=True,
    )
    bp3 = ax.boxplot(
        data_chip3,
        positions=positions_chip3,
        widths=box_width,
        patch_artist=True,
        showfliers=True,
    )
    bp4 = ax.boxplot(
        data_chip4,
        positions=positions_chip4,
        widths=box_width,
        patch_artist=True,
        showfliers=True,
    )

    # Color the boxes
    for bp, color, chip in [
        (bp1, colors["CHIP1"], "CHIP1"),
        (bp3, colors["CHIP3"], "CHIP3"),
        (bp4, colors["CHIP4"], "CHIP4"),
    ]:
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        for element in ["whiskers", "caps", "medians"]:
            for item in bp[element]:
                item.set_color("black")
        for flier in bp["fliers"]:
            flier.set_markerfacecolor(color)
            flier.set_markeredgecolor(color)

    # Set x-axis ticks and labels (adjusted for new spacing)
    ax.set_xticks([i * group_spacing for i in range(len(all_vg))])
    ax.set_xticklabels([str(vg) for vg in all_vg])

    # Labels and title
    ax.set_xlabel(r"Stress $V_G$ (V)", fontsize=12)
    ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)", fontsize=12)
    ax.set_title(
        "Forward CNP Shift vs Stress Voltage - All Chips Comparison", fontsize=14
    )

    # Legend
    legend_patches = [
        plt.Line2D([0], [0], color=colors["CHIP1"], lw=10, alpha=0.7, label="CHIP1"),
        plt.Line2D([0], [0], color=colors["CHIP3"], lw=10, alpha=0.7, label="CHIP3"),
        plt.Line2D([0], [0], color=colors["CHIP4"], lw=10, alpha=0.7, label="CHIP4"),
    ]
    ax.legend(handles=legend_patches, loc="upper left", frameon=False)

    ax.grid(True, axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig
