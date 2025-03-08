# Home Access Center Grade Scraper

This program scrapes gives easy access to your HAC grades, GPA, and rank. You can also edit the weighted scale of certain grades and calculate what your GPA would've been with different grades. 

## Description

This script uses the requests library to send secure api calls to Home Access Center with your username and password and parse the data it recieves into things such as grades and rank.

## Getting Started

### Installing
```
pip install -r requirements.txt
```
* Ensure all dependencies are installed and up to date

### Executing Program

* Configure the program by adding a .env file with your HAC username, password, max GPA, and HAC base URL
    * A base URL is just the link from the beginning to the backslash right before the word HomeAcces in the URL

* Run the program by executing allFunctionality.py

### Expected Output From Testing Data

![Screenshot Of Working Script Output](<https://media-hosting.imagekit.io//1c68f8c7208b4dc6/screenshot_1741415870664.png?Expires=1836023870&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=U2PjeZsRtnNnl7npyht~4V0ZSHQsy2vX6ZY2uvNA0-jpQaeKw5X3ErtbCwOOp67q9qKSTHlsRKJmKKtYIfr4dyvB8vMLB12IqEjUiEAisjJ7igV0oQmrKlAFSScJHN5PorqBZjp19myJwhlicZSg8dcVOqlKaMlETK-u64pnBrLmz2d~~cwPd6EaxWiYHadggDwvBAItaQFDETAuzpld2wBeD3SfEWZ6TCo4g8KS92ky1X50j1FEvZsSh733ZAcOlpYRoRMET3PzJnPHhVfd1NtA9aiVf1qQheXw~q52Qi3mf4NRvW2d7xgK74~7PvEY0Ir-CLYr9aZ2QLMUvRcnqw__>)

## Help

If there are any issues such as compatibility with different school districts, please contact me at the email below:

## Authors

Contributors names and contact info

Aarjit Adhikari
[@microrew0@gmail.com](https://gmail.com)

## Version History
* 0.3
    * Added Theoretical Assignment Feature and GPA Calculator
* 0.2
    * Upgraded/Reworked Assignment Reading Feature
* 0.15
    * Added Assignment Reading Feature
* 0.1
    * Initial Release