"""
This is a boilerplate pipeline 'CNP_spatial_heatmaps'
generated using Kedro 0.19.11
"""

from functools import partial

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_cnp_shift_heatmap


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

    nodes = [
        node(
            func=partial(
                create_cnp_shift_heatmap,
                chip_name="CHIP1",
                sample_letters=chip1_samples,
            ),
            inputs=chip1_inputs,
            outputs="cnp_shift_heatmap_CHIP1",
            name="create_cnp_shift_heatmap_CHIP1",
        ),
        node(
            func=partial(
                create_cnp_shift_heatmap,
                chip_name="CHIP3",
                sample_letters=chip3_samples,
            ),
            inputs=chip3_inputs,
            outputs="cnp_shift_heatmap_CHIP3",
            name="create_cnp_shift_heatmap_CHIP3",
        ),
        node(
            func=partial(
                create_cnp_shift_heatmap,
                chip_name="CHIP4",
                sample_letters=chip4_samples,
            ),
            inputs=chip4_inputs,
            outputs="cnp_shift_heatmap_CHIP4",
            name="create_cnp_shift_heatmap_CHIP4",
        ),
    ]

    return pipeline(nodes)
