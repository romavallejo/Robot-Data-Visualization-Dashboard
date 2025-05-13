import mysql.connector
import paho.mqtt.client as mqtt
import time

db_config = {
    "host": "localhost",        
    "user": "api",            
    "password": "2024",   
    "database": "proyecto" 
}

topic_to_sensor = {
    "sensores/distancia": 1, 
    "sensores/fotoresistencia": 2,   
    "sensores/bmppresion": 3,     
	"sensores/bmptemp": 4,
	"sensores/bmpaltura": 5,
	"sensores/acelx": 6,
	"sensores/acely": 7,
	"sensores/acelz": 8,
}

def connect_database():
    return mysql.connector.connect(**db_config)

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8").strip()  
    print(f"Received message on topic {topic}: {payload}")

    id_sensor = topic_to_sensor.get(topic)
    if id_sensor is None:
        print(f"Unknown topic: {topic}. Skipping this message.")
        return

    try:
        medicion = float(payload)
    except ValueError:
        print(f"Invalid payload: {payload}. Skipping this message.")
        return

    try:
        db = connect_database()
        cursor = db.cursor()
        query = """
            INSERT INTO Lecturas (id_sensor, medicion)
            VALUES (%s, %s)
        """
        values = (id_sensor, medicion)
        cursor.execute(query, values)
        db.commit()
        print("Data stored successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        db.close()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in topic_to_sensor.keys():
        client.subscribe(topic)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("broker.hivemq.com", 1883, 60)  # Replace with your MQTT broker details

while True:
    try:
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"Error: {e}. Reconnecting in 5 seconds...")
        time.sleep(5)
