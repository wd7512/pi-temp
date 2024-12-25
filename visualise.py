from firebase_admin import credentials, initialize_app, firestore
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.io as pio

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

units = ["°C", "%", "Kpa"]

# Create subplots
fig = sp.make_subplots(
    rows=1, cols=3, 
    subplot_titles=[f'{col.capitalize()} Over Time ({unit})' for col, unit in zip(df.columns, units)],
    shared_xaxes=True
)

# Define y-axis limits for each chart
y_limits = [
    (df[df.columns[0]].min() - 5, df[df.columns[0]].max() + 5),          # First plot: °C
    (0, 100),           # Second plot: %
    (df[df.columns[2]].min() - 5, df[df.columns[2]].max() + 5)  # Third plot: Kpa
]

# Plot each column with specified y-axis limits
for idx, col in enumerate(df.columns, start=1):
    fig.add_trace(
        go.Scatter(x=df.index, y=df[col], mode='lines', name=col),
        row=1, col=idx
    )
    fig.update_yaxes(range=y_limits[idx-1], row=1, col=idx)

# Update layout
fig.update_layout(
    title="BME280 Data Over Time",
    xaxis_title='Timestamp',
    yaxis_title='Measurement',
    template='plotly_dark',
)

# Display the interactive plot
pio.show(fig)
