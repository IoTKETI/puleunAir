from SHT31 import SHT31
import time
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

pureunHost = '121.137.228.240'

mqtt_client = None
pub_temphumi_topic = "/puleunair/temphumi"

sht31 = SHT31()


def read_temphumi():
    global sht31
    global mqtt_client
    global pub_temphumi_topic

    sht31.write_command()
    time.sleep(0.3)
    result = sht31.read_data()
    if mqtt_client is not None:
        mqtt_client.publish(pub_temphumi_topic, str(result['c']) + ',' + str(result['h']))
    else:
        mqtt_client.reconnect()

    print('\n', datetime.utcnow().strftime(
        '%Y-%m-%d %H:%M:%S.%f') + " Relative Humidity: {0:0.2f} %% Temperature in Celsius: {1:0.2f} C".format(
        result['h'], result['c']))

    threading.Timer(2, read_temphumi).start()


def on_connect(client, userdata, flags, rc):
    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6-255: Currently unused.
    global mqtt_client
    global pureunHost

    if rc == 0:
        print('[mqtt_client_connect] connect to ' + pureunHost)
    elif rc == 1:
        print("incorrect protocol version")
        mqtt_client.reconnect()
    elif rc == 2:
        print("invalid client identifier")
        mqtt_client.reconnect()
    elif rc == 3:
        print("server unavailable")
        mqtt_client.reconnect()
    elif rc == 4:
        print("bad username or password")
        mqtt_client.reconnect()
    elif rc == 5:
        print("not authorised")
        mqtt_client.reconnect()
    else:
        print("Currently unused.")
        mqtt_client.reconnect()


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, _msg):
    print("Received " + _msg.payload.decode('utf-8') + " From " + _msg.topic)


if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message
    mqtt_client.connect("121.137.228.240", 1883)

    mqtt_client.loop_start()

    read_temphumi()
