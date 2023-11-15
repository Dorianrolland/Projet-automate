
def create_AEF():
    """"
    Cette fonction permet de créer un nouvel AEF grâce à la méthode set()
    on crée un dictinnaire prenant 5 clés :
    set () states pour créer un dictionnaire contenant chaque état de l'automate
    set () alphabet pour créer un dictionnaire contenant tous les symbols utilisés par l'automate
    un dictionnaire vide transitions qui sera rempli de tel sorte à avoir : Chaque clé sera un état et aura comme valeur un dictionnaire avec le symbole de la liaison et en valeurs l'état d'arrviée
    start_state en None car un automate peut ne pas avoir d'état initial
    set () final_states pour créer un dictionnaire contenant un ou plusieurs états finaux 
    
    """
    return {"states": set(), "alphabet" : set(), "transitions": {}, "start_state": None, "final_states": set() }


def add_state(AEF, state):
    """
    Cette fonction permet de créer un nouvel état
    On utilise la méthode add() pour ajouter un nouvel élement à AEF["states"]
    AEF["states"] permet de récuperer les valeurs du dictionnaire assimilées à la clé "states" 
    Concernant state, cette valeur représente l'état que l'utilisateur va entrer en console pour ajouter un nouvel état
    Elle sert aussi à l'importation du fichier plus tard 
    Enfin un print pour annoncer à l'utilisateur le succés de son ajout 
    
    """
    AEF["states"].add(state)
    print ("\nEtat ", state, "ajouté ! \n\n")


def add_transition(AEF, from_state, to_state, symbol):
    """
    Cette fonction permet d'ajouter une liaison entre 2 états
    from_state représente l'état de départ 
    to_state représente l'état d'arrivée
    symbol représente le symbol de la liaison
    """

    # Tout d'abord, on vérifie que l'état "from_state" ou "to_state" est bien présent dans l'automate
    # On renvoie une ValueError si l'état n'existe pas
    if from_state not in AEF["states"] or to_state not in AEF["states"]:
        raise ValueError("L'état doit exister dans l'automate ! ")

    # On vérifie maintenant si le symbole fait partie de l'alphabet de l'automate
    if symbol not in AEF["alphabet"]:
        # On ajoute le symbole s'il n'existe pas
        AEF["alphabet"].add(symbol)

    # Si l'état de départ n'existe pas dans AEF["transitions"], on lui crée un dictionnaire vide
    if from_state not in AEF["transitions"]:
        AEF["transitions"][from_state] = {}

    # On récupère la liste des états d'arrivée pour le symbole
    destinations = AEF["transitions"][from_state].get(symbol, [])
    # On ajoute l'état d'arrivée à la liste
    destinations.append(to_state)

    # On met à jour la liste des états d'arrivée pour le symbole
    AEF["transitions"][from_state][symbol] = destinations

    print(f"\nTransition ajoutée : {from_state} --({symbol})--> {to_state}")


def set_start_state (AEF, state): 
    """
    Cette fonction permet de définir l'état initial de l'automate
    Elle vérifie que l'état initial est d'abord présent dans l'automate
    
    """
    if state not in AEF["states"]:
        raise ValueError ("L'état n'éxiste pas dans l'AEF")
    AEF["start_state"] = state

def add_final_state(AEF, state):
    """
    Cette fonction permet d'ajouter un état final, elle fonctionne sur le même principe que set_start_state 
    Contrairement à l'état initial qui lui est unique (d'où le choix de pas utiliser set() pour l'état initial), il peut y'avoir plusieurs états finaux 
    
    """
    if state not in AEF["states"]:
        raise ValueError ("L'état n'éxiste pas dans l'AEF")
    AEF["final_states"].add(state)



def remove_state(AEF, state):
    """
    Cette fonction permet de retirer un état de l'automate
    """

    # tout d'abord on vérifie que l'état qu'on veut supprimer existe, si il n'existe pas on renvoit une erreur
    if state not in AEF["states"]:
        raise ValueError("L'état que vous voulez supprimer n'existe pas dans l'automate !")

    # On retire l'état voulu grâce à la méthode de suppression d'un set() qui est .remove()
    AEF["states"].remove(state)

    # On retire l'état final avec la méthode discard() qui permet de supprimer un élement si celui ci existe, sinon elle ne fait rien
    # (si on avait mis remove, on aurait eu une erreur)
    # On fait cela car l'état qu'on supprime peut être final donc si on supprime un état, il faut le supprimer de la clé "final_states"
    AEF["final_states"].discard(state)

    # Ensuite il faut aussi supprimer l'état s'il est initial (on supprime la valeur de la clé "start_state" de notre dictionnaire AEF)
    if AEF["start_state"] == state:
        AEF["start_state"] = None

    # Ensuite on parcourt toutes les liaisons en utilisant la méthode keys() des dictionnaires.
    # Le point de départ de toute liaison est from_state
    for from_state in list(AEF["transitions"].keys()):
        if from_state == state:
            del AEF["transitions"][from_state]
        else:
            # On parcourt les liaisons pour chaque état.
            # On a vérifié que state n'est pas initial auparavant, donc on prend l'état de départ de la liaison
            for symbol in list(AEF["transitions"][from_state].keys()):
                to_states = AEF["transitions"][from_state][symbol]  # On récupère la liste des états finaux de la liaison

                # On supprime l'état de la liste des états finaux s'il est présent
                if state in to_states:
                    to_states.remove(state)

                    # On met à jour la liaison avec la nouvelle liste des états finaux
                    AEF["transitions"][from_state][symbol] = to_states

                    # Si la liste des états finaux est vide, on supprime la liaison
                    if not to_states:
                        del AEF["transitions"][from_state][symbol]

            # Si la liste des liaisons pour un état de départ donné est vide, on supprime cet état de départ des transitions
            if not AEF["transitions"][from_state]:
                del AEF["transitions"][from_state]
            else:
                # Correction ici pour éviter la suppression d'un état qui n'est pas présent dans la liste des liaisons
                AEF["transitions"][from_state] = {
                    symbol: to_states
                    for symbol, to_states in AEF["transitions"][from_state].items()
                    if state not in to_states
                }

    print(f"\nÉtat supprimé : {state}")



def remove_transition(AEF, from_state, to_state, symbol):
    """
    Cette fonction permet de supprimer une liaison précise de l'AEF
    """

    # On vérifie que l'état de départ ou l'état d'arrivée de la liaison existe
    if from_state not in AEF["states"] or to_state not in AEF["states"]:
        print("L'état dont vous essayez de supprimer la liaison n'existe pas dans votre automate !")
    
    # On vérifie que le symbol à supprimer existe ou pas dans le langage de l'automate
    if symbol not in AEF["alphabet"]:
        print("La liaison que vous souhaitez supprimer ne possède pas ce symbole !")
    
    # Il se peut que les états de départ et d'arrivée existent dans l'automate, ainsi que le symbole
    # Il faut donc vérifier dans les liaisons si la liaison existe entre les 2 états, possédant le symbole choisi
    if from_state not in AEF["transitions"] or symbol not in AEF["transitions"][from_state]:
        print("La liaison que vous voulez supprimer n'existe pas !")
    
    to_values = AEF["transitions"][from_state][symbol]

    # On supprime l'état d'arrivée de la liste des états finaux
    to_values.remove(to_state)

    # On met à jour la liaison avec la nouvelle liste des états finaux
    AEF["transitions"][from_state][symbol] = to_values

    # Si la liste des états finaux est vide après la mise à jour, on supprime la liaison
    if not to_values:
        del AEF["transitions"][from_state][symbol]

    # Si la liste des liaisons pour un état de départ donné est vide, on supprime cet état de départ des transitions
    if not AEF["transitions"][from_state]:
        del AEF["transitions"][from_state]

    print(f"\nLiaison supprimée : {from_state} --({symbol})--> {to_state}")



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
    



def verifword(AEF):
    """
    Cette fonction permet de vérifier si l'automate reconnaît un mot grâce à son langage
    """

    # Vérifier s'il y a un état de départ, sinon demander à l'utilisateur d'en définir un
    if AEF["start_state"] is None:
        print("\nL'AEF n'a pas d'état de départ.")
        state = input("Veuillez définir un état de départ : ")
        set_start_state(AEF, state)

    # Vérifier s'il y a des états d'arrivée, sinon demander à l'utilisateur d'en définir au moins un
    if not AEF["final_states"]:
        print("\nL'AEF n'a pas d'état d'arrivée.")
        state = input("Veuillez définir au moins un état d'arrivée : ")
        add_final_state(AEF, state)

    # Demander à l'utilisateur de donner le mot qu'il souhaite vérifier
    answer = input("\nÉcrivez votre mot : ")

    # Initialiser l'état actuel à l'état initial de l'automate
    current_state = AEF["start_state"]

    # Parcourir tous les symboles du mot saisi par l'utilisateur
    for symbol in answer:

        # Si le symbole n'existe pas dans l'automate, afficher une erreur
        if symbol not in AEF["alphabet"]:
            print(
                f"\nLe symbole \033[1m\033[91m{symbol}\033[0m\033[0m n'existe pas dans le langage de l'AEF"
            )
            return False

        # Vérifier si l'état actuel est dans les liaisons ou si ses symboles de liaisons existent
        if (
            current_state not in AEF["transitions"]
            or symbol not in AEF["transitions"][current_state]
        ):
            print(
                f"\nVotre mot n'est pas reconnu dans l'AEF.\nIl n'y a pas de liaison entre l'état {current_state} et le symbole {symbol}"
            )
            return False

        # Mettre à jour l'état actuel
        current_state = AEF["transitions"][current_state][symbol]

        # Si l'état actuel est une liste, prenez le premier état de la liste
        if isinstance(current_state, list):
            current_state = current_state[0]

    print("\nVotre mot a été reconnu avec succès par le langage de l'automate")
    return current_state in AEF["final_states"]



def is_complete(AEF):
    """
    Cette fonction vérifie si l'automate est complet ou pas
    """

    # On récupère l'alphabet de l'automate
    alphabet = AEF["alphabet"]

    # On parcourt tous les états de l'automate
    for state in AEF["states"]:

        # On vérifie si l'état est dans les liaisons, donc s'il a au moins une liaison avec un autre état
        if state not in AEF["transitions"]:
            print(
                f"\nL'état \033[1m\033[91m{state}\033[0m\033[0m ne possède aucune liaison\nAutomate incomplet !"
            )
            return False

        # On parcourt les symboles de l'alphabet de l'automate
        for symbol in alphabet:

            # On vérifie si les états dans la clé "transitions" ont tous au moins une liaison avec chaque symbole de l'alphabet
            if state not in AEF["transitions"] or symbol not in AEF["transitions"][state]:
                print(
                    f"\nLe symbole \033[1m\033[91m{symbol}\033[0m\033[0m de l'état \033[1m\033[91m{state}\033[0m\033[0m n'existe pas\nAutomate incomplet !"
                )
                return False

    print("\nVotre automate est complet !")
    return True


def make_complete(AEF):
    """
    Cette fonction permet de rendre un automate complet. Elle possède la même structure que la fonction is_complete(AEF)
    """

    # Si l'automate est complet, on ne fait rien
    if is_complete(AEF):
        print("\nVotre automate est déjà complet !")
        return True

    # On ajoute un nouvel état phi grâce à la fonction add_state(AEF, state)
    add_state(AEF, state="phi")
    alphabet = AEF["alphabet"]

    for state in AEF["states"]:
        for symbol in alphabet:
            if state not in AEF["transitions"]:
                
                # On ajoute une liaison à l'état phi avec un symbol en utilisant add_transition 
                add_transition(AEF, from_state=state, to_state="phi", symbol=symbol)

            if symbol not in AEF["transitions"][state]:

                # On ajoute une liaison à phi si un état n'a pas de liaison avec un autre avec un symbol de l'alphabet 
                add_transition(AEF, from_state=state, to_state="phi", symbol=symbol)

    print("\nVotre automate a été rendu complet avec succès !")
    return True



def is_deterministic(AEF):
    """
    Cette fonction vérifie si un automate est déterministe.
    """

    # Vérifier s'il y a un état de départ, sinon demander à l'utilisateur d'en définir un
    if AEF["start_state"] is None:
        print("\nL'AEF n'a pas d'état de départ.")
        state = input("Veuillez définir un état de départ : ")
        set_start_state(AEF, state)
    
      # Vérifier s'il y a des états d'arrivée, sinon demander à l'utilisateur d'en définir au moins un
    if not AEF["final_states"]:
        print("\nL'AEF n'a pas d'état d'arrivée.")
        state = input("Veuillez définir au moins un état d'arrivée : ")
        add_final_state(AEF, state)

    # Parcourir tous les états de l'automate
    for state in AEF["states"]:
        
        # Vérifier si l'état a des transitions définies
        if state in AEF["transitions"]:
            
            # Parcourir les symboles des transitions pour cet état
            for symbol in AEF["transitions"][state]:
                
                # Vérifier si la valeur associée au symbole est une liste avec une taille supérieure à 1
                if len(AEF["transitions"][state][symbol]) > 1:
                    print(f"\nL'automate n'est pas déterministe. État {state} a plusieurs transitions pour le symbole {symbol}.")
                    return False
    
    # Si aucune violation n'a été détectée, l'automate est déterministe
    print("\nL'automate est déterministe.")
    return True







def complementaire(AEF):
    print ("AEF initial :")
    print(AEF)
    temp = []
    for  state in AEF["final_states"]:
        temp.append(state)
    AEF["final_states"] = set()
    for state in AEF["states"]:
        if state not in temp:
                add_final_state(AEF,state)
    return

def miroir(AEF):
    new_AEF = {}
    for a in AEF:
        new_AEF[a]=AEF[a]
        new_AEF["transitions"] = {}

    if (len(AEF["final_states"])) != 1:
        raise ValueError("Il faut que votre AEF n'ait qu'un état final")
    
    else:
        for start in AEF["transitions"]:
            i = 0
            for states in AEF["transitions"][start].values():
                for value in states:
                    add_transition(new_AEF, value, start, list(AEF["transitions"][start].keys())[i])
                i+=1
        print('Miroir de votre AEF : ')
        print(new_AEF)
        return

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
            answer = input ("Avant de quitter, voulez vous exporter votre AEF sur un fichier ?  (yes/no):  ")
            if answer == "yes" :
                export_AEF(AEF, "AEF_exported.txt")
            else :
                break
        else :
            print ("Choix invalide !!!")



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
        AEF = import_AEF("AEF.txt")
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

