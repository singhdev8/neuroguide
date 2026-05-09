def generate_explanation(inputs, technique):
    text = ", ".join(inputs)

    return f"{technique} is recommended based on your condition ({text}), as it is connected through psychological and behavioral pathways in the knowledge graph."
