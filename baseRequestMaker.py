import requests

cookies = {
    '_ga': 'GA1.1.878361632.1723506218',
    '_fbp': 'fb.1.1723506218213.914476372463750677',
    '__gsas': 'ID=98e4acf4f4aa4548:T=1724287401:RT=1724287401:S=ALNI_MZO5v6unU1zosbZKHkg9OfdQHzAog',
    '_ga_BQ269GBVTL': 'GS1.1.1740188963.7.0.1740188963.60.0.0',
    '_gcl_au': '1.1.780050007.1740188964',
    '_ga_JQF7CXB5GN': 'GS1.1.1740188963.6.0.1740188963.60.0.0',
    'SPIHACSiteCode': '',
    '__RequestVerificationToken_L0hvbWVBY2Nlc3M1': 'DdMBAGWuNqUxYvOv72EafFKlq-7X2pg5k36zvyrHqG8BE9UlGIvAXWcFJIDOYIdA2yGPnTSdmq56NbcmlcaArzrLbFMG8rqVlG2S9G8fMU01',
    'apt.sid': 'AP-YDUVDTYHCH0C-2-1740799091641-28293366',
    'apt.uid': 'AP-YDUVDTYHCH0C-2-1740799091641-23845684.0.2.556ebf96-5303-416f-9f46-64fa500839b3',
    'ASP.NET_SessionId': '1xeovakh4i50e2kldssnbkgp',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://accesscenter.roundrockisd.org',
    'Referer': 'https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ga=GA1.1.878361632.1723506218; _fbp=fb.1.1723506218213.914476372463750677; __gsas=ID=98e4acf4f4aa4548:T=1724287401:RT=1724287401:S=ALNI_MZO5v6unU1zosbZKHkg9OfdQHzAog; _ga_BQ269GBVTL=GS1.1.1740188963.7.0.1740188963.60.0.0; _gcl_au=1.1.780050007.1740188964; _ga_JQF7CXB5GN=GS1.1.1740188963.6.0.1740188963.60.0.0; SPIHACSiteCode=; __RequestVerificationToken_L0hvbWVBY2Nlc3M1=DdMBAGWuNqUxYvOv72EafFKlq-7X2pg5k36zvyrHqG8BE9UlGIvAXWcFJIDOYIdA2yGPnTSdmq56NbcmlcaArzrLbFMG8rqVlG2S9G8fMU01; apt.sid=AP-YDUVDTYHCH0C-2-1740799091641-28293366; apt.uid=AP-YDUVDTYHCH0C-2-1740799091641-23845684.0.2.556ebf96-5303-416f-9f46-64fa500839b3; ASP.NET_SessionId=1xeovakh4i50e2kldssnbkgp',
}

data = {
    '__RequestVerificationToken': 'ssyrALaxQ8OZ81eoCLTCprRJR3G4gU5y7UxKF9YhJWLOfXF4TD_s7By7H04c9yNmZoauVlIZDh2tIbGiRqBv8wP-dUEgUBLojD-9xZ-xG141',
    'SCKTY00328510CustomEnabled': 'False',
    'SCKTY00436568CustomEnabled': 'False',
    'Database': '10',
    'VerificationOption': 'UsernamePassword',
    'LogOnDetails.UserName': 'USERNAME HERE',
    'tempUN': '',
    'tempPW': '',
    'LogOnDetails.Password': 'PASSWORD HERE',
}

response = requests.post(
    'https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f',
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.text)