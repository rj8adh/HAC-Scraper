import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from sessionStarter import login

load_dotenv()
MAXGPA = float(os.getenv("MAXGPA"))
BASEURL = os.getenv("BASELINK")

# Scraping data from HAC front page
def getHomeScreen(session):
    home_url = BASEURL + "HomeAccess/Home/WeekView"
    try:
        response = session.get(home_url)
        response.raise_for_status()

        print("\nHOMEPAGE PROCESSED SUCCESSFULLY\n")
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving transcript: {e}")
        return None
    

# Fetching all transcript data    
def getTranscript(session):
    try:
        transcriptURL = BASEURL + "HomeAccess/Content/Student/Transcript.aspx"
        response = session.get(transcriptURL)
        response.raise_for_status()

        print("\nTRANSCRIPT PROCESSED SUCCESSFULLY\n")
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving transcript: {e}")
        return None


def getAssignmentsForClass(session, sectionKey: str, course_session: str, rc_run: str):
    assignmentURL = BASEURL + "HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx"
    # API parameters/details
    params = {
        "section_key": sectionKey,
        "course_session": course_session,
        "RC_RUN": rc_run,
        "MARK_TITLE": "MP   .Trim()",
        "MARK_TYPE": "MP   .Trim()",
        "SLOT_INDEX": "1",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = session.get(assignmentURL, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request to assignment details successful")
        return response.content 
    else:
        # Some debugging stuff in case request wasn't successful
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)