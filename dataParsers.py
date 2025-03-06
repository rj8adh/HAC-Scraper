from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

load_dotenv()
MAXGPA = float(os.getenv("MAXGPA"))
BASEURL = os.getenv("BASELINK")

# This function is currently outdated, it's still here in case I need it to scrape the page on click of class average
def getAssignmentPageIDs(homeSourceCode, returnID: bool = True):
    classAndPageLinks = {}
    homeSoup = BeautifulSoup(homeSourceCode, 'html.parser')

    # Finding all boxes containing grades
    allGradeBoxes = homeSoup.find("tbody")
    gradeBoxes = allGradeBoxes.find_all("tr")

    for gradeBox in gradeBoxes:
        # Filtering to get course name and necessary details
        className = gradeBox.find("a", attrs={'id':'courseName'}).getText()
        grade = gradeBox.find("a", attrs={'id':'average'})
        # print(grade['href'])
        classAndPageLinks[className] = grade['href']

    # Return IDs for each class instead of the base href value
    if returnID:
        for className in classAndPageLinks:
            assignmentPageID = re.findall(r'\d+', classAndPageLinks[className]) # Finding all numbers in the url
            classAndPageLinks[className] = assignmentPageID
            # print(f"Assignment Page Details{assignmentPageID}")
    
    return classAndPageLinks


# Returns a dictionary with the key being the class name and the value being a list of all assignments and their corresponding attributes
def parseAssignments(assignmentSC):
    assignmentSoup = BeautifulSoup(assignmentSC, 'html.parser')
    allClassData = {}
    allClassNames = []

    # Get all class names
    assignmentHeaders = assignmentSoup.find_all('div', attrs={'class':'AssignmentClass'})
    for header in assignmentHeaders:
        className = header.find('a', attrs={'class':'sg-header-heading'}).getText().strip()
        allClassNames.append(className)

    # Find all assignment tables
    assignmentTables = assignmentSoup.find_all('table', id=lambda x: x and x.startswith('plnMain_rptAssigmnetsByCourse_dgCourseAssignments_')) # The "x and" part is just to make sure that whitespaces dont mess it up
    # print(f"ASSIGNMENT TABLES:{assignmentTables}")
    for classKey, assignmentTable in enumerate(assignmentTables): # Making classKey a counter starting from 0 adding one each iteration

        if allClassNames[classKey] not in allClassData:
            allClassData[allClassNames[classKey]] = {'assignments': [], 'categories': []}

        assignments = []
        rows = assignmentTable.find_all('tr')
        rows = rows[1:]  # Skipping the header row

        for row in rows:
            # Getting every row's data (basically getting each column for each row)
            cols = row.find_all('td')
            if cols:
                assignmentData = {}
                try:
                    assignmentData['due_date'] = cols[0].text.strip()
                    assignmentData['assigned_date'] = cols[1].text.strip()
                    assignmentData['name'] = cols[2].text.strip()
                    assignmentData['category'] = cols[3].text.strip()
                    assignmentData['score'] = cols[4].text.strip()
                    assignmentData['weight'] = cols[5].text.strip()
                    assignmentData['weighted_score'] = cols[6].text.strip()
                    assignmentData['total_points'] = cols[7].text.strip()
                    assignmentData['weighted_total_points'] = cols[8].text.strip()
                except IndexError: # Some assignments don't have variables for certain fields
                    continue
                assignments.append(assignmentData)
                # print(f"\nUPDATED ASSIGNMENTS {assignments}\n")
        allClassData[allClassNames[classKey]]['assignments'] = assignments

    # Find all category tables
    categTables = assignmentSoup.find_all('table', id=lambda x: x and x.startswith('plnMain_rptAssigmnetsByCourse_dgCourseCategories_'))

    for classKey, table in enumerate(categTables):

        if allClassNames[classKey] not in allClassData:
            allClassData[allClassNames[classKey]] = {'assignments': [], 'categories': []}

        categRows = table.find_all('tr')
        categRows = categRows[1:-1]  # Skipping header and total rows
        categories = []

        # Getting information on each category for each class
        for row in categRows:
            cols = row.find_all('td')
            if cols:
                categData = {}
                try:
                    categData['category_name'] = cols[0].text.strip()
                    categData['student_points'] = cols[1].text.strip()
                    categData['max_points'] = cols[2].text.strip()
                    categData['percent'] = cols[3].text.strip()
                    categData['category_weight'] = cols[4].text.strip()
                    categData['category_points'] = cols[5].text.strip()
                except IndexError:
                    continue
                categories.append(categData)
        allClassData[allClassNames[classKey]]['categories'] = categories

    return allClassData


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