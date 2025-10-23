from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

current_degrees = {"servo1": 0, "servo2": 0, "servo3": 0, "servo4": 0}


class ServoDegrees(BaseModel):
    servo1: int
    servo2: int
    servo3: int
    servo4: int


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/update_servo")
async def update_servo(data: ServoDegrees):
    current_degrees.update(data.dict())
    return {"status": "ok"}


@app.get("/update_servo")
async def get_servo():
    print(current_degrees)
    return current_degrees
    # return "{},{},{},{}".format(
    #     current_degrees["servo1"],
    #     current_degrees["servo2"],
    #     current_degrees["servo3"],
    #     current_degrees["servo4"]
    # )
