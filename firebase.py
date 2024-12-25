from firebase_admin import credentials, initialize_app, firestore


# Initialize Firebase
cred = credentials.Certificate("pi-temp-key.json")
initialize_app(cred)
db = firestore.client()

def upload_sensor_data(timestamp, temp_c, humidity, pressure):
    data = {
        "temperature_c": temp_c,
        "humidity": humidity,
        "pressure": pressure
    }
    try:
        t = timestamp.strftime("%Y-%m-%d %H:%M")
        db.collection('BME280Collection').document(t).set(data)
        print("Data uploaded successfully!", t, data)
    except Exception as e:
        print(f"Error uploading data: {e}")