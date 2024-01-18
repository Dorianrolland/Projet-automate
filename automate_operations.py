import pandas as pd

# Toutes les fonctions d'opérations et vérifications sur les automates (rendre complet, déterministe, miroir...)


from automate_util import add_state, add_final_state, add_transition, set_start_state, remove_state, remove_transition, str_to_state, state_to_str
from automate_creator import create_AEF
from Add_AEF2 import add_AEF


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

    if current_state in AEF["final_states"]:
         print("\nVotre mot a été reconnu avec succès par le langage de l'automate")
         return True 
    else : 
          print ("\nVotre mot n'a pas atteint un état final dans l'automate")
          return False


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


def determinize_AEF(AEF):
    """ Fonction pour rendre un automate déterministe """

    # On crée un AEF vide
    det_AEF = create_AEF()
    # Transformation de l'état initial en string
    start_state_str = state_to_str(AEF["start_state"])
    to_process = [start_state_str]

    while to_process:
        # Retirer un état de la file à traiter
        current_state_str = to_process.pop()
        current_state = str_to_state(current_state_str)
        det_AEF["states"].add(current_state_str)

        # Vérifier si l'un des états actuels est un état final
        if any(s in AEF["final_states"] for s in current_state):
            det_AEF["final_states"].add(current_state_str)

        # Parcourir les symboles de l'alphabet
        for symbol in AEF["alphabet"]:
            next_states = set()

            # Pour chaque état actuel, trouver les états suivants avec le symbole actuel
            for state in current_state:
                if state in AEF["transitions"] and symbol in AEF["transitions"][state]:
                    next_states.update(AEF["transitions"][state][symbol])

            # S'il y a des états suivants
            if next_states:
                next_states_str = state_to_str(next_states)

                # Ajouter les états suivants à la file à traiter s'ils ne sont pas déjà présents
                if next_states_str not in det_AEF["states"]:
                    to_process.append(next_states_str)

                # Créer ou mettre à jour les transitions dans l'AEF déterministe
                if current_state_str not in det_AEF["transitions"]:
                    det_AEF["transitions"][current_state_str] = {}

                det_AEF["transitions"][current_state_str][symbol] = [next_states_str]

    # Définir l'état initial de l'AEF déterministe et copier l'alphabet
    det_AEF["start_state"] = start_state_str
    det_AEF["alphabet"] = AEF["alphabet"].copy()

    # Mettre à jour l'AEF d'origine avec l'AEF déterministe
    AEF = det_AEF
    return AEF


def complementaire(AEF):
    # Afficher l'AEF initial
    print("AEF initial :", AEF)
    
    # Copier les états finaux dans une liste temporaire
    temp = []
    for state in AEF["final_states"]:
        temp.append(state)
    
    # Remplacer les états finaux par le complément de l'ensemble des états
    AEF["final_states"] = set()
    for state in AEF["states"]:
        if state not in temp:
            add_final_state(AEF, state)
    
    return 0


# Cette fonction permet de récuperer tous les états accessibles à partir d'un état donné avec un symbol donné 
def next_states(AEF, state, symbol): 
    states = set()
    if state in AEF["transitions"]:
        if symbol in AEF["transitions"][state]: 
            states.update(AEF["transitions"][state][symbol])
    return states


# Cette fonction permet de récuperer tous les états accessibles à partir d'un ensemble d'états donné avec un symbole donné 
def next_states_set(AEF, states, symbol): 
    next_states_set = set()
    for state in states :
        next_states_set.update(next_states(AEF, state, symbol))
    return next_states_set

# Cette fonction permet de créer l'ensemble des transitions possibles à partir d'un ensemble d'états donné 
def create_transition_set(AEF, states):
    transition_set = {}
    for symbol in AEF["alphabet"]:
        next_states = next_states_set(AEF, states, symbol)
        if next_states : 
            transition_set[symbol] = list(next_states)
    return transition_set


