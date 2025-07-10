import plotly.graph_objects as go
import kaleido
import plotly.io as pio
import os

# Source data
data = [
    [100.0, 89.0, 75.7, 11.0, 13.4, 26.5, 49.2],
    [100.0, 89.6, 77.0, 10.4, 12.7, 25.0, 51.9],
    [100.0, 90.9, 79.6, 9.1, 11.4, 22.0, 57.6],
    [100.0, 92.2, 82.3, 7.8, 10.0, 18.7, 63.6],
    [100.0, 94.2, 86.4, 5.8, 7.8, 13.3, 73.1],
]

sources = [0, 0, 1, 1, 3, 3]
targets = [1, 2, 3, 4, 5, 6]

custom_colors_1 = {
    "Total harvested":                  "rgba(167, 167, 167, 1)",
    "Food-use":                         "rgba(197, 215, 231, 1)",
    "Non-food-use":                     "rgba(126, 5, 38, 1)",
    "Consumed":                         "rgba(74, 145, 192, 1)",
    "Post-harvest loss and waste":      "rgba(237, 92, 42 1)",
    "Unutilized by-products":           "rgba(248, 218, 137, 1)",
    "Final human consumption":         "rgba(19, 74, 134, 1)",
}

custom_colors_2 = {
    "Total harvested -- Food-use":              "rgba(197, 215, 231, 0.5)",
    "Total harvested -- Non-food-use":          "rgba(126, 5, 38, 0.5)",
    "Food-use -- Consumed":                     "rgba(74, 145, 192, 0.5)",
    "Food-use -- Post-harvest loss and waste":  "rgba(237, 92, 42, 0.5)",
    "Consumed -- Final human consumption":     "rgba(19, 74, 134, 0.5)",
    "Consumed -- Unutilized by-products":       "rgba(248, 218, 137, 0.5)",
}

node_color_map = [
    custom_colors_1["Total harvested"],
    custom_colors_1["Food-use"],
    custom_colors_1["Non-food-use"],
    custom_colors_1["Consumed"],
    custom_colors_1["Post-harvest loss and waste"],
    custom_colors_1["Unutilized by-products"],
    custom_colors_1["Final human consumption"]
]

link_color_map = [
    custom_colors_2["Total harvested -- Food-use"],             # 0 → 1
    custom_colors_2["Total harvested -- Non-food-use"],         # 0 → 2
    custom_colors_2["Food-use -- Consumed"],                    # 1 → 3
    custom_colors_2["Food-use -- Post-harvest loss and waste"], # 1 → 4
    custom_colors_2["Consumed -- Unutilized by-products"],      # 3 → 5
    custom_colors_2["Consumed -- Final human consumption"]      # 3 → 6
]


# Sanky plot
for i, d in enumerate(data):
    harvested, food_use, edible, non_food, loss, byprod, food = d

    # Calculation of values for the Sankey diagram
    values = [
        food_use / 100,                 # 0→1
        non_food / 100,                 # 0→2
        edible / 100,                   # 1→3
        loss /100,                      # 1→4
        byprod / 100,                   # 3→5
        food / 100                      # 3→6
    ]

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=15,
            line=dict(color="black", width=0),
            color=node_color_map
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            # line=dict(color="black", width=1.5),
            color=link_color_map
        )
    )])

    # Figure layout
    fig.update_layout(
        font=dict(family="Times New Roman", size=12, color="black"),
        width=283*120/90,
        height=151*120/90,
        margin=dict(l=5, r=5, t=5, b=5),  # Tight margins
    )

    outfile = f"sankey_stage_{i+1}.html"
    fig.write_html(outfile)
    os.startfile(outfile)



