from abc import ABC, abstractmethod
import scipy.integrate as integrate
from collections.abc import Mapping, Sequence
import copy
import pandas as pd

class Model(ABC):
    def __init__(self) -> None:
        self._result: Mapping[str, Sequence[float]] = dict()
        self.time_series: Sequence[int] = []

    @property
    def result(self):
        return self._result
    @abstractmethod
    def train(self, input_data):
        pass

    @abstractmethod
    def compute(self, initial_state, time_series):
        pass

    def save_to_csv(self, filename: str):
        dataframe_content = copy.copy(self._result)
        dataframe_content['day'] = self.time_series

        df = pd.DataFrame(dataframe_content)
        df.to_csv(f'{filename}.csv', index=False)


class RibbyOdeModel(Model):
    def __init__(self, hyperparameters):
        self.hyperparameters = hyperparameters
        self._result = dict()
        self.time_series = []

        def ode_equations(y, t):
            P, Q, Qp, C = y

            KDE = self.hyperparameters['KDE']
            K = self.hyperparameters['K']
            k_QpP = self.hyperparameters['k_QpP']
            k_PQ = self.hyperparameters['k_PQ']
            gamma_P = self.hyperparameters['gamma_P']
            gamma_Q = self.hyperparameters['gamma_Q']
            delta_Qp = self.hyperparameters['delta_Qp']
            lambda_P = self.hyperparameters['lambda_P']

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

    def compute(self, initial_state, time_series):
        self.time_series = time_series
        result = integrate.odeint(self.__ode_equations, initial_state, time_series)
        P, Q, Qp, C = result.T
        self._result = {
            'P': P,
            'Q': Q,
            'Qp': Qp,
            'C': C,
        }
        

class RibbySimplifiedOdeModel(Model):
    def __init__(self, hyperparameters):
        self.hyperparameters = hyperparameters
        self._result = dict()
        self.time_series = []


        def ode_equations(y, t):
            KDE = self.hyperparameters['KDE']
            K = self.hyperparameters['K']
            lambda_P = self.hyperparameters['lambda_P']
            gamma_P = self.hyperparameters['gamma_P']

            P, C = y
            P_star = P
            # Two differential equations
            dCdt = -KDE * C
            dPdt = lambda_P * P * (1 - P_star / K)  - gamma_P * C * KDE * P
            return dPdt, dCdt

        self.__ode_equations = ode_equations

    def train(self, input_data):
        pass

    def compute(self, initial_state, time_series):
        self.time_series = time_series
        result = integrate.odeint(self.__ode_equations, initial_state, time_series)
        P, C = result.T
        self._result = {
            'P': P,
            'C': C,
        }



# Proliferative cells initial population - according to research
P0 = 7.13
# Quiescent cells initial population - according to research
Q0 = 41.2
# Damaged quiescent cells - 0 as we start before any treatments
Qp0 = 0
# Drug dose - arbitrary number - should be set to 1 at the start of each cycle
C0 = 1

# lambda_P = 0.121
# k_PQ = 0.0295
# k_QpP = 0.0031
# delta_Qp = 0.00867
# gamma_P = 0.729
# gamma_Q = 0.729
# KDE = 0.24
# K = 100

# Setting initial values vector
initial_tuple_ribba = P0, Q0, Qp0, C0
initial_tuple_simple = P0, C0

# Hyperparameters obtained from paper

baseline_hyperparams = {
    'lambda_P': 6.80157379e-01,
    'k_PQ': 4.17370748e-01,
    'k_QpP': 0.00000001e+00,
    'delta_Qp': 6.78279483e-01,
    'gamma_P': 5.74025981e+00,
    'gamma_Q': 1.34300000e+00,
    'KDE': 9.51318080e-02,
    'K': 1.60140838e+02,
}

baseline_ribba_hyperparams = {
    "lambda_P": 0.121,
    "k_PQ": 0.0295,
    "k_QpP": 0.0031,
    "delta_Qp": 0.00867,
    "gamma_P": 0.729,
    "gamma_Q": 0.729,
    "KDE": 0.24,
    "K": 100,
}

surrogate_hyperparams = {
    **baseline_hyperparams,
    'KDE': baseline_hyperparams['KDE'] * 0.98,
    'lambda_P': baseline_hyperparams['lambda_P'] * 1.03,
    'gamma_Q': baseline_hyperparams['gamma_Q'] * 1.01
}

raw_surrogate_hyperparams = {
    **baseline_ribba_hyperparams,
    'KDE': baseline_hyperparams['KDE'] * 0.98,
    'lambda_P': baseline_hyperparams['lambda_P'] * 1.03,
    'gamma_Q': baseline_hyperparams['gamma_Q'] * 1.01
}

baseline_raw_model = RibbyOdeModel(baseline_ribba_hyperparams)
baseline_model = RibbyOdeModel(baseline_hyperparams)
baseline_raw_simple_model = RibbySimplifiedOdeModel(baseline_ribba_hyperparams)
baseline_simple_model = RibbySimplifiedOdeModel(baseline_hyperparams)

surrogate_model = RibbyOdeModel(surrogate_hyperparams)
raw_surrogate_model = RibbyOdeModel(raw_surrogate_hyperparams)



