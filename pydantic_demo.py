from pydantic import BaseModel, Field,EmailStr, field_validator
from typing import Annotated, List, Dict

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, description="Give the name of the patient", examples=['King'])]
    age: int
    email: EmailStr

    #default mode is after in fiel_validator which gets value after type cohersion
    @field_validator("email")
    @classmethod
    def email_validation(cls, value):

        valid_domains = ['hdfc.com', 'icic.com']

        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("not a valid domain")

        return value

def insert_patient_data(patient: Patient):
    print(patient.name, patient.age, patient.email)

patient_info = {'name':'Ritesh', 'age':23, 'email':"abc@hdfc.in"}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)