import ast
from database import init_database


def add_AEF():
    print("Comment souhaitez-vous ajouter un AEF?")
    print("1. Écrire l'AEF sur le terminal")
    print("2. Importer depuis un fichier AEF2.txt")
    print("3. Récupérer depuis la base de données des AEF")
    
    choice = input("Votre choix (1, 2 ou 3) : ")

    if choice == "1":
        return input_AEF_terminal()
    elif choice == "2":
        return input_AEF_from_file()
    elif choice == "3":
        return input_AEF_from_database()
    else:
        print("Choix invalide. Veuillez choisir 1, 2 ou 3.")
        return add_AEF()

def input_AEF_terminal():
    AEF2 = input("saisissez votre AEF !")
    return AEF2

def input_AEF_from_file():
    try:
        with open("AEF2.txt", "r") as file:
            content = file.read()
            AEF = ast.literal_eval(content)
            return AEF
    except FileNotFoundError:
        print("Le fichier AEF2.txt n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

def input_AEF_from_database():
    # Connexion à la base de données et récupération des AEF enregistrés
    conn = init_database()
    c = conn.cursor()
    c.execute("SELECT * FROM AEF")
    rows = c.fetchall()

    # Affichage des AEF disponibles avec un numéro associé
    print("Choisissez un AEF depuis la base de données :")
    for i, row in enumerate(rows, start=1):
        print(f"{i}. AEF {i}")

    # Demande à l'utilisateur de choisir un AEF en entrant le numéro correspondant
    choice = input("Votre choix (1, 2, etc.) : ")

    try:
        # Conversion de la saisie utilisateur en indice d'AEF
        index = int(choice) - 1
    
     # Vérification de la validité de l'indice
        if 0 <= index < len(rows):
            # Construction du dictionnaire AEF à partir des données de la base de données
            AEF = {
            "states": ast.literal_eval(rows[index][1]),
            "alphabet": ast.literal_eval(rows[index][2]),
            "transitions": ast.literal_eval(rows[index][3]),
            "final_states": ast.literal_eval(rows[index][4]),
            "start_state": rows[index][5]
            }
            return AEF
        else:
            print("Choix invalide.")
            return None
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return None


