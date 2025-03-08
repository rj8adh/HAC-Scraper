from dotenv import load_dotenv
import os

load_dotenv()
MAXGPA = float(os.getenv("MAXGPA"))
BASEURL = os.getenv("BASELINK")


def modifyTranGrades(tranGrades: list, gradesToModify: dict):
    updatedTranGrades = [
        [
            gradeInfo[0],
            gradeInfo[1],
            gradeInfo[2],
            gradesToModify[gradeInfo[1]]
            if gradeInfo[1] in gradesToModify else gradeInfo[3],
        ]  # Made it a list instead of tuple in case I want to add info later
        for gradeInfo in tranGrades
    ]  # Using list comprehension to overcomplicate things 😎

    return updatedTranGrades


def addTheoreticalGrade(currAssignments: list, categories: list, assignment: dict):
    try:
        for i in range(len(categories)):
            if assignment['category'] in categories[i].values():
                # print(f"Previous Max Points: {categories[i]['max_points']}")
                categories[i]['max_points'] = float(categories[i]['max_points'])
                categories[i]['max_points'] += float(assignment['weight'])
                print(f"Updated Max Points: {categories[i]['max_points']}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    currAssignments.append(assignment)


def calcAverage(assignments: list, categories: list):
    categoriesAndDetails = []
    categoryNames = []
    usedCategories = []
    onlyOneCategory = False

    if not categories:
        onlyOneCategory = True
        runningTotal = 0
        print("No Categories Given So Defaulting To Single Category With Weight 1.0")

    maxGrade = 0
    classGrade = 0

    # print(f"CLASS CATEGORIES: {categories}")

    # Getting all category detail and starting a running count of the points each category has (because HAC doesn't provide it)
    for category in categories:
        try:
            categoryDetails = {'running_points': 0.0}
            categoryDetails['name'] = category['category_name']
            # print(f"CATEGORY NAME: {categoryDetails['name']}")
            categoryDetails['max_points'] = float(category['max_points'])
            categoryDetails['weight'] = float(category['category_weight'])
            categoriesAndDetails.append(categoryDetails)
            categoryNames.append(categoryDetails['name'])
        except Exception as e:
            print(f"Exception: {e}")
            print(f"Category may not have expected values.\nCategory:\n{category}")

    # Looping through every assignment and updating values accordingly
    for assignment in assignments:
        try:
            assignmentCategory = assignment['category']
            if assignmentCategory in categoryNames:

                if assignmentCategory not in usedCategories:
                    usedCategories.append(assignmentCategory)
                    categIdx = categoryNames.index(assignmentCategory)
                    maxGrade += categoriesAndDetails[categIdx]['weight'] * 100 # Getting maxGrade in the case that the end grade doesn't add up to 100 
                                                                               # (happens if teacher hasn't entered all grades in yet)

                if assignment.get('score'):  # Making sure score isn't empty and exists
                    categoriesAndDetails[categoryNames.index(assignmentCategory)]['running_points'] += float(assignment['score'])
            # Adding to maxGrade in case no categories are given (meaning everything is weight 1.0)
            elif onlyOneCategory:
                # print(f"No categories given, default constructing category: {assignmentCategory} with weight 1")
                if assignment.get('score'):  # Making sure score isn't empty and exists
                    runningTotal += float(assignment['score'])
                    maxGrade += 100
            else:
                print(f"Category: {assignmentCategory} Not Found")
        except:
            print("NO CATEGORY KEY OR INVALID DATA")
        # print(assignment)
    if not onlyOneCategory:
        for category in categoriesAndDetails:
            try:
                # print(category)
                if category['max_points'] != 0:
                    classGrade += (category['running_points'] / category['max_points']) * category['weight'] * 100 # Calculating weighted class grade
                else:
                    print(f"Warning: Category '{category['name']}' has max_points of 0.")
            except Exception as e:
                print(f"Error: {e}\nFor: {category}")
        if maxGrade:
            # print(f"MAXGRADE: {maxGrade}\nCLASSGRADE: {classGrade}")
            return round((classGrade / maxGrade) * 100) # In case classGrade doesn't add up to 100
        return classGrade
    else:
        return round((runningTotal / maxGrade) * 100)


# Calculating GPA based on grades
def calcGPA(classGrades: list, ignoreClasses: list = [], difScaleClasses: dict = {}):
    courseGrades = {}
    numGrades = 0

    # Finding and averaging grades between classes with same name
    for gradeInfo in classGrades:
        courseDesc = gradeInfo[1]
        avgGrade = float(gradeInfo[3])

        if courseDesc in ignoreClasses:
            continue

        if courseDesc not in courseGrades:
            courseGrades[courseDesc] = []
        courseGrades[courseDesc].append(avgGrade)

    # Rounding and Calculating each grade for each class
    averagedGrades = {}
    for courseDesc, grades in courseGrades.items():
        averagedGrades[courseDesc] = round(sum(grades) / len(grades))

    gradeTotal = 0.0

    # Calculating GPA with our grade values for each class
    for courseDesc, avgGrade in averagedGrades.items():
        if courseDesc in difScaleClasses:
            classMaxGPA = difScaleClasses[courseDesc]
            weightedGrade = (classMaxGPA - 1) + ((avgGrade - 90) / 10)
        else:
            weightedGrade = (MAXGPA - 1) + ((avgGrade - 90) / 10)

        gradeTotal += weightedGrade
        numGrades += 1

    if numGrades == 0:
        print("No grades to calculate GPA.")
        return None

    average = gradeTotal / numGrades
    return round(average, 3)


#TODO Extra functions for front-end compatibility
def addGradesToTranscript(grades: dict, trans: list):
    for grade in grades:
        trans.append(["", grade, "", float(grades[grade])])


def changeGrade():
    return


def getCurrentYearGPA(grades: list):
    return


def getMPGPA():
    return