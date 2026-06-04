"""
Stability analysis pipeline nodes.

Processes VVgCooldown files: for files with >2 unique sweep repetitions,
computes the forward CNP voltage per sweep and returns a time-series DataFrame.
"""

from typing import Dict, Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def _get_forward(df: pd.DataFrame) -> pd.DataFrame:
    fwd = df["Vg (V)"].diff() > 0
    return df[fwd | fwd.shift(-1, fill_value=False)]


def _get_CNP(df: pd.DataFrame):
    df = df.sort_values("VDS (V)", ascending=False).head(5)
    if len(df) < 5:
        return None
    fit = np.polyfit(df["Vg (V)"], df["VDS (V)"], 2)
    return -fit[1] / (2 * fit[0])


def get_stability_CNPs(
    data: Dict[str, Callable], cnp_abs_limit: float | None = None
) -> pd.DataFrame:
    """
    For each VVgCooldown file with >2 unique sweeps_num values,
    compute the forward CNP for each sweep.

    Args:
        data: Partitioned dataset dict {key: callable} where each callable
              returns (props_dict, data_df).
        cnp_abs_limit: If set, discard sweeps where |CNP| > cnp_abs_limit (V).

    Returns:
        DataFrame with columns: t_elapsed_s (sweeps_num * Inter-sweep wait),
        CNP_gate_voltage_forward, sweeps_num, source_key.
    """
    records = []

    for key, experiment_callable in data.items():
        try:
            props, df = experiment_callable()
        except Exception:
            result = experiment_callable
            if isinstance(result, tuple):
                props, df = result
            else:
                continue

        if "sweeps_num" not in df.columns:
            continue

        unique_sweeps = df["sweeps_num"].dropna().unique()
        if len(unique_sweeps) <= 2:
            continue

        inter_sweep_wait = props.get("Inter-sweep wait", 0)
        cumulative_duration = 0.0

        for sweep_num in sorted(unique_sweeps):
            sweep_df = df[df["sweeps_num"] == sweep_num].copy()
            duration = sweep_df["t (s)"].max()

            fwd = _get_forward(sweep_df)
            cnp = _get_CNP(fwd)
            if cnp is not None and (cnp_abs_limit is None or abs(cnp) <= cnp_abs_limit):
                t_elapsed_h = (int(sweep_num) * inter_sweep_wait + cumulative_duration) / 3600
                records.append({
                    "t_elapsed_s": t_elapsed_h,
                    "CNP_gate_voltage_forward": cnp,
                    "sweeps_num": int(sweep_num),
                    "source_key": key,
                })

            cumulative_duration += duration

    result = pd.DataFrame(records)
    if not result.empty:
        result = result.sort_values("t_elapsed_s").reset_index(drop=True)
    return result


def get_stability_CNPs_new(
    data: Dict[str, Callable], cnp_abs_limit: float | None = None
) -> pd.DataFrame:
    """
    Like get_stability_CNPs but for files where t(s) is monotonically increasing
    across all sweeps (not reset per sweep). Uses sweep_num column.

    Absolute time = Start Time (Unix) + first t(s) of each sweep.
    All files are anchored to the earliest Start Time so elapsed hours
    start at 0 for the first file regardless of how many files there are.
    """
    # First pass: load all valid files and index them by (date, start_ts)
    candidates: dict[str, tuple] = {}  # key -> (start_ts, props, df)

    for key, experiment_callable in data.items():
        try:
            props, df = experiment_callable()
        except Exception:
            result = experiment_callable
            if isinstance(result, tuple):
                props, df = result
            else:
                continue

        if "sweep_num" not in df.columns:
            continue

        start_ts = props.get("Start time", 0)
        if hasattr(start_ts, "timestamp"):
            start_ts = start_ts.timestamp()
        else:
            start_ts = float(start_ts)

        import datetime as _dt
        date = _dt.datetime.fromtimestamp(start_ts).date()

        # Keep only the last (highest start_ts) VVgCooldown per calendar date
        if date not in {_dt.datetime.fromtimestamp(v[0]).date() for v in candidates.values()} \
                or start_ts > max((v[0] for v in candidates.values()
                                   if _dt.datetime.fromtimestamp(v[0]).date() == date),
                                  default=-1):
            candidates[key] = (start_ts, props, df)

    # Deduplicate: for each date keep only the latest
    by_date: dict = {}
    import datetime as _dt2
    for key, (start_ts, props, df) in candidates.items():
        date = _dt2.datetime.fromtimestamp(start_ts).date()
        if date not in by_date or start_ts > by_date[date][0]:
            by_date[date] = (start_ts, props, df, key)

    # Second pass: extract CNPs from the selected files
    records = []
    for date, (start_ts, props, df, key) in by_date.items():
        unique_sweeps = df["sweep_num"].dropna().unique()
        for sweep_num in sorted(unique_sweeps):
            sweep_df = df[df["sweep_num"] == sweep_num].copy()
            fwd = _get_forward(sweep_df)
            cnp = _get_CNP(fwd)
            if cnp is None:
                continue
            if cnp_abs_limit is not None and abs(cnp) > cnp_abs_limit:
                continue

            abs_t = start_ts + sweep_df["t (s)"].iloc[0]
            records.append({
                "abs_t": abs_t,
                "CNP_gate_voltage_forward": cnp,
                "sweep_num": int(sweep_num),
                "source_key": key,
            })

    result = pd.DataFrame(records)
    if not result.empty:
        result = result.sort_values("abs_t").reset_index(drop=True)
        t0 = result["abs_t"].iloc[0]
        result["t_elapsed_h"] = (result["abs_t"] - t0) / 3600
        result = result.drop(columns="abs_t")
    return result


