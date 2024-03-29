import numpy as np
from Models import Model
from typing import NewType
from collections.abc import Callable, Mapping, Sequence
from Models import baseline_model, baseline_simple_model
import copy
import pandas as pd

class Therapy:
    def __init__(self, model: Model, strategy: Callable[[Model, int], (Mapping[str, Sequence[float]], int, Sequence[float])]):
        self.model = model
        self.strategy = strategy
        self.time_series = []
        self.results = dict()
    
    def compute_therapy(self, time_series, y0):
        self.results = dict()
        current_step = 0
        self.time_series = time_series
        t = time_series[current_step:]
        iteration = 0
        y = y0
        while current_step < len(time_series):
            self.model.compute(y, t)
            strategy_results, next_step, next_y = self.strategy(self.model, iteration)

            for key in strategy_results:
                partial_results = self.results.get(key, [])
                self.results[key] = np.concatenate([partial_results, strategy_results[key]])
            
            current_step += next_step
            y = next_y
            t = time_series[current_step:]
            iteration += 1

    def save_to_csv(self, filename):
        dataframe_content = copy.copy(self.results)
        dataframe_content['day'] = self.time_series

        df = pd.DataFrame(dataframe_content)
        df.to_csv(f'{filename}.csv', index=False)
    
def gliomas_strategy(model: Model, iteration: int) -> tuple[Mapping[str, Sequence[float]], int, Sequence[float]]:
    result = model.result
    Q = result['Q']
    P = result['P']
    Qp = result['Qp']

    next_treatment_index = 0
    for index, value in enumerate(Q):
        if index + 1 >= len(Q) or iteration >= 5:
            return result, len(Q), (0,0,0,1) 
        elif value < Q[index + 1]:
            next_treatment_index = index + 1
            break
    
    partial_results = dict()
    for key in model.result:
        partial_results[key] = result[key][:next_treatment_index]

    next_y = P[next_treatment_index], Q[next_treatment_index], Qp[next_treatment_index], 1
    return partial_results, next_treatment_index, next_y 

def gliomas_simple_strategy(model: Model, iteration: int) -> tuple[Mapping[str, Sequence[float]], int, Sequence[float]]:
    result = model.result
    P = result['P']

    next_treatment_index = 0
    for index, value in enumerate(P):
        if index + 1 >= len(P) or iteration >= 5:
            return result, len(P), (0,0,0,1) 
        elif value < P[index + 1]:
            next_treatment_index = index + 1
            break

    partial_results = dict()
    for key in model.result:
        partial_results[key] = result[key][:next_treatment_index]

    next_y = P[next_treatment_index], 1
    return partial_results, next_treatment_index, next_y


def predefined_strategy(model: Model, iteration:int) -> tuple[Mapping[str, Sequence[float]], int, Sequence[float]]:
    result = model.result
    treatments = [30,25,25,25]

    if iteration >= 4:
        return result, len(model.result['C']), (0,0,0,1) 

    next_treatment_index = treatments[iteration]

    partial_results = dict()
    for key in model.result:
        partial_results[key] = result[key][:next_treatment_index]

    next_y = [value[next_treatment_index] for value in model.result.values()]
    next_y[-1] = 1
    return partial_results, next_treatment_index, next_y


gliomas_therapy = Therapy(baseline_model, gliomas_strategy)
gliomas_simple_therapy = Therapy(baseline_simple_model, gliomas_simple_strategy)