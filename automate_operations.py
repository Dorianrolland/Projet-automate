 

# Toutes les fonctions d'opérations et vérifications sur les automates (rendre complet, déterministe, miroir...)


from automate_util import add_state, add_final_state, add_transition, set_start_state, remove_state, remove_transition, str_to_state, state_to_str
from automate_creator import create_AEF



def verification_AEF(AEF):

     # Vérifier s'il y a un état de départ, sinon demander à l'utilisateur d'en définir un
    if AEF["start_state"] is None:
        print("\nL'AEF n'a pas d'état de départ.")
        state = input("Veuillez définir un état de départ : ")
        set_start_state(AEF, state)

    # Vérifier s'il y a des états d'arrivée, sinon demander à l'utilisateur d'en définir au moins un
    if not AEF["final_states"] or AEF["final_states"] == set():
        print("\nL'AEF n'a pas d'état d'arrivée.")
        state = input("Veuillez définir au moins un état d'arrivée : ")
        add_final_state(AEF, state)    


def verifword(AEF):
    """
    Cette fonction permet de vérifier si l'automate reconnaît un mot grâce à son langage
    """
    verification_AEF(AEF)

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

    verification_AEF(AEF)

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

    verification_AEF(AEF)

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


def determinize_AEF(AEF) : 
    # On crée un AEF vide 
    det_AEF = create_AEF()
    # Transformation de l'état initial en string 
    start_state_str = state_to_str(AEF["start_state"])
    to_process = [start_state_str]

    while to_process: 
        current_state_str = to_process.pop()
        current_state = str_to_state(current_state_str)
        det_AEF["states"].add(current_state_str)
        
        if any(s in AEF["final_states"] for s in current_state) : 
            det_AEF["final_states"].add(current_state_str)
        
        for symbol in AEF["alphabet"]:
            next_states = set()
        
            for state in current_state : 
                if state in AEF["transitions"] and symbol in AEF["transitions"][state]:
                    next_states.update(AEF["transitions"][state][symbol])
            
            if next_states : 
                next_states_str = state_to_str(next_states)

                if next_states_str not in det_AEF["states"] :
                    to_process.append(next_states_str)

                if current_state_str not in det_AEF["transitions"] : 
                    det_AEF["transitions"][current_state_str] = {}

                det_AEF["transitions"][current_state_str][symbol] = [next_states_str]
    
    det_AEF["start_state"] = start_state_str
    det_AEF["alphabet"] = AEF["alphabet"].copy()

    AEF = det_AEF
    return AEF




def complementaire(AEF):
    print ("AEF initial :",AEF)
    temp = []
    for  state in AEF["final_states"]:
        temp.append(state)
    AEF["final_states"] = set()
    for state in AEF["states"]:
        if state not in temp:
                add_final_state(AEF,state)
    return 0



def miroir(AEF):
    new_AEF = {}
    for a in AEF:
        new_AEF[a]=AEF[a]
        new_AEF["transitions"] = {}
        new_AEF["final_states"] = {}

    for a in AEF["final_states"]:
        set_start_state (new_AEF, a)  
    
    new_AEF["final_states"]= {AEF["start_state"]}

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




def reachable_states(AEF):
    # Initialiser un ensemble pour stocker les états accessibles 
    reachable = set()
    # Initialiser une liste pour stocker les états à visiter 
    to_visit = [AEF["start_state"]]

    # Parcourir les états à visiter 
    while to_visit:
        state = to_visit.pop()
        if state not in reachable :
            reachable.add(state)
            if state in AEF["transitions"] :
                for symbol in AEF["transitions"][state]:
                    to_visit.extend(AEF["transitions"][state][symbol])

    return reachable


def coaccess_states(AEF):
    # Initialiser un ensemble pour stocker les états coaccessibles 
    coaccessible = set (AEF["final_states"])
    # Initialiser une liste pour stocker les états à visiter 
    to_visit = list (AEF["final_states"])

    # Parcourir kes états à visiter 
    while to_visit:
        state = to_visit.pop()
        for from_state in AEF["transitions"]:
            for symbol in AEF["transitions"][from_state]:
                if state in AEF["transitions"][from_state][symbol] and from_state not in coaccessible :
                    coaccessible.add(from_state)
                    to_visit.append(from_state)
    
    return coaccessible




def trimmed_AEFv2(AEF):

    """Cette fonction permet d'émonder un automate en récupérant les états inutiles 
        et les supprimants grâce aux fonctions de base d'un automate"""
    
    # Verification des paramètres de l'automate 
    verification_AEF(AEF)

    print("Automate avant émondage : \n")
    print(AEF)

    # Obtenir les états accessibles et coaccessibles
    reachable = reachable_states(AEF)
    print("Etats accessibles : ")
    print(reachable)

    coaccessible = coaccess_states(AEF)
    print("Etats coaccessibles : ")
    print(coaccessible)

    # Obtenir les états utiles en calculant l'intersection des ensembles accessibles et coaccessibles
    useful_states = reachable.intersection(coaccessible)
    print("Etats utiles : ")
    print(useful_states)

    # Vérifier si l'automate est émondable ou pas 
    if AEF["states"] == useful_states:
        print ("\nVotre automate ne peut pas être émondé, tous les états sont utiles")
        return AEF

    # Supprimer les états inutiles
    for state in set(AEF["states"]) - useful_states:
        remove_state(AEF, state)

    # Supprimer les transitions inutiles
    for from_state in AEF["transitions"]:
        for symbol in AEF["transitions"][from_state]:
            to_states = AEF["transitions"][from_state][symbol]
            for to_state in set(to_states) - useful_states:
                remove_transition(AEF, from_state, to_state, symbol)

    print("\nVotre automate a été émondé avec succès ! ")
    return AEF
