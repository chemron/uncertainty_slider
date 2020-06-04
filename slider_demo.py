import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import rcParams
from matplotlib.lines import Line2D
from scipy.stats import beta

rcParams['mathtext.fontset'] = 'stix'
rcParams['font.family'] = 'STIXGeneral'

fig, axs = plt.subplots(2, 5)
plots = np.empty((2, 5), dtype=Line2D)

plt.subplots_adjust(bottom=0.20)
t = np.arange(0, 1, 0.01)

n = 0
for i in range(2):
    for j in range(5):
        ax = axs[i, j]
        # mean:
        a_0 = 2.5
        # variance:
        b_0 = 2.5
        delta_a = 0.1
        plots[i, j], = ax.plot(t, beta.pdf(t, a_0, b_0), lw=2, color="red")
        ax.set_title(repr(n))
        ax.axis(xmin=0, xmax=1, ymin=0, ymax=5)
        n += 1
        ax.margins(x=0)

axcolor = 'w'
ax_a = fig.add_axes([0.1, 0.025, 0.8, 0.03], facecolor=axcolor)
ax_b = fig.add_axes([0.1, 0.075, 0.8, 0.03], facecolor=axcolor)

s_a = Slider(ax_a, r'Alpha', 0.1, 5., valinit=a_0, valstep=delta_a, color="k")
s_b = Slider(ax_b, r'Beta', 0.1, 5, valinit=b_0, valstep=0.1, color="k")


def update(val):
    for i in range(2):
        for j in range(5):
            a = s_a.val
            b = s_b.val
            if i == 1 and j == 3:
                a, b = b, a
            plots[i, j].set_ydata(beta.pdf(t, a, b))
            fig.canvas.draw_idle()

# def plot(a, b)


s_a.on_changed(update)
s_b.on_changed(update)

plt.show()
