from Models import surrogate_model, baseline_model, initial_tuple_ribba, baseline_hyperparams, initial_tuple_test, RibbySimplifiedOdeModel, simplified_baseline_hyperparams
from Assimilation import ribba_model_trainer, compute_assimilated_parameters, to_params, simple_therapy_trainer, to_params_simple, simple_less_params_therapy_trainer
from utils import compare_simple_model_results
import numpy as np
from Therapy import gliomas_therapy, gliomas_simple_therapy, gliomas_simple_strategy, Therapy

time_range = np.linspace(0, 101, 101)
gliomas_therapy.compute_therapy(time_range, initial_tuple_ribba)

parsed_baseline_model_results = {
  'P': gliomas_therapy.results['P'] + gliomas_therapy.results['Q'] + gliomas_therapy.results['Qp'],
  'C': gliomas_therapy.results['C']
}

bounds = [[None,None] for _ in range(4)]
bounds[2] = [0.05, 0.15]
assimilated_hyperparams = compute_assimilated_parameters(simple_less_params_therapy_trainer, parsed_baseline_model_results, simplified_baseline_hyperparams, bounds)

assimilated_therapy = Therapy(RibbySimplifiedOdeModel(to_params_simple(assimilated_hyperparams)), gliomas_simple_strategy)
assimilated_therapy.compute_therapy(time_range, initial_tuple_test)

gliomas_simple_therapy.compute_therapy(time_range, initial_tuple_test)

compare_simple_model_results([parsed_baseline_model_results, assimilated_therapy.results, gliomas_simple_therapy.results], 
  time_range,
  ['baseline', 'assimilated', 'simple'])
