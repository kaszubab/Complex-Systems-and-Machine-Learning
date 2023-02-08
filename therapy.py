import numpy as np

def gliomas_therapy(ribby_model, time_range, y0):
    y = y0
    t = time_range
    treatment_results = [[], [], [], []]
    for i in range(5):
        P, Q, Qp, C = ribby_model.compute(y, t)
        next_treatment_month = [ind for ind, x in enumerate(Q) if ind + 1 < Q.size and x < Q[ind + 1]][0]
        for idx, value in enumerate([P, Q, Qp, C]):
            treatment_results[idx].append(value[0: next_treatment_month])
        y = P[next_treatment_month], Q[next_treatment_month], Qp[next_treatment_month], 1
    treatment_results = [np.concatenate(x) for x in treatment_results]
    return treatment_results

def gliomas_simple_therapy(ribby_simple_model, time_range, y0):
    y = y0
    t = time_range
    treatment_results = [[], []]
    for i in range(5):
        P, C = ribby_simple_model.compute(y, t)
        next_treatment_month = [ind for ind, x in enumerate(P) if ind + 1 < P.size and x < P[ind + 1]][0]
        for idx, value in enumerate([P, C]):
            treatment_results[idx].append(value[0: next_treatment_month])
        y = P[next_treatment_month], 1

    treatment_results = [np.concatenate(x) for x in treatment_results]
    return treatment_results

