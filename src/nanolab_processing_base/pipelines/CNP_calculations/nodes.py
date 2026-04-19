"""
This is a boilerplate pipeline 'CNP_calculations'
generated using Kedro 0.19.11
"""

import os
import numpy as np
from typing import Dict, Callable
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle


def normalize_key(key: str) -> str:
    """Normalize path separators to forward slashes for cross-platform compatibility."""
    return key.replace("\\", "/")


def get_forward(df):
    forward = df["Vg (V)"].diff() > 0
    return df[forward | forward.shift(-1, fill_value=False)]

def get_backward(df):
    dv = df["Vg (V)"].diff()
    mask = (dv < 0) | (dv.shift(-1) < 0)
    out = df[mask]
    return out.sort_values(by="Vg (V)")


def get_CNP(df):
    """
    This function fits a parabola to the 8 highest VDS (V) values and returns the CNP voltage and the corresponding Vg (V) value.
    """
    df = df.sort_values(by="VDS (V)", ascending=False)
    df = df.head(8)

    # fit a parabola to the 8 highest VDS (V) values
    fit = np.polyfit(df["Vg (V)"], df["VDS (V)"], 2)
    
    a_coef, b_coef, _ = fit
    CNP_gate_voltage = -b_coef / (2 * a_coef)
    CNP_drain_voltage = np.polyval(fit, CNP_gate_voltage)
    return CNP_gate_voltage, CNP_drain_voltage


def get_partitioned_CNPs(data: Dict[str, Callable], props: pd.DataFrame) -> pd.DataFrame:

    # Normalize data_key column for cross-platform compatibility (handles backslashes from Windows)
    props["data_key"] = props["data_key"].apply(normalize_key)
    
    # temporary set 'data_key' to be the index of the props dataframe, at the end of the function we will reset the index and set the column back to 'data_key'
    props = props.set_index("data_key")

    for key, experiment_callable in data.items():
        # Normalize the key to use forward slashes (cross-platform compatibility)
        normalized_key = normalize_key(key)
        # first we check that the experiment type is VVg
        if props.loc[normalized_key, "Procedure type"] != "VVg":
            continue
        try:
            df = experiment_callable()
        except:
            df = experiment_callable

        forward = get_forward(df)
        backward = get_backward(df)
        if len(forward) < 8 or len(backward) < 8:
            continue
        forward_CNP_gate_voltage, forward_CNP_drain_voltage = get_CNP(forward)
        backward_CNP_gate_voltage, backward_CNP_drain_voltage = get_CNP(backward)

        forward_CNP_drain_resistance = forward_CNP_drain_voltage / props.loc[normalized_key, "Drain-Source current"]
        backward_CNP_drain_resistance = backward_CNP_drain_voltage / props.loc[normalized_key, "Drain-Source current"]

        props.loc[normalized_key, "CNP_gate_voltage_forward"] = forward_CNP_gate_voltage
        props.loc[normalized_key, "CNP_drain_resistance_forward"] = forward_CNP_drain_resistance
        props.loc[normalized_key, "CNP_gate_voltage_backward"] = backward_CNP_gate_voltage
        props.loc[normalized_key, "CNP_drain_resistance_backward"] = backward_CNP_drain_resistance
    
    props.reset_index(inplace=True)
        
    return props


_BASELINE_PLOTS_DIR = "data/08_reporting/baseline_diagnostics"
_CNP_JUMP_THRESHOLD = 5.0  # V


def get_partitioned_CNPs_baseline(
    data: Dict[str, Callable], props: pd.DataFrame
) -> pd.DataFrame:
    """
    Like get_partitioned_CNPs but also saves diagnostic figures whenever
    consecutive VVg sweeps (sorted by start time) show a forward-CNP jump
    larger than _CNP_JUMP_THRESHOLD.

    One figure per chip-sample execution; each subplot shows one offending
    pair (before sweep vs after sweep overlaid), with a title containing
    all relevant metadata.
    """
    props = props.set_index("data_key")
    raw_dfs: dict[str, pd.DataFrame] = {}

    for key, experiment_callable in data.items():
        if props.loc[key, "Procedure type"] != "VVg":
            continue
        try:
            df = experiment_callable()
        except Exception:
            df = experiment_callable

        forward = get_forward(df)
        backward = get_backward(df)
        if len(forward) < 8 or len(backward) < 8:
            continue

        raw_dfs[key] = df

        forward_CNP_gate_voltage, forward_CNP_drain_voltage = get_CNP(forward)
        backward_CNP_gate_voltage, backward_CNP_drain_voltage = get_CNP(backward)

        forward_CNP_drain_resistance = (
            forward_CNP_drain_voltage / props.loc[key, "Drain-Source current"]
        )
        backward_CNP_drain_resistance = (
            backward_CNP_drain_voltage / props.loc[key, "Drain-Source current"]
        )

        props.loc[key, "CNP_gate_voltage_forward"] = forward_CNP_gate_voltage
        props.loc[key, "CNP_drain_resistance_forward"] = forward_CNP_drain_resistance
        props.loc[key, "CNP_gate_voltage_backward"] = backward_CNP_gate_voltage
        props.loc[key, "CNP_drain_resistance_backward"] = backward_CNP_drain_resistance

    # --- diagnostic: find consecutive VVg pairs with large CNP jumps ---
    if "CNP_gate_voltage_forward" not in props.columns:
        props.reset_index(inplace=True)
        return props
    vvg_props = (
        props[props["Procedure type"] == "VVg"]
        .dropna(subset=["CNP_gate_voltage_forward"])
    )
    vvg_props = vvg_props.sort_values("Start time")
    keys_sorted = [k for k in vvg_props.index if k in raw_dfs]

    pairs = []
    for i in range(len(keys_sorted) - 1):
        k1, k2 = keys_sorted[i], keys_sorted[i + 1]
        cnp1 = vvg_props.loc[k1, "CNP_gate_voltage_forward"]
        cnp2 = vvg_props.loc[k2, "CNP_gate_voltage_forward"]
        if abs(cnp2 - cnp1) > _CNP_JUMP_THRESHOLD:
            pairs.append((k1, k2, cnp1, cnp2))

    if pairs:
        _save_baseline_diagnostic_figure(pairs, raw_dfs, vvg_props)

    props.reset_index(inplace=True)
    return props


