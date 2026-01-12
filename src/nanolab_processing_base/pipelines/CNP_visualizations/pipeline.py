"""
This is a boilerplate pipeline 'CNP_visualizations'
generated using Kedro 0.19.11
"""

from functools import partial

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    create_forward_cnp_boxplot_chip,
    create_forward_cnp_boxplot_comparison,
)


def create_pipeline(**kwargs) -> Pipeline:
    # Define sample letters for each chip (excluding removed samples: 3E, 4F)
    chip1_samples = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
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

    return pipeline(nodes)
