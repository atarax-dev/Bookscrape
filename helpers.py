import requests
from bs4 import BeautifulSoup
import os
import urllib.request


def get_soup_object(url):
    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, "lxml")
    return soup


def extract_categories():
    soup = get_soup_object("http://books.toscrape.com/")
    categories = soup.find("div", class_="side_categories").find("ul", class_="nav nav-list").ul.findAll("li")
    categories_and_links = {}
    for i in categories:
        category = i.a.text.strip()
        link = "http://books.toscrape.com/" + i.a["href"]
        categories_and_links[category] = link
    return categories_and_links


def extract_books(link):
    soup = get_soup_object(link)
    booklist = soup.find("section").find("ol", class_="row").findAll("li")
    books_per_category = []
    for book in booklist:
        booktitle = book.find("article", class_="product_pod").h3.text
        booklink = book.find("article", class_="product_pod").h3.a["href"]
        booklink = booklink.replace("../../..", "http://books.toscrape.com/catalogue")
        title_and_link = {booktitle: booklink}
        books_per_category.append(title_and_link)
    return books_per_category


def extract_categories_and_books(categories_and_links):
    categories_and_books = {}
    for (category, link) in categories_and_links.items():
        print(f"Extracting {category}")
        first_extracted_page = extract_books(link)
        total_extracted_pages = first_extracted_page
        page = 2
        print("\nCopying titles and links for page 1")
        while requests.get(link.replace("index.html", f"page-{page}.html")).ok:
            next_extracted_page = extract_books(link.replace("index.html", f"page-{page}.html"))
            total_extracted_pages += next_extracted_page
            print(f"Copying titles and links for page {page}")
            page += 1
        print("---")
        categories_and_books[category] = total_extracted_pages
    return categories_and_books


def extract_infos(booklink):
    soup = get_soup_object(booklink)
    universal_product_code = soup.find("th", string="UPC").find_next("td").text
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    number_available = soup.find("th", string="Availability").find_next("td").text
    category_in_lis = soup.find("div", class_="container-fluid page").find("ul", class_="breadcrumb").findAll("li")
    category = category_in_lis[2].a.text
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    product_page_url = booklink
    title = soup.find("div", class_="col-sm-6 product_main").h1.text
    try:
        product_description = "\"" + (soup.find("div",
                                                id="product_description").find_next("p").text).replace(
            "&#x27;", "'").replace("&quot;", "\"").replace(";", "") + "\""
    except AttributeError:
        product_description = "No product description"
    image_url = soup.find("div", class_="item active").find_next("img")["src"]
    image_url = image_url.replace("../..", "http://books.toscrape.com")
    infos = [product_page_url,
             universal_product_code,
             title,
             price_including_tax,
             price_excluding_tax,
             number_available,
             product_description,
             category,
             review_rating,
             image_url]

    return infos


def extract_complete_infos_for_category(categories_and_books):
    complete_infos = {}
    for (category, bookslist) in categories_and_books.items():
        category_and_booksinfos = {}
        for elem in bookslist:
            tmp_item = elem.items()
            for (key, value) in tmp_item:
                if key not in category_and_booksinfos:
                    booktitle = key
                elif (key + "_") not in category_and_booksinfos:
                    booktitle = key + "_"
                else:
                    booktitle = key + "__"
                booklink = value
                infos = (extract_infos(booklink))
                category_and_booksinfos[booktitle] = infos
                print(f"Extracting infos about : {category}-{booktitle}")
        complete_infos[category] = category_and_booksinfos
        print(f"Category {category} successfully extracted\n")
    return complete_infos


def convert_datalist_to_dataline(datalist):
    dataline = ""
    for i in datalist:
        dataline += f"{i} ;"
    return dataline


def init_csv(file_name):
    with open(file_name, "w+") as f:
        f.write("product_page_url ;universal_ product_code (upc) ;title ;price_including_tax ;price_excluding_tax "
                ";number_available ;product_description ;category ;review_rating ;image_url\n")


def write_csv(file_name, dataline):
    with open(file_name, "a+", encoding="utf-8") as f:
        f.write(dataline + "\n")


def create_csv(complete_infos):
    if not os.path.isdir("./download"):
        os.mkdir("./download")
        print("Download directory created")

    for category in complete_infos:
        file_name = f"{category}.csv"
        if os.path.isfile(f"./download/{file_name}"):
            print(f"{file_name} will be updated")
            init_csv(f"./download/{file_name}")
        else:
            init_csv(f"./download/{file_name}")
            print(f"{file_name} has been created")
        for (book, infos) in complete_infos[category].items():
            dataline = convert_datalist_to_dataline(infos)
            write_csv(f"./download/{file_name}", dataline)
            print(f"Writing {book} informations in {file_name}")
        print(f"{file_name} completed")
    print("---")


def replace_special_characters(text):
    special_characters_list = [".", "/", ":", "?", "\""]
    for i in special_characters_list:
        text = text.replace(i, "_")
    return text


def download_images(complete_infos):
    if not os.path.isdir("./download/images"):
        os.mkdir("./download/images")
    for category in complete_infos:
        if not os.path.isdir(f"./download/images/{category}"):
            os.mkdir(f"./download/images/{category}")
            print("---")
            print(f"{category} directory created in download directory")
        for (book, infos) in complete_infos[category].items():
            truncated_title = replace_special_characters(infos[2][0:9])
            image_url = infos[-1]
            save_name = f"./download/images/{category}/{truncated_title + infos[1]}.jpg"
            if not os.path.isfile(f"./download/images/{category}/{truncated_title + infos[1]}.jpg"):
                urllib.request.urlretrieve(image_url, save_name)
        print(f"All images for {category} downloaded")
