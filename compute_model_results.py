import sys
from models import baseline_model, surrogate_model, y0
import numpy as np
from therapy_display import plot_therapy
import pandas as pd
import os

def save_to_csv(results, time_range, name):
  P, Q, Qp, C, cancer_cells = results
  df = pd.DataFrame({ 'P': P, 'Q': Q, 'Qp': Qp, 'C': C, 'day': time_range, 'cancer_cells': cancer_cells})
  df.to_csv(f'{name}.csv', index=False)  

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
  model_result = model.compute(y0, time_range)
  cancer_cells = []
  for i in range(len(time_range)):
    cancer_cells.append(model_result[0][i] + model_result[1][i] + model_result[2][i])
  save_to_csv((*model_result, cancer_cells), time_range, model_type)
