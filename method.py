import pandas as pd
from scipy.spatial.distance import pdist,squareform

def apply_method(decision_matrix:pd.DataFrame, criteria_type:dict):
    apply_critic(decision_matrix,criteria_type)
    print("executando método")

def min_max_normalize(criteria:pd.Series,criteria_type:str):
    if criteria_type == "MAX":
        return criteria.apply(lambda x: (x - criteria.min()) / (criteria.max() - criteria.min()))
    else:
        return criteria.apply(lambda x: (x - criteria.max()) / (criteria.min() - criteria.max()))
        
def get_distance_matrix(min_max_matrix:pd.DataFrame):
    return squareform(pdist(min_max_matrix))

def apply_critic(decision_matrix:pd.DataFrame,criteria_type:dict):
    min_max_matrix = decision_matrix.apply(lambda criteria: min_max_normalize(criteria,criteria_type[criteria.name]))
    distance_matrix = get_distance_matrix(min_max_matrix)
    return

def apply_moora(decision_matrix:pd.DataFrame,criteria_type:dict,weights:dict):
    return

if __name__ == "__main__":

    # decicion matrix
    criteria = ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
    alternatives = [
                    "a1",
                    "a2",
                    "a3",
                    "a4",
                    "a5",
                    "a6",
                    "a7",
                    "a8",
                    ]
    vars = [
    [61300,1350000,1,813,91,22,7.95,7.95,3923,310,800,2,2],
    [65000,1400000,0,815,93.4,22,8.7,8,4229,403.7,750,4,2],
    [32500,900000,1,584,76.5,17.5,6.5,7.6,2774,216,550,0,2],
    [62500,1100000,1,798,92.7,22,9.5,7.8,4800,272,750,4,1,],
    [62500,1100000,1,754.72,87.4,21,9.3,7.8,3954,272,750,3,4],
    [62500,1100000,1,760,95,24,9.8,7.8,4900,339,750,4,2],
    [63500,1150000,1,750,95,24,9.8,7.8,5000,337,750,4,2],
    [64500,1200000,1,760,91,22,9.6,7.95,4500,280,800,4,3]
            ]

    decision_matrix = pd.DataFrame(
        vars,
        columns = criteria,
        index = alternatives)

    #weights

    #criteria
    criteria_type = ['MIN','MIN','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX','MAX']
    criteria_dict = dict(zip(criteria,criteria_type))
    print("iniciou o método")
    print(f"matrix de decisão: {decision_matrix}")
    apply_method(decision_matrix,criteria_dict)
    print("terminou de rodar o método")