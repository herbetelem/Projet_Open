import requests
from bs4 import BeautifulSoup
import os

""" function to clear an element in my table """
def clear_tab(element, tables):
    tables = [table.replace(element, "") for table in tables]
    return tables

""" function to get an element with soup """
def find_something(soup, balise, class_find=False):
    if class_find:
        result = soup.find_all(balise, class_=class_find)
    else:
        result = soup.find_all(balise)
    return result

""" function to get the number of book in a list """
def get_nb_books(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    nb = find_something(soup, "form", "form-horizontal")
    nb = str(nb[0]).split("<strong>")
    del nb[0]
    nb = str(nb[0]).split("</strong>")
    nb = nb[0]
    return int(nb)

""" Function to parse and get all the link bay lane """
def parse_lane_for_categ(lane):
    lane = str(lane).split("<h3>")
    lane = str(lane[1]).split("</h3>")
    lane = str(lane[0]).split('<a href="')
    lane = str(lane[1]).split('" ')
    lane = str(lane[0])
    lane = lane.replace(".", "")
    lane = lane.replace("/", "")
    lane = lane.replace("indexhtml", "/index.html")
    return lane

""" function to clear the console from the terminal """
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)
