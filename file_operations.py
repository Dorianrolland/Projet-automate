
# Toutes les fonctions d'opérations sur les fichiers (import/export)



def import_AEF(filename) :
    """
    Cette fonction permet d'importer un AEF depuis un fichier enregistré dans le même dossier que ce projet (en local)
    On ouvre le fichier en mode lecture, on vérifie qu'il contienne bien les clés du dictionnaire de l'AEF et on retrun AEF

    """
    with open(filename, "r") as f:
        AEF = eval(f.read())
    if not isinstance(AEF, dict) or "states" not in AEF or "alphabet" not in AEF or "transitions" not in AEF or "start_state" not in AEF or "final_states" not in AEF :
        raise ValueError ("le fichier doit conteneir un AEF")
    return AEF 



def export_AEF(AEF, filename):
    """
    Cette fonction permet d'exporter un AEF dans un fichier en local 

    """
    with open(filename, "w") as f :
        f.write(str(AEF))
    