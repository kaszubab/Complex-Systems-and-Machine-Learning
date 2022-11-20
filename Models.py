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
