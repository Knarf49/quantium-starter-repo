import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

df = pd.read_csv("output/product.csv")
df["date"] = pd.to_datetime(df["date"])

sales_by_date = df.groupby("date", as_index=False)["sales"].sum()
line_fig = px.line(
    sales_by_date,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"},
)
line_fig.update_layout(paper_bgcolor="#1e1e2e", plot_bgcolor="#1e1e2e", font_color="#cdd6f4")
line_fig.update_traces(line_color="#89b4fa")

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"backgroundColor": "#1e1e2e", "minHeight": "100vh", "padding": "24px", "fontFamily": "sans-serif"},
    children=[
        html.H1(
            "Pink Morsel Sales Dashboard",
            style={"color": "#cba6f7", "textAlign": "center", "marginBottom": "32px"},
        ),
        dcc.Graph(figure=line_fig),
    ],
)

if __name__ == "__main__":
    app.run(debug=True)
