# Testing usage
from sessionStarter import login
from dataParsers import *
from pageScrapers import *
import os

loginURL = BASEURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"

username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

session = login(loginURL, username, password)
homeSC = getHomeScreen(session)
grades = parseGrades(homeSC)
transcript = getTranscript(session)
tranGrades = getTranscriptGrades(transcript)
test = getAssignmentPageLinks(homeSC)
getAssignmentsForClass(session, "2754856")
tranGrades = modifyTranGrades(tranGrades, {'CHEM':'0'})
calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses={'SPAN 1':5.0})
getOfficialGPA(transcript)

# Assignment Page Testing Links
# https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx
# https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx?section_key=2754856&course_session=1&RC_RUN=3&MARK_TITLE=MP%20%20%20.Trim()&MARK_TYPE=MP%20%20%20.Trim()&SLOT_INDEX=1'