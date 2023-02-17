from Models import baseline_model, RibbySimplifiedOdeModel, baseline_simple_model, simplified_baseline_hyperparams, initial_tuple_simple, initial_tuple_ribba
from Assimilation import compute_assimilated_parameters, simple_less_params_trainer, to_params_simple
from utils import compare_simple_model_results, plot_simple_model_results
import numpy as np
from Therapy import predefined_strategy, Therapy

def transform_results_to_simple(results):
  return {
  'P': results['P'] + results['Q'] + results['Qp'],
  'C': results['C']
}

time_range = np.linspace(0, 101, 101)
baseline_model.compute(initial_tuple_ribba, time_range)
measurement_days = list(range(0,41,10))
baseline_results = transform_results_to_simple(baseline_model.result)

day_measurements_results = {key:value[measurement_days] for key,value in baseline_results.items()}

bounds = [[None,None] for _ in range(4)]
bounds[2] = [0.05, 0.15]
assimilated_hyperparams = compute_assimilated_parameters(simple_less_params_trainer, day_measurements_results, simplified_baseline_hyperparams, measurement_days, bounds)

assimilated_model = RibbySimplifiedOdeModel(to_params_simple(assimilated_hyperparams))
assimilated_model.compute(initial_tuple_simple, time_range)

baseline_simple_model.compute(initial_tuple_simple, time_range)

pre_assimilation_results = baseline_simple_model.result
assimilation_results = assimilated_model.result

compare_simple_model_results([baseline_results, assimilation_results, pre_assimilation_results], 
  time_range,
  ['baseline', 'assimilated', 'surrogate'])

therapy_results = []
for model in [assimilated_model]:
  therapy = Therapy(model, predefined_strategy)
  therapy.compute_therapy(np.linspace(0, 131, 131), initial_tuple_simple)
  therapy_results.append(therapy.results)

therapy = Therapy(baseline_model, predefined_strategy)
therapy.compute_therapy(np.linspace(0, 131, 131), initial_tuple_ribba)
therapy_results.append(transform_results_to_simple(therapy.results))

compare_simple_model_results(therapy_results, 
  np.linspace(0, 131, 131),
  ['assimilated', 'surrogate', 'baseline'])