# Cette fonction donne le produit de 2 AEF 
def produit_AEF(AEF, AEF2):
    # Création d'un nouvel automate fini 
    new_AEF = create_AEF()
    # On combine les alphabets des 2 AEF 
    new_AEF["alphabet"] = AEF["alphabet"] | AEF2["alphabet"]

    # Création des états et de leurs transitions grâces aux fonctions contruites auparavant 
    for state1 in AEF["states"]: 
        for state2 in AEF2["states"] : 
            # Creation de l'état dans le produit 
            new_state = state1 + state2
            new_AEF["states"].add(new_state)

            # Un état du produit est final uniquement si les deux correspondants de AEF et AEF2 sont finaux
            if state1 in AEF["final_states"] and state2 in AEF2["final_states"]:
                new_AEF["final_states"].add(new_state)
            
            # La meme chose mais pour l'état initial 
            if (AEF["start_state"] == state1) and (AEF2["start_state"] == state2) : 
                new_AEF["start_state"] = new_state
            
            # Creation des transitions 
            transition_set_A = create_transition_set(AEF, {state1})
            transition_set_B = create_transition_set( AEF2, {state2})
            transition_set = {}
            for symbol in new_AEF["alphabet"]:
                next_states_A = next_states_set(AEF, {state1}, symbol)
                next_states_B = next_states_set(AEF2, {state2}, symbol)
                if next_states_A and next_states_B : 
                    transition_set[symbol] = [next_state_A + next_state_B for next_state_A in next_states_A for next_state_B in next_states_B]
            if transition_set :
                new_AEF["transitions"][new_state] = transition_set
    
    print ("\nLe produit de vos 2 AEF est : \n", new_AEF)

    return new_AEF



def miroir(AEF):
    # Créer un nouvel AEF
    new_AEF = {}
    
    # Copier les propriétés de l'AEF original dans le nouvel AEF
    for a in AEF:
        new_AEF[a] = AEF[a]
    new_AEF["transitions"] = {}
    new_AEF["final_states"] = {}

    # Définir les états finaux du nouvel AEF comme l'état initial de l'AEF original
    for a in AEF["final_states"]:
        set_start_state(new_AEF, a)

    new_AEF["final_states"] = {AEF["start_state"]}

    # Vérifier s'il y a exactement un état final dans l'AEF original
    if len(AEF["final_states"]) != 1:
        raise ValueError("Il faut que votre AEF n'ait qu'un état final")
    else:
        # Copier les transitions en inversant les états
        for start in AEF["transitions"]:
            i = 0
            for states in AEF["transitions"][start].values():
                for value in states:
                    add_transition(new_AEF, value, start, list(AEF["transitions"][start].keys())[i])
                i += 1
        
        # Afficher le miroir de l'AEF
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
        if state not in reachable:
            reachable.add(state)
            if state in AEF["transitions"]:
                for symbol in AEF["transitions"][state]:
                    to_visit.extend(AEF["transitions"][state][symbol])

    return reachable



def coaccess_states(AEF):
    # Initialiser un ensemble pour stocker les états coaccessibles
    coaccessible = set(AEF["final_states"])
    # Initialiser une liste pour stocker les états à visiter
    to_visit = list(AEF["final_states"])

    # Parcourir les états à visiter
    while to_visit:
        state = to_visit.pop()
        for from_state in AEF["transitions"]:
            for symbol in AEF["transitions"][from_state]:
                if state in AEF["transitions"][from_state][symbol] and from_state not in coaccessible:
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





def find_paths(AEF, df):
    """ Fonction pour retrouver tous les chemins possibles dans un automate """

    def check_final_states_transitions(AEF, df) : 
        """ Cette fonction permet de collécter les symboles des transitions des états finaux d'un automate et de les ajouter au chemin """
        final_states = AEF["final_states"]
        self_transitions = []

        for final_state in final_states : 
            transitions = df [(df["from_state"]== final_state) & (df["to_state"]== final_state)]
            if not transitions.empty : 
                symbols = transitions["symbol"].tolist()
                concatenated_symbols = '(' + '|'.join([f"{symbol}" for symbol in symbols] ) + ')*'
                self_transitions.append((final_state, concatenated_symbols))
        
        return self_transitions

    # création d'une liste pour stocker les chemins traversés
    paths = []
    # Pile pour effectuer une recherche en profondeur
    stack = [([ ], AEF["start_state"])]
    # Ensemble pour stocker les états déjà visités
    visited = set()

    self_transitions = check_final_states_transitions(AEF, df)
    while stack:
        # Retirer le chemin et l'état actuel de la pile
        path, state = stack.pop()

        # Vérifier si l'état actuel est un état final
        if state in AEF["final_states"]:
            if state in dict(self_transitions):
                # Ajouter les symboles de liaisons bouclés de l'état si il est final 
                path.append(dict(self_transitions)[state])
            # Ajouter le chemin à la liste des chemins
            paths.append(path)
        else:
            # Marquer l'état comme visité
            visited.add(state)
            # Filtrer les transitions depuis l'état actuel
            transitions = df[df["from_state"] == state ]
            # Regrouper les transitions par état de départ et d'arrivée, puis concaténer les symboles avec '|'
            grouped_transitions = transitions.groupby( ["from_state", "to_state"]) ["symbol"].apply(lambda x: '(' + '|'.join(x) + ')').reset_index()
            # Parcourir les transitions regroupées
            for _, transition in grouped_transitions.iterrows() :
                symbol = transition["symbol"]
                next_state = transition["to_state"]
                # Vérifier si l'état suivant n'a pas été visité
                if next_state not in visited : 
                    # Ajouter le chemin avec le symbole et passer à l'état suivant
                    stack.append((path + [symbol], next_state)) 
                # Sinon, si l'état suivant est le même que l'état actuel
                elif state == next_state:
                    # Ajouter le symbole avec '*' au chemin (auto-transition)
                    path.append(symbol + "*")
                      
    # Retourner la liste des chemins traversés
    return paths



