import numpy as np
from adao import adaoBuilder
from Models import RibbyOdeModel, initial_tuple_ribba, RibbySimplifiedOdeModel, initial_tuple_simple, simplified_baseline_hyperparams, Model
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

def model_trainer_factory(transform_params, model_class, y0, transform_output=None):
  def model_trainer(hyperparams, measurement_days):
    params = transform_params(hyperparams)
    model:Model = model_class(params)
    time_range = np.linspace(0, 101, 101)
    model.compute(y0, time_range)
    result = model.result
    if(transform_output):
      result = transform_output(result)
    return np.array([np.array(value)[measurement_days] for value in result.values()])
  return model_trainer

simple_model_trainer = model_trainer_factory(to_params, RibbySimplifiedOdeModel, initial_tuple_simple)
simple_less_params_trainer = model_trainer_factory(to_params_simple, RibbySimplifiedOdeModel, initial_tuple_simple)
def simple_constrained_trainer(*args):
  def transform(params):
    params = to_params_constrained(params)
    params['KDE'] = simplified_baseline_hyperparams['KDE']
  return model_trainer_factory(transform, RibbySimplifiedOdeModel, initial_tuple_simple)(*args)
def ribba_model_trainer(*args):
  def result_transform(result):
    return {'P': result['P'] + result['Q'] + result['Qp'], 'C': result['C']}
  return model_trainer_factory(to_params, RibbyOdeModel, initial_tuple_ribba, result_transform)(*args)


def compute_assimilated_parameters(
  assimilated_model_trainer,
  baseline_model_observations,
  initial_hyperparameters,
  measurement_days,
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
  case.set('ObservationOperator',  OneFunction = lambda params: assimilated_model_trainer(params, measurement_days))
  case.execute()
  result = case.get('Analysis')[-1]

  return result
