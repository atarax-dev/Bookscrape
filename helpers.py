import requests
from bs4 import BeautifulSoup


def get_response(url):
    response = requests.get(url)
    return response


def get_soup_object(url):
    html_content = requests.get(url).text
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
#    print(books_per_category)
    return books_per_category


def extract_infos(category, booklink, booktitle):
    soup = get_soup_object(booklink)
#    tr_tags = soup.find("table", class_="table table-striped").find("tbody").findAll("tr")
    universal_product_code = soup.find("th", string="UPC").find_next("td").text
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next("td").text
    price_excluding_tax = price_excluding_tax.replace("Â", "")
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next("td").text
    price_including_tax = price_including_tax.replace("Â", "")
    number_available = soup.find("th", string="Availability").find_next("td").text
    review_rating = soup.find("th", string="Number of reviews").find_next("td").text
    product_page_url = booklink
    title = booktitle
    try:
        product_description = soup.find("div", id="product_description").find_next("p").text
    except AttributeError:
        product_description = "No product description"
    image_url = soup.find("div", class_="item active").find_next("img")["src"]
    image_url = image_url.replace("../..", "http://books.toscrape.com")
    category = category
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

