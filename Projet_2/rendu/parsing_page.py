import requests
from bs4 import BeautifulSoup
import function_parse as fp

""" Function who will parse the data from a page of a specific book """
def get_info_product(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # I set up my final dictionary who will stock all the data
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

    # get the title and description
    titles = fp.find_something(soup, "h1")
    final_result["title"] = titles[0].string
    description = fp.find_something(soup, "article", "product_page")
    description = str(description[0]).split("<p>")
    del description[0]
    if len(description) > 0:
        description = str(description[0]).split("</p>")
        del description[1]
        final_result["product_description"] = description[0]
    else:
        final_result["product_description"] = "no description"


    # get the all info from the table
    tables = fp.find_something(soup, "table", "table-striped")
    tables = str(tables[0]).split("<tr>")

    del tables[0]

    tables = fp.clear_tab("</tr>", tables)
    tables = fp.clear_tab("\n", tables)

    for i in range(len(tables)):
        tables[i] = tables[i].split("><")
        del tables[i][0]
        tables[i] = tables[i][0]

    tables = fp.clear_tab("</td>", tables)
    tables = fp.clear_tab("td>", tables)
    tables = fp.clear_tab("</td", tables)

    final_result["universal_product_code"] = tables[0]
    final_result["price_excluding_tax"] = tables[2]
    final_result["price_including_tax"] = tables[3]
    final_result["number_available"] = tables[5]

    # get the image
    img = fp.find_something(soup, "div", "item active")
    img = str(img[0]).split('src="')
    del img[0]
    img = fp.clear_tab('"/>\n</div>', img)
    img = fp.clear_tab('../../', img)
    final_result["image_url"] = "http://books.toscrape.com/" + img[0]

    # get the rating
    note = fp.find_something(soup, "p", "star-rating")
    note = str(note[0]).split(">")
    note = note[0].split(" ")
    note = note[2].replace('"', '')
    final_result["review_rating"] = note

    # get the category
    categ = fp.find_something(soup, "ul", "breadcrumb")
    categ = str(categ[0]).split("<li>")
    categ = categ[3].split('">')
    categ = categ[1]
    categ = categ.split("</a>")
    categ = categ[0]
    final_result["category"] = categ

    return final_result