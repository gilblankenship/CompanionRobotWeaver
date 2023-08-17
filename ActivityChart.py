import matplotlib.pyplot as plt
import random
import numpy as np

# Generate a random partition of 24 hours
ActitiyTimes = [random.randint(0, 23) for _ in range(7)]

# Create a list of Activities over a day
Activities = ["Sleep", "Reading", "Meals", 
              "Exercise", "Communications", "TV", "Other"]
results = {
    'Monday': [10, 15, 17, 32, 26],
    'Tuesday': [26, 22, 29, 10, 13],
    'Wednesday': [35, 37, 7, 2, 19],
    'Thursday': [32, 11, 9, 15, 33],
    'Friday': [21, 29, 5, 5, 40],
    'Saturday': [8, 19, 5, 30, 38],
    'Sunday': [35, 37, 7, 2, 19]
}

def ShowActivityDistribution(results, acts):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(acts, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncols=len(acts), 
              loc='lower center', fontsize='small')
    return fig, ax

ShowActivityDistribution(results, Activities)

plt.title("Mary Smith: 24 Hour ADL over One Week")
plt.show()


