from firebase_admin import credentials, initialize_app, firestore
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.io as pio
from weather import get_weather_data

call_firestore = False

def get_data():
    # Initialize Firebase
    cred = credentials.Certificate("pi-temp-key.json")
    initialize_app(cred)
    db = firestore.client()

    # Fetch Firestore data
    time_series_ref = db.collection("BME280Collection")
    docs = time_series_ref.stream()

    # Load data into DataFrame
    df = pd.DataFrame()
    for doc in docs:
        df = pd.concat([df, pd.DataFrame(doc.to_dict(), index=[doc.id])], axis=0)

    df.index = pd.to_datetime(df.index)
    df.to_csv("BME280_data.csv")
    df.rename({
        'temperature_c': 'Temperature(°C)',
        'humidity': 'Humidity(%)',
        'pressure': 'Pressure(Kpa)'
    }, axis = 1, inplace=True)
    return df

if call_firestore:
    df = get_data()
else:
    df = pd.read_csv("BME280_data.csv", index_col=0)
    df.index = pd.to_datetime(df.index)

df = df[df.index.year > 2024]

ox = (51.745937862265606, -1.2318304746100621)
outside_df = get_weather_data(ox[0], ox[1],0, df.index[0], df.index[-1], granularity="hourly")[["temp", "rhum", "pres"]]
n = len(outside_df)
outside_df.columns = df.columns
outside_df = outside_df.reindex(df.index).interpolate(method="pchip")

# Create subplots
fig = sp.make_subplots(
    rows=2, cols=3,
    subplot_titles=[
        f'{col.capitalize()} Over Time' for col in df.columns
    ] + [
        f'Delta {col.capitalize()} (BME280 - Outside)' for col in df.columns
    ],
    shared_xaxes=True  # Ensures x-axes are shared within columns
)

# Define y-axis limits for each chart
y_limits = [
    (0, 40),  # First plot: °C
    (0, 100),                          # Second plot: %
    (950,1050)  # Third plot: Kpa
]

# Top row: Original charts
for idx, col in enumerate(df.columns, start=1):
    fig.add_trace(
        go.Scatter(x=df.index, y=df[col], mode='lines', name=f"BME280.{col}"),
        row=1, col=idx
    )
    fig.add_trace(
        go.Scatter(x=outside_df.index, y=outside_df[col], mode='lines', name=f"Outside.{col}", line=dict(dash='dot')),
        row=1, col=idx
    )
    fig.update_yaxes(range=y_limits[idx-1], row=1, col=idx)

# Bottom row: Delta charts as bar charts
for idx, col in enumerate(df.columns, start=1):
    delta = df[col] - outside_df[col]
    fig.add_trace(
        go.Bar(x=df.index, y=delta, name=f"Delta {col}"),
        row=2, col=idx
    )
    # Set dynamic y-axis limits for delta
    delta_range = max(-delta.min(), delta.max())*1.1
    fig.update_yaxes(
        range=[-delta_range, delta_range],
        row=2, col=idx
    )

# Set a consistent x-axis range for all columns (shared_xaxes ensures bottom rows are synced)
x_range = [df.index[-1] - pd.Timedelta("1h"), df.index[-1]]
for idx in range(1, len(df.columns) + 1):
    fig.update_xaxes(range=x_range, row=1, col=idx)

# Update layout
fig.update_layout(
    title="BME280 Data and Delta Over Time",
    xaxis_title='Timestamp',
    yaxis_title='Measurement',
    template='plotly_dark',
)

# Display the interactive plot
pio.show(fig)

