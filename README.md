# Bookscrape
 Projet n°2 OC

Pour pouvoir lancer le programme, créez un environnement virtuel dans votre terminal: :

  
python -m venv venv
- Activez l'environnement : 
  
source env/Scripts/activate
- Installez les packages requis à l'aide de la commande suivante: 
  
pip install -r requirements.txt


Ce programme dispose de 4 fonctionnalités:

extract_and_display_bookswithlinks_in_category("Catégorie")
-> vous permet d'extraire et d'afficher la liste des livres et leurs liens dans une catégorie donnée

extract_and_display_specific_infos("lien du livre")
-> vous permet d'extraire et d'afficher les informations détaillées d'un livre ; pour trouver le lien d'un livre,
vous pouvez le trouver à l'aide de la fonction précédente

extract_download_specific_categories("Catégorie", paramètres optionels="Autre catégorie")
-> vous permet d'extraire et de télécharger les informations au format csv et les images de chaque catégorie donnée

extract_download_all() 
-> vous permet d'extraire et de télécharger toutes les informations et toutes les images de toutes les catégories
