from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np

class SensitivityAnalisys:
    PARAMETERS = ["P", "Q", "Qp", "C", "ALL"]
    SIMPLE_PARAMETERS = ["P", "C", "ALL"]

    def __init__(self, model_class, starting_vals, time_range):
        self.model_class = model_class
        self.starting_vals = starting_vals
        self.time_range = time_range

    def analyze(self, base_params, parameter, N):
        if parameter not in SensitivityAnalisys.PARAMETERS:
            raise ArgumentError(f"Unsupported parameter: {parameter}")
            
        boudns_percentage = 0.04

        problem = {
            'num_vars': 8,
            'names': [
                "KDE",
                "lambda_P",
                "K",
                "k_QpP",
                "k_PQ",
                "gamma_P",
                "gamma_Q",
                "delta_Qp"
            ],
            'bounds': [[(1 - boudns_percentage) * param, (1 + boudns_percentage) * param] for param in list(base_params)]
        }
        

        param_values = saltelli.sample(problem, N, calc_second_order=False)

        idx = SensitivityAnalisys.PARAMETERS.index(parameter)
        
        if parameter == "ALL":
            y = np.array([np.sum(self.model_class(tuple(params)).compute(self.starting_vals, self.time_range)[:3], axis=0) for params in param_values])
        else:
            y = np.array([self.model_class(tuple(params)).compute(self.starting_vals, self.time_range)[idx] for params in param_values])

        sobol_indices = [sobol.analyze(problem, Y, print_to_console=False, calc_second_order=False) for Y in y.T]

        return [Si.to_df() for Si in sobol_indices]
    
    def analyze_simple(self, base_params, parameter, N):
        if parameter not in SensitivityAnalisys.SIMPLE_PARAMETERS:
            raise ArgumentError(f"Unsupported parameter: {parameter}")
        boudns_percentage = 0.04

        problem = {
            'num_vars': 4,
            'names': [
                "lambda_P",
                "gamma_P",
                "KDE",
                "K",
            ],
            'bounds': [[(1 -boudns_percentage) * param, (1 + boudns_percentage) * param] for param in list(base_params)]
        }

        param_values = saltelli.sample(problem, N, calc_second_order=False)

        idx = SensitivityAnalisys.SIMPLE_PARAMETERS.index(parameter)
        
        y = np.array([self.model_class(self.params_for_simple_analysis(params)).compute(self.starting_vals, self.time_range)[idx] for params in param_values])

        sobol_indices = [sobol.analyze(problem, Y, print_to_console=False, calc_second_order=False) for Y in y.T]

        return [Si.to_df() for Si in sobol_indices]
    
    def params_for_simple_analysis(self, generated):
        lambda_P, gamma_P, KDE, K = generated
        
        return (KDE, lambda_P, K, 0, 0, gamma_P, 0, 0)
        
        
