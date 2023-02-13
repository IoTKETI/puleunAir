# -*- coding: utf-8 -*-
"""
 @ Created by Wonseok Jung in KETI on 2023-02-10.
"""

import paho.mqtt.client as mqtt
import SX1509
import Control
import time

local_mqtt_client = None

g_set_event = 0x00

SET_Control1 = 0x01
SET_Control2 = 0x02
SET_Control3 = 0x04
SET_Control4 = 0x08
SET_Control5 = 0x10

Control1_val = 0
Control2_val = 0
Control3_val = 0
Control4_val = 0
Control5_val = 0

Control1_pin = 10
Control2_pin = 11
Control3_pin = 12
Control4_pin = 13
Control5_pin = 14

i2c_addr = 0x3e
i2c_bus = 4
sx = SX1509.SX1509(i2c_addr, i2c_bus)
ctl = Control.Control(sx)


def set_Control1(val):
    # ctl.DOUT(Control1_pin, val)
    print("Control Control1 - ", val)


def set_Control2(val):
    # ctl.DOUT(Control2_pin, val)
    print("Control Control2 - ", val)


def set_Control3(val):
    # ctl.DOUT(Control3_pin, val)
    print("Control Control3 - ", val)


def set_Control4(val):
    # ctl.DOUT(Control4_pin, val)
    print("Control Control4 - ", val)


def set_Control5(val):
    # ctl.DOUT(Control5_pin, val)
    print("Control Control5 - ", val)


def on_connect(client, userdata, flags, rc):
    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6-255: Currently unused.

    global local_mqtt_client

    if rc is 0:
        print('[local_mqtt_client_connect] connect to 127.0.0.1')
        local_mqtt_client.subscribe("/puleunair/Control1/set")
        local_mqtt_client.subscribe("/puleunair/Control2/set")
        local_mqtt_client.subscribe("/puleunair/Control3/set")
        local_mqtt_client.subscribe("/puleunair/Control4/set")
        local_mqtt_client.subscribe("/puleunair/Control5/set")
    elif rc is 1:
        print("incorrect protocol version")
        local_mqtt_client.reconnect()
    elif rc is 2:
        print("invalid client identifier")
        local_mqtt_client.reconnect()
    elif rc is 3:
        print("server unavailable")
        local_mqtt_client.reconnect()
    elif rc is 4:
        print("bad username or password")
        local_mqtt_client.reconnect()
    elif rc is 5:
        print("not authorised")
        local_mqtt_client.reconnect()
    else:
        print("Currently unused.")
        local_mqtt_client.reconnect()


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, _msg):
    global g_set_event
    global SET_Control1
    global SET_Control2
    global SET_Control3
    global SET_Control4
    global SET_Control5
    global Control1_val
    global Control2_val
    global Control3_val
    global Control4_val
    global Control5_val

    if _msg.topic == '/puleunair/Control1/set':
        Control1_val = int(_msg.payload.decode('utf-8'))
        g_set_event |= SET_Control1
    elif _msg.topic == '/puleunair/Control2/set':
        Control2_val = int(_msg.payload.decode('utf-8'))
        g_set_event |= SET_Control2
    elif _msg.topic == '/puleunair/Control3/set':
        Control3_val = int(_msg.payload.decode('utf-8'))
        g_set_event |= SET_Control3
    elif _msg.topic == '/puleunair/Control4/set':
        Control4_val = int(_msg.payload.decode('utf-8'))
        g_set_event |= SET_Control4
    elif _msg.topic == '/puleunair/Control5/set':
        Control5_val = int(_msg.payload.decode('utf-8'))
        g_set_event |= SET_Control5
    else:
        print("Received " + _msg.payload.decode('utf-8') + " From " + _msg.topic)


if __name__ == "__main__":
    local_mqtt_client = mqtt.Client()
    local_mqtt_client.on_connect = on_connect
    local_mqtt_client.on_disconnect = on_disconnect
    local_mqtt_client.on_subscribe = on_subscribe
    local_mqtt_client.on_message = on_message
    local_mqtt_client.connect("127.0.0.1", 1883)

    local_mqtt_client.loop_start()

    while True:
        if g_set_event & SET_Control1:
            g_set_event &= (~SET_Control1)
            set_Control1(Control1_val)
        elif g_set_event & SET_Control2:
            g_set_event &= (~SET_Control2)
            set_Control2(Control2_val)
        elif g_set_event & SET_Control3:
            g_set_event &= (~SET_Control3)
            set_Control3(Control3_val)
        elif g_set_event & SET_Control4:
            g_set_event &= (~SET_Control4)
            set_Control4(Control4_val)
        elif g_set_event & SET_Control5:
            g_set_event &= (~SET_Control5)
            set_Control5(Control5_val)
#
# count = 0
#
# while True:
#     count += 1
#     count %= 2
#     ctl.DOUT(Control1_pin, count)
#     ctl.DOUT(Control2_pin, count)
#     ctl.DOUT(Control3_pin, count)
#     ctl.DOUT(Control4_pin, count)
#     ctl.DOUT(Control5_pin, count)
#     print(count)
#     time.sleep(1)
