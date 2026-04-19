"""
This is a boilerplate pipeline 'CNP_calculations'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa

from .nodes import get_partitioned_CNPs, get_partitioned_CNPs_baseline, after_stress_CNP_calculations


def create_pipeline(**kwargs) -> Pipeline:
    CHIP1A = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1A", "properties_project_CHIP1A"],
                outputs="properties_project_CHIP1A_with_CNPs",
                name="sample1A_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1A_with_CNPs",
                outputs="properties_project_CHIP1A_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1B = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1B", "properties_project_CHIP1B"],
                outputs="properties_project_CHIP1B_with_CNPs",
                name="sample1B_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1B_with_CNPs",
                outputs="properties_project_CHIP1B_with_CNPs_after_stress",
            ),
        ]
    )

    CHIP1C = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1C", "properties_project_CHIP1C"],
                outputs="properties_project_CHIP1C_with_CNPs",
                name="sample1C_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1C_with_CNPs",
                outputs="properties_project_CHIP1C_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1D = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1D", "properties_project_CHIP1D"],
                outputs="properties_project_CHIP1D_with_CNPs",
                name="sample1D_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1D_with_CNPs",
                outputs="properties_project_CHIP1D_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1E = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1E", "properties_project_CHIP1E"],
                outputs="properties_project_CHIP1E_with_CNPs",
                name="sample1E_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1E_with_CNPs",
                outputs="properties_project_CHIP1E_with_CNPs_after_stress",
            ),
        ]
    )

    CHIP1F = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1F", "properties_project_CHIP1F"],
                outputs="properties_project_CHIP1F_with_CNPs",
                name="sample1F_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1F_with_CNPs",
                outputs="properties_project_CHIP1F_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1G = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1G", "properties_project_CHIP1G"],
                outputs="properties_project_CHIP1G_with_CNPs",
                name="sample1G_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1G_with_CNPs",
                outputs="properties_project_CHIP1G_with_CNPs_after_stress",
            ),
        ]
    )

    CHIP1H = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP1H", "properties_project_CHIP1H"],
                outputs="properties_project_CHIP1H_with_CNPs",
                name="sample1H_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1H_with_CNPs",
                outputs="properties_project_CHIP1H_with_CNPs_after_stress",
            ),
        ]
    )

    CHIP3A = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3A", "properties_project_CHIP3A"],
                outputs="properties_project_CHIP3A_with_CNPs",
                name="sample3A_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3A_with_CNPs",
                outputs="properties_project_CHIP3A_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3B = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3B", "properties_project_CHIP3B"],
                outputs="properties_project_CHIP3B_with_CNPs",
                name="sample3B_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3B_with_CNPs",
                outputs="properties_project_CHIP3B_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3C = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3C", "properties_project_CHIP3C"],
                outputs="properties_project_CHIP3C_with_CNPs",
                name="sample3C_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3C_with_CNPs",
                outputs="properties_project_CHIP3C_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3D = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3D", "properties_project_CHIP3D"],
                outputs="properties_project_CHIP3D_with_CNPs",
                name="sample3D_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3D_with_CNPs",
                outputs="properties_project_CHIP3D_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3F = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3F", "properties_project_CHIP3F"],
                outputs="properties_project_CHIP3F_with_CNPs",
                name="sample3F_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3F_with_CNPs",
                outputs="properties_project_CHIP3F_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3G = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3G", "properties_project_CHIP3G"],
                outputs="properties_project_CHIP3G_with_CNPs",
                name="sample3G_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3G_with_CNPs",
                outputs="properties_project_CHIP3G_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3H = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3H", "properties_project_CHIP3H"],
                outputs="properties_project_CHIP3H_with_CNPs",
                name="sample3H_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3H_with_CNPs",
                outputs="properties_project_CHIP3H_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3I = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3I", "properties_project_CHIP3I"],
                outputs="properties_project_CHIP3I_with_CNPs",
                name="sample3I_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3I_with_CNPs",
                outputs="properties_project_CHIP3I_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3J = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP3J", "properties_project_CHIP3J"],
                outputs="properties_project_CHIP3J_with_CNPs",
                name="sample3J_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3J_with_CNPs",
                outputs="properties_project_CHIP3J_with_CNPs_after_stress",
            ),
        ]
    )

    CHIP4A = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4A", "properties_project_CHIP4A"],
                outputs="properties_project_CHIP4A_with_CNPs",
                name="sample4A_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4A_with_CNPs",
                outputs="properties_project_CHIP4A_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4B = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4B", "properties_project_CHIP4B"],
                outputs="properties_project_CHIP4B_with_CNPs",
                name="sample4B_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4B_with_CNPs",
                outputs="properties_project_CHIP4B_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4C = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4C", "properties_project_CHIP4C"],
                outputs="properties_project_CHIP4C_with_CNPs",
                name="sample4C_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4C_with_CNPs",
                outputs="properties_project_CHIP4C_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4D = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4D", "properties_project_CHIP4D"],
                outputs="properties_project_CHIP4D_with_CNPs",
                name="sample4D_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4D_with_CNPs",
                outputs="properties_project_CHIP4D_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4E = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4E", "properties_project_CHIP4E"],
                outputs="properties_project_CHIP4E_with_CNPs",
                name="sample4E_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4E_with_CNPs",
                outputs="properties_project_CHIP4E_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4G = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4G", "properties_project_CHIP4G"],
                outputs="properties_project_CHIP4G_with_CNPs",
                name="sample4G_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4G_with_CNPs",
                outputs="properties_project_CHIP4G_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4H = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4H", "properties_project_CHIP4H"],
                outputs="properties_project_CHIP4H_with_CNPs",
                name="sample4H_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4H_with_CNPs",
                outputs="properties_project_CHIP4H_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4I = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4I", "properties_project_CHIP4I"],
                outputs="properties_project_CHIP4I_with_CNPs",
                name="sample4I_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4I_with_CNPs",
                outputs="properties_project_CHIP4I_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4J = pipeline(
        [
            node(
                func=get_partitioned_CNPs,
                inputs=["data_project_CHIP4J", "properties_project_CHIP4J"],
                outputs="properties_project_CHIP4J_with_CNPs",
                name="sample4J_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4J_with_CNPs",
                outputs="properties_project_CHIP4J_with_CNPs_after_stress",
            ),
        ]
    )

    # --- Baseline chips ---
    CHIP1A_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1A_baseline", "properties_project_CHIP1A_baseline"],
                outputs="properties_project_CHIP1A_baseline_with_CNPs",
                name="sample1A_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1A_baseline_with_CNPs",
                outputs="properties_project_CHIP1A_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1B_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1B_baseline", "properties_project_CHIP1B_baseline"],
                outputs="properties_project_CHIP1B_baseline_with_CNPs",
                name="sample1B_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1B_baseline_with_CNPs",
                outputs="properties_project_CHIP1B_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1C_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1C_baseline", "properties_project_CHIP1C_baseline"],
                outputs="properties_project_CHIP1C_baseline_with_CNPs",
                name="sample1C_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1C_baseline_with_CNPs",
                outputs="properties_project_CHIP1C_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1D_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1D_baseline", "properties_project_CHIP1D_baseline"],
                outputs="properties_project_CHIP1D_baseline_with_CNPs",
                name="sample1D_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1D_baseline_with_CNPs",
                outputs="properties_project_CHIP1D_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1E_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1E_baseline", "properties_project_CHIP1E_baseline"],
                outputs="properties_project_CHIP1E_baseline_with_CNPs",
                name="sample1E_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1E_baseline_with_CNPs",
                outputs="properties_project_CHIP1E_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1F_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1F_baseline", "properties_project_CHIP1F_baseline"],
                outputs="properties_project_CHIP1F_baseline_with_CNPs",
                name="sample1F_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1F_baseline_with_CNPs",
                outputs="properties_project_CHIP1F_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1G_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1G_baseline", "properties_project_CHIP1G_baseline"],
                outputs="properties_project_CHIP1G_baseline_with_CNPs",
                name="sample1G_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1G_baseline_with_CNPs",
                outputs="properties_project_CHIP1G_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP1H_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP1H_baseline", "properties_project_CHIP1H_baseline"],
                outputs="properties_project_CHIP1H_baseline_with_CNPs",
                name="sample1H_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP1H_baseline_with_CNPs",
                outputs="properties_project_CHIP1H_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3A_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3A_baseline", "properties_project_CHIP3A_baseline"],
                outputs="properties_project_CHIP3A_baseline_with_CNPs",
                name="sample3A_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3A_baseline_with_CNPs",
                outputs="properties_project_CHIP3A_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3B_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3B_baseline", "properties_project_CHIP3B_baseline"],
                outputs="properties_project_CHIP3B_baseline_with_CNPs",
                name="sample3B_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3B_baseline_with_CNPs",
                outputs="properties_project_CHIP3B_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3C_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3C_baseline", "properties_project_CHIP3C_baseline"],
                outputs="properties_project_CHIP3C_baseline_with_CNPs",
                name="sample3C_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3C_baseline_with_CNPs",
                outputs="properties_project_CHIP3C_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3D_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3D_baseline", "properties_project_CHIP3D_baseline"],
                outputs="properties_project_CHIP3D_baseline_with_CNPs",
                name="sample3D_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3D_baseline_with_CNPs",
                outputs="properties_project_CHIP3D_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3F_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3F_baseline", "properties_project_CHIP3F_baseline"],
                outputs="properties_project_CHIP3F_baseline_with_CNPs",
                name="sample3F_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3F_baseline_with_CNPs",
                outputs="properties_project_CHIP3F_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3G_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3G_baseline", "properties_project_CHIP3G_baseline"],
                outputs="properties_project_CHIP3G_baseline_with_CNPs",
                name="sample3G_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3G_baseline_with_CNPs",
                outputs="properties_project_CHIP3G_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3H_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3H_baseline", "properties_project_CHIP3H_baseline"],
                outputs="properties_project_CHIP3H_baseline_with_CNPs",
                name="sample3H_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3H_baseline_with_CNPs",
                outputs="properties_project_CHIP3H_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3I_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3I_baseline", "properties_project_CHIP3I_baseline"],
                outputs="properties_project_CHIP3I_baseline_with_CNPs",
                name="sample3I_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3I_baseline_with_CNPs",
                outputs="properties_project_CHIP3I_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP3J_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP3J_baseline", "properties_project_CHIP3J_baseline"],
                outputs="properties_project_CHIP3J_baseline_with_CNPs",
                name="sample3J_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP3J_baseline_with_CNPs",
                outputs="properties_project_CHIP3J_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4A_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4A_baseline", "properties_project_CHIP4A_baseline"],
                outputs="properties_project_CHIP4A_baseline_with_CNPs",
                name="sample4A_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4A_baseline_with_CNPs",
                outputs="properties_project_CHIP4A_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4B_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4B_baseline", "properties_project_CHIP4B_baseline"],
                outputs="properties_project_CHIP4B_baseline_with_CNPs",
                name="sample4B_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4B_baseline_with_CNPs",
                outputs="properties_project_CHIP4B_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4C_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4C_baseline", "properties_project_CHIP4C_baseline"],
                outputs="properties_project_CHIP4C_baseline_with_CNPs",
                name="sample4C_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4C_baseline_with_CNPs",
                outputs="properties_project_CHIP4C_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4D_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4D_baseline", "properties_project_CHIP4D_baseline"],
                outputs="properties_project_CHIP4D_baseline_with_CNPs",
                name="sample4D_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4D_baseline_with_CNPs",
                outputs="properties_project_CHIP4D_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4E_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4E_baseline", "properties_project_CHIP4E_baseline"],
                outputs="properties_project_CHIP4E_baseline_with_CNPs",
                name="sample4E_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4E_baseline_with_CNPs",
                outputs="properties_project_CHIP4E_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4G_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4G_baseline", "properties_project_CHIP4G_baseline"],
                outputs="properties_project_CHIP4G_baseline_with_CNPs",
                name="sample4G_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4G_baseline_with_CNPs",
                outputs="properties_project_CHIP4G_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4H_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4H_baseline", "properties_project_CHIP4H_baseline"],
                outputs="properties_project_CHIP4H_baseline_with_CNPs",
                name="sample4H_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4H_baseline_with_CNPs",
                outputs="properties_project_CHIP4H_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4I_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4I_baseline", "properties_project_CHIP4I_baseline"],
                outputs="properties_project_CHIP4I_baseline_with_CNPs",
                name="sample4I_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4I_baseline_with_CNPs",
                outputs="properties_project_CHIP4I_baseline_with_CNPs_after_stress",
            ),
        ]
    )
    CHIP4J_baseline = pipeline(
        [
            node(
                func=get_partitioned_CNPs_baseline,
                inputs=["data_project_CHIP4J_baseline", "properties_project_CHIP4J_baseline"],
                outputs="properties_project_CHIP4J_baseline_with_CNPs",
                name="sample4J_baseline_CNPs",
            ),
            node(
                func=after_stress_CNP_calculations,
                inputs="properties_project_CHIP4J_baseline_with_CNPs",
                outputs="properties_project_CHIP4J_baseline_with_CNPs_after_stress",
            ),
        ]
    )

    non_baseline = (
        CHIP1A
        + CHIP1B
        + CHIP1C
        + CHIP1D
        + CHIP1E
        + CHIP1F
        + CHIP1G
        + CHIP1H
        + CHIP3A
        + CHIP3B
        + CHIP3C
        + CHIP3D
        + CHIP3F
        + CHIP3G
        + CHIP3H
        + CHIP3I
        + CHIP3J
        + CHIP4A
        + CHIP4B
        + CHIP4C
        + CHIP4D
        + CHIP4E
        + CHIP4G
        + CHIP4H
        + CHIP4I
        + CHIP4J
    )

    baseline = (
        CHIP1A_baseline
        + CHIP1B_baseline
        + CHIP1C_baseline
        + CHIP1D_baseline
        + CHIP1E_baseline
        + CHIP1F_baseline
        + CHIP1G_baseline
        + CHIP1H_baseline
        + CHIP3A_baseline
        + CHIP3B_baseline
        + CHIP3C_baseline
        + CHIP3D_baseline
        + CHIP3F_baseline
        + CHIP3G_baseline
        + CHIP3H_baseline
        + CHIP3I_baseline
        + CHIP3J_baseline
        + CHIP4A_baseline
        + CHIP4B_baseline
        + CHIP4C_baseline
        + CHIP4D_baseline
        + CHIP4E_baseline
        + CHIP4G_baseline
        + CHIP4H_baseline
        + CHIP4I_baseline
        + CHIP4J_baseline
    )

    return pipeline(non_baseline, tags="non_baseline") + pipeline(baseline, tags="baseline")
