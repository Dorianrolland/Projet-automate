

# Fonctions du menu sur le terminal 

from automate_operations import verifword, is_complete, is_deterministic, make_complete, complementaire, miroir
from file_operations import export_AEF
from automate_util import add_final_state, add_state, add_transition, remove_state, remove_transition, set_start_state



def firstchoice () :
    """
    Cette fonction propose différente action avant de modifier un AEF

    """
    print ("\nBonjour :) \nQue souhaitez-vous faire ?")
    print ("1. Créer un AEF ")
    print ("2. Importer un AEF ")
    print ("3. Modifier un AEF existant ")
    print ("4. Exporter un AEF ")
    print ("5. Rien faire, vous aimez pas trop les automates\n ")
    choice = input("Entrez votre choix : ")
    return choice 



def modify_AEF (AEF) :
    """
    Cette fonction permet de faire pleins d'actions sur un AEF

    """
    # Tant que l'utilisateur n'a pas fini de modifier son AEF, on lui propose des actions 
    while True :
        print ("\n\nAEF actuel : ")
        print (AEF, "\n\n")
        print ("Que voulez-vous faire ?")
        print ("1. Ajouter un état") 
        print ("2. Ajouter une transition")
        print ("3. Définir l'état initial")
        print ("4. Ajouter un état final")
        print ("5. Supprimer un état")
        print ("6. Supprimer une transition")
        print ("7. Vérifier si un mot est reconnu par votre AEF")
        print ("8. Vérifier si votre AEF est complet")
        print ("9. Rendre un AEF complet")
        print ("10. Vérifier si votre AEF est déterministe")
        print ("11. Rendre votre AEF déterministe")
        print ("12. Transformer votre AEF en son complémentaire")
        print ("13. Afficher le miroir de votre AEF")
        
        print ("20. Quitter")
        
        # On initialise une variable grâce à la méthode input(), qui prendra la valeur de la réponse de l'utilisateur 
        choice = input ("\nEntrez votre choix : ")

        # A chaque réponse, on dédie les fonctions à utiliser 
        if choice =="1" :
            state = input ("Entrez le nom de l'état : ")
            add_state(AEF, state)
        elif choice == "2" :
            from_state = input ("Entrez le nom de l'état de départ : ")
            to_state= input ("Entrez le nom de l'état d'arrivée : ")
            symbol = input ("Entrez le symbol de la transition : ")
            add_transition (AEF, from_state, to_state, symbol)
        elif choice == "3" :
            state = input("Entrez le nom de l'état initial : ")
            set_start_state (AEF, state)
        elif choice == "4" :
            state = input ("Entrez le nom de l'état final : ")
            add_final_state (AEF, state)
        elif choice == "5" :
            state = input("Entrez le nom de l'état à supprimer : ")
            remove_state (AEF, state)
        elif choice == "6" :
            from_state = input ("Entrez le nom de l'état de départ de la transition à supprimer : ")
            to_state= input ("Entrez le nom de l'état d'arrivée de la transition à supprimer : ")
            symbol = input ("Entrez le symbol de la transition à supprimer : ")
            remove_transition(AEF, from_state, to_state, symbol)
        elif choice == "7" :
            verifword(AEF)
        elif choice == "8" :
            is_complete(AEF)
        elif choice == "9" :
            make_complete(AEF)
        elif choice == "10" :
            is_deterministic(AEF)
        elif choice == "12":
            complementaire(AEF)
        elif choice == "13":
            miroir(AEF)
    

        # à finir ici !!!!!!!!!!!!!!!!!!!

    
        elif choice == "20" :
            answer = input ("Avant de quitter, voulez vous exporter votre AEF sur un fichier ?  :  ")
            if answer == "yes" :
                export_AEF(AEF, "AEF_exported.txt")
            else :
                break
        else :
            print ("Choix invalide !!!")
