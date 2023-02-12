import sys
import numpy as np
import matplotlib.pyplot as plt
from Models import initial_tuple_ribba, initial_tuple_simple
from Therapy import gliomas_therapy, gliomas_simple_therapy
from utils import plot_ribba_model_results, plot_simple_model_results

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

    # import os
    # os.exit(1)
    # # Sensitivity analisys
    # base_params =  [
    #         lambda_P,
    #         k_PQ,
    #         k_QpP,
    #         delta_Qp,
    #         gamma_P,
    #         gamma_Q,
    #         KDE,
    #         K
    # ]
    # problem = {
    #     'num_vars': 8,
    #     'names': [
    #         "lambda_P",
    #         "k_PQ",
    #         "k_QpP",
    #         "delta_Qp",
    #         "gamma_P",
    #         "gamma_Q",
    #         "KDE",
    #         "K",
    #     ],
    #     'bounds': [[0.9 * param, 1.1 * param] for param in base_params]
    # }

    # from SALib.sample import saltelli
    # from SALib.analyze import sobol

    # param_values = saltelli.sample(problem, 2**6)

    # time_range = np.linspace(0, 100, 100)


    # for i in range(0, 4):
    #     y = np.array([RibbyOdeModel(tuple(params)).compute(y0, time_range)[i] for params in param_values])

    #     # P, Q, Qp, C = ribby_model.compute(y, t)

    #     # analyse
    #     sobol_indices = [sobol.analyze(problem, Y[1], print_to_console=False) for Y in enumerate(y.T)]
    #     Si = sobol_indices[1]
    #     print(Si.to_df())
    #     break
    # # print(sobol_indices)


    # # y = []
    # # for params in param_values:
    # #     model = RibbyOdeModel(tuple(params))
    # #     P, Q, Qp, C = model.compute(y0, time_range)
    # #     y.append(P)
    # #     # y.append([P, Q, Qp, C])
    # #
    # # Y = np.array(y)
    # # # print(Y.shape)
    # # Si = sobol.analyze(problem, Y)
    # #
    # # print(Si)
    # #
    # # y = np.array([parabola(x, *params) for params in param_values])
    # #
    # # sobol_indices = [sobol.analyze(problem, Y) for Y in y.T]
    # #
    # # x = np.linspace(0, 100, 100)
