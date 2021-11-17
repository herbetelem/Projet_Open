from typing import final
import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv


def clear_tab(element, tables):
    tables = [table.replace(element, "") for table in tables]
    return tables

def find_something(soup, balise, class_find=False):
    if class_find:
        result = soup.find_all(balise, class_=class_find)
    else:
        result = soup.find_all(balise)
    return result

def get_info_product(link):
    # je recupere ma page et je la met au format lisible par soup
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # je definit mon dico qui stockera mes valeurs
    final_result = {
        "product_page_url" : link,
        "universal_product_code" : False,
        "title" : False,
        "price_including_tax" : False,
        "price_excluding_tax" : False,
        "number_available" : False,
        "product_description" : False,
        "category" : False,
        "review_rating" : False,
        "image_url" : False,
    }

    # je recupere le titre et la description
    titles = find_something(soup, "h1")
    final_result["title"] = titles[0].string
    description = find_something(soup, "article", "product_page")
    description = str(description[0]).split("<p>")
    del description[0]
    description = str(description[0]).split("</p>")
    del description[1]
    final_result["product_description"] = description[0]


    # je recupere les infos qui proviennent du tableau
    tables = find_something(soup, "table", "table-striped")
    tables = str(tables[0]).split("<tr>")

    del tables[0]

    tables = clear_tab("</tr>", tables)
    tables = clear_tab("\n", tables)

    for i in range(len(tables)):
        tables[i] = tables[i].split("><")
        del tables[i][0]
        tables[i] = tables[i][0]

    tables = clear_tab("</td>", tables)
    tables = clear_tab("td>", tables)
    tables = clear_tab("</td", tables)

    final_result["universal_product_code"] = tables[0]
    final_result["price_excluding_tax"] = tables[2]
    final_result["price_including_tax"] = tables[3]
    final_result["number_available"] = tables[5]

    # je recupere l'image
    img = find_something(soup, "div", "item active")
    img = str(img[0]).split('src="')
    del img[0]
    img = clear_tab('"/>\n</div>', img)
    img = clear_tab('../../', img)
    final_result["image_url"] = "http://books.toscrape.com/" + img[0]

    #je recupere la note
    note = find_something(soup, "p", "star-rating")
    note = str(note[0]).split(">")
    note = note[0].split(" ")
    note = note[2].replace('"', '')
    final_result["review_rating"] = note

    # je recupere la catégorie
    categ = find_something(soup, "ul", "breadcrumb")
    categ = str(categ[0]).split("<li>")
    categ = categ[3].split('">')
    categ = categ[1]
    categ = categ.split("</a>")
    categ = categ[0]
    final_result["category"] = categ

    # exporter en csv
    # en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
    # with open('data.csv', 'w') as fichier_csv:
    #     writer = csv.writer(fichier_csv, delimiter=',')
    #     writer.writerow(en_tete)
    #     ligne = []
    #     for key, value in final_result.items():
    #         ligne.append(value)
    #     writer.writerow(ligne)

    # # exporter en pandas
    for key, value in final_result.items():
        final_result[key] = [value]
    dataframe= pd.DataFrame(final_result)
    dataframe.to_excel('test.xlsx')
    return True

def get_info_category(link):
    return True


get_info_product("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")