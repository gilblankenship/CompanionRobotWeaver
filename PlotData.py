import matplotlib.pyplot as plt
def PlotData(x):
    numValues=len(x)
    plt.plot(range(numValues), x, '--ro')
    plt.grid()
    plt.title('Random Serial Data from Arduino')
    plt.xlabel('Counter')
    plt.ylabel('Data Value')
    plt.show()