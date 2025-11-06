import json
import random
import paho.mqtt.client as mqtt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

current_degrees = {"servo1": 0, "servo2": 0, "servo3": 0, "servo4": 0}

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "roboticarm/servos"

mqtt_client = mqtt.Client(client_id=f"fastapi_pub_{random.randint(0, 9999)}")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("MQTT connected successfully!")
    else:
        print("MQTT connection failed, code:", rc)


mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # Run MQTT network loop in background


class ServoDegrees(BaseModel):
    servo1: int
    servo2: int
    servo3: int
    servo4: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "degrees": current_degrees})


@app.post("/update_servo")
async def update_servo(data: ServoDegrees):
    current_degrees.update(data.dict())
    payload = json.dumps(current_degrees)

    try:
        mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"📡 Published to MQTT: {payload}")
        return {"status": "ok", "sent": current_degrees}
    except Exception as e:
        print("MQTT publish error:", e)
        return {"status": "error", "message": str(e)}


@app.get("/update_servo")
async def get_servo():
    return current_degrees
