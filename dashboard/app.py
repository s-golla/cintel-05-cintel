
# Arctic Climate Dashboard - PyShiny Express Version
# --------------------------------------------------
# This dashboard provides live monitoring of Arctic temperature and humidity data.
# It features a modern UI, value boxes, interactive charts, and a sidebar with resources.
# Technologies: PyShiny Express, pandas, plotly, Font Awesome icons, shinywidgets.

# ----------------------
# Imports
# ----------------------

from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats
from faicons import icon_svg 
import plotly.graph_objs as go


# ----------------------
# Constants and reactive data setup
# ----------------------


# Interval (seconds) for live data updates
UPDATE_INTERVAL_SECS: int = 10
# Number of recent readings to keep in memory
DEQUE_SIZE: int = 5
# Wrapper for the deque storing recent readings
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))


# ----------------------
# Reactive calculation: data engine
# ----------------------

@reactive.calc()
def reactive_calc_combined():
    """
    Core data engine for the dashboard.
    - Triggers every UPDATE_INTERVAL_SECS seconds to simulate new readings.
    - Appends new temperature/humidity/timestamp to a deque.
    - Returns: (deque, pandas DataFrame, latest reading dict)
    """
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Simulate Arctic climate readings
    temperature = round(random.uniform(-30, -25), 1)  # Temperature in °C
    humidity = round(random.uniform(70, 95), 1)       # Humidity in %
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": timestamp
    }

    # Append new reading to deque
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Prepare outputs
    deque_snapshot = reactive_value_wrapper.get()
    df = pd.DataFrame(deque_snapshot)
    latest_dictionary_entry = new_dictionary_entry
    return deque_snapshot, df, latest_dictionary_entry


# ----------------------
# Layout and sidebar section
# ----------------------

ui.page_opts(title="Polar Climate Dashboard", fillable=True)
# Sidebar: App title, description, and resource links
with ui.sidebar(open="open"):
    ui.h2(ui.HTML(f"<span style='color:#00BFFF'>{icon_svg('snowflake', style='solid')}</span> Arctic Research Center"), class_="text-center")
    ui.p("Live monitoring of Arctic temperature and humidity.", class_="text-center")
    ui.hr()
    ui.h6(ui.HTML(f"<span style='color:#FF9800'>{icon_svg('book-open', style='solid')}</span> Resources:"))
    ui.a("GitHub Repository", href="https://github.com/s-golla/cintel-05-cintel", target="_blank")
    ui.a("PyShiny Documentation", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("PyShiny Express Blog", href="https://shiny.posit.co/blog/posts/shiny-express/", target="_blank")


# ----------------------
# Value boxes: live readings
# ----------------------

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("temperature-high"),
        theme="bg-gradient-blue-purple",
    ):
        # Temperature value box
        "Temperature"
        @render.text
        def render_temperature():
            """Return latest temperature value as string (°C)"""
            _, _, latest = reactive_calc_combined()
            return f"{latest['temperature']} °C"
        "Live Arctic Temperature"

    with ui.value_box(
        showcase=icon_svg("droplet"),
        theme="bg-gradient-green-cyan",
    ):
        # Humidity value box
        "Humidity"
        @render.text
        def render_humidity():
            """Return latest humidity value as string (%)"""
            _, _, latest = reactive_calc_combined()
            return f"{latest['humidity']} %"
        "Live Arctic Humidity"

    with ui.value_box(
        showcase=icon_svg("clock"),
        theme="bg-gradient-gray-dark",
    ):
        # Last Update value box
        ui.HTML("<span style='font-weight:bold; font-size:1.3em;'>Last Update</span>")
        @render.ui
        def render_timestamp():
            """Return latest timestamp value as styled HTML"""
            _, _, latest = reactive_calc_combined()
            return ui.HTML(f"<span style='font-size:0.75em; color:#FF9800; font-family:monospace;'>{latest['timestamp']}</span>")
        "Last Update Time"


# ----------------------
# Data table: recent readings
# ----------------------

