import uuid
from fastapi import FastAPI
from pydantic import Field, BaseModel
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, String, create_engine, ForeignKey
DATABASE_URL = "postgresql://postgres:postgresql@localhost:5432/cstpy"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker()


class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True)
    name = Column(String)
    surname = Column(String)
    course_id = Column(String, ForeignKey("course.id"))
    course = relationship("Course", back_populates="students")


class Course(Base):
    __tablename__ = "course"
    id = Column(String, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="course")


Base.metadata.create_all(bind=engine)


class StudentEntry(BaseModel):
    name: str = Field(..., example="random")
    surname: str = Field(..., example="random")
    course_id: str = Field(..., example="FOREIGN KEY COURSE")


class StudentUpdate(BaseModel):
    id: str = Field(..., example="Enter your ID")
    name: str = Field(..., example="random")
    surname: str = Field(..., example="random")
    course_id: str = Field(..., example="FOREIGN KEY COURSE")

class CourseEntry(BaseModel):
    name: str = Field(..., example="random")

class CourseUpdate(BaseModel):
    id: str = Field(..., example="Enter your ID")
    name: str = Field(..., example="random")


app = FastAPI(
)


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

@app.get("/student")
async def find_student(studentid:str):
    session = Session(bind=engine)
    return session.query(Student).get(studentid)

@app.get("/students")
async def find_all_students():
    session = Session(bind=engine)
    return session.query(Student).all()

@app.post("/students")
async def register_student(student: StudentEntry):
    ID = str(uuid.uuid1())
    name = str(student.name)
    surname = str(student.surname)
    courseId = str(student.course_id)
    local_session = Session(bind=engine)
    lstudent = Student(id=ID, name=name, surname=surname,course_id=courseId)
    local_session.add(lstudent)
    local_session.commit()
    return {
        "id": ID,
        "name": name,
        "surname": surname,
        "course_id": courseId
    }


@app.put("/students")
async def update_student(student: StudentUpdate):
    local_session = Session(bind=engine)
    update_student = local_session.query(Student).get(student.id)
    update_student.name = student.name
    update_student.surname = student.surname
    update_student.course_id=student.course_id
    local_session.commit()
    return local_session.query(Student).get(student.id)

@app.get("/studentdelete")
async def delete_student(studentid:str):
    session = Session(bind=engine)
    deleteuser= session.query(Student).get(studentid)
    session.delete(deleteuser)
    session.commit()





@app.get("/course")
async def getcourse():
    session = Session(bind=engine)
    course=session.query(Course).first()
    return {
        "id":course.id,
        "name":course.name,
        "students":course.students
    }

@app.post("/course")
async def register_course(course: CourseEntry):
    ID = str(uuid.uuid1())
    name = str(course.name)
    local_session = Session(bind=engine)
    lcourse = Course(id=ID,name=name)
    local_session.add(lcourse)
    local_session.commit()
    return {
        "id": ID,
        "name": name,
    }


@app.put("/course")
async def update_course(course: CourseUpdate):
    local_session = Session(bind=engine)
    update_course = local_session.query(Course).get(course.id)
    update_course.name=course.name
    local_session.commit()
    return local_session.query(Course).get(course.id)

@app.get("/coursedelete")
async def delete_course(courseid:str):
    session = Session(bind=engine)
    delete_course= session.query(Course).get(courseid)
    session.delete(delete_course)
    session.commit()