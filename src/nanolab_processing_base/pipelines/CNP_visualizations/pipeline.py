"""
This is a boilerplate pipeline 'CNP_visualizations'
generated using Kedro 0.19.11
"""

from functools import partial

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    create_forward_cnp_boxplot_chip,
    create_forward_cnp_boxplot_comparison,
    create_forward_cnp_boxplot_baseline_comparison,
    create_baseline_vs_nonbaseline_chip,
    create_baseline_vs_nonbaseline_all,
)



def create_pipeline(**kwargs) -> Pipeline:
    # Define sample letters for each chip (excluding removed samples: 3E, 4F)
    chip1_samples = ["A", "B", "C", "D", "E", "F", "G", "H"]  # I, J removed (faulty)
    chip3_samples = ["A", "B", "C", "D", "F", "G", "H", "I", "J"]  # E removed
    chip4_samples = ["A", "B", "C", "D", "E", "G", "H", "I", "J"]  # F removed

    # Create input lists for each chip
    chip1_inputs = [
        f"properties_project_CHIP1{s}_with_CNPs_after_stress" for s in chip1_samples
    ]
    chip3_inputs = [
        f"properties_project_CHIP3{s}_with_CNPs_after_stress" for s in chip3_samples
    ]
    chip4_inputs = [
        f"properties_project_CHIP4{s}_with_CNPs_after_stress" for s in chip4_samples
    ]

    # For comparison plot: all inputs as flat list with counts to split them
    all_inputs = chip1_inputs + chip3_inputs + chip4_inputs
    chip1_count = len(chip1_inputs)
    chip3_count = len(chip3_inputs)

    nodes = [
        # Individual chip boxplots
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP1"),
            inputs=chip1_inputs,
            outputs="forward_cnp_boxplot_CHIP1",
            name="create_forward_cnp_boxplot_CHIP1",
        ),
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP3"),
            inputs=chip3_inputs,
            outputs="forward_cnp_boxplot_CHIP3",
            name="create_forward_cnp_boxplot_CHIP3",
        ),
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP4"),
            inputs=chip4_inputs,
            outputs="forward_cnp_boxplot_CHIP4",
            name="create_forward_cnp_boxplot_CHIP4",
        ),
        # Comparison boxplot (all chips side by side per VG)
        node(
            func=partial(
                create_forward_cnp_boxplot_comparison,
                chip1_count=chip1_count,
                chip3_count=chip3_count,
            ),
            inputs=all_inputs,
            outputs="forward_cnp_boxplot_comparison",
            name="create_forward_cnp_boxplot_comparison",
        ),
    ]

    # --- Baseline visualization nodes (CHIP2 excluded from study) ---
    chip1_baseline_samples = list("ABCDEFGH")  # I, J removed (faulty)
    chip3_baseline_samples = list("ABCDFGHIJ")  # 3E removed (faulty)
    chip4_baseline_samples = list("ABCDEGHIJ")  # 4F excluded (not in non-baseline)

    chip1_baseline_inputs = [
        f"properties_project_CHIP1{s}_baseline_with_CNPs_after_stress"
        for s in chip1_baseline_samples
    ]
    chip3_baseline_inputs = [
        f"properties_project_CHIP3{s}_baseline_with_CNPs_after_stress"
        for s in chip3_baseline_samples
    ]
    chip4_baseline_inputs = [
        f"properties_project_CHIP4{s}_baseline_with_CNPs_after_stress"
        for s in chip4_baseline_samples
    ]

    all_baseline_inputs = chip1_baseline_inputs + chip3_baseline_inputs + chip4_baseline_inputs

    baseline_nodes = [
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP1_baseline"),
            inputs=chip1_baseline_inputs,
            outputs="forward_cnp_boxplot_CHIP1_baseline",
            name="create_forward_cnp_boxplot_CHIP1_baseline",
        ),
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP3_baseline"),
            inputs=chip3_baseline_inputs,
            outputs="forward_cnp_boxplot_CHIP3_baseline",
            name="create_forward_cnp_boxplot_CHIP3_baseline",
        ),
        node(
            func=partial(create_forward_cnp_boxplot_chip, chip_name="CHIP4_baseline"),
            inputs=chip4_baseline_inputs,
            outputs="forward_cnp_boxplot_CHIP4_baseline",
            name="create_forward_cnp_boxplot_CHIP4_baseline",
        ),
        node(
            func=partial(
                create_forward_cnp_boxplot_baseline_comparison,
                chip1_count=len(chip1_baseline_inputs),
                chip3_count=len(chip3_baseline_inputs),
            ),
            inputs=all_baseline_inputs,
            outputs="forward_cnp_boxplot_baseline_comparison",
            name="create_forward_cnp_boxplot_baseline_comparison",
        ),
    ]

    # --- Baseline vs non-baseline comparison nodes ---
    comparison_nodes = [
        node(
            func=partial(
                create_baseline_vs_nonbaseline_chip,
                chip_name="CHIP1",
                baseline_count=len(chip1_baseline_inputs),
            ),
            inputs=chip1_baseline_inputs + chip1_inputs,
            outputs="baseline_vs_nonbaseline_CHIP1",
            name="baseline_vs_nonbaseline_CHIP1",
        ),
        node(
            func=partial(
                create_baseline_vs_nonbaseline_chip,
                chip_name="CHIP3",
                baseline_count=len(chip3_baseline_inputs),
            ),
            inputs=chip3_baseline_inputs + chip3_inputs,
            outputs="baseline_vs_nonbaseline_CHIP3",
            name="baseline_vs_nonbaseline_CHIP3",
        ),
        node(
            func=partial(
                create_baseline_vs_nonbaseline_chip,
                chip_name="CHIP4",
                baseline_count=len(chip4_baseline_inputs),
            ),
            inputs=chip4_baseline_inputs + chip4_inputs,
            outputs="baseline_vs_nonbaseline_CHIP4",
            name="baseline_vs_nonbaseline_CHIP4",
        ),
        node(
            func=partial(
                create_baseline_vs_nonbaseline_all,
                chip1_baseline_count=len(chip1_baseline_inputs),
                chip3_baseline_count=len(chip3_baseline_inputs),
                chip4_baseline_count=len(chip4_baseline_inputs),
                chip1_nonbaseline_count=len(chip1_inputs),
                chip3_nonbaseline_count=len(chip3_inputs),
            ),
            inputs=(
                chip1_baseline_inputs
                + chip3_baseline_inputs
                + chip4_baseline_inputs
                + chip1_inputs
                + chip3_inputs
                + chip4_inputs
            ),
            outputs="baseline_vs_nonbaseline_all",
            name="baseline_vs_nonbaseline_all",
        ),
    ]

    return (
        pipeline(nodes, tags="non_baseline")
        + pipeline(baseline_nodes, tags="baseline")
        + pipeline(comparison_nodes, tags=["baseline", "non_baseline", "comparison"])
    )
