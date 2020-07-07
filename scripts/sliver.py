import requests
from bs4 import BeautifulSoup

def get_pizza():
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
    response = requests.get('https://www.sliverpizzeria.com/', headers=headers).text
    soup = BeautifulSoup(response, features="html.parser")
    weekly = soup.find_all("div", {"class": "summary-excerpt"})
    index = 0
    parts = list(weekly[index])
    day = parts[1].getText()
    hours = parts[2].getText()
    menu = ' '.join([x for x in parts[3].getText().split(' ') if x != ''])

    return f"Here's today's Pizza at Sliver (Telegraph).\n\n{menu}"