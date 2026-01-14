"""
This is a boilerplate pipeline 'CNP_calculations'
generated using Kedro 0.19.11
"""

import numpy as np
from typing import Dict, Callable
import pandas as pd


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
        props.loc[i, "delta_CNP_gate_voltage_forward"] = props.loc[i, "CNP_gate_voltage_forward"] - props.loc[i - 2, "CNP_gate_voltage_forward"]
        props.loc[i, "delta_CNP_drain_resistance_forward"] = props.loc[i, "CNP_drain_resistance_forward"] - props.loc[i - 2, "CNP_drain_resistance_forward"]
        # also for backward
        props.loc[i, "delta_CNP_gate_voltage_backward"] = props.loc[i, "CNP_gate_voltage_backward"] - props.loc[i - 2, "CNP_gate_voltage_backward"]
        props.loc[i, "delta_CNP_drain_resistance_backward"] = props.loc[i, "CNP_drain_resistance_backward"] - props.loc[i - 2, "CNP_drain_resistance_backward"]
    # Select those rows
    props = props.loc[previous_idx + next_idx]
    return props