def join_language(paths):
    return ' U '.join(' + '.join(path) for path in paths)

def join_regex(paths) : 
    return ' + '.join(' + '.join(path) for path in paths)



# Fonction pour créer un DataFrame à partir de la structure d'un automate
def df_from_AEF(AEF):
    data = []
    for state, transitions in AEF["transitions"].items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                data.append([state, symbol, next_state])
    return pd.DataFrame(data, columns=["from_state", "symbol", "to_state"])



def regex(AEF) : 
    df = df_from_AEF(AEF)
    # Obtenir la liste des chemins traversés dans l'AEF
    paths = find_paths(AEF, df)
    # Obtenir l'expression régulière en regroupant les chemins
    exp = join_regex(paths)
    # Afficher l'expression régulière
    print(f"Voici l'expression réfulière de votre AEF : {exp}")


def language(AEF):
    df= df_from_AEF(AEF)
    # Obtenir la liste des chemins traversés dans l'AEF
    paths = find_paths(AEF, df)
    # Obtenir le langage en regroupant les chemins
    language = join_language(paths)
    # Afficher le langage
    print(f'Voici le langage reconnu par votre AEF : {language}')




def are_automata_equivalent(AEF):
    """ Fonction qui permet de renvoyé si 2 AEF sont équivalents """

    # Ajout du deuxième automate 
    AEF2 = add_AEF()
    # Obtenir les chemins pour les deux automates
    paths_AEF1 = find_paths(AEF, df_from_AEF(AEF))
    paths_AEF2 = find_paths(AEF2, df_from_AEF(AEF2))

    # Vérifier si les langages sont équivalents en prenant en compte l'ordre entre les "+"
    language_AEF1 = join_language(paths_AEF1)
    language_AEF2 = join_language(paths_AEF2)
    print (f"\n\nVoici l'AEF que vous avez choisi comme 2éme AEF. Celui ci ne sera pas modifiable : \n{AEF2}")
    print (f"\nVoici le langage de votre AEF : {language_AEF1}")
    print (f"\nVoici le langage du 2éme AEF : {language_AEF2}")
    if language_AEF1 == language_AEF2 : 
        print ("\nLes 2 AEF sont équivalents !")
    else : 
        print("\nLes 2 AEF ne sont pas équivalents !")

def concat(aef1):
    # Création de l'automate résultant

    aef2 = add_AEF()

    result_aef = {
        'states': aef1['states'].union(aef2['states']),
        'alphabet': aef1['alphabet'].union(aef2['alphabet']),
        'transitions': {},
        'start_state': aef1['start_state'],
        'final_states': aef2['final_states']
    }

    # Copie des transitions de l'AEF_1 vers le résultat
    for state in aef1['transitions']:
        result_aef['transitions'][state] = aef1['transitions'][state].copy()

    # Ajout de la transition entre l'état final de l'AEF_1 et l'état initial de l'AEF_2
    
    for final_state_1 in list(aef1['final_states']):
        add_transition(result_aef, final_state_1, aef2['start_state'], '')

    # Copie des transitions de l'AEF_2 vers le résultat
    for state in aef2['transitions']:
        if state not in result_aef['transitions']:
            result_aef['transitions'][state] = aef2['transitions'][state].copy()
        else:
            for symbol in aef2['transitions'][state]:
                if symbol not in result_aef['transitions'][state]:
                    result_aef['transitions'][state][symbol] = aef2['transitions'][state][symbol].copy()
                else:
                    result_aef['transitions'][state][symbol].extend(aef2['transitions'][state][symbol])

    # On trie les états et l'alphabet pour remettre un peu d'ordre

    result_aef['states'] = sorted(result_aef['states'])
    result_aef['alphabet'] = sorted(result_aef['alphabet'])
    if '' in result_aef['alphabet']:
        result_aef['alphabet'].remove('')

    print('Nouvel AEF issu de la concaténation : ', result_aef)
    return result_aef
