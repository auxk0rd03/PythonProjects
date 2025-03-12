import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import requests
import pandas as pd
import random
import threading
import time
import folium
from io import BytesIO
import base64
from flask import Flask

# Initialize Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# Simulated Threat Intelligence API (Replace with real APIs)
def fetch_threat_data():
    threat_sources = ["Phishing", "Malware", "Ransomware", "DDoS", "SQL Injection"]
    locations = [(37.7749, -122.4194), (51.5074, -0.1278), (35.6895, 139.6917), (-33.8688, 151.2093)]
    return {
        "source": random.choice(threat_sources),
        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
        "count": random.randint(1, 50),
        "location": random.choice(locations)
    }

# Background thread to update data
threat_data = []
def update_data():
    while True:
        new_data = fetch_threat_data()
        threat_data.append(new_data)
        if len(threat_data) > 50:
            threat_data.pop(0)
        time.sleep(5)

threading.Thread(target=update_data, daemon=True).start()

# Generate a folium map
def generate_map():
    threat_map = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbdark_matter")
    for threat in threat_data:
        folium.Marker(threat["location"], popup=threat["source"], icon=folium.Icon(color="red" if threat["severity"] in ["High", "Critical"] else "orange")).add_to(threat_map)
    return threat_map

def map_to_base64():
    threat_map = generate_map()
    map_bytes = BytesIO()
    threat_map.save(map_bytes, close_file=False)
    return base64.b64encode(map_bytes.getvalue()).decode()

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Ultimate Cyber Security Dashboard", style={"color": "#FFA500", "textAlign": "center"}),
    
    html.Div([
        html.Button("Refresh Data", id="refresh-button", style={"backgroundColor": "#FFA500", "color": "#000"}),
        html.Button("Show Alerts", id="show-alerts", style={"backgroundColor": "#FFA500", "color": "#000", "margin-left": "10px"}),
        html.Div(id="alert-box", style={"margin-top": "10px", "color": "red", "font-weight": "bold"})
    ], style={"textAlign": "center", "margin-bottom": "20px"}),
    
    html.Div([
        html.Div([
            dcc.Graph(id="threat-graph"),
            html.Label("Set Alert Severity Level:", style={"color": "#FFA500"}),
            dcc.Dropdown(
                id="alert-severity",
                options=[{"label": level, "value": level} for level in ["Low", "Medium", "High", "Critical"]],
                value="High",
                clearable=False,
                style={"backgroundColor": "#333", "color": "#FFA500"}
            )
        ], style={"flex": "50%"}),

        html.Div([
            html.Img(id="threat-map", style={"width": "100%"})
        ], style={"flex": "50%"})
    ], style={"display": "flex", "gap": "20px"}),
    
    html.H3("Upload Security Logs for Analysis", style={"color": "#FFA500"}),
    dcc.Upload(id="upload-data", children=html.Button("Upload File", style={"backgroundColor": "#FFA500", "color": "#000"})),
    html.Div(id="output-data-upload", style={"color": "white"}),
    
    html.Div(id="incident-response-panel", style={"color": "#FFA500", "marginTop": "20px"})
], style={"backgroundColor": "#000", "padding": "20px"})

@app.callback(
    [Output("threat-graph", "figure"), Output("threat-map", "src")],
    [Input("refresh-button", "n_clicks")]
)
def refresh_dashboard(n_clicks):
    df = pd.DataFrame(threat_data)
    if df.empty:
        return px.bar(title="No Threat Data Available", template="plotly_dark"), ""
    
    fig = px.bar(df, x=df.index, y="count", color="severity", title="Threat Activity", labels={"x": "Time", "count": "Threat Count"}, template="plotly_dark")
    return fig, f"data:image/png;base64,{map_to_base64()}"

@app.callback(
    Output("alert-box", "children"),
    [Input("show-alerts", "n_clicks")],
    [State("alert-severity", "value")]
)
def show_alerts(n_clicks, alert_level):
    df = pd.DataFrame(threat_data)
    high_threats = df[df["severity"] == alert_level]
    return "Alert! High threat activity detected!" if not high_threats.empty else "No alerts."

@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def analyze_logs(contents, filename):
    if contents is None:
        return "No file uploaded."
    return f"Log file {filename} uploaded and under analysis."

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
