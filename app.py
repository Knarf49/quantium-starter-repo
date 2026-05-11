import pandas as pd
import dash
from dash import dcc, html, callback, clientside_callback, Input, Output
import plotly.express as px

df = pd.read_csv("output/product.csv")
df["date"] = pd.to_datetime(df["date"])

regions = ["All"] + sorted(df["region"].unique().tolist())

DARK = "#1e1e2e"
SURFACE = "#313244"
TEXT = "#cdd6f4"
ACCENT = "#cba6f7"
BLUE = "#89b4fa"
COLORS = [BLUE, ACCENT, "#a6e3a1", "#f38ba8"]

# static line chart — all regions
sales_by_date = df.groupby("date", as_index=False)["sales"].sum()
line_fig = px.line(
    sales_by_date,
    x="date",
    y="sales",
    title="Sales Over Time (All Regions)",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)
line_fig.update_layout(
    paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
    font_color=TEXT, title_font_color=ACCENT,
)
line_fig.update_traces(line_color=BLUE)

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": DARK,
        "minHeight": "100vh",
        "padding": "32px",
        "fontFamily": "'Segoe UI', sans-serif",
        "maxWidth": "1200px",
        "margin": "0 auto",
    },
    children=[
        html.H1(
            "Pink Morsel Sales Dashboard",
            style={
                "color": ACCENT,
                "textAlign": "center",
                "marginBottom": "8px",
                "fontSize": "2rem",
                "letterSpacing": "0.05em",
            },
        ),
        html.Hr(style={"borderColor": SURFACE, "marginBottom": "32px"}),

        # --- Line chart (static, no radio) ---
        html.Div(
            style={
                "backgroundColor": SURFACE,
                "borderRadius": "12px",
                "padding": "24px",
                "marginBottom": "32px",
                "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
            },
            children=[
                dcc.Graph(figure=line_fig),
            ],
        ),

        # --- Bar chart + radio by region ---
        html.Div(
            style={
                "backgroundColor": SURFACE,
                "borderRadius": "12px",
                "padding": "24px",
                "boxShadow": "0 4px 20px rgba(0,0,0,0.4)",
            },
            children=[
                html.H2(
                    "Sales by Region",
                    style={"color": TEXT, "marginTop": "0", "fontSize": "1.1rem", "marginBottom": "12px"},
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": r, "value": r} for r in regions],
                    value="All",
                    inline=True,
                    style={"color": TEXT, "marginBottom": "16px"},
                    inputStyle={"marginRight": "6px", "accentColor": ACCENT},
                    labelStyle={"marginRight": "20px", "cursor": "pointer", "color": "#ffffff"},
                ),
                html.Div(
                    id="bar-wrapper",
                    children=[dcc.Graph(id="region-bar-chart")],
                ),
            ],
        ),
    ],
)


@callback(Output("region-bar-chart", "figure"), Input("region-filter", "value"))
def update_bar(region):
    grouped = df.groupby("region", as_index=False)["sales"].sum().sort_values("region")
    colors = [
        BLUE if (region == "All" or r == region) else "#45475a"
        for r in grouped["region"]
    ]
    fig = px.bar(
        grouped,
        x="region",
        y="sales",
        title=f"Total Sales — {region}",
        labels={"region": "Region", "sales": "Total Sales ($)"},
    )
    fig.update_traces(marker_color=colors, width=0.3)
    fig.update_layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font_color=TEXT,
        title_font_color=ACCENT,
        showlegend=False,
    )
    return fig


clientside_callback(
    """
    function(region, figure) {
        const sortedRegions = ["east", "north", "south", "west"];
        const selectedIdx = sortedRegions.indexOf(region);

        setTimeout(function() {
            const chart = document.getElementById('region-bar-chart');
            if (!chart) return;
            const bars = chart.querySelectorAll('g.barlayer .point path');
            bars.forEach(function(bar, i) {
                bar.style.transformBox = 'fill-box';
                bar.style.transformOrigin = '50% 100%';
                bar.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
                bar.style.transform = (selectedIdx !== -1 && i === selectedIdx) ? 'scale(1.2)' : 'scale(1)';
            });
        }, 80);

        return '';
    }
    """,
    Output("bar-wrapper", "className"),
    Input("region-filter", "value"),
    Input("region-bar-chart", "figure"),
)

if __name__ == "__main__":
    app.run(debug=True)
