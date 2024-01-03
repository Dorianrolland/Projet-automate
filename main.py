
# Le main du script 


from automate_creator import create_AEF
from file_operations import import_AEF, export_AEF
from menu import firstchoice, modify_AEF



def main() :
    """
    Cette fonction est le main du projet, permettant d'utiliser toutes les fonctionalités et gérer un automate 
    
    """
    # On initialise l'AEF à un dictionnaire vide 
    AEF = {}
    
    # On utilise la fonction firstchoice() pour avoir la première réponse de l'utilisateur. On l'utilise qu'une fois lorsqu'on lance un
    answer = firstchoice()

    # A chaque réponse de l'utilisateur, on dédie les fonctions à utiliser
    if answer == "1" :
        AEF = create_AEF()
        modify_AEF(AEF)
    elif answer == "2" : 
        AEF = import_AEF("AEF.txt")
    elif answer == "3" : 
        AEF = import_AEF("AEF_exported.txt")
        modify_AEF(AEF)
    elif answer == "4" :
        AEF = input ("Ecrivez l'AEF que vous souhaitez exporter :  ")
        export_AEF (AEF, "AEF_exported.txt")
    elif answer == "5" :
        print ("FIN")
    else :
        raise ValueError ("Choix invalide ! ")

    print ("\nVotre AEF est : \n", AEF)

 


if __name__ == "__main__" :
    main()

