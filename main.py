from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):

    id:Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    Name:Annotated[str, Field(..., description="Name of the patient")]
    city:Annotated[str, Field(..., description="City of the patient is living")]
    age:Annotated[int, Field(..., description="Age of the patient")]
    gender:Annotated[Literal['male', 'female', 'others'], Field(..., description="City of the patient is living")]
    height:Annotated[float, Field(..., gt=0, description="height of the patient in meters")]
    weight: Annotated[float, Field(..., gt = 0, description="weight of the patients in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/ (self.height**2),2)

        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "undeweight"
        elif self.bmi < 25:
            return "normal"
        else:
            return "obese"

class PatientUpdate(BaseModel):

    id:Annotated[Optional[str], Field(default=None)]
    Name:Annotated[Optional[str], Field(default=None)]
    city:Annotated[Optional[str], Field(default=None)]
    age:Annotated[Optional[int], Field(default=None)]
    gender:Annotated[Optional[str], Field(default=None)]
    height:Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient management system api"}

@app.get("/about")
def about():
    return {"message" : " A fully functional api to manage patient records."}


@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="id of the patient in DB.",example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(404, "patient not Found")


@app.get("/sort")
def sort_patient(sort_by:str = Query(..., description="sort on basis of height, weight and bmi"), order:str = Query('asc', description="sort in ascending or descending order")):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(400, f"invalid valids select from {valid_fields}")

    order_fields = ['asc', 'desc']
    if order not in order_fields:
        raise HTTPException(400, f"invalid order select from {order_fields}")

    data = load_data()

    val = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=val)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(400, "patient already exist")

    # used to convert pydantic obj to dict
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content="Patient created successfully")

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(404, "patient not found")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, val in updated_patient_info.items():
        existing_patient_info[key] = val

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content="Patient updated successfully")

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(404, "Patient not exist")

    del(data[patient_id])

    save_data(data)

    return JSONResponse(status_code=200, content="Patient deleted successfully")
    

    