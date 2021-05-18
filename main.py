from helpers import*
from pprint import pprint
import requests.exceptions


def main():
    wannaquit = False
    while not wannaquit:
        print("Fonctionnalites disponibles:\n"
              ""
              "[1] Afficher la liste des categories\n"
              "[2] Afficher la liste des livres et leurs liens dans une categorie\n"
              "[3] Afficher les informations d'un livre en particulier\n"
              "[4] Extraire et telecharger les informations et les images d'une ou plusieurs categories\n"
              "[5] Extraire et telecharger les informations et les images de toutes les categories\n")

        validnumber = 0
        choice = ""
        while not 1 <= validnumber < 6:
            try:
                choice = int(input("Votre choix: "))
                validnumber = choice
                if not 1 <= validnumber < 6:
                    print("Vous devez entrer un chiffre entre 1 et 5")
                choice = str(choice)
                print()
            except ValueError:
                print("Vous devez entrer un chiffre entre 1 et 5")

        if choice == "1":
            display_categories()

        elif choice == "2":
            category = input("Categorie souhaitee: ")
            category = str.upper(category[0]) + category[1:]
            extract_and_display_bookswithlinks_in_category(category)

        elif choice == "3":
            booklink = input("Entrez le lien du livre: ")
            extract_and_display_specific_infos(booklink)

        elif choice == "4":
            print("Entrez le ou les noms des categories separes uniquement par une virgule")
            categories = input("Categories souhaitees: ")
            optionals = categories.split(",")
            category = optionals[0]
            optionals.remove(category)
            category = str.upper(category[0]) + category[1:]
            extract_download_specific_categories(category)
            for arg in optionals:
                arg = str.upper(arg[0]) + arg[1:]
                extract_download_specific_categories(arg)

        elif choice == "5":
            extract_download_all()

        valid_answer = False
        while not valid_answer:
            answer = input("Voulez-vous executer une autre fonction? (O/N)\n")
            try:
                answer = str.lower(answer)
                if answer == "n":
                    print("A bientot")
                    wannaquit = True
                    valid_answer = True
                elif answer == "o":
                    print("Retour au menu\n")
                    valid_answer = True
                else:
                    print("Vous devez entrez (O)ui ou (N)on")
                    print(f"Vous avez ecris {answer}")
            except ValueError:
                print("Vous devez entrez (O)ui ou (N)on")
                print(f"Vous avez ecris {answer}")


def display_categories():
    categories_and_links = extract_categories()
    for (key, value) in categories_and_links.items():
        print(key)
    return


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
        print(f"Categorie {category} inexistante ou mal orthographiee")
        print("La liste des categories est disponible a l'aide la fonction [1]")
        return


def extract_and_display_specific_infos(booklink):
    try:
        pprint(extract_infos(booklink))
        return
    except requests.exceptions.MissingSchema:
        print("Lien invalide ou mal orthographie")
        print(f"Vous avez ecris {booklink}")
        print("La liste des liens par categorie est disponible a l'aide la fonction [2]")
        return


def extract_download_specific_categories(category, *args):
    try:
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
    except KeyError:
        print(f"Categorie {category} inexistante ou mal orthographiee")
        print("La liste des categories est disponible a l'aide la fonction [1]")
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


if __name__ == "__main__":
    main()
