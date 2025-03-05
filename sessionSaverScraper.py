import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
MAXGPA = 6.0
BASEURL = "https://accesscenter.roundrockisd.org/"

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

    # Error handling
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return None
    except TypeError:
        print("Error: CSRF token input field not found.")
        return None
    

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


# TODO Get this script working properly
def getAssignmentPageLinks(homeSourceCode):
    classAndPageLinks = {}
    homeSoup = BeautifulSoup(homeSourceCode, 'html.parser')

    # Finding all boxes containing grades
    allGradeBoxes = homeSoup.find("tbody")
    gradeBoxes = allGradeBoxes.find_all("tr")

    for gradeBox in gradeBoxes:
        # Filtering to get course name and corresponding grade average
        className = gradeBox.find("a", attrs={'id':'courseName'}).getText()
        grade = gradeBox.find("a", attrs={'id':'average'})
        print(grade['href'])
        for property in grade:
            print(f"Property of grade: {property}")
        classAndPageLinks[className] = grade
    
    return classAndPageLinks


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

loginURL = BASEURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"

username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

session = login(loginURL, username, password)
homeSC = getHomeScreen(session)
getAssignmentsForClass(session, "2353121") # TODO Get id from href a tag with "courseName" id


# Current Testing Area (will make it a seperate script tomorrow)








# Parsing grades from homepage info
def parseGrades(homeSourceCode):
    classAndGrades = {}
    homeSoup = BeautifulSoup(homeSourceCode, 'html.parser')

    # Finding all boxes containing grades
    allGradeBoxes = homeSoup.find("tbody")
    gradeBoxes = allGradeBoxes.find_all("tr")

    for gradeBox in gradeBoxes:
        # Filtering to get course name and corresponding grade average
        className = gradeBox.find("a", attrs={'id':'courseName'}).getText()
        grade = gradeBox.find("a", attrs={'id':'average'}).getText()

        print(f"Your average in {className} is {grade}")
        classAndGrades[className] = grade
    
    return classAndGrades


# Parsing transcript grades from transcript source code
def getTranscriptGrades(tranSourceCode, hsOnly: bool = True):

    transcriptSoup = BeautifulSoup(tranSourceCode, 'html.parser')
    bigTable = transcriptSoup.find("table")
    allTranGrades = []

    if not bigTable:
        print("Error: Main table not found.")
        return

    gradeTranBoxes = bigTable.find_all("td", attrs={'class': 'sg-transcript-group'})

    for box in gradeTranBoxes:
        # Basic CSS selector getting any span class with an id that starts with that
        gradeData = box.select(f'span[id^="plnMain_rpTranscriptGroup_lblGradeValue"]')[0] # .select() returns a list so I have to specify index 0
        
        # Skip empty grades and grades before hs if hsOnly is true
        if not gradeData:
            continue 
        gradeLevel = int(gradeData.getText())
        if hsOnly and gradeLevel < 9:
            continue  

        courseTable = box.select(f'table[id^="plnMain_rpTranscriptGroup_dgCourses_"]')[0]

        # Filtering through the nested tables and different rows to get all previous grades
        if courseTable:
            rows = courseTable.find_all('tr', attrs={'class':'sg-asp-table-data-row'})
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    courseCode = cols[0].text.strip()
                    courseDescription = cols[1].text.strip()
                    sem1 = cols[2].text.strip()
                    sem2 = cols[3].text.strip()
                    final = cols[4].text.strip()

                    grades = [sem1, sem2, final]
                    validGrades = [int(grade) for grade in grades if grade.isdigit()] # Making sure all grades are numbers (some classes may be N/A)

                    if validGrades:
                        average = sum(validGrades) / len(validGrades)
                        print(f"Grade: {gradeLevel}, Course: {courseDescription} ({courseCode}), Average: {round(average, 2)}")
                        allTranGrades.append([gradeLevel, courseDescription, courseCode, round(average, 2)])
                    else:
                        print(f"Grade: {gradeLevel}, Course: {courseDescription} ({courseCode}), Average: N/A")
        else:
            print(f"Grade: {gradeLevel}, Course table not found.")

    return allTranGrades


# Calculating GPA based on grades
def calcGPA(pastTranGrades: list, ignoreClasses: list = [], difScaleClasses: dict = {}):
    numGrades = 0
    gradeTotal = 0.0

    for gradeInfo in pastTranGrades:
        courseDesc = gradeInfo[1]
        avgGrade = int(gradeInfo[3])

        if courseDesc in ignoreClasses:
            continue

        if courseDesc in difScaleClasses:
            # Using different max GPA based on provided different scale classes
            classMaxGPA = difScaleClasses[courseDesc]
            weightedGrade = (classMaxGPA - 1) + ((avgGrade - 90) / 10)
        else:
            # Using the default MAXGPA scale
            weightedGrade = (MAXGPA - 1) + ((avgGrade - 90) / 10)

        gradeTotal += weightedGrade
        numGrades += 1

    if numGrades == 0:
        print("No grades to calculate GPA.")
        return

    average = gradeTotal / numGrades
    print(f"CALCULATED GPA IS {round(average, 3)}")


def getOfficialGPA(transcriptCode):
    transcriptSoup = BeautifulSoup(transcriptCode, 'html.parser')
    GPAtable = transcriptSoup.find('table', attrs={'id':'plnMain_rpTranscriptGroup_tblCumGPAInfo'}) # Getting the table with GPA info
    if GPAtable:
        rows = GPAtable.find_all('tr', attrs={'class':'sg-asp-table-data-row'})
        # Getting every row and corresponding data from columns
        for row in rows:
            cols = row.find_all('td')
            if cols:
                GPAtype = cols[0].find('span').text.strip()
                GPAval = cols[1].find('span').text.strip()
                rank = cols[2].find('span').text.strip() if cols[2].find('span') else "N/A" # Handle empty rank

                print(f"GPA Type: {GPAtype}, GPA: {GPAval}, Rank: {rank}")
    else:
        print("GPA table not found.")


def modifyTranGrades(tranGrades: list, gradesToModify: dict):
    updatedTranGrades = [
        [
            gradeInfo[0],
            gradeInfo[1],
            gradeInfo[2],
            gradesToModify[gradeInfo[1]] if gradeInfo[1] in gradesToModify else gradeInfo[3],
        ] # Made it a list instead of tuple in case I want to add info later
        for gradeInfo in tranGrades 
    ] # Using list comprehension to overcomplicate things 😎

    return updatedTranGrades


# Testing usage
# loginURL = BASEURL + "HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"

# username = os.getenv('HACUSERNAME')
# password = os.getenv('HACPASSWORD')

# session = login(loginURL, username, password)
# homeSC = getHomeScreen(session)
# # grades = parseGrades(homeSC)
# # transcript = getTranscript(session)
# # tranGrades = getTranscriptGrades(transcript)
# # test = getAssignmentPageLinks(homeSC)
# getAssignments(session)
# tranGrades = modifyTranGrades(tranGrades, {'CHEM':'0'})
# calcGPA(tranGrades, ignoreClasses=['TACS1', 'TAGMPD', 'LIFEFIT', 'W HIST', 'APTACSAL', 'IED', 'TH1TECH', 'VIDGD'], difScaleClasses={'SPAN 1':5.0})
# getOfficialGPA(transcript)

# https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx
# https://accesscenter.roundrockisd.org/HomeAccess/Content/Student/AssignmentsFromRCPopUp.aspx?section_key=2754856&course_session=1&RC_RUN=3&MARK_TITLE=MP%20%20%20.Trim()&MARK_TYPE=MP%20%20%20.Trim()&SLOT_INDEX=1'