"""
This is a boilerplate pipeline 'CNP_first_last_comparison'
generated using Kedro 0.19.11
"""

import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for headless execution
import matplotlib.pyplot as plt
import nanoplot as nplt
import pandas as pd
from typing import Dict, Callable

nplt.apply()


def normalize_key(key: str) -> str:
    """Normalize path separators to forward slashes for cross-platform compatibility."""
    return key.replace("\\", "/")


def get_forward(df: pd.DataFrame) -> pd.DataFrame:
    """Extract only the forward sweep from a VVg experiment."""
    forward = df["Vg (V)"].diff() > 0
    return df[forward | forward.shift(-1, fill_value=False)]


def get_after_annealing_vvg_keys(props: pd.DataFrame) -> list[str]:
    """
    Get the data_key values for VVg experiments that occur just before stress.
    These are the experiments "after annealing" - the baseline measurements
    before each stress cycle.

    Args:
        props: DataFrame with properties (must have 'Start time', 'Procedure type', 'data_key').

    Returns:
        List of data_key values for VVg rows immediately before stress experiments.
    """
    props = props.sort_values(by="Start time").reset_index(drop=True).copy()

    # Find indices where "Procedure type" is "Stress"
    stress_idx = props.index[props["Procedure type"] == "Stress"]

    # Get the row index just before each "Stress" (these are VVg after annealing)
    previous_idx = [i - 1 for i in stress_idx if (i - 1) in props.index]

    # Get the data_keys for these rows
    after_annealing_keys = props.loc[previous_idx, "data_key"].tolist()

    return after_annealing_keys


def create_first_last_resistance_plot(
    data: Dict[str, Callable],
    props: pd.DataFrame,
) -> plt.Figure:
    """
    Create a plot comparing the first and last VVg after annealing.
    Shows Resistance vs Vg for both experiments.

    Args:
        data: Partitioned dataset with raw VVg data.
        props: DataFrame with properties including 'Drain-Source current'.

    Returns:
        matplotlib Figure object with the comparison plot.
    """
    # Get the data_keys for VVg experiments after annealing
    after_annealing_keys = get_after_annealing_vvg_keys(props)

    if len(after_annealing_keys) < 2:
        # Not enough data to compare
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Not enough VVg after annealing data", 
                ha='center', va='center', transform=ax.transAxes)
        return fig

    # Get first and last keys
    first_key = after_annealing_keys[0]
    last_key = after_annealing_keys[-1]

    # Get drain-source current from props
    props = props.copy()
    props["data_key"] = props["data_key"].apply(normalize_key)
    props = props.set_index("data_key")

    first_current = props.loc[normalize_key(first_key), "Drain-Source current"]
    last_current = props.loc[normalize_key(last_key), "Drain-Source current"]

    # Load the raw data
    # NanoLabDataSet returns a tuple (props, data), we need the data (second element)
    first_df = None
    last_df = None

    for key, experiment_callable in data.items():
        normalized_key = normalize_key(key)
        if normalized_key == normalize_key(first_key):
            try:
                result = experiment_callable()
            except:
                result = experiment_callable
            # NanoLabDataSet returns (props, data) tuple
            first_df = result[1] if isinstance(result, tuple) else result
        elif normalized_key == normalize_key(last_key):
            try:
                result = experiment_callable()
            except:
                result = experiment_callable
            # NanoLabDataSet returns (props, data) tuple
            last_df = result[1] if isinstance(result, tuple) else result

    if first_df is None or last_df is None:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Could not load VVg data", 
                ha='center', va='center', transform=ax.transAxes)
        return fig

    # Get only forward sweep
    first_df = get_forward(first_df.copy())
    last_df = get_forward(last_df.copy())

    # Calculate resistance in kOhm: R = V / I = VDS / Drain-Source current
    first_df["Resistance"] = first_df["VDS (V)"] / first_current / 1000
    last_df["Resistance"] = last_df["VDS (V)"] / last_current / 1000

    fig, ax = plt.subplots()

    # Plot first VVg (after first annealing)
    ax.plot(
        first_df["Vg (V)"],
        first_df["Resistance"],
        label="First (after annealing)",
    )

    # Plot last VVg (after last annealing)
    ax.plot(
        last_df["Vg (V)"],
        last_df["Resistance"],
        label="Last (after annealing)",
    )

    ax.set_xlabel(r"$V_G$ (V)")
    ax.set_ylabel(r"Resistance (k$\Omega$)")
    ax.legend()

    return fig
