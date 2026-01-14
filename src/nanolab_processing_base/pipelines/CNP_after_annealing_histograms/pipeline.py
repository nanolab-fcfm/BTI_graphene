"""
This is a boilerplate pipeline 'CNP_after_annealing_histograms'
generated using Kedro 0.19.11
"""

from functools import partial

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_cnp_histogram, create_cnp_deviation_summary, create_cnp_deviation_histograms


def create_pipeline(**kwargs) -> Pipeline:
    # Define all samples for each chip (excluding removed samples: 3E, 4F)
    samples = {
        "CHIP1": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        "CHIP3": ["A", "B", "C", "D", "F", "G", "H", "I", "J"],  # E removed
        "CHIP4": ["A", "B", "C", "D", "E", "G", "H", "I", "J"],  # F removed
    }

    nodes = []

    # Build list of all sample names and inputs for summary plot
    all_sample_names = []
    all_inputs = []

    for chip, letters in samples.items():
        for letter in letters:
            sample_name = f"{chip}{letter}"
            all_sample_names.append(sample_name)
            all_inputs.append(f"properties_project_{sample_name}_with_CNPs")

            nodes.append(
                node(
                    func=partial(create_cnp_histogram, sample_name=sample_name),
                    inputs=f"properties_project_{sample_name}_with_CNPs",
                    outputs=f"cnp_after_annealing_histogram_{sample_name}",
                    name=f"create_cnp_histogram_{sample_name}",
                )
            )

    # Add summary plot node
    nodes.append(
        node(
            func=partial(create_cnp_deviation_summary, sample_names=all_sample_names),
            inputs=all_inputs,
            outputs="cnp_after_annealing_deviation_summary",
            name="create_cnp_deviation_summary",
        )
    )

    # Add deviation histograms node
    nodes.append(
        node(
            func=partial(create_cnp_deviation_histograms, sample_names=all_sample_names),
            inputs=all_inputs,
            outputs="cnp_after_annealing_deviation_histograms",
            name="create_cnp_deviation_histograms",
        )
    )

    return pipeline(nodes)
