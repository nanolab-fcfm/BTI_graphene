"""
This is a boilerplate pipeline 'CNP_first_last_comparison'
generated using Kedro 0.19.11
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_first_last_resistance_plot


def create_pipeline(**kwargs) -> Pipeline:
    nodes = [
        node(
            func=create_first_last_resistance_plot,
            inputs=["project_CHIP3A", "properties_project_CHIP3A_with_CNPs"],
            outputs="first_last_resistance_plot_CHIP3A",
            name="create_first_last_resistance_plot_CHIP3A",
        ),
    ]

    return pipeline(nodes)
