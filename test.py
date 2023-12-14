AEF_1 = {'states': {'A','B','C'}, 'alphabet': {'x', 'y'}, 'transitions': {'A': {'x': ['B']}, 'B': {'y': ['C']}}, 'start_state': 'A' , 'final_states': {'B', 'C'}} 
AEF_2 = {'states': {'D','E','F'}, 'alphabet': {'w', 'z'}, 'transitions': {'D': {'z': ['E']}, 'E':{'w':['F']}}, 'start_state': 'D', 'final_states': {'F'}} 

from automate_util import add_transition

def concat(aef1, aef2):
    # Création de l'automate résultant
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

    print(result_aef)
    return result_aef

concat(AEF_1, AEF_2)
