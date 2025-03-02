# TODO Increase readability and add comments

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
MAXGPA = 6.0

def login(url, username, password):
    # Starting a requests session to save and transfer cookies/data
    session = requests.Session()

    try:
        # Get login page and valid CSRF token
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        # Prepare login data
        data = {
            '__RequestVerificationToken': csrf_token,
            'SCKTY00328510CustomEnabled': 'False',
            'SCKTY00436568CustomEnabled': 'False',
            'Database': '10',
            'VerificationOption': 'UsernamePassword',
            'LogOnDetails.UserName': username,
            'tempUN': '',
            'tempPW': '',
            'LogOnDetails.Password': password,
        }

        # Getting link to test if login is successful
        login_post_url = url.split("Account")[0] + "Account/LogOn?ReturnUrl=%2fhomeaccess%2f"
        
        # This is just to make this script not seem like a bot
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = session.post(login_post_url, data=data, headers=headers)
        response.raise_for_status()

        # The rest of the code is checking for successful login:

        updatedSoup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())

        allTitles = updatedSoup.find_all("title")

        for title in allTitles:
            print(title.getText())
            # Making sure the login was successful and the page has changed to what we want
            if "Home View Summary" == title.getText(): # Change this check if HAC sourecode changes
                print("Login successful!")
                return session
        else:
            print("Login failed. Check credentials or website structure.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return None
    except TypeError:
        print("Error: CSRF token input field not found.")
        return None
    

def getHomeScreen(session):
    home_url = "https://accesscenter.roundrockisd.org/HomeAccess/Home/WeekView"
    try:
        response = session.get(home_url)
        response.raise_for_status()

        print("\nHOMEPAGE:\n", response.text)
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving transcript: {e}")
        return None
    

def parseGrades(homeSourceCode):
    classAndGrades = {}
    homeSoup = BeautifulSoup(homeSourceCode, 'html.parser')

    allGradeBoxes = homeSoup.find("tbody")
    gradeBoxes = allGradeBoxes.find_all("tr")

    for gradeBox in gradeBoxes:
        className = gradeBox.find("a", attrs={'id':'courseName'}).getText()
        grade = gradeBox.find("a", attrs={'id':'average'}).getText()

        print(f"Your average in {className} is {grade}")
        classAndGrades[className] = grade
    
    return classAndGrades

    
def getTranscript(session):
    try:
        transcript_url = "https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/Transcript.aspx"
        
        response = session.get(transcript_url)
        response.raise_for_status()

        print("\nTRANSCRIPT:\n", response.text)

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving transcript: {e}")
        return None
    

# Parsing transcript data from transcript source code
def getTranscriptGrades(tranSourceCode, hsOnly: bool = True):

    transcriptSoup = BeautifulSoup(tranSourceCode, 'html.parser')
    bigTable = transcriptSoup.find("table")
    allTranGrades = []

    if not bigTable:
        print("Error: Main table not found.")
        return

    gradeTranBoxes = bigTable.find_all("td", attrs={'class': 'sg-transcript-group'})

    for box in gradeTranBoxes:
        gradeData = box.select(f'span[id^="plnMain_rpTranscriptGroup_lblGradeValue"]')
        if not gradeData:
            continue  # Skip if grade data is missing

        gradeLevel = int(gradeData[0].getText())
        if hsOnly and gradeLevel < 9:
            continue  # Skip grades before high school if hsOnly is True

        courseTable = box.find('table', id=lambda x: x and x.startswith('plnMain_rpTranscriptGroup_dgCourses_'))

        if courseTable:
            rows = courseTable.find_all('tr', class_='sg-asp-table-data-row')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    courseCode = cols[0].text.strip()
                    courseDescription = cols[1].text.strip()
                    sem1 = cols[2].text.strip()
                    sem2 = cols[3].text.strip()
                    final = cols[4].text.strip()

                    grades = [sem1, sem2, final]
                    valid_grades = [int(grade) for grade in grades if grade.isdigit()]
                    if valid_grades:
                        average = sum(valid_grades) / len(valid_grades)
                        print(f"Grade: {gradeLevel}, Course: {courseDescription} ({courseCode}), Average: {round(average, 2)}")
                        allTranGrades.append([gradeLevel, courseDescription, courseCode, round(average, 2)])
                    else:
                        print(f"Grade: {gradeLevel}, Course: {courseDescription} ({courseCode}), Average: N/A")
        else:
            print(f"Grade: {gradeLevel}, Course table not found.")
    return allTranGrades


def calcGPA(pastTranGrades: list, ignoreClasses: list = [], difScaleClasses: dict = {}):
    numGrades = 0
    gradeTotal = 0.0

    for gradeInfo in pastTranGrades:
        course_description = gradeInfo[1]
        average_grade = gradeInfo[3]

        if course_description in ignoreClasses:
            continue

        if course_description in difScaleClasses:
            # Use the provided scale for this class
            class_max_gpa = difScaleClasses[course_description]
            weighted_grade = (class_max_gpa - 1) + ((average_grade - 90) / 10)
        else:
            # Use the default MAXGPA scale
            weighted_grade = (MAXGPA - 1) + ((average_grade - 90) / 10)

        gradeTotal += weighted_grade
        numGrades += 1

    if numGrades == 0:
        print("No grades to calculate GPA.")
        return

    average = gradeTotal / numGrades
    print(f"CALCULATED GPA IS {average:.3f}")

# Example usage
login_url = "https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"
username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

session = login(login_url, username, password)
# homeSoup = getHomeScreen(session)
# grades = parseGrades(homeSoup)
transcript = getTranscript(session)
tranGrades = getTranscriptGrades(transcript)
calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses={'SPAN 1':5.0})