def create_stability_plot_new(
    cnp_df: pd.DataFrame, stress_label: str | None = None
) -> plt.Figure:
    """Plot CNP forward gate voltage vs elapsed time (h) for new-format stability data."""
    fig, ax = plt.subplots()

    t = cnp_df["t_elapsed_h"]
    cnp = cnp_df["CNP_gate_voltage_forward"]

    ax.scatter(t, cnp, s=16)
    ax.set_xlabel("Elapsed time (h)")
    ax.set_ylabel(r"CNP forward $V_G$ (V)")

    sources = ", ".join(f"{s}.csv" for s in sorted(cnp_df["source_key"].astype(str).unique()))
    heading = f"CNP recovery after {stress_label} stress" if stress_label else "CNP recovery"
    ax.set_title(f"{heading}\nsource: {sources}", fontsize=9)

    fig.tight_layout()

    return fig


def create_stability_plot_dual(
    cnp_plus: pd.DataFrame, cnp_minus: pd.DataFrame
) -> plt.Figure:
    """Plot CNP-vs-time recovery for +40 V (left axis) and -40 V (right axis) stresses.

    Both axes use the same ΔV span (driven by the larger drift) and are anchored to
    each curve's own first point, so the two recoveries are directly comparable.
    """
    fig, ax_minus = plt.subplots()

    cnp_plus = cnp_plus.sort_values("t_elapsed_h")
    cnp_minus = cnp_minus.sort_values("t_elapsed_h")

    start_plus = cnp_plus["CNP_gate_voltage_forward"].iloc[0]
    start_minus = cnp_minus["CNP_gate_voltage_forward"].iloc[0]
    span_plus = start_plus - cnp_plus["CNP_gate_voltage_forward"].min()
    span_minus = start_minus - cnp_minus["CNP_gate_voltage_forward"].min()
    span = max(span_plus, span_minus)
    margin = span * 0.05

    color_minus = "tab:red"
    ax_minus.scatter(
        cnp_minus["t_elapsed_h"],
        cnp_minus["CNP_gate_voltage_forward"],
        s=16,
        color=color_minus,
        label="-40 V",
    )
    ax_minus.set_xlabel("Elapsed time (h)")
    ax_minus.set_ylabel("CNP evolution after -40 V stress (V)", color=color_minus)
    ax_minus.tick_params(axis="y", labelcolor=color_minus)
    ax_minus.set_ylim(start_minus - span - margin, start_minus + margin)

    color_plus = "tab:blue"
    ax_plus = ax_minus.twinx()
    ax_plus.scatter(
        cnp_plus["t_elapsed_h"],
        cnp_plus["CNP_gate_voltage_forward"],
        s=16,
        color=color_plus,
        label="+40 V",
    )
    ax_plus.set_ylabel("CNP evolution after +40 V stress (V)", color=color_plus)
    ax_plus.tick_params(axis="y", labelcolor=color_plus)
    ax_plus.set_ylim(start_plus - span - margin, start_plus + margin)

    src_plus = ", ".join(f"{s}.csv" for s in sorted(cnp_plus["source_key"].astype(str).unique()))
    src_minus = ", ".join(f"{s}.csv" for s in sorted(cnp_minus["source_key"].astype(str).unique()))
    ax_plus.set_title(
        "CNP recovery after gate stress\n"
        f"+40 V source: {src_plus}\n-40 V source: {src_minus}",
        fontsize=8,
    )

    fig.tight_layout()

    return fig


