from helpers import*

categories_and_links = extract_categories()
categories_and_books = {}
# print(categories_and_links["Mystery"])

for (category, link) in categories_and_links.items():
    print(f"\nExtracting {category}")
    first_extracted_page = extract_books(link)
    total_extracted_pages = first_extracted_page
    page = 2
    print("\nCopying titles and links for first page")
    while get_response(link.replace("index.html", f"page-{page}.html")).ok:
        next_extracted_page = extract_books(link.replace("index.html", f"page-{page}.html"))
        total_extracted_pages += next_extracted_page
        print(f"Copying titles and links for page {page}")
        page += 1
#    print(f"total={total_extracted_pages}")
    categories_and_books[category] = total_extracted_pages


# print(categories_and_books["Mystery"])

complete_infos = {}
categories_and_booksinfos = []

for (category, bookslist) in categories_and_books.items():
    for elem in bookslist:
        tmp_item = elem.items()
#        print(tmp_item)
        for (key, value) in tmp_item:
            booktitle = key
            booklink = value
            categories_and_booksinfos.append(extract_infos(category, booklink, booktitle))
            print(f"Writing infos for : {category}-{booktitle}")
        complete_infos[category] = categories_and_booksinfos
    print(f"Category {category} successfully extracted")

print(complete_infos["Mystery"])
