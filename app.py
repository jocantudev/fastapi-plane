# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime

app = FastAPI()

planedb = []

# plane model
class Plane(BaseModel):
    id: int
    model: str
    manufacturer: str
    first_flight: int
    published: Optional[bool] = False

@app.get("/")
def read_root():
  return {"home": "Home page"}

@app.get("/planes")
def get_planes():
    return planedb

@app.post("/planes")
def add_plane(plane: Plane):
    planedb.append(plane.dict())
    return planedb[-1]

@app.get("/planes/{plane_id}")
def get_plane(plane_id: int):
    plane = plane_id - 1
    return planedb[plane]

@app.put("/planes/{plane_id}")
def update_plane(plane_id: int, plane: Plane):
    planedb[plane_id] = plane
    return {"message": "Plane has been updated succesfully"}

@app.delete("/planes/{plane_id}")
def delete_plane(plane_id: int):
    planedb.pop(plane_id-1)
    return {"message": "Plane has been deleted succesfully"}