def _stretched_exp(t, A, tau, beta, C):
    return A * np.exp(-((t / tau) ** beta)) + C


def fit_stretched_exponential(cnp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fit CNP(t) = A * exp(-(t/tau)^beta) + C (Kohlrausch / KWW stretched exponential).

    Returns a single-row DataFrame with fit parameters and uncertainties.
    """
    t = cnp_df["t_elapsed_h"].values
    cnp = cnp_df["CNP_gate_voltage_forward"].values

    C0 = cnp[-1]
    A0 = cnp[0] - C0

    p0 = [A0, 50.0, 0.5, C0]
    bounds = (
        [0,   0.1, 0.01, -np.inf],
        [np.inf, np.inf, 1.0,  np.inf],
    )

    popt, pcov = curve_fit(_stretched_exp, t, cnp, p0=p0, bounds=bounds, maxfev=10000)
    perr = np.sqrt(np.diag(pcov))

    return pd.DataFrame({
        "parameter": ["A", "tau", "beta", "C"],
        "value": popt,
        "uncertainty": perr,
    })


def create_stretched_exp_fit_plot(
    cnp_df: pd.DataFrame, fit_params: pd.DataFrame, stress_label: str | None = None
) -> plt.Figure:
    """Scatter plot of CNP data with the stretched-exponential fit overlaid."""
    t = cnp_df["t_elapsed_h"].values
    cnp = cnp_df["CNP_gate_voltage_forward"].values

    params = fit_params.set_index("parameter")["value"]
    unc = fit_params.set_index("parameter")["uncertainty"]
    popt = [params["A"], params["tau"], params["beta"], params["C"]]

    t_fit = np.linspace(t.min(), t.max(), 2000)
    cnp_fit = _stretched_exp(t_fit, *popt)

    fig, ax = plt.subplots()
    ax.scatter(t, cnp, s=4, alpha=0.4, label="data")
    ax.plot(t_fit, cnp_fit, color="red", linewidth=1.5, label="stretched exp fit")

    annotation = (
        f"$A$ = {params['A']:.4f} ± {unc['A']:.4f} V\n"
        f"$\\tau$ = {params['tau']:.2f} ± {unc['tau']:.2f} h\n"
        f"$\\beta$ = {params['beta']:.4f} ± {unc['beta']:.4f}\n"
        f"$C$ = {params['C']:.4f} ± {unc['C']:.4f} V"
    )
    ax.text(
        0.97, 0.97, annotation,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8),
    )

    ax.legend()
    ax.set_xlabel("Elapsed time (h)")
    ax.set_ylabel(r"CNP forward $V_G$ (V)")
    sources = ", ".join(f"{s}.csv" for s in sorted(cnp_df["source_key"].astype(str).unique()))
    heading = f"Stretched-exp fit — CNP recovery after {stress_label} stress" if stress_label else "Stretched-exp fit"
    ax.set_title(f"{heading}\nsource: {sources}", fontsize=9)
    fig.tight_layout()

    return fig


def _double_exp(t, A1, tau1, A2, tau2, C):
    return A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) + C


def fit_double_exponential(cnp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fit CNP(t) = A1*exp(-t/tau1) + A2*exp(-t/tau2) + C to the stability data.

    Returns a single-row DataFrame with the fit parameters and their uncertainties.
    """
    t = cnp_df["t_elapsed_h"].values
    cnp = cnp_df["CNP_gate_voltage_forward"].values

    C0 = cnp[-1]
    amp0 = cnp[0] - C0

    p0 = [amp0 * 0.6, 5.0, amp0 * 0.4, 100.0, C0]
    bounds = (
        [0,   0.1,  0,   1.0,  -np.inf],
        [np.inf, np.inf, np.inf, np.inf,  np.inf],
    )

    popt, pcov = curve_fit(_double_exp, t, cnp, p0=p0, bounds=bounds, maxfev=10000)
    perr = np.sqrt(np.diag(pcov))

    labels = ["A1", "tau1", "A2", "tau2", "C"]
    return pd.DataFrame({
        "parameter": labels,
        "value": popt,
        "uncertainty": perr,
    })


def create_double_exp_fit_plot(
    cnp_df: pd.DataFrame, fit_params: pd.DataFrame, stress_label: str | None = None
) -> plt.Figure:
    """
    Scatter plot of CNP data with the double-exponential fit overlaid.
    Fit parameters and uncertainties are annotated on the plot.
    """
    t = cnp_df["t_elapsed_h"].values
    cnp = cnp_df["CNP_gate_voltage_forward"].values

    params = fit_params.set_index("parameter")["value"]
    popt = [params["A1"], params["tau1"], params["A2"], params["tau2"], params["C"]]

    t_fit = np.linspace(t.min(), t.max(), 2000)
    cnp_fit = _double_exp(t_fit, *popt)

    fig, ax = plt.subplots()
    ax.scatter(t, cnp, s=4, alpha=0.4, label="data")
    ax.plot(t_fit, cnp_fit, color="red", linewidth=1.5, label="double exp fit")

    unc = fit_params.set_index("parameter")["uncertainty"]
    annotation = (
        f"$A_1$ = {params['A1']:.4f} ± {unc['A1']:.4f} V\n"
        f"$\\tau_1$ = {params['tau1']:.2f} ± {unc['tau1']:.2f} h\n"
        f"$A_2$ = {params['A2']:.4f} ± {unc['A2']:.4f} V\n"
        f"$\\tau_2$ = {params['tau2']:.2f} ± {unc['tau2']:.2f} h\n"
        f"$C$ = {params['C']:.4f} ± {unc['C']:.4f} V"
    )
    ax.text(
        0.97, 0.97, annotation,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8),
    )

    ax.legend()
    ax.set_xlabel("Elapsed time (h)")
    ax.set_ylabel(r"CNP forward $V_G$ (V)")
    sources = ", ".join(f"{s}.csv" for s in sorted(cnp_df["source_key"].astype(str).unique()))
    heading = f"Double-exp fit — CNP recovery after {stress_label} stress" if stress_label else "Double-exp fit"
    ax.set_title(f"{heading}\nsource: {sources}", fontsize=9)
    fig.tight_layout()

    return fig


