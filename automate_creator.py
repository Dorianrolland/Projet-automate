
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
