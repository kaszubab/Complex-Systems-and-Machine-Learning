import matplotlib.pyplot as plt

def prepare_axis(ax):
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)


def plot_ribba_model_results(results, time_series, title):
    fig = plt.figure(facecolor='w')
    data_labels = {
        'P': 'Proliferate cells',
        'Q': 'Quiescent cells',
        'Qp': 'Quiescent damaged cells',
        'C': 'Drug concentration',
    }
    colors = ['b', 'r', 'g', 'y']

    ax = fig.add_subplot(212, facecolor='#dddddd', axisbelow=True)
    ax.set_title(title)
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')

    for idx, key in enumerate(results):
        ax.plot(time_series, results[key], colors[idx], alpha=0.5, lw=2, label=data_labels[key])

    prepare_axis(ax)

    ax = fig.add_subplot(211, facecolor='#dddddd', axisbelow=True)
    ax.set_title(title)
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')

    ax.plot(time_series, results['P'] + results['Q'] + results['Qp'], 'b', alpha=0.5, lw=2, label='Total cells')
    ax.plot(time_series, results['C'], 'y', alpha=0.5, lw=2, label='Drug concentration')

    prepare_axis(ax)
    plt.show()

def plot_simple_model_results(results, time_series, title):
    data_labels = {
        'P': 'Total cells',
        'C': 'Drug concentration',
    }
    colors = ['b', 'r', 'g', 'y']

    
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(212, facecolor='#dddddd', axisbelow=True)
    ax.set_title(title)
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')

    for idx, key in enumerate(results):
        ax.plot(time_series, results[key], colors[idx], alpha=0.5, lw=2, label=data_labels[key])

    prepare_axis(ax)
    plt.show()
    
