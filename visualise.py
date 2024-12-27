from firebase_admin import credentials, initialize_app, firestore
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.io as pio

call_firestore = True

def read_tapo(path):
    df = pd.read_csv(path, index_col=0, usecols=[0,1,3])
    df.index = pd.to_datetime(df.index)
    return df

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

garage_df = read_tapo("data_garage.csv")
house_df = read_tapo("data_house.csv")


# Create subplots
fig = sp.make_subplots(
    rows=1, cols=3, 
    subplot_titles=[f'{col.capitalize()} Over Time' for col in df.columns],
    shared_xaxes=True
)

# Define y-axis limits for each chart
y_limits = [
    (0, df[df.columns[0]].max() + 5),          # First plot: °C
    (0, 100),           # Second plot: %
    (df[df.columns[2]].min() - 5, df[df.columns[2]].max() + 5)  # Third plot: Kpa
]

# Plot each column with specified y-axis limits


foo = 0  # Initialize foo before the loop

for idx, col in enumerate(df.columns, start=1):
    if foo<2:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[col], mode='lines', name='BME280 ' + col),
            row=1, col=idx
        )
        fig.add_trace(
            go.Scatter(x=garage_df.index, y=garage_df[garage_df.columns[foo]], mode='lines', name='Garage ' + garage_df.columns[foo]),  # Combine both traces
            row=1, col=idx
        )
        fig.add_trace(
            go.Scatter(x=house_df.index, y=house_df[house_df.columns[foo]], mode='lines', name='House ' + house_df.columns[foo]),  # Combine both traces
            row=1, col=idx
        )
        foo += 1  # Set foo to False after first iteration
    else:
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
