import sys
import numpy as np
import pandas as pd
from Models import baseline_model, surrogate_model, initial_tuple_ribba
import os

if __name__=='__main__':
  model_type = sys.argv[1]
  model = None
  if model_type == 'baseline':
    model = baseline_model
  elif model_type == 'surrogate':
    model = surrogate_model
  else:
    os.exit(1)

  time_range = np.linspace(0, 50, 51)
  model.compute(initial_tuple_ribba, time_range)
  model.save_to_csv(model_type)
