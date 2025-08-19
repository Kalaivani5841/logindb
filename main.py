import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    phone: str
    email: str
    password: str

class UpdateRequest(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    password: str

class DeleteRequest(BaseModel):
    id: int


def connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="office",
        port=3307
    )


@app.post("/login")
def Login(data: LoginRequest):
    Email = data.email
    Password = data.password
    mydb = connection()
    mypost = mydb.cursor()
    mypost.execute("SELECT * FROM logindb WHERE email='" + Email + "' AND password='" + Password + "'")
    result = mypost.fetchall()
    mydb.close()

    if result:
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}


@app.post("/register")
def Register(datas: RegisterRequest):
    mydb = connection()
    mypost = mydb.cursor()
    mypost.execute("INSERT INTO logindb(name, phone, email, password) VALUES('" + datas.name + "', '" + datas.phone + "', '" + datas.email + "', '" + datas.password + "')")
    mydb.commit()
    mydb.close()
    return {"message": "Register successful"}



@app.get("/users")
def view_users():
    db = connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM logindb")
    result = cursor.fetchall()
    db.close()
    return {"users": result}


@app.post("/update")
def UpdateUser(data: UpdateRequest):
    mydb = connection()
    mypost = mydb.cursor()
    mypost.execute("UPDATE logindb SET name='" + data.name + "', phone='" + data.phone + "', email='" + data.email + "', password='" + data.password + "' WHERE id=" + str(data.id))
    mydb.commit()
    mydb.close()
    return {"message": "Update successful"}



@app.post("/delete")
def DeleteUser(data: DeleteRequest):
    mydb = connection()
    mypost = mydb.cursor()
    mypost.execute("DELETE FROM logindb WHERE id=" + str(data.id))
    mydb.commit()
    mydb.close()
    return {"message": "User deleted successfully"}