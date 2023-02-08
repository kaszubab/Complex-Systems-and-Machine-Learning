import numpy as np
from adao import adaoBuilder
import pandas as pd
import matplotlib.pyplot as plt
import sys


FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else ''

labels = ['P', 'Q', 'Qp','C', 'cancer_cells']
baseline = pd.read_csv(FILE_PATH + 'baseline.csv')
surrogate = pd.read_csv(FILE_PATH + 'surrogate.csv')
iterations = [1, 5]
sizes = [2,4]

def save_plots(labels, backgrounds, observations, name_suffix, iterations):
  for label in labels:
      background = backgrounds[label]
      observation = observations[label]

      operator = np.identity(observation.shape[0])
      t = np.arange(observation.shape[0])
      case = adaoBuilder.New()

      if iterations is None:
        case.set( 'AlgorithmParameters',
          Algorithm = '3DVAR',
        )
      else:
        case.set( 'AlgorithmParameters',
          Algorithm = '3DVAR',     
          Parameters = {
              "MaximumNumberOfIterations": iterations,
          }
        )

      case.set( 'Background',          Vector = background )
      case.set( 'Observation',         Vector = observation )
      case.set( 'ObservationOperator', Matrix = operator )
      case.execute()

      result = case.get('Analysis')[-1]

      # plot
      fig = plt.figure(facecolor='w')
      ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
      ax.plot(t, background, 'green', alpha=0.5, lw=2, label=f'baseline')
      ax.plot(t, observation, 'red', alpha=0.5, lw=2, label=f'model')
      ax.plot(t, result, 'blue', alpha=0.5, lw=2, label=f'assimilation')
      ax.set_xlabel('Time /days')
      ax.set_ylabel('Volume')
      ax.yaxis.set_tick_params(length=0)
      ax.xaxis.set_tick_params(length=0)
      ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
      legend = ax.legend()
      legend.get_frame().set_alpha(0.5)
      ax.set_title(label)
      for spine in ('top', 'right', 'bottom', 'left'):
          ax.spines[spine].set_visible(False)
      plt.savefig(f"assimilation/{label}{name_suffix}.png")
      plt.close()


background = {label:baseline[label].to_numpy() for label in labels}
noise = {label: np.random.normal(0,0.05,background[label].shape[0]) for label in labels}
background = {label:background[label] * (1 + noise[label]) for label in labels}
observation = {label:surrogate[label].to_numpy() for label in labels}

save_plots(labels, background, observation, '', None)
for iteration in iterations:
  save_plots(labels, background, observation, f'_iteration_{iteration}', iteration)
for size in sizes:
  background_smaller = {}
  observation_smaller = {}
  for label in labels:
    background_smaller[label] = []
    observation_smaller[label] = []
    for i, item in enumerate(background[label]):
      if i % size == 0:
        background_smaller[label].append(background[label][i])
        observation_smaller[label].append(observation[label][i])
    background_smaller[label] = np.array(background_smaller[label])
    observation_smaller[label] = np.array(observation_smaller[label])

  save_plots(labels, background_smaller, observation_smaller, f'size_{50 / size}', None)