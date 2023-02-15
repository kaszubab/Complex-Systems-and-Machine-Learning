import numpy as np
from adao import adaoBuilder
from Models import RibbyOdeModel, initial_tuple_ribba, RibbySimplifiedOdeModel, initial_tuple_simple, simplified_baseline_hyperparams
from Therapy import Therapy, gliomas_simple_strategy

def to_params(tuple_params):
  lambda_P, k_PQ, k_QpP, delta_Qp, gamma_P, gamma_Q, KDE, K = tuple_params
  hyperparams = dict()
  hyperparams['lambda_P'] = lambda_P
  hyperparams['k_PQ'] = k_PQ
  hyperparams['k_QpP'] = k_QpP
  hyperparams['delta_Qp'] = delta_Qp
  hyperparams['gamma_P'] = gamma_P
  hyperparams['gamma_Q'] = gamma_Q
  hyperparams['KDE'] = KDE
  hyperparams['K'] = K
  return hyperparams

def to_params_simple(tuple_params):
  lambda_P, gamma_P, KDE, K = tuple_params
  hyperparams = dict()
  hyperparams['lambda_P'] = lambda_P
  hyperparams['gamma_P'] = gamma_P
  hyperparams['KDE'] = KDE
  hyperparams['K'] = K
  return hyperparams

def to_params_constrained(tuple_params):
  lambda_P, gamma_P, K = tuple_params
  hyperparams = dict()
  hyperparams['lambda_P'] = lambda_P
  hyperparams['gamma_P'] = gamma_P
  hyperparams['K'] = K
  return hyperparams

def result_to_arr(result):
  return np.array([np.array(value) for value in result.values()])

def simple_model_trainer(hyperparams):
  params_dict = to_params(hyperparams)
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)
  model.compute(initial_tuple_simple, time_range)
  return result_to_arr(model.result)

def simple_less_params_trainer(hyperparams):
  params_dict = to_params_simple(hyperparams)
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)
  model.compute(initial_tuple_simple, time_range)
  return result_to_arr(model.result)

def simple_constrained_trainer(hyperparams):
  params_dict = to_params_constrained(hyperparams)
  params_dict['KDE'] = simplified_baseline_hyperparams['KDE']
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)
  model.compute(initial_tuple_simple, time_range)
  return result_to_arr(model.result)


def ribba_model_trainer(hyperparams):
  params_dict = to_params(hyperparams)
  model = RibbyOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)
  model.compute(initial_tuple_ribba, time_range)
  return result_to_arr(model.result)

def simple_therapy_trainer(hyperparams):
  params_dict = to_params(hyperparams)
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)

  therapy = Therapy(model, gliomas_simple_strategy)
  therapy.compute_therapy(time_range, initial_tuple_simple)

  return result_to_arr(therapy.results)

def simple_less_params_therapy_trainer(hyperparams):
  params_dict = to_params_simple(hyperparams)
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)

  therapy = Therapy(model, gliomas_simple_strategy)
  therapy.compute_therapy(time_range, initial_tuple_simple)

  return result_to_arr(therapy.results)

def simple_constrained_therapy_trainer(hyperparams):
  params_dict = to_params_constrained(hyperparams)
  params_dict['KDE'] = simplified_baseline_hyperparams['KDE']
  model = RibbySimplifiedOdeModel(params_dict)
  time_range = np.linspace(0, 101, 101)

  therapy = Therapy(model, gliomas_simple_strategy)
  therapy.compute_therapy(time_range, initial_tuple_simple)

  return result_to_arr(therapy.results)

def compute_assimilated_parameters(
  assimilated_model_trainer,
  baseline_model_observations,
  initial_hyperparameters,
  bounds = None):
  case = adaoBuilder.New()
  if bounds:
    case.set( 'AlgorithmParameters',
      Algorithm = '3DVAR',
      Parameters = {"Bounds": bounds}
      )
  else:
    case.set( 'AlgorithmParameters', Algorithm = '3DVAR')
  case.set('Background', Vector = np.array([x for x in initial_hyperparameters.values()]))
  case.set('Observation', Vector = result_to_arr(baseline_model_observations))
  case.set('ObservationOperator',  OneFunction = assimilated_model_trainer)
  case.execute()
  result = case.get('Analysis')[-1]

  return result
