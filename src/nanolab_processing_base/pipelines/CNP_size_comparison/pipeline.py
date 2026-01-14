"""
This is a boilerplate pipeline 'CNP_size_comparison'
generated using Kedro 0.19.11
"""

from functools import partial

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_mean_shift_by_size_plot


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

    # All inputs as flat list
    all_inputs = chip1_inputs + chip3_inputs + chip4_inputs

    nodes = [
        node(
            func=partial(
                create_mean_shift_by_size_plot,
                chip1_samples=chip1_samples,
                chip3_samples=chip3_samples,
                chip4_samples=chip4_samples,
            ),
            inputs=all_inputs,
            outputs="mean_shift_by_size_plot",
            name="create_mean_shift_by_size_plot",
        ),
    ]

    return pipeline(nodes)