_OUTLIER_T_MIN = 125  # h — start of outlier-detection window
_OUTLIER_T_MAX = 150  # h — end of outlier-detection window
_OUTLIER_N = 5        # number of top-residual points to flag


def _flag_outliers(t: pd.Series, cnp: pd.Series) -> pd.Series:
    """Return a boolean mask: True for the _OUTLIER_N points inside
    [_OUTLIER_T_MIN, _OUTLIER_T_MAX] with the largest absolute residual
    from a linear regression fit on that interval.
    """
    mask = pd.Series(False, index=t.index)
    window = (t >= _OUTLIER_T_MIN) & (t <= _OUTLIER_T_MAX)
    if window.sum() < _OUTLIER_N + 2:
        return mask

    t_w = t[window].values
    cnp_w = cnp[window].values
    coeffs = np.polyfit(t_w, cnp_w, 1)
    residuals = np.abs(cnp_w - np.polyval(coeffs, t_w))

    top_idx = window[window].index[np.argsort(residuals)[-_OUTLIER_N:]]
    mask.loc[top_idx] = True
    return mask


def create_stability_plot(
    cnp_df: pd.DataFrame,
    t_max_h: float | None = None,
    y_lim: tuple | None = None,
    stress_label: str | None = None,
) -> plt.Figure:
    """
    Plot CNP forward gate voltage as a function of time.
    The 5 points in [125 h, 150 h] with the largest linear-regression residuals
    are excluded from the plot.

    Args:
        cnp_df: DataFrame from get_stability_CNPs.

    Returns:
        matplotlib Figure.
    """
    fig, ax = plt.subplots()

    plot_df = cnp_df if t_max_h is None else cnp_df[cnp_df["t_elapsed_s"] <= t_max_h]
    t = plot_df["t_elapsed_s"]
    cnp = plot_df["CNP_gate_voltage_forward"]
    is_outlier = _flag_outliers(t, cnp)

    ax.scatter(t[~is_outlier], cnp[~is_outlier], s=16)

    if y_lim is not None:
        ax.set_ylim(y_lim)

    ax.set_xlabel("Elapsed time (h)")
    ax.set_ylabel(r"CNP forward $V_G$ (V)")
    sources = ", ".join(f"{s}.csv" for s in sorted(cnp_df["source_key"].astype(str).unique()))
    heading = f"CNP recovery after {stress_label} stress" if stress_label else "CNP recovery"
    ax.set_title(f"{heading}\nsource: {sources}", fontsize=9)
    fig.tight_layout()

    return fig
