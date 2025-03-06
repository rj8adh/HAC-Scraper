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


def getAssignmentsForClass(session, sectionKey: str):
    assignmentURL = "https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx"
    params = {
        "section_key": sectionKey,
        "course_session": "1",
        "RC_RUN": "3",
        "MARK_TITLE": "MP   .Trim()",
        "MARK_TYPE": "MP   .Trim()",
        "SLOT_INDEX": "1",
    }

    response = session.get(assignmentURL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        return response.content 
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text) # For debugging purposes