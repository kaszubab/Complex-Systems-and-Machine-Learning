import sys
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
from Models import RibbyOdeModel

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

# Setting constants
consts = (KDE, lambda_P, K, k_QpP, k_PQ, gamma_P, gamma_Q, delta_Qp)


if __name__ == "__main__":

    ribby_model = RibbyOdeModel(consts)
    t = np.linspace(0, 100, 100)

    def gliomas_therapy(y0, consts):
        y = y0
        treatment_results = [[], [], [], []]
        for i in range(5):
            P, Q, Qp, C = ribby_model.compute(y, t)
            next_treatment_month = [ind for ind, x in enumerate(Q) if ind + 1 < Q.size and x < Q[ind + 1]][0]
            for idx, value in enumerate([P, Q, Qp, C]):
                treatment_results[idx].append(value[0: next_treatment_month])
            y = P[next_treatment_month], Q[next_treatment_month], Qp[next_treatment_month], 1
        treatment_results = [np.concatenate(x) for x in treatment_results]
        return treatment_results


    treatment_results = gliomas_therapy(y0, consts)
    P, Q, Qp, C = treatment_results
    t = np.linspace(0, P.size, P.size)


    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(212, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, P, 'b', alpha=0.5, lw=2, label='Proliferate cells')
    ax.plot(t, Q, 'r', alpha=0.5, lw=2, label='Quiescent')
    ax.plot(t, Qp, 'g', alpha=0.5, lw=2, label='Quiescent damaged cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    ax.spines[spine].set_visible(False)
    ax = fig.add_subplot(211, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, P + Q + Qp, 'b', alpha=0.5, lw=2, label='Total cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    plt.show()