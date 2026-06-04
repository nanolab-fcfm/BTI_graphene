"""
Stability analysis pipeline.
"""

from functools import partial

from kedro.pipeline import node, Pipeline, pipeline

from .nodes import (
    get_stability_CNPs,
    create_stability_plot,
    get_stability_CNPs_new,
    create_stability_plot_new,
    create_stability_plot_dual,
    fit_double_exponential,
    create_double_exp_fit_plot,
    fit_stretched_exponential,
    create_stretched_exp_fit_plot,
)


def create_pipeline(**kwargs) -> Pipeline:
    CHIP3G = pipeline(
        [
            node(
                func=get_stability_CNPs,
                inputs="stability_raw_CHIP3G",
                outputs="stability_cnp_CHIP3G",
                name="stability_cnp_CHIP3G",
            ),
            node(
                func=partial(create_stability_plot, stress_label="-40 V"),
                inputs="stability_cnp_CHIP3G",
                outputs="stability_plot_CHIP3G",
                name="stability_plot_CHIP3G",
            ),
        ]
    )

    CHIP3G_stability_2 = pipeline(
        [
            node(
                func=partial(get_stability_CNPs, cnp_abs_limit=50.0),
                inputs="stability_raw_CHIP3G_stability_2",
                outputs="stability_cnp_CHIP3G_stability_2",
                name="stability_cnp_CHIP3G_stability_2",
            ),
            node(
                func=partial(create_stability_plot, t_max_h=50.0, y_lim=(3, 5), stress_label="+40 V"),
                inputs="stability_cnp_CHIP3G_stability_2",
                outputs="stability_plot_CHIP3G_stability_2",
                name="stability_plot_CHIP3G_stability_2",
            ),
        ]
    )

    CHIP3G_stability_new = pipeline(
        [
            node(
                func=get_stability_CNPs_new,
                inputs="stability_raw_CHIP3G_stability_new",
                outputs="stability_cnp_CHIP3G_stability_new",
                name="stability_cnp_CHIP3G_stability_new",
            ),
            node(
                func=partial(create_stability_plot_new, stress_label="+40 V"),
                inputs="stability_cnp_CHIP3G_stability_new",
                outputs="stability_plot_CHIP3G_stability_new",
                name="stability_plot_CHIP3G_stability_new",
            ),
            node(
                func=fit_double_exponential,
                inputs="stability_cnp_CHIP3G_stability_new",
                outputs="stability_fit_params_CHIP3G_stability_new",
                name="stability_fit_params_CHIP3G_stability_new",
            ),
            node(
                func=partial(create_double_exp_fit_plot, stress_label="+40 V"),
                inputs=["stability_cnp_CHIP3G_stability_new", "stability_fit_params_CHIP3G_stability_new"],
                outputs="stability_fit_plot_CHIP3G_stability_new",
                name="stability_fit_plot_CHIP3G_stability_new",
            ),
            node(
                func=fit_stretched_exponential,
                inputs="stability_cnp_CHIP3G_stability_new",
                outputs="stability_stretched_fit_params_CHIP3G_stability_new",
                name="stability_stretched_fit_params_CHIP3G_stability_new",
            ),
            node(
                func=partial(create_stretched_exp_fit_plot, stress_label="+40 V"),
                inputs=["stability_cnp_CHIP3G_stability_new", "stability_stretched_fit_params_CHIP3G_stability_new"],
                outputs="stability_stretched_fit_plot_CHIP3G_stability_new",
                name="stability_stretched_fit_plot_CHIP3G_stability_new",
            ),
            node(
                func=get_stability_CNPs_new,
                inputs="stability_raw_CHIP3G_stability_new_minus40",
                outputs="stability_cnp_CHIP3G_stability_new_minus40",
                name="stability_cnp_CHIP3G_stability_new_minus40",
            ),
            node(
                func=create_stability_plot_dual,
                inputs=[
                    "stability_cnp_CHIP3G_stability_new",
                    "stability_cnp_CHIP3G_stability_new_minus40",
                ],
                outputs="stability_plot_CHIP3G_stability_new_dual",
                name="stability_plot_CHIP3G_stability_new_dual",
            ),
        ]
    )

    return (
        pipeline(CHIP3G, tags="stability")
        + pipeline(CHIP3G_stability_2, tags="stability")
        + pipeline(CHIP3G_stability_new, tags="stability")
    )
