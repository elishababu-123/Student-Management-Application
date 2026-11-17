# from fastapi import FastAPI,Request,Form
# from  fastapi.templating import Jinja2Templates
# from pydantic import BaseModel,Field
# from fastapi.responses import RedirectResponse
# import sqlite3
# class StudentCreate(BaseModel):
#     name: str = Field(min_length=2, max_length=50),
#     age: int = Field( ge=3, le=100)
#     gender: str
#     marks: int = Field( ge=0, le=100)
#     course: str = Field( min_length=2, max_length=50)
#     image: str
#     status: int = Field(ge=0, le=1)


# def  get_connection():
#     connection=sqlite3.connect(
#         "students.db"

#     )
#     return connection
# get_connection()

# def create_table():
#     connection=get_connection()
#     cursor=connection.cursor()
    
#     q = """
#     CREATE TABLE IF NOT EXISTS students (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER,
#         gender TEXT,
#         marks INTEGER,
#         course TEXT,
#         image TEXT,
#         status INTEGER
#     )
#     """
#     cursor.execute(q)
#     connection.commit()
#     connection.close()


# create_table()

# templates = Jinja2Templates(directory="templates")

# app = FastAPI()


# @app.get("/")
# def home(req: Request):
#     connection=get_connection()
#     cursor=connection.cursor()

#     q="select * from students"


#     cursor.execute(q)
#     students=cursor.fetchall()
#     print(students)
#     connection.close()


#     return templates.TemplateResponse(
#         request=req,
#         name="home.html",
#         context={"std":students}
#     )
# @app.get("/students/add")
# def send_std_from(req: Request):
#     return templates.TemplateResponse(
#         request=req,
#         name="create-student.html",
#         context={}
#     )


# @app.get("/students/{std_id}")
# def single_std(req: Request, std_id: int):
#     connection = get_connection()
#     cursor = connection.cursor()

#     q = "select * from students where id=?"
#     cursor.execute(q, (std_id,))
#     student = cursor.fetchone()
#     connection.close()

#     return templates.TemplateResponse(
#         request=req,
#         name="single-std.html",
#         context={"std": student}
#     )
# @app.post('/students/add')
# def create_std(
#     name = Form(),
#     age = Form(),
#     gender=Form(),
#     marks = Form(),
#     course = Form(),
#     image = Form(),
#     status = Form()
# ):
#      student = StudentCreate(
#                 name=name,
#                 age=age,
#                 gender=gender,
#                 marks=marks,
#                 course=course,
#                 image=image,
#                 status=status,
#             )
#      values=(student.name, student.age,student.gender,student.marks, student.course,student. image, student.status)
#      connection =get_connection()
#      cursor=connection.cursor()
#      q="""
#     INSERT INTO
#     students(name, age,gender,marks, course, image, status)
#     values
#     (?,?,?,?,?,?,?)
#     """
#      cursor.execute(q,values)
#      connection.commit()
#      connection.close()
#      return RedirectResponse(url="/",status_code=303)
         
      
    


from fastapi import FastAPI,Request,Form,status
from fastapi.templating import Jinja2Templates
import sqlite3
from fastapi.responses import RedirectResponse
from pydantic import BaseModel,Field

def get_connection():
    connection=sqlite3.connect(
        "students.db"
    )
    return connection
get_connection()

def create_table():
    connection=get_connection()
    cursor=connection.cursor()

    q="""
    CREATE TABLE  IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    marks INTEGER,
    course TEXT,
    image TEXT,
    status INTEGER
    )
    """

    cursor.execute(q)
    connection.commit()
    connection.close()

create_table()


templates=Jinja2Templates(
    directory="templates"
)

class student(BaseModel):
    name:str=Field(min_length=3,max_length=25)
    age:int=Field(le=60,ge=18)
    gender:str
    marks:int=Field(le=100,ge=1)
    course:str
    image:str
    status:int


app=FastAPI()

@app.get("/")
def home(req:Request):
    connection=get_connection()
    cursor=connection.cursor()
    q="""
    select * from students
    """
    cursor.execute(q)
    student=cursor.fetchall()
    connection.close()
    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={
            "stds":student
        }
    )

@app.get("/student/{std_id}")
def singe_std(req:Request,std_id:int):

    connection=get_connection()
    cursor=connection.cursor()
    q="""
    select * from students where id=?
    """
    cursor.execute(q,(std_id,))
    student=cursor.fetchone()
    connection.close()
    return templates.TemplateResponse(
        request=req,
        name="single-std.html",
        context={
            "std":student
        }
    )

@app.post("/std/delete/{std_id}")
def std_delete(std_id:int):
    connection=get_connection()
    cursor=connection.cursor()
    q="""
    delete from students where id=?
    """
    cursor.execute(q,(std_id,))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/",status_code=303)




@app.get("/students/add")
def create_student(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="create-student.html",
        context={}
    )

@app.post("/students/add")
def create_std(name=Form(),age=Form(),gender=Form(),marks=Form(),course=Form(),image=Form(),status=Form()):
    std_obj=student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    values=(std_obj.name,std_obj.age,std_obj.gender,std_obj.marks,std_obj.course,std_obj.image,bool(std_obj.status))

    connection=get_connection()
    cursor=connection.cursor()
    q="""
    INSERT INTO students(name,age,gender,marks,course,image,status)
    values(?,?,?,?,?,?,?);
    """

    cursor.execute(q ,values)
    connection.commit()
    connection.close()
    return RedirectResponse(url="/",status_code=303)


@app.get("/student/edit/{std_id}")
def edit_std(req: Request, std_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("select * from students where id=?", (std_id,))
    student = cursor.fetchone()
    connection.close()
    return templates.TemplateResponse(
        request=req,
        name="edit-student.html",
        context={"std": student}
    )


@app.post("/student/edit/{std_id}")
def update_std(std_id: int, name=Form(), age=Form(), gender=Form(),
               marks=Form(), course=Form(), image=Form(), status=Form()):
    std_obj = student(name=name, age=age, gender=gender, marks=marks,
                      course=course, image=image, status=status)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE students
        SET name=?, age=?, gender=?, marks=?, course=?, image=?, status=?
        WHERE id=?
        """,
        (std_obj.name, std_obj.age, std_obj.gender, std_obj.marks,
         std_obj.course, std_obj.image, std_obj.status, std_id)
    )
    connection.commit()
    connection.close()
    return RedirectResponse(url="/", status_code=303)























