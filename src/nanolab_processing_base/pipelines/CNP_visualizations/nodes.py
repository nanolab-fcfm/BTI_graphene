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


def _make_chip_boxplot(ax, combined: pd.DataFrame, title: str, ylabel: bool = True) -> None:
    """Helper: draw a single forward-CNP boxplot onto ax."""
    combined = combined[
        combined["delta_CNP_gate_voltage_forward"].abs() <= DELTA_CNP_OUTLIER_THRESHOLD
    ]
    all_vg = sorted(combined["VG"].dropna().unique())
    tick_vg = [-40, -20, 0, 20, 40]

    data = [
        combined[combined["VG"] == vg]["delta_CNP_gate_voltage_forward"].dropna().values
        for vg in all_vg
    ]
    ax.boxplot(data, positions=range(len(all_vg)), showfliers=True)

    tick_positions = [i for i, vg in enumerate(all_vg) if vg in tick_vg]
    tick_labels = [str(int(vg)) for vg in all_vg if vg in tick_vg]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([10, 0, -10, -20])
    ax.set_xlabel(r"Stress $V_G$ (V)")
    if ylabel:
        ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)")
    ax.set_title(title)


def create_baseline_vs_nonbaseline_chip(
    *all_props: pd.DataFrame,
    chip_name: str,
    baseline_count: int,
) -> plt.Figure:
    """
    Two-panel figure: left = baseline, right = non-baseline for one chip.

    Args:
        *all_props: baseline sample DataFrames first, then non-baseline.
        chip_name: e.g. "CHIP1".
        baseline_count: number of baseline DataFrames in all_props.
    """
    baseline_props = all_props[:baseline_count]
    nonbaseline_props = all_props[baseline_count:]

    baseline_data = pd.concat(baseline_props, ignore_index=True)
    nonbaseline_data = pd.concat(nonbaseline_props, ignore_index=True)

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(40, 20), sharey=True)
    _make_chip_boxplot(ax_l, baseline_data, f"{chip_name} — baseline")
    _make_chip_boxplot(ax_r, nonbaseline_data, f"{chip_name} — non-baseline", ylabel=False)
    fig.tight_layout()
    return fig


def _make_grouped_chip_boxplot(ax, chip1_data: pd.DataFrame, chip3_data: pd.DataFrame,
                               chip4_data: pd.DataFrame, title: str, ylabel: bool = True,
                               legend: bool = True) -> None:
    """Helper: draw a grouped (3 boxes per VG) forward-CNP boxplot onto ax."""
    colors = {"CHIP1": "#1f77b4", "CHIP3": "#ff7f0e", "CHIP4": "#2ca02c"}
    box_width = 0.25
    box_spacing = 0.3
    group_spacing = 1.5
    tick_vg = [-40, -20, 0, 20, 40]

    chip_keys = ["chip1", "chip3", "chip4"]
    chip_dfs = [chip1_data, chip3_data, chip4_data]
    offsets = [-box_spacing, 0, box_spacing]

    all_vg = sorted(
        set(chip1_data["VG"].dropna())
        | set(chip3_data["VG"].dropna())
        | set(chip4_data["VG"].dropna())
    )

    positions = {k: [] for k in chip_keys}
    data = {k: [] for k in chip_keys}

    for i, vg in enumerate(all_vg):
        base_pos = i * group_spacing
        for key, df, offset in zip(chip_keys, chip_dfs, offsets):
            vg_data = df[df["VG"] == vg]["delta_CNP_gate_voltage_forward"].dropna()
            data[key].append(vg_data.values if len(vg_data) > 0 else [])
            positions[key].append(base_pos + offset)

    for key, chip_name in zip(chip_keys, ["CHIP1", "CHIP3", "CHIP4"]):
        bp = ax.boxplot(
            data[key],
            positions=positions[key],
            widths=box_width,
            patch_artist=True,
            showfliers=True,
        )
        color = colors[chip_name]
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
        for flier in bp["fliers"]:
            flier.set_markerfacecolor(color)
            flier.set_markeredgecolor(color)

    tick_positions = [i * group_spacing for i, vg in enumerate(all_vg) if vg in tick_vg]
    tick_labels = [str(int(vg)) for vg in all_vg if vg in tick_vg]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([10, 0, -10, -20])
    ax.set_xlabel(r"Stress $V_G$ (V)")
    if ylabel:
        ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)")
    ax.set_title(title)

    if legend:
        legend_patches = [
            plt.Line2D([0], [0], color=colors[c], lw=10, label=c)
            for c in ["CHIP1", "CHIP3", "CHIP4"]
        ]
        ax.legend(handles=legend_patches)


def create_baseline_vs_nonbaseline_all(
    *all_props: pd.DataFrame,
    chip1_baseline_count: int,
    chip3_baseline_count: int,
    chip4_baseline_count: int,
    chip1_nonbaseline_count: int,
    chip3_nonbaseline_count: int,
) -> plt.Figure:
    """
    Two-panel figure: left = all baseline chips grouped by chip,
    right = all non-baseline chips grouped by chip.

    Props order: CHIP1 baseline, CHIP3 baseline, CHIP4 baseline,
                 CHIP1 non-baseline, CHIP3 non-baseline, CHIP4 non-baseline.
    """
    i0 = chip1_baseline_count
    i1 = i0 + chip3_baseline_count
    i2 = i1 + chip4_baseline_count
    i3 = i2 + chip1_nonbaseline_count
    i4 = i3 + chip3_nonbaseline_count

    def _filter(props):
        df = pd.concat(props, ignore_index=True)
        return df[df["delta_CNP_gate_voltage_forward"].abs() <= DELTA_CNP_OUTLIER_THRESHOLD]

    chip1_bl = _filter(all_props[:i0])
    chip3_bl = _filter(all_props[i0:i1])
    chip4_bl = _filter(all_props[i1:i2])
    chip1_nb = _filter(all_props[i2:i3])
    chip3_nb = _filter(all_props[i3:i4])
    chip4_nb = _filter(all_props[i4:])

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(40, 20), sharey=True)
    _make_grouped_chip_boxplot(ax_l, chip1_bl, chip3_bl, chip4_bl, "All chips — baseline")
    _make_grouped_chip_boxplot(ax_r, chip1_nb, chip3_nb, chip4_nb, "All chips — non-baseline", ylabel=False, legend=False)
    fig.tight_layout()
    return fig


def create_forward_cnp_boxplot_baseline_comparison(
    *all_props: pd.DataFrame,
    chip1_count: int,
    chip3_count: int,
) -> plt.Figure:
    """
    Create a boxplot comparing Forward CNP Shift across baseline CHIP1, CHIP3, CHIP4.

    Args:
        *all_props: All DataFrames in order: CHIP1 samples, CHIP3 samples, CHIP4 samples.
        chip1_count: Number of CHIP1 samples.
        chip3_count: Number of CHIP3 samples.

    Returns:
        matplotlib Figure object with the comparison boxplot.
    """
    chip1_props = all_props[:chip1_count]
    chip3_props = all_props[chip1_count : chip1_count + chip3_count]
    chip4_props = all_props[chip1_count + chip3_count :]

    chip1_data = pd.concat(chip1_props, ignore_index=True)
    chip3_data = pd.concat(chip3_props, ignore_index=True)
    chip4_data = pd.concat(chip4_props, ignore_index=True)

    for df in [chip1_data, chip3_data, chip4_data]:
        df.drop(
            df[df["delta_CNP_gate_voltage_forward"].abs() > DELTA_CNP_OUTLIER_THRESHOLD].index,
            inplace=True,
        )

    all_vg = sorted(
        set(chip1_data["VG"].dropna())
        | set(chip3_data["VG"].dropna())
        | set(chip4_data["VG"].dropna())
    )

    tick_vg = [-40, -20, 0, 20, 40]

    fig, ax = plt.subplots()

    colors = {"CHIP1": "#1f77b4", "CHIP3": "#ff7f0e", "CHIP4": "#2ca02c"}

    box_width = 0.25
    box_spacing = 0.3
    group_spacing = 1.5

    chip_keys = ["chip1", "chip3", "chip4"]
    chip_dfs = [chip1_data, chip3_data, chip4_data]
    offsets = [-box_spacing, 0, box_spacing]

    positions = {k: [] for k in chip_keys}
    data = {k: [] for k in chip_keys}

    for i, vg in enumerate(all_vg):
        base_pos = i * group_spacing
        for key, df, offset in zip(chip_keys, chip_dfs, offsets):
            vg_data = df[df["VG"] == vg]["delta_CNP_gate_voltage_forward"].dropna()
            data[key].append(vg_data.values if len(vg_data) > 0 else [])
            positions[key].append(base_pos + offset)

    bps = {}
    for key, chip_name in zip(chip_keys, ["CHIP1", "CHIP3", "CHIP4"]):
        bps[key] = ax.boxplot(
            data[key],
            positions=positions[key],
            widths=box_width,
            patch_artist=True,
            showfliers=True,
        )
        color = colors[chip_name]
        for patch in bps[key]["boxes"]:
            patch.set_facecolor(color)
        for flier in bps[key]["fliers"]:
            flier.set_markerfacecolor(color)
            flier.set_markeredgecolor(color)

    tick_positions = [i * group_spacing for i, vg in enumerate(all_vg) if vg in tick_vg]
    tick_labels = [str(int(vg)) for vg in all_vg if vg in tick_vg]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_yticks([10, 0, -10, -20])

    ax.set_xlabel(r"Stress $V_G$ (V)")
    ax.set_ylabel(r"$\Delta$ CNP forward $V_G$ (V)")

    legend_patches = [
        plt.Line2D([0], [0], color=colors[c], lw=10, label=c)
        for c in ["CHIP1", "CHIP3", "CHIP4"]
    ]
    ax.legend(handles=legend_patches)

    return fig
