# Bookscrape
 Projet n°2 OC
#Introduction:
Ce programme peut être utilisé pour extraire et télécharger les informations 
 des livres de la librairie en ligne books.toscrape.com
#Prérequis
Ce programme nécessite l'installation de Python 3 (au minimum) au préalable
https://www.python.org/downloads/

Lancez un terminal

Récupérez l'ensemble du projet :
- git clone https://github.com/atarax-dev/Bookscrape.git

Placez-vous dans le répertoire qui contient le fichier main.py

Pour pouvoir lancer le programme, créez un environnement virtuel:
- python -m venv venv

Activez l'environnement :
- source venv/Scripts/activate (sous windows)
- source venv/bin/activate (sous Mac ou linux)

Installez les packages requis à l'aide de la commande suivante:
- pip install -r requirements.txt

#Utilisation
Toujours depuis le répertoire qui contient main.py dans le terminal, exécutez le programme:
- python main.py

#Fichiers créés
Un dossier "download" sera créé dans le répertoire contenant main.py

Il contiendra les fichiers CSV et un dossier "images" contenant les images associées aux catégories

Les fichiers CSV, doivent être ouverts avec le séparateur ";"
