import numpy as np
import matplotlib.pyplot as plt

def plot_simple_therapy(results):
    P, C = results
    t = np.linspace(0, P.size, P.size)


    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(212, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, P, 'b', alpha=0.5, lw=2, label='Proliferate cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    ax.spines[spine].set_visible(False)
    ax = fig.add_subplot(211, facecolor='#dddddd', axisbelow=True)
    ax.plot(t, P, 'b', alpha=0.5, lw=2, label='Total cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    plt.show()


def plot_therapy(results, title="Model"):
    P, Q, Qp, C = results
    t = np.linspace(0, P.size, P.size)


    # Plot the data on three separate curves for S(t), I(t) and R(t)
    fig = plt.figure(facecolor='w')
    ax = fig.add_subplot(212, facecolor='#dddddd', axisbelow=True)
    ax.set_title(title)
    ax.plot(t, P, 'b', alpha=0.5, lw=2, label='Proliferate cells')
    ax.plot(t, Q, 'r', alpha=0.5, lw=2, label='Quiescent')
    ax.plot(t, Qp, 'g', alpha=0.5, lw=2, label='Quiescent damaged cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    ax.spines[spine].set_visible(False)
    ax = fig.add_subplot(211, facecolor='#dddddd', axisbelow=True)
    ax.set_title(title)
    ax.plot(t, P + Q + Qp, 'b', alpha=0.5, lw=2, label='Total cells')
    ax.plot(t, C, 'y', alpha=0.5, lw=2, label='Drug concentration')
    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Size (mm)')
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    plt.show()

