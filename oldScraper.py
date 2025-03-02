import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def login(url, username, password):
    session = requests.Session()

    try:
        # Get login page and valid CSRF token
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '__RequestVerificationToken'})['value']

        # Setting up the data for login
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

        # Sending post request to login to HAC
        response = session.post(url, data=data)
        # print(response.status_code)
        # print(response.text)
        response.raise_for_status()

        # Check for successful login (this may change if they update HAC's code)
        updatedSoup = BeautifulSoup(response.content, 'html.parser')

        allTitles = updatedSoup.find_all("title")

        print(updatedSoup.prettify())

        for title in allTitles:
            print(title.getText())
            # Making sure the login was successful and the page has changed to what we want
            if "Home View Summary" == title.getText(): # Change this check if HAC sourecode changes
                print("Login successful!")
                return updatedSoup
        else:
            print("Login failed. Check credentials or website sourcecode.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return None
    
    except TypeError:
        print("Error: CSRF token input field not found.")
        return None


# Testing functionality
login_url = "https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f"
username = os.getenv('HACUSERNAME')
password = os.getenv('HACPASSWORD')

# print(username, password)

try:
    gradesSoup = login(login_url, username, password)
except requests.exceptions.RequestException as e:
    print(f"Error after login: {e}")

try:
    transcriptSoup = login("https://accesscenter.roundrockisd.org/HomeAccess/Grades/Transcript", username, password)
except requests.exceptions.RequestException as e:
    print(f"Error after login for transcript: {e}")

if gradesSoup:
    print("Successfully Logged In")

else:
    print("Login process failed.")