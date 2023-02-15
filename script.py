import sys
import numpy as np
import matplotlib.pyplot as plt
from Models import initial_tuple_ribba, initial_tuple_simple, baseline_hyperparams, RibbyOdeModel
from Therapy import gliomas_therapy, gliomas_simple_therapy
from utils import plot_ribba_model_results, plot_simple_model_results
from SALib.sample import saltelli
from SALib.analyze import sobol

def to_params(tuple_params):
    lambda_P, k_PQ, k_QpP, delta_Qp, gamma_P, gamma_Q, KDE, K = tuple_params
    hyperparams = dict()
    hyperparams['lambda_P'] = lambda_P
    hyperparams['k_PQ'] = k_PQ
    hyperparams['k_QpP'] = k_QpP
    hyperparams['delta_Qp'] = delta_Qp
    hyperparams['gamma_P'] = gamma_P
    hyperparams['gamma_Q'] = gamma_Q
    hyperparams['KDE'] = KDE
    hyperparams['K'] = K
    return hyperparams

if __name__ == "__main__":
    time_range = np.linspace(0, 101, 101)
    model_type = "else"

    # Proposed therapy
    if model_type == "simple":
        gliomas_simple_therapy.compute_therapy(time_range, initial_tuple_simple)
        print(gliomas_simple_therapy.results)
        plot_simple_model_results(gliomas_simple_therapy.results, time_range, 'Simple')
    else:
        gliomas_therapy.compute_therapy(time_range, initial_tuple_ribba)
        plot_ribba_model_results(gliomas_therapy.results, time_range, 'Ribba')

    # Sensitivity analisys
    base_params =  [
        baseline_hyperparams['lambda_P'],
        baseline_hyperparams['k_PQ'],
        baseline_hyperparams['k_QpP'],
        baseline_hyperparams['delta_Qp'],
        baseline_hyperparams['gamma_P'],
        baseline_hyperparams['gamma_Q'],
        baseline_hyperparams['KDE'],
        baseline_hyperparams['K']
    ]
    problem = {
        'num_vars': 8,
        'names': [
            "lambda_P",
            "k_PQ",
            "k_QpP",
            "delta_Qp",
            "gamma_P",
            "gamma_Q",
            "KDE",
            "K",
        ],
        'bounds': [[0.9 * param, 1.1 * param] for param in base_params]
    }


    param_values = saltelli.sample(problem, 2**6)
    time_range = np.linspace(0, 101, 101)


    for key in ['P', 'Q', 'Qp', 'C']:
        y = np.array([RibbyOdeModel(to_params(tuple(params))) for params in param_values])
        for model in y:
            model.compute(initial_tuple_ribba, time_range)
        y = np.array([model.result[key] for model in y])

        # analyse
        sobol_indices = [sobol.analyze(problem, Y[1], print_to_console=False) for Y in enumerate(y.T)]
        Si = sobol_indices[1]
        print(Si.to_df())
        break

    # y = []
    # for params in param_values:
    #     model = RibbyOdeModel(tuple(params))
    #     P, Q, Qp, C = model.compute(y0, time_range)
    #     y.append(P)
    #     # y.append([P, Q, Qp, C])
    #
    # Y = np.array(y)
    # # print(Y.shape)
    # Si = sobol.analyze(problem, Y)
    #
    # print(Si)
    #
    # y = np.array([parabola(x, *params) for params in param_values])
    #
    # sobol_indices = [sobol.analyze(problem, Y) for Y in y.T]
    #
    # x = np.linspace(0, 100, 100)
