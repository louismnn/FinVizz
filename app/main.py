from dash import Dash, html, dcc, Input, Output, State, callback, ctx, no_update
from app.widgets import DerivativeInput
from CTkMessagebox import CTkMessagebox
from flask import request
import plotly.graph_objects as go
from app.file import File
import numpy as np
import json



with open(r"app\assets\database.json", "r") as file:
    datas = json.load(file)

    list_of_derivatives = tuple(datas["list_of_derivatives"].keys())
    my_colors = tuple(datas["colors"])


class Main():

    def __init__(self):

        self.file_manager = File()

        self.return_data = {
            "Delta": (self.file_manager.deltas, 0),
            "Gamma": (self.file_manager.gammas, 1),
            "Vega": (self.file_manager.vegas, 2),
            "Theta": (self.file_manager.thetas, 3),
            "Rho": (self.file_manager.rhos, 4)
        }

    def create_plot(self) -> go.Figure:

        fig = go.Figure()

        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                        autosize=True, margin=dict(l=15, r=10, t=15, b=10))

        fig.update_xaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True),
                        showline=True, linewidth=1, linecolor='black', mirror=True)

        fig.update_yaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True),
                        showline=True, linewidth=1, linecolor='black', mirror=True)

        return fig

    def reset(self) -> go.Figure:

        self.file_manager = File()

        self.return_data = {
            "Delta": (self.file_manager.deltas, 0),
            "Gamma": (self.file_manager.gammas, 1),
            "Vega": (self.file_manager.vegas, 2),
            "Theta": (self.file_manager.thetas, 3),
            "Rho": (self.file_manager.rhos, 4)
        }

        return self.create_plot()

    def graph_element(self, state : dict, fig : go.Figure) -> go.Figure:

        x_title = "Interest Rate" if state["greek"] == "Rho" else "Underlying Price"
        x = self.file_manager.R if state["greek"] == "Rho" else self.file_manager.S

        fig.update_layout(xaxis_title=f"<b>{x_title}</b>", yaxis_title=f"<b>{state['greek']}</b>", font_color="black")

        data, num = self.return_data[state["greek"]]

        if sum([np.any(el) for el in data]) > 1:
            fig.add_trace(go.Scatter(x=x, y=self.file_manager.overall[num], mode="lines", line = dict(color="black", width=1), name="Portfolio"))

        i = 0
        for el, dev in zip(data, self.file_manager.derivatives_types):

            if np.any(el):
                fig.add_trace(go.Scatter(x=x, y=el, mode="lines", line = dict(color = my_colors[i], width=3), name=dev))
                i += 1
            else: 
                continue

        return fig


app = Dash(title="Finance Greeks Visualization")


@app.server.after_request
def notify_dash_request_error(response):
    if request.path == "/_dash-update-component" and response.status_code >= 400:
        CTkMessagebox(
            title="Chart Update Error",
            message=(
                f"The server could not update the chart (HTTP {response.status_code}).\n"
                 "Please retry."
            ),
            icon="cancel",
        )
    return response


main = Main()
widget = DerivativeInput()

plot = main.create_plot()

app.layout = html.Div([

    dcc.Store(id="state-store", data={"greek": "Delta"}),

        html.Div([
            dcc.Tabs(
                id="custom-tabs",
                value='Delta',
                children=[
                    dcc.Tab(label='Delta', value='Delta', className='custom-tab', selected_className='custom-tab--selected'),
                    dcc.Tab(label='Gamma', value='Gamma', className='custom-tab', selected_className='custom-tab--selected'),
                    dcc.Tab(label='Vega', value='Vega', className='custom-tab', selected_className='custom-tab--selected'),
                    dcc.Tab(label='Theta', value='Theta', className='custom-tab', selected_className='custom-tab--selected'),
                    dcc.Tab(label='Rho', value='Rho', className='custom-tab', selected_className='custom-tab--selected')
                ]
            ),

            dcc.Dropdown(
                [{"label": html.Span([el], className="span"), "value" : el} for el in list_of_derivatives],
                placeholder="Select a derivative product",
                searchable=False,
                id="dropdown",
                className="custom-dropdown"
            ),

            dcc.Button(
                "🔄 Reset Portfolio", 
                n_clicks=0,
                id="custom-button",
                className="custom-button"  
            ),

            dcc.Graph(
                figure=go.Figure(plot),
                id='graph',
                className='custom-graph'
            )

        ], className="main-panel")

], className="main-container")


@callback(
    Output("graph", "figure"),
    Output("state-store", "data"),
    Output("dropdown", "value"),
    Output("custom-tabs", "value"),
    Output("custom-button", "n_clicks"),

    Input("custom-tabs", "value"),
    Input("dropdown", "value"),
    Input("custom-button", "n_clicks"),
    State("state-store", "data")
)
def update_graph(tab, selected_derivative, nclicks, state):
    dropdown_value = selected_derivative

    if ctx.triggered_id == "custom-button":
        fig = main.reset()
        return fig, state, None, tab, 0

    elif ctx.triggered_id == "dropdown" and selected_derivative:

        inputs = widget.get_data(selected_derivative)
        if inputs is None:
            return no_update, state, None, tab, nclicks

        main.file_manager.add_element(derivative_type=selected_derivative, data=inputs)
        dropdown_value = None

    state["greek"] = tab

    fig = go.Figure(plot)
    fig = main.graph_element(state, fig)

    return fig, state, dropdown_value, tab, nclicks