def _save_baseline_diagnostic_figure(pairs, raw_dfs, vvg_props):
    """Create one figure with one subplot per offending pair and save it as PNG."""
    os.makedirs(_BASELINE_PLOTS_DIR, exist_ok=True)

    n = len(pairs)
    with mplstyle.context("default"):
        fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n), squeeze=False)

        for ax, (k1, k2, cnp1, cnp2) in zip(axes[:, 0], pairs):
            df1 = raw_dfs[k1]
            df2 = raw_dfs[k2]

            ax.plot(df1["Vg (V)"], df1["VDS (V)"], color="steelblue", label="before")
            ax.axvline(cnp1, color="steelblue", linestyle="--", alpha=0.7)
            ax.plot(df2["Vg (V)"], df2["VDS (V)"], color="tomato", label="after")
            ax.axvline(cnp2, color="tomato", linestyle="--", alpha=0.7)
            ax.legend(fontsize=8)
            ax.set_xlabel("Vg (V)")
            ax.set_ylabel("VDS (V)")

            r1 = vvg_props.loc[k1]
            r2 = vvg_props.loc[k2]
            chip = f"Chip {r1.get('Chip number', '?')}{r1.get('Sample', '?')}"
            info1 = r1.get("Information", "") or ""
            info2 = r2.get("Information", "") or ""
            t1 = str(r1.get("Start time", ""))[:19]
            t2 = str(r2.get("Start time", ""))[:19]
            vg_range = f"VG [{r1.get('VG start','?')} to {r1.get('VG end','?')}] V"
            ids = f"keys: {k1}  |  {k2}"
            delta = cnp2 - cnp1
            title = (
                f"{chip}  |  dCNP_fwd = {delta:+.2f} V  "
                f"(before={cnp1:.2f} V, after={cnp2:.2f} V)\n"
                f"before: {t1}  info='{info1}'  {vg_range}\n"
                f"after:  {t2}  info='{info2}'\n"
                f"{ids}"
            )
            ax.set_title(title, fontsize=8, loc="left")

        fig.tight_layout()

        r = vvg_props.loc[pairs[0][0]]
        chip_tag = f"CHIP{r.get('Chip number', 'X')}{r.get('Sample', 'X')}_baseline"
        date_tag = str(pairs[0][0]).split("/")[0]
        filename = os.path.join(
            _BASELINE_PLOTS_DIR, f"diagnostic_{chip_tag}_{date_tag}.png"
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close(fig)


def after_stress_CNP_calculations(props: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a props and returns only the rows that are immediate before and after a stress experiment.
    """
    props = props.sort_values(by="Start time").copy()
    props["VG"] = props["VG"].ffill()
    # Find indices where "Procedure type" is "Stress"
    stress_idx = props.index[props["Procedure type"] == "Stress"]
    # Get the next row index after each "Stress" (if within bounds)
    previous_idx = [i - 1 for i in stress_idx if (i - 1) in props.index]
    next_idx = [i + 1 for i in stress_idx if (i + 1) in props.index]
    # for the rows that are after the stress, we add the value of the CNP values of that row minus the value of the CNP values of the previous row
    for i in next_idx:
        if (i - 2) not in props.index:
            continue
        props.loc[i, "delta_CNP_gate_voltage_forward"] = props.loc[i, "CNP_gate_voltage_forward"] - props.loc[i - 2, "CNP_gate_voltage_forward"]
        props.loc[i, "delta_CNP_drain_resistance_forward"] = props.loc[i, "CNP_drain_resistance_forward"] - props.loc[i - 2, "CNP_drain_resistance_forward"]
        # also for backward
        props.loc[i, "delta_CNP_gate_voltage_backward"] = props.loc[i, "CNP_gate_voltage_backward"] - props.loc[i - 2, "CNP_gate_voltage_backward"]
        props.loc[i, "delta_CNP_drain_resistance_backward"] = props.loc[i, "CNP_drain_resistance_backward"] - props.loc[i - 2, "CNP_drain_resistance_backward"]
    # Select those rows
    props = props.loc[previous_idx + next_idx]
    return props