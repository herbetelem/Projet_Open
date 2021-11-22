import requests
import pandas as pd
from bs4 import BeautifulSoup
import function_parse as fp
import parsing_page as pp

""" Main function who will run all the function our programms will need"""
def main():
    category = get_info_category()
    all_data = {
        "product_page_url" : [],
        "universal_product_code" : [],
        "title" : [],
        "price_including_tax" : [],
        "price_excluding_tax" : [],
        "number_available" : [],
        "product_description" : [],
        "category" : [],
        "review_rating" : [],
        "image_url" : [],
    }

    fp.clearConsole()
    print("all the category have been know")

    i = 1
    for categ in category:
        # call the function to get the list of book from a category
        list_books = get_list_book_by_categ(categ)

        o = 1
        for book in list_books:
            tmp_link = "http://books.toscrape.com/catalogue/" + str(book)
            
            # call the function to parse a specific page
            info_book = pp.get_info_product(tmp_link)
            
            # store all the data into my dictionnary
            all_data["product_page_url"].append(info_book["product_page_url"])
            all_data["universal_product_code"].append(info_book["universal_product_code"])
            all_data["title"].append(info_book["title"])
            all_data["price_including_tax"].append(info_book["price_including_tax"])
            all_data["price_excluding_tax"].append(info_book["price_excluding_tax"])
            all_data["number_available"].append(info_book["number_available"])
            all_data["product_description"].append(info_book["product_description"])
            all_data["category"].append(info_book["category"])
            all_data["review_rating"].append(info_book["review_rating"])
            all_data["image_url"].append(info_book["image_url"])
            
            fp.clearConsole()
            print("catégory " + str(i) + "/" + str(len(category)))
            print("book " + str(o) + "/" + str(len(list_books)))
            o = o+1
        i = i+1
    
    # # export to pandas at excel format
    dataframe = pd.DataFrame(all_data)
    dataframe.to_excel('all_data.xlsx')

""" Function who get the category's list of books from the home page """
def get_info_category(link="http://books.toscrape.com/index.html"):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    category = []
    categs = fp.find_something(soup, "ul", "nav-list")
    categs = str(categs[0]).split("<ul>")
    del categs[0]
    categs = categs[0]
    categs = str(categs).split("                                ")
    for categ in categs:
        categ = str(categ).split("\n")
        for line in categ:
            if len(line) > 0 and line[0].isupper and line[0] not in ["<", ">", " "]:
                line = line.replace("(", "")
                line = line.replace(")", "")
                line = line.replace("#", "")
                line = line.replace("'", "")
                category.append(line.replace(" ", "-"))
    for i in range(len(category)):
        link = "http://books.toscrape.com/catalogue/category/books/" + str(str(category[i]) + "_" + str(i + 2)).lower() + "/index.html"
        category[i] = [category[i], link, fp.get_nb_books(link)]
    
    return category

""" Function who get the list of book from a cetagory specific """  
def get_list_book_by_categ(category):
    link = category[1]
    nb = category[2]
    final_list = []

    # if there is more than 20 books, there is a pagination so i have to handle this
    if nb <= 20:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        lists = fp.find_something(soup, "article", "product_pod")
        for lane in lists:
            final_list.append(fp.parse_lane_for_categ(lane))
    else:
        nb_tmp = nb
        i = 1
        # with this 'while' i can read the all page
        while nb_tmp > 0:
            nb_tmp = nb_tmp - 20
            link_tmp = link.replace("index.html", "page-" + str(i) + ".html")
            i = i + 1
            page = requests.get(link_tmp)
            soup = BeautifulSoup(page.content, 'html.parser')
            lists = fp.find_something(soup, "article", "product_pod")
            for lane in lists:
                final_list.append(fp.parse_lane_for_categ(lane))
    return final_list

main()