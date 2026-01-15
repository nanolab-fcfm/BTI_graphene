"""
This is a boilerplate pipeline 'CNP_spatial_heatmaps'
generated using Kedro 0.19.11
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for headless execution
import matplotlib.pyplot as plt
import nanoplot as nplt
import numpy as np
import pandas as pd

nplt.apply()

# Maximum absolute delta CNP gate voltage (V) to include in plots (filter outliers)
DELTA_CNP_OUTLIER_THRESHOLD = 40


def create_cnp_shift_heatmap(
    *sample_props: pd.DataFrame,
    chip_name: str,
    sample_letters: list[str],
) -> plt.Figure:
    """
    Create a heatmap showing CNP shift per sample (X-axis, alphabetical order)
    and stress voltage (Y-axis). This visualizes whether spatial geometry
    affects the shifts.

    Args:
        *sample_props: DataFrames with CNP calculations after stress for each sample,
                       in the same order as sample_letters.
        chip_name: Name of the chip (e.g., "CHIP1") for the plot title.
        sample_letters: List of sample letters in order (e.g., ["A", "B", "C", ...]).

    Returns:
        matplotlib Figure object with the heatmap.
    """
    # Get all unique VG values across all samples
    all_vg = set()
    for props in sample_props:
        all_vg.update(props["VG"].dropna().unique())
    all_vg = sorted(all_vg)

    # Create a 2D array for the heatmap (VG x samples)
    # Each cell is the mean CNP shift for that sample at that VG
    heatmap_data = np.full((len(all_vg), len(sample_letters)), np.nan)

    for j, (props, letter) in enumerate(zip(sample_props, sample_letters)):
        # Filter out outliers
        props_filtered = props[
            props["delta_CNP_gate_voltage_forward"].abs() <= DELTA_CNP_OUTLIER_THRESHOLD
        ]

        for i, vg in enumerate(all_vg):
            vg_data = props_filtered[props_filtered["VG"] == vg][
                "delta_CNP_gate_voltage_forward"
            ].dropna()
            if len(vg_data) > 0:
                heatmap_data[i, j] = vg_data.mean()

    fig, ax = plt.subplots()

    # Create heatmap with diverging colormap centered at 0
    vmax = np.nanmax(np.abs(heatmap_data))
    im = ax.imshow(
        heatmap_data,
        aspect="auto",
        cmap="RdBu_r",
        vmin=-vmax,
        vmax=vmax,
    )

    # Set axis labels
    ax.set_xticks(range(len(sample_letters)))
    ax.set_xticklabels(sample_letters)
    ax.set_xlabel("Sample")

    ax.set_yticks(range(len(all_vg)))
    ax.set_yticklabels([f"{int(vg)}" for vg in all_vg])
    ax.set_ylabel(r"Stress $V_G$ (V)")

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(r"Mean $\Delta$ CNP forward $V_G$ (V)")

    return fig
