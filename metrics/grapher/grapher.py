import parsers
import matplotlib.pyplot as plt


def plot_data(parser, directory, title, xlabel, ylabel, x=[], ylim=1000):
    results = parser(directory)
    
    if len(x) == len(results):
        plt.plot(x, results)
    else:
        for i, real_times in enumerate(results):
            plt.plot(real_times, label="Run {}".format(i))

    plt.xlabel(xlabel)
    plt.xticks(x)
    plt.ylabel(ylabel)
    plt.ylim(0, ylim)
    plt.title(title)
    plt.legend()
    
    
def dual_bar_data(parser, directory, title, xlabel, ylabel, x=[], ylim=1000):
    results = []
    for i in [0, 1]:
        results.append(parser[i](directory[i])[-1])
    
    if len(x) == len(results):
        plt.bar(x, results)
    else:
        for i, real_times in enumerate(results):
            plt.bar(real_times, label="Run {}".format(i))

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim(0, ylim)
    plt.title(title)
    plt.legend()


def dual_plot_data(parser, directory, title, xlabel, ylabel, x=[], ylim=1000, label=[1, 2]):
    for i in [0, 1]:
        results = parser[i](directory[i])
        if len(x) == len(results):
            plt.plot(x, results, label=label[i])
        else:
            for j, real_times in enumerate(results):
                plt.plot(real_times, label="Run {}".format(j))
                
    plt.xlabel(xlabel)
    plt.xticks(x)
    plt.ylabel(ylabel)
    plt.ylim(0, ylim)
    plt.title(title)
    plt.legend()
        