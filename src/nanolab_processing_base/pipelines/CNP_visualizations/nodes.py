"""
This is a boilerplate pipeline 'CNP_visualizations'
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

    fig, ax = plt.subplots()

    # Fixed VG values and tick marks (same as comparison plot)
    all_vg = sorted(combined_props["VG"].dropna().unique())
    tick_vg = [-40, -20, 0, 20, 40]

    data = []
    for vg in all_vg:
        vg_data = combined_props[combined_props["VG"] == vg][
            "delta_CNP_gate_voltage_forward"
        ].dropna()
        data.append(vg_data.values if len(vg_data) > 0 else [])

    ax.boxplot(
        data,
        positions=range(len(all_vg)),
        showfliers=True,
    )

    # Set x-axis ticks and labels only for specified tick values
    tick_positions = [i for i, vg in enumerate(all_vg) if vg in tick_vg]
    tick_labels = [str(int(vg)) for vg in all_vg if vg in tick_vg]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    # Set y-axis ticks (same as comparison plot)
    ax.set_yticks([10, 0, -10, -20])

    ax.set_xlabel(r"Stress $V_G$ (V)")
    ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)")

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

    # Tick marks to display
    tick_vg = [-40, -20, 0, 20, 40]

    fig, ax = plt.subplots()

    # Colors for each chip
    colors = {"CHIP1": "#1f77b4", "CHIP3": "#ff7f0e", "CHIP4": "#2ca02c"}

    # Spacing: boxes within group are close, groups are separated
    box_width = 0.25  # Width of each box
    box_spacing = 0.3  # Space between box centers within a VG group
    group_spacing = 1.5  # Space between VG groups

    positions_chip1 = []
    positions_chip3 = []
    positions_chip4 = []

    # Prepare data and positions for each VG
    data_chip1 = []
    data_chip3 = []
    data_chip4 = []

    for i, vg in enumerate(all_vg):
        base_pos = i * group_spacing  # Base position for this VG group

        # CHIP1
        chip1_vg_data = chip1_data[chip1_data["VG"] == vg][
            "delta_CNP_gate_voltage_forward"
        ].dropna()
        data_chip1.append(chip1_vg_data.values if len(chip1_vg_data) > 0 else [])
        positions_chip1.append(base_pos - box_spacing)

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
        positions_chip4.append(base_pos + box_spacing)

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
    for bp, color in [
        (bp1, colors["CHIP1"]),
        (bp3, colors["CHIP3"]),
        (bp4, colors["CHIP4"]),
    ]:
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
        for flier in bp["fliers"]:
            flier.set_markerfacecolor(color)
            flier.set_markeredgecolor(color)

    # Set x-axis ticks and labels only for specified tick values
    tick_positions = [i * group_spacing for i, vg in enumerate(all_vg) if vg in tick_vg]
    tick_labels = [str(int(vg)) for vg in all_vg if vg in tick_vg]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    # Set y-axis ticks
    ax.set_yticks([10, 0, -10, -20])

    # Labels and title
    ax.set_xlabel(r"Stress $V_G$ (V)")
    ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)")

    # Legend
    legend_patches = [
        plt.Line2D([0], [0], color=colors["CHIP1"], lw=10, label="CHIP1"),
        plt.Line2D([0], [0], color=colors["CHIP3"], lw=10, label="CHIP3"),
        plt.Line2D([0], [0], color=colors["CHIP4"], lw=10, label="CHIP4"),
    ]
    ax.legend(handles=legend_patches)

    return fig