with ui.card(full_screen=True):
    ui.card_header("Recent Climate Data Table")
    @render.data_frame
    def render_data_table():
        """Return recent readings as a pandas DataGrid table"""
        _, df, _ = reactive_calc_combined()
        pd.set_option('display.width', None)
        return render.DataGrid(df, width="100%")
    

# ----------------------
# Charts: temperature, humidity, distribution
# ----------------------

with ui.layout_columns():
    with ui.card():
        ui.card_header("Temperature Trend")
        @render_plotly
        def render_temperature_chart():
            """Return temperature trend chart (Plotly) with trend line"""
            _, df, _ = reactive_calc_combined()
            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                fig = go.Figure()
                # Main temperature line: bold, gradient blue
                fig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["temperature"],
                    mode="lines+markers",
                    name="Temperature",
                    line=dict(color="#1976D2", width=4),
                    marker=dict(color="#64B5F6", size=8, symbol="circle"),
                ))
                # Add trend line (magenta, dotted)
                if len(df) >= 2:
                    x_vals = list(range(len(df)))
                    slope, intercept, *_ = stats.linregress(x_vals, df["temperature"])
                    trend = [slope * x + intercept for x in x_vals]
                    fig.add_trace(go.Scatter(
                        x=df["timestamp"],
                        y=trend,
                        mode="lines",
                        name="Trend",
                        line=dict(color="#D81B60", dash="dot", width=3)
                    ))
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Temperature (°C)",
                    plot_bgcolor="#F3F6FB",
                    paper_bgcolor="#E3EAF2",
                    font=dict(color="#212121"),
                    title_font=dict(size=22, color="#1976D2"),
                    legend=dict(bgcolor="#E3EAF2", bordercolor="#BDBDBD", borderwidth=1),
                    transition=dict(duration=500)
                )
                return fig

    with ui.card():
        ui.card_header("Humidity Trend")
        @render_plotly
        def render_humidity_chart():
            """Return humidity trend chart (Plotly) with trend line"""
            _, df, _ = reactive_calc_combined()
            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                fig = go.Figure()
                # Main humidity line: bold, teal
                fig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["humidity"],
                    mode="lines+markers",
                    name="Humidity",
                    line=dict(color="#00897B", width=4),
                    marker=dict(color="#4DD0E1", size=8, symbol="diamond"),
                ))
                # Add trend line (orange, dotted)
                if len(df) >= 2:
                    x_vals = list(range(len(df)))
                    slope, intercept, *_ = stats.linregress(x_vals, df["humidity"])
                    trend = [slope * x + intercept for x in x_vals]
                    fig.add_trace(go.Scatter(
                        x=df["timestamp"],
                        y=trend,
                        mode="lines",
                        name="Trend",
                        line=dict(color="#FFB300", dash="dot", width=3)
                    ))
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Humidity (%)",
                    plot_bgcolor="#F3F6FB",
                    paper_bgcolor="#E3EAF2",
                    font=dict(color="#212121"),
                    title_font=dict(size=22, color="#00897B"),
                    legend=dict(bgcolor="#E3EAF2", bordercolor="#BDBDBD", borderwidth=1),
                    transition=dict(duration=500)
                )
                return fig

    with ui.card():
        ui.card_header("Recent Temperature Distribution")
        @render_plotly
        def render_temperature_distribution():
            """Return histogram of recent temperature readings (Plotly)"""
            _, df, _ = reactive_calc_combined()
            if not df.empty:
                fig = px.histogram(
                    df,
                    x="temperature",
                    nbins=7,
                    title="Recent Temperature Histogram",
                    color_discrete_sequence=["#1976D2"],
                    opacity=0.85,
                )
                fig.update_traces(marker_line_color="#D81B60", marker_line_width=2)
                fig.update_layout(
                    xaxis_title="Temperature (°C)",
                    yaxis_title="Frequency",
                    plot_bgcolor="#F3F6FB",
                    paper_bgcolor="#E3EAF2",
                    font=dict(color="#212121"),
                    title_font=dict(size=22, color="#1976D2"),
                    legend=dict(bgcolor="#E3EAF2", bordercolor="#BDBDBD", borderwidth=1),
                    transition=dict(duration=500),
                )
                return fig