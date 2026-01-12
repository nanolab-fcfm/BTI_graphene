"""
This is a boilerplate pipeline 'CNP_calculations'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa

from .nodes import get_partitioned_CNPs, after_stress_CNP_calculations


def create_pipeline(**kwargs) -> Pipeline:
    
    CHIP1A = pipeline([
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
        )
    ])
    CHIP1B = pipeline([
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
        )
    ])
    
    CHIP1C = pipeline([
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
        )
    ])
    CHIP1D = pipeline([
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
        )
    ])
    CHIP1E = pipeline([
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
        )
    ])

    CHIP1F = pipeline([
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
        )
    ])
    CHIP1G = pipeline([
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
        )
    ])

    CHIP1H = pipeline([
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
        )
    ])
    CHIP1I = pipeline([
        node(
            func=get_partitioned_CNPs,
            inputs=["data_project_CHIP1I", "properties_project_CHIP1I"],
            outputs="properties_project_CHIP1I_with_CNPs",
            name="sample1I_CNPs",
        ),
        node(
            func=after_stress_CNP_calculations,
            inputs="properties_project_CHIP1I_with_CNPs",
            outputs="properties_project_CHIP1I_with_CNPs_after_stress",
        )
    ])

    CHIP3A = pipeline([
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
        )
    ])
    CHIP3B = pipeline([
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
        )
    ])
    CHIP3C = pipeline([
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
        )
    ])
    CHIP3D = pipeline([
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
        )
    ])
    CHIP3E = pipeline([
        node(
            func=get_partitioned_CNPs,
            inputs=["data_project_CHIP3E", "properties_project_CHIP3E"],
            outputs="properties_project_CHIP3E_with_CNPs",
            name="sample3E_CNPs",
        ),
        node(
            func=after_stress_CNP_calculations,
            inputs="properties_project_CHIP3E_with_CNPs",
            outputs="properties_project_CHIP3E_with_CNPs_after_stress",
        )
    ])
    CHIP3F = pipeline([
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
        )
    ])
    CHIP3G = pipeline([
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
        )
    ])
    CHIP3H = pipeline([
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
        )
    ])
    CHIP3I = pipeline([
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
        )
    ])
    CHIP3J = pipeline([
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
        )
    ])

    CHIP4A = pipeline([
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
        )
    ])
    CHIP4B = pipeline([
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
        )
    ])
    CHIP4C = pipeline([
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
        )
    ])
    CHIP4D = pipeline([
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
        )
    ])
    CHIP4E = pipeline([
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
        )
    ])
    CHIP4F = pipeline([
        node(
            func=get_partitioned_CNPs,
            inputs=["data_project_CHIP4F", "properties_project_CHIP4F"],
            outputs="properties_project_CHIP4F_with_CNPs",
            name="sample4F_CNPs",
        ),
        node(
            func=after_stress_CNP_calculations,
            inputs="properties_project_CHIP4F_with_CNPs",
            outputs="properties_project_CHIP4F_with_CNPs_after_stress",
        )
    ])
    CHIP4G = pipeline([
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
        )
    ])
    CHIP4H = pipeline([
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
        )
    ])
    CHIP4I = pipeline([
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
        )
    ])
    CHIP4J = pipeline([
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
        )
    ])

    return (CHIP1A + CHIP1B + CHIP1C + CHIP1D + CHIP1E + CHIP1F + CHIP1G + CHIP1H + CHIP1I +
            CHIP3A + CHIP3B + CHIP3C + CHIP3D + CHIP3E + CHIP3F + CHIP3G + CHIP3H + CHIP3I + CHIP3J +
            CHIP4A + CHIP4B + CHIP4C + CHIP4D + CHIP4E + CHIP4F + CHIP4G + CHIP4H + CHIP4I + CHIP4J)