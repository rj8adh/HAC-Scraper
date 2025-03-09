import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
MAXGPA = float(os.getenv("MAXGPA"))
BASEURL = os.getenv("BASELINK")

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