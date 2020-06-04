import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
t = np.arange(0, 1, 0.001)
# mean:
mu_0 = 0.5
# variance:
sigma_0 = 0.055
delta_mu = 0.1
s = (1/(sigma_0*np.sqrt(2*np.pi))) * np.exp(-(1/2)*((t-mu_0)/sigma_0)**2)
l, = plt.plot(t, s, lw=2)
ax.margins(x=0)

axcolor = 'w'
ax_mu = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_sigma = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

s_mu = Slider(ax_mu, 'Freq', 0., 1., valinit=mu_0, valstep=delta_mu, color="k")
s_sigma = Slider(ax_sigma, 'Amp', 0.1, 1, valinit=sigma_0, color="k")


def update(val):
    mu = s_mu.val
    sigma = s_sigma.val
    l.set_ydata((1/(sigma*np.sqrt(2*np.pi))) * np.exp(-(1/2)*((t-mu)/sigma)**2))
    fig.canvas.draw_idle()


s_mu.on_changed(update)
s_sigma.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    s_mu.reset()
    s_sigma.reset()


button.on_clicked(reset)

l.set_color('red')
l.axes.axis(xmin=0, xmax=1, ymin=0, ymax=5)
plt.show()
