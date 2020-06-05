import numpy as np
import gzip
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.lines import Line2D
from scipy.stats import beta

# make subplots for each output neuron
fig, axs = plt.subplots(3, 6)
plots = np.empty((3, 6), dtype=Line2D)

# move to make space for slider and digit
plt.subplots_adjust(bottom=0.20)
fig.suptitle("Output neuron pdfs")
t = np.arange(0, 1, 0.01)


# make plots for each output neuron
n = 0
for i in range(2):
    for j in range(1, 6):
        ax = axs[i, j]
        # mean:
        a_0 = 2.5
        # variance:
        b_0 = 2.5
        delta_a = 0.1
        plots[i, j], = ax.plot(t, beta.pdf(t, a_0, b_0), lw=2, color="red")
        ax.set_title(repr(n))
        ax.axis(xmin=0, xmax=1, ymin=0, ymax=10)
        n += 1
        ax.margins(x=0)


# add sliders
axcolor = 'w'
ax_a = fig.add_axes([0.1, 0.025, 0.8, 0.03], facecolor=axcolor)
ax_b = fig.add_axes([0.1, 0.075, 0.8, 0.03], facecolor=axcolor)

s_a = Slider(ax_a, r'Alpha', 0.1, 10., valinit=a_0, valstep=delta_a, color="k")
s_b = Slider(ax_b, r'Beta', 0.1, 10, valinit=b_0, valstep=0.1, color="k")


# update plot from sliders
def update(val):
    for i in range(2):
        for j in range(1, 6):
            a = s_a.val
            b = s_b.val
            # swap a and b for neuron 7
            if i == 1 and j == 3:
                a, b = b, a
            plots[i, j].set_ydata(beta.pdf(t, a, b))
            fig.canvas.draw_idle()


s_a.on_changed(update)
s_b.on_changed(update)


# get image of digit
f = gzip.open('t10k-images-idx3-ubyte.gz', 'r')

image_size = 28

f.read(16)
buf = f.read(image_size * image_size)
data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
data = data.reshape(image_size, image_size, 1)

image = np.asarray(data).squeeze()

# put image in an axes
ax_img = axs[0, 0]
ax_img.set_axis_off()
img = ax_img.imshow(image)

# remove ticks from empty axes
axs[1, 0].set_axis_off()
for j in range(6):
    axs[2, j].set_axis_off()

plt.tight_layout()
plt.show()
