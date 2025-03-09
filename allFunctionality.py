from sessionStarter import login
from dataParsers import *
from pageScrapers import *
from gradeOperations import *
import os
from dotenv import load_dotenv

load_dotenv()

BASEURL = os.getenv("BASELINK")
username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

loginURL = BASEURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"

session = login(loginURL, username, password)
homeSC = getHomeScreen(session)
grades = parseGrades(homeSC)
transcript = getTranscript(session)
tranGrades = getTranscriptGrades(transcript)
allAssignmentData = getAssignmentsForClass(session)
classAssignments = parseAssignments(allAssignmentData)

theoGrade = {'name': 'This Better Work', 'category': 'Daily', 'weight': 100, 'score': 0}
classesToChange = ["Adv Spanish II"]
for classToChange in classesToChange:
    print(f"\nADDING THEORETICAL GRADE TO {classToChange}: {theoGrade}")
    addTheoreticalGrade(classAssignments[classToChange]['assignments'], classAssignments[classToChange]['categories'], theoGrade)
print()

classAverages = {}
for className in classAssignments:
    print(f"Assignments Average For: {repr(className)}:")
    newClassAverage = calcAverage(classAssignments[className]['assignments'], classAssignments[className]['categories'])
    print(newClassAverage)
    classAverages[className] = newClassAverage # Storing the average
print()

# Update transcript grade with new class average
for averageInfo in classAverages:
    tranGrades.append([10, averageInfo, '', classAverages[averageInfo]]) # The blank stuff is for ID, 10 is just the grade of the student which doesn't matter right now

updatedTranValue = {'CHEM': '0'}
print(f"UPDATED CLASS VALUE IN TRANSCRIPT: {updatedTranValue}")
tranGrades = modifyTranGrades(tranGrades, updatedTranValue)

difScaleClass = {'SPAN 1': 5.0}
print(f"Different Scale Class: {difScaleClass}")
calculatedGPA = calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses=difScaleClass)
# print(tranGrades)
print(f"Calculated GPA Based On Completed Semesters: {calculatedGPA}")
offGPA = getOfficialGPA(transcript)