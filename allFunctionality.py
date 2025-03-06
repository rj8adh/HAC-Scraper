# Testing usage
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
classAssignmentIDs = getAssignmentPageIDs(homeSC)
for id in classAssignmentIDs:
    print(f"\n\n{getAssignmentsForClass(session, id[0], id[1], id[2])}\n\n")
tranGrades = modifyTranGrades(tranGrades, {'CHEM':'0'})
calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses={'SPAN 1':5.0})
getOfficialGPA(transcript)