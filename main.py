from helpers import*
from pprint import pprint


def extract_and_display_bookswithlinks_in_category(category):
    try:
        # Extraction des catégories et liens correspondants pour retrouver la catégorie en paramètre
        categories_and_links = extract_categories()

        # Association de la catégorie avec le lien correspondant
        link = categories_and_links[category]

        # Extraction et affichage de la catégorie et des livres contenus
        pprint(extract_books(link))
        return
    except KeyError:
        print("Unvalid category")
        return


def extract_and_display_specific_infos(booklink):
    pprint(extract_infos(booklink))
    return


def extract_download_specific_categories(category, *args):
    # Extraction de la catégorie et du lien correspondant
    categories_and_links = {category: extract_categories()[category]}

    # Extraction de la liste des livres pour la catégorie
    categories_and_books = extract_categories_and_books(categories_and_links)

    # Extraction des infos par livre et par catégorie
    complete_infos = extract_complete_infos_for_category(categories_and_books)

    # Création et écriture des fichiers CSV pour chaque catégorie
    create_csv(complete_infos)

    # Récupération et téléchargement de toutes les images par catégories
    download_images(complete_infos)

    # Itération à travers les paramètres optionnels et rappel de la fonction pour les autres catégories
    for arg in args:
        extract_download_specific_categories(arg)
    return


def extract_download_all():
    # Extraction des catégories et liens correspondants
    categories_and_links = extract_categories()

    # Extraction de la liste des livres par catégories
    categories_and_books = extract_categories_and_books(categories_and_links)

    # Extraction des infos par livre et par catégorie
    complete_infos = extract_complete_infos_for_category(categories_and_books)

    # Un dictionnaire ayant pour clé chaque catégorie et pour valeur un dictionnaire {Livre : [infos]} a été créé

    # Création et écriture des fichiers CSV pour chaque catégorie
    create_csv(complete_infos)

    # Récupération et téléchargement de toutes les images par catégories
    download_images(complete_infos)
    return
