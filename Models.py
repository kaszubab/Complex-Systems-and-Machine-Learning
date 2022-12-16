from abc import ABC, abstractmethod
import scipy.integrate as integrate

class Model(ABC):
    @abstractmethod
    def train(self, input_data):
        pass

    @abstractmethod
    def compute(self, initialParameters, time_series):
        pass


class RibbyOdeModel(Model):
    def __init__(self, params):
        self.params = params

        def ode_equations(y, t, KDE, lambda_P, K, k_QpP, k_PQ, gamma_P, gamma_Q, delta_Qp):
            P, Q, Qp, C = y
            P_star = P + Q + Qp
            # Four differential equations
            dCdt = -KDE * C
            dPdt = lambda_P * P * (1 - P_star / K) + k_QpP * Qp - k_PQ * P - gamma_P * C * KDE * P
            dQdt = k_PQ * P - gamma_Q * C * KDE * Q
            dQpdt = gamma_Q * C * KDE * Q - k_QpP * Qp - delta_Qp * Qp
            return dPdt, dQdt, dQpdt, dCdt

        self.__ode_equations = ode_equations

    def train(self, input_data):
        pass

    def compute(self, initial_parameters, time_series):
        result = integrate.odeint(self.__ode_equations, initial_parameters, time_series, args=self.params)
        return result.T

class RibbySimplifiedOdeModel(Model):
    def __init__(self, params):
        self.params = params

        def ode_equations(y, t, KDE, lambda_P, K, _1, k_PQ, gamma_P, _2, _3):
            P, C = y
            P_star = P
            # Four differential equations
            dCdt = -KDE * C
            dPdt = lambda_P * P * (1 - P_star / K)  - gamma_P * C * KDE * P
            return dPdt, dCdt

        self.__ode_equations = ode_equations

    def train(self, input_data):
        pass

    def compute(self, initial_parameters, time_series):
        result = integrate.odeint(self.__ode_equations, initial_parameters, time_series, args=self.params)
        return result.T


# Proliferative cells initial population - according to research
P0 = 7.13
# Quiescent cells initial population - according to research
Q0 = 41.2
# Damaged quiescent cells - 0 as we start before any treatments
Qp0 = 0
# Drug dose - arbitrary number - should be set to 1 at the start of each cycle
C0 = 1

lambda_P = 6.80157379e-01
k_PQ = 4.17370748e-01
k_QpP = 0.00000001e+00
delta_Qp = 6.78279483e-01
gamma_P = 5.74025981e+00
gamma_Q = 1.34300000e+00
KDE = 9.51318080e-02
K = 1.60140838e+02

# lambda_P = 0.121
# k_PQ = 0.0295
# k_QpP = 0.0031
# delta_Qp = 0.00867
# gamma_P = 0.729
# gamma_Q = 0.729
# KDE = 0.24
# K = 100

# Setting initial values vector
y0 = P0, Q0, Qp0, C0
y0_simple = P0, C0

# Setting constants
baseline_consts = (KDE, lambda_P, K, k_QpP, k_PQ, gamma_P, gamma_Q, delta_Qp)
surrogate_consts = (KDE * 0.98, 1.03 * lambda_P, K, k_QpP, k_PQ, gamma_P, 1.01 * gamma_Q, delta_Qp)

baseline_model = RibbyOdeModel(baseline_consts)
baseline_simple_model = RibbySimplifiedOdeModel(baseline_consts)

surrogate_model = RibbyOdeModel(surrogate_consts)



