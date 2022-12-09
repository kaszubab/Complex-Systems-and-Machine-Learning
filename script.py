import sys
import numpy as np
import matplotlib.pyplot as plt
from Models import RibbyOdeModel, RibbySimplifiedOdeModel

from therapy_display import plot_simple_therapy, plot_therapy
import therapy

# Proliferative cells initial population - according to research
P0 = 7.13
# Quiescent cells initial population - according to research
Q0 = 41.2
# Damaged quiescent cells - 0 as we start before any treatments
Qp0 = 0
# Drug dose - arbitrary number - should be set to 1 at the start of each cycle
C0 = 1

# According to research
# lambda_P = 6.80157379e-01
# k_PQ = 4.17370748e-01
# k_QpP = 0.00000001e+00
# delta_Qp = 6.78279483e-01
# gamma_P = 5.74025981e+00
# gamma_Q = 1.34300000e+00
# KDE = 9.51318080e-02
# K = 1.60140838e+02

lambda_P = 0.121
k_PQ = 0.0295
k_QpP = 0.0031
delta_Qp = 0.00867
gamma_P = 0.729
gamma_Q = 0.729
KDE = 0.24
K = 100

# Setting initial values vector
y0 = P0, Q0, Qp0, C0
y0_simple = P0, C0

# Setting constants
consts = (KDE, lambda_P, K, k_QpP, k_PQ, gamma_P, gamma_Q, delta_Qp)

if __name__ == "__main__":

    ribby_model = RibbyOdeModel(consts)
    ribby_simple_model = RibbySimplifiedOdeModel(consts)
    time_range = np.linspace(0, 100, 100)

    model_type = "else"

    # Proposed therapy
    if model_type == "simple":
        treatment_results = therapy.gliomas_simple_therapy(ribby_simple_model, time_range, y0_simple)
        print(treatment_results)
        plot_simple_therapy(treatment_results)
    else:
        treatment_results = therapy.gliomas_therapy(ribby_model, time_range, y0)
        plot_therapy(treatment_results)

    import os
    os.exit(1)
    # Sensitivity analisys
    base_params =  [
            lambda_P,
            k_PQ,
            k_QpP,
            delta_Qp,
            gamma_P,
            gamma_Q,
            KDE,
            K
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

    from SALib.sample import saltelli
    from SALib.analyze import sobol

    param_values = saltelli.sample(problem, 2**6)

    time_range = np.linspace(0, 100, 100)


    for i in range(0, 4):
        y = np.array([RibbyOdeModel(tuple(params)).compute(y0, time_range)[i] for params in param_values])

        # P, Q, Qp, C = ribby_model.compute(y, t)

        # analyse
        sobol_indices = [sobol.analyze(problem, Y[1], print_to_console=False) for Y in enumerate(y.T)]
        Si = sobol_indices[1]
        print(Si.to_df())
        break
    # print(sobol_indices)


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
