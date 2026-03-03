from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import *

app = FastAPI()

class information(BaseModel):
    name : str
    age : int
    selected: bool = False
    achievements: Optional[int] = None



students_data = [{"name": "kar", "age":20, "selected":False , "achievements":"10", "id":1},
                 {"name": "ni", "age":21, "selected": False, "id":2}
                ]

def find_students(id):
    for st_id in students_data:
        if st_id['id'] == id:
            return st_id

def find_index_post(id):
    for i, p in enumerate(students_data):
        if p['id'] == id:
            return i

@app.get("/")
async def display():
    return "Hello World"

@app.get("/students_info")
def show_info():
    return {"infoo": students_data}

@app.post("/students")
def students(student_info: information):
    student_details = student_info.dict()
    student_details["id"] = randrange(0,100000)
    students_data.append(student_details)
    return student_details

@app.get("/students_id/latest")
def get_latest():
    last_id = students_data[len(students_data)-1]
    return {"details": last_id}

@app.get("/students_id/{id}")
def get_student_id(id: int, response: Response):
    student_id = find_students(int(id))
    if not student_id:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"id of {id} not found"}
    return {"post_details": student_id}

    
@app.delete("/students_delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id : int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" studnt with id {id} dosent exists")

    students_data.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/update_student/{id}")
def update_post(id:int, student: information):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" studnt with id {id} dosent exists")
    
    updates_student = student.dict()
    updates_student['id'] = id
    students_data[index] = updates_student
    return {"info": updates_student}


