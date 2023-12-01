 

# Toutes les fonctions d'opérations et vérifications sur les automates (rendre complet, déterministe, miroir...)


from automate_util import add_state, add_final_state, add_transition, set_start_state



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
