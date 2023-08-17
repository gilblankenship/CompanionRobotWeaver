import matplotlib.pyplot as plt

data = {'Sleep': 8.5, 'TV': 6.2, 'Comm': 0.5, 
        'Eating': 2, 'Nap': 1.2, 'Dressing': 0.2, 'Exer': 0.1}
names = list(data.keys())
values = list(data.values())
fig, ax = plt.subplots()
bar_colors = ['tab:green', 'tab:blue', 'tab:purple', 'tab:orange']
bar_labels = names
ax.bar(names, values, label=bar_labels, color=bar_colors)
fig.suptitle('Mary Smith: Distribution of ADL Times 2023-08-10')
ax.set_ylabel('Time (hrs)')
# ax.legend(title='Times')
# plt.grid('true')
plt.show()