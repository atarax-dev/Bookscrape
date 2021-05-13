from helpers import*

# Extraction des catégories et liens correspondants
categories_and_links = extract_categories()

# Extraction de la liste des livres par catégories
categories_and_books = extract_categories_and_books(categories_and_links)

# Extraction des infos par livre et par catégorie
complete_infos = extract_complete_infos_for_category(categories_and_books)

# Un dictionnaire ayant pour clé chaque catégorie et pour valeur un dictionnaire {Livre : [infos]} a été créé

# Création et écriture des fichiers CSV pour chaque catégorie
create_csv_files(complete_infos)

# Récupération et téléchargement de toutes les images par catégories
download_images(complete_infos)
