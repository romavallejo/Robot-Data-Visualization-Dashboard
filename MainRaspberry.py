import time
import board
from time import sleep
# biblioteca para MQTT
import paho.mqtt.client as mqtt
# biblioteca para BMP
import adafruit_bmp280
# biblioteca para ADC
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
# biblioteca para Axl acelerometro
import adafruit_adxl34x
import RPi.GPIO as GPIO

#///////////////////////////////////////////////////SET UPS 
i2c = busio.I2C(board.SCL, board.SDA)

# bmp
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76) # address

# set up de ADC
ads = ADS.ADS1115(i2c, address=0x48) # address
channel = AnalogIn(ads, ADS.P0)

# set up de Axl acelerometro
accel = adafruit_adxl34x.ADXL345(i2c, address=0x53) # address
accel.enable_freefall_detection(threshold=10, time=25)
accel.enable_motion_detection(threshold=18)
accel.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)

# distancia
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
print("medicion en progreso")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# motor
Motor11 = 16  # Entrada
Motor21 = 20    # Entrada
Motor31 = 21   # Habilitar

Motor12 = 6  # Entrada
Motor22 = 13    # Entrada
Motor32 = 19   # Habilitar

GPIO.setup(Motor11, GPIO.OUT)
GPIO.setup(Motor21, GPIO.OUT)
GPIO.setup(Motor31, GPIO.OUT)
GPIO.setup(Motor12, GPIO.OUT)
GPIO.setup(Motor22, GPIO.OUT)
GPIO.setup(Motor32, GPIO.OUT)

#--------------------------- functions for sensors
# bmp
def bmpSensor():
    bmp280.sea_level_pressure = 1013.25
    presion = bmp280.pressure
    return f"{presion}"
    
# adc
def adcSensor():
    adcVal = channel.value
    return f"{adcVal}"

# acelerometro
def acelerometroSensor():
    # Obtener las tres componentes de la aceleración en x, y, z
    acceleration = accel.acceleration
    x, y, z = acceleration  # Desempaquetar los valores de la aceleración en x, y, z
    
    # Retornar como tres mensajes separados para MQTT
    return f"{x:.3f}", f"{y:.3f}", f"{z:.3f}"

# distancia
def distanciaSensor():
    GPIO.output(TRIG, False)
    print("esperando datos")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulso_dura = pulse_end - pulse_start
    dist = pulso_dura * 17150
    dist = round(dist, 2)
    return f"{dist}"

# motor
def controlMotor(direction):
    if direction == "fw":
        print("adelante")
        GPIO.output(Motor11, GPIO.HIGH)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor31, GPIO.HIGH)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor22, GPIO.LOW)
        GPIO.output(Motor32, GPIO.HIGH)
    elif direction == "bk":
        print("atras")
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor21, GPIO.HIGH)
        GPIO.output(Motor31, GPIO.HIGH)
        GPIO.output(Motor12, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor32, GPIO.HIGH)
    elif direction == "lf":
        print("izq")
        GPIO.output(Motor11, GPIO.HIGH)
        GPIO.output(Motor21, GPIO.LOW)
        GPIO.output(Motor31, GPIO.HIGH)
        GPIO.output(Motor12, GPIO.LOW)
        GPIO.output(Motor22, GPIO.HIGH)
        GPIO.output(Motor32, GPIO.HIGH)
    elif direction == "rt":
        print("der")
        GPIO.output(Motor11, GPIO.LOW)
        GPIO.output(Motor21, GPIO.HIGH)
        GPIO.output(Motor31, GPIO.HIGH)
        GPIO.output(Motor12, GPIO.HIGH)
        GPIO.output(Motor22, GPIO.LOW)
        GPIO.output(Motor32, GPIO.HIGH)
    elif direction == "st":
        print("detener")
        GPIO.output(Motor31, GPIO.LOW)
        GPIO.output(Motor32, GPIO.LOW)
        sleep(3)

#////////////////////////////////////////////// MQTT set up
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
        client.subscribe("rover/motor")
    else:
        print("Error al conectar, código de retorno:", rc)

def on_message(client, userdata, msg):
    print(f"Nuevo mensaje en {msg.topic}: {msg.payload.decode('utf-8')}")
    controlMotor(msg.payload.decode('utf-8'))

unacked_publish = set()
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.user_data_set(unacked_publish)
mqttc.connect("broker.hivemq.com", 1883)

mqttc.loop_start()

#///////////////////////////////////////////////////// PUBLISH USING MQTT
try:
    while True:
        # Asegúrate de que el cliente MQTT esté conectado antes de publicar
        if not mqttc.is_connected():
            print("No conectado, reconectando...")
            mqttc.reconnect()
        
        # Publicar en sensor 1 BMP
        mqttc.publish("sensores/bmp", bmpSensor(), qos=2)
        mqttc.publish("sensores/adc", adcSensor(), qos=2)
        x_msg, y_msg, z_msg = acelerometroSensor()
        mqttc.publish("sensores/acelx", x_msg, qos=2)
        mqttc.publish("sensores/acely", y_msg, qos=2)
        mqttc.publish("sensores/acelz", z_msg, qos=2)
        mqttc.publish("sensores/distancia", distanciaSensor(), qos=2)
        mqttc.publish("sensores/bmptemp", bmp280.temperature, qos=2)
        mqttc.publish("sensores/bmppresion", bmp280.pressure, qos=2)
        mqttc.publish("sensores/bmpaltura", bmp280.altitude, qos=2)
        time.sleep(5)

except KeyboardInterrupt:  # control + c
    print("Interrupción detectada. Limpiando recursos...")
    mqttc.disconnect()
    mqttc.loop_stop()
    GPIO.cleanup()
    print("Recursos limpiados y programa terminado.")