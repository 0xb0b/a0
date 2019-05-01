from copy import copy
import numpy as np
from matplotlib import pyplot as plt


# based on
# https://github.com/anujgupta82/Musings
# https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

# to make the dynamic figure updates work one needs to cast
# "%matplotlib notebook" magic in the notebook before plotting the figure


class Display:
    # visualize the game state (2048 board with numbered tiles) in jupyter
    # notebook

    def __init__(self, state_size=(4, 4), display_size=(8, 8),
                 colormap="magma_r", background_color="grey",
                 textcolors=("black", "white"), text_threshold=None):
        # copy to not modify the library colormap
        self.cmap = copy(plt.cm.get_cmap(colormap))
        self.cmap.set_bad(background_color)

        self.fig, axes = plt.subplots(figsize=display_size)

        # remove frame and ticks
        axes.set_frame_on(False)
        axes.tick_params(axis="both", which="both",
                         bottom=False, top=False, left=False, right=False,
                         labelbottom=False, labeltop=False,
                         labelleft=False, labelright=False)

        # set up the grid
        # first axis in matrix (vertical) is y axis on the plot and second axis
        # in matrix is x axis on the plot
        axes.set_xticks(np.arange(state_size[1]+1)-.5, minor=True)
        axes.set_yticks(np.arange(state_size[0]+1)-.5, minor=True)
        axes.grid(which="minor", color=background_color, linestyle='-',
                  linewidth=8)

        self.axes = axes

        # text color change threshold (to show light text on dark background
        # and vice versa)
        self.text_threshold = text_threshold

        self.text_kw = {'horizontalalignment': 'center',
                        'verticalalignment': 'center', 'fontsize': 16}
        self.textcolors = textcolors
        self.texts = []

        empty_state = np.zeros(state_size, dtype=int)
        self.draw(empty_state)

    def draw(self, state):
        # value 0 is masked in state so it is shown in background color on the
        # plot (this is set by the call to colormap method set_bad() in init)
        self.axes.imshow(np.ma.masked_equal(state, 0), cmap=self.cmap,
                         vmin=0, vmax=16)
        self.annotate(state)
        self.fig.canvas.draw()

    def annotate(self, state):
        # draw numbers (powers of 2) on the board tiles
        for text in self.texts:
            text.remove()
        self.texts.clear()
        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                if state[i, j] > 0:
                    # first axis in matrix is y axis on the plot,
                    # and second axis in matrix is x axis on the plot
                    if self.text_threshold is None:
                        text_color = self.textcolors[0]
                    else:
                        text_color = self.textcolors[state[i, j] >
                                                     self.text_threshold]
                    text = self.axes.text(j, i, 1 << state[i, j],
                                          color=text_color, **self.text_kw)
                    self.texts.append(text)


def test():
    import time
    display = Display(text_threshold=10)
    for i in range(4):
        state = np.random.randint(17, size=(4, 4), dtype=int)
        display.draw(state)
        time.sleep(2)
