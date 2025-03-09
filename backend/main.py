import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from sessionStarter import login
from dataParsers import *
from pageScrapers import *
from gradeOperations import *
import requests

app = FastAPI()

origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: Dict[str, requests.Session] = {}  # Storing active sessions in a dictionary

class Credentials(BaseModel):
    username: str
    password: str
    baseURL: str

class TheoreticalGrade(BaseModel):
    name: str
    category: str
    weight: float
    score: float

class UpdateTranscriptGrades(BaseModel):
    grades: Dict[str, str]

class DifScaleClasses(BaseModel):
    classes: Dict[str, float]

@app.post("/login")
def login_api(credentials: Credentials):
    try:
        session = login(credentials.baseURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f", credentials.username, credentials.password)
        if session:
            sessions[credentials.username] = session  # Store session
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Login failed")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {e}")

@app.get("/grades")
def get_grades(username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        homeSC = getHomeScreen(session)
        grades = parseGrades(homeSC)
        return grades
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting grades: {e}")

@app.get("/transcript")
def get_transcript(username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        transcript = getTranscript(session)
        tranGrades = getTranscriptGrades(transcript)
        return tranGrades
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting transcript: {e}")

@app.get("/assignments")
def get_assignments(username: str):
    try:
        print("getting assignments")
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        allAssignmentData = getAssignmentsForClass(session)
        classAssignments = parseAssignments(allAssignmentData)
        return classAssignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting assignments: {e}")

@app.post("/add_theoretical_grade/{class_name}")
def add_theoretical_grade_api(class_name: str, theoretical_grade: TheoreticalGrade, username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        allAssignmentData = getAssignmentsForClass(session)
        classAssignments = parseAssignments(allAssignmentData)
        addTheoreticalGrade(classAssignments[class_name]['assignments'], classAssignments[class_name]['categories'], theoretical_grade.dict())
        return {"message": f"Theoretical grade added to {class_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding theoretical grade: {e}")

@app.get("/calculate_class_averages")
def calculate_class_averages(username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        allAssignmentData = getAssignmentsForClass(session)
        classAssignments = parseAssignments(allAssignmentData)
        classAverages = {}
        for className in classAssignments:
            classAverages[className] = calcAverage(classAssignments[className]['assignments'], classAssignments[className]['categories'])
        return classAverages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating class averages: {e}")

@app.put("/update_transcript_grades")
def update_transcript_grades_api(update_grades: UpdateTranscriptGrades, username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        transcript = getTranscript(session)
        tranGrades = getTranscriptGrades(transcript)
        tranGrades = modifyTranGrades(tranGrades, update_grades.grades)
        return tranGrades
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating transcript grades: {e}")

@app.post("/calculate_gpa")
def calculate_gpa_api(dif_scale_classes: DifScaleClasses, username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        transcript = getTranscript(session)
        tranGrades = getTranscriptGrades(transcript)
        calculatedGPA = calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses=dif_scale_classes.classes)
        return {"gpa": calculatedGPA}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating GPA: {e}")

@app.get("/official_gpa")
def get_official_gpa_api(username: str):
    try:
        session = sessions.get(username)
        if not session:
            raise HTTPException(status_code=401, detail="Session not found")
        transcript = getTranscript(session)
        official_gpa = getOfficialGPA(transcript)
        print(f"OFFICIAL GPA: {official_gpa}")
        return official_gpa
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting official GPA: {e}")

@app.get("/")
def root():
    return {"message": "Backend Is Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)