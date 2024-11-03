import matplotlib.pyplot as plt

def scatter_plot(data: list, title: str, xlabel: str):
    x_values = [x[0] for x in data]
    y_values = [x[1] for x in data]
    plt.scatter(x_values, y_values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()