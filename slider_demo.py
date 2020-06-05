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
fig.suptitle("Output neuron pdfs", x=7/12, ha="center")
t = np.arange(0, 1, 0.01)


# make plots for each output neuron
n = 0
for i in range(2):
    for j in range(1, 6):
        ax = axs[i, j]
        a_0 = 2
        b_0 = 20
        if i == 1 and j == 3:
            a_0, b_0 = b_0, a_0
        delta_a = 0.1
        plots[i, j], = ax.plot(t, beta.pdf(t, a_0, b_0), lw=2, color="red")
        ax.set_title(repr(n))
        ax.axis(xmin=0, xmax=1, ymin=0, ymax=10)
        n += 1
        ax.margins(x=0)


# add sliders
axcolor = 'w'
ax_a = fig.add_axes([0.1, 0.225, 0.8, 0.03], facecolor=axcolor)
ax_b = fig.add_axes([0.1, 0.175, 0.8, 0.03], facecolor=axcolor)
ax_c = fig.add_axes([0.1, 0.125, 0.8, 0.03], facecolor=axcolor)
ax_d = fig.add_axes([0.1, 0.075, 0.8, 0.03], facecolor=axcolor)
ax_e = fig.add_axes([0.1, 0.025, 0.8, 0.03], facecolor=axcolor)


s_a = Slider(ax_a, '# Epochs', 1, 100, valinit=a_0*5, valstep=1, color="k")
s_b = Slider(ax_b, '# Layers', 1, 10, valinit=b_0/5, valstep=1, color="k")
s_c = Slider(ax_c, 'Dataset size', 100, 1000, valinit=200, valstep=10, color="k")
s_d = Slider(ax_d, 'Batch Size', 1, 10, valinit=4, valstep=1, color="k")
s_e = Slider(ax_e, 'Learning Rate', 0.001, 0.01, valinit=0.003, valstep=0.001, color="k")


# update plot from sliders
def update(val):
    for i in range(2):
        for j in range(1, 6):
            a = s_a.val/2.5
            b = s_b.val*5
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
ax_img.set_title("Input\n ")
img = ax_img.imshow(image)

# remove ticks from empty axes
axs[1, 0].set_axis_off()
for j in range(6):
    axs[2, j].set_axis_off()

plt.tight_layout()
plt.show()
