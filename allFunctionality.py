# TODO Fix bug where certain grading categories dont show up (Primarily in IED)
from sessionStarter import login
from dataParsers import *
from pageScrapers import *
import os

BASEURL = os.getenv("BASELINK")
username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

loginURL = BASEURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"

session = login(loginURL, username, password)
homeSC = getHomeScreen(session)
grades = parseGrades(homeSC)
transcript = getTranscript(session)
tranGrades = getTranscriptGrades(transcript)
# classAssignmentIDs = getAssignmentPageIDs(homeSC) # No longer useful for new assignment scraping strategy
allAssignmentData = getAssignmentsForClass(session)
classAssignments = parseAssignments(allAssignmentData)

for className in classAssignments:
    print(f"\n\nASSIGNMENTS FOR {className}:\n\n")
    print(calcAverage(classAssignments[className]['assignments'], classAssignments[className]['categories']))
    # for assignmentData in classAssignments[className]['assignments']:
    #     for data in assignmentData:
    #         print(f"{data}: {assignmentData[data]}")
    #     print()

# print(getAssignmentsForClass(session, "2353121", "1", "3"))
tranGrades = modifyTranGrades(tranGrades, {'CHEM':'0'})
calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses={'SPAN 1':5.0})
getOfficialGPA(transcript)