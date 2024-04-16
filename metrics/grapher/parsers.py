import matplotlib.pyplot as plt
import os


def delay(directory):
    results = []
    for file in os.listdir(directory):
        if file.endswith(".log"):
            with open(os.path.join(directory, file), "r") as f:
                real_times = []
                for line in f:
                    _, real_time = line.split()
                    real_times.append(convert_to_milliseconds(real_time))
                
                results.append(sum(real_times) / len(real_times))

    return results


def lossnum(directory):
    results = []
    for file in os.listdir(directory):
        if file.endswith("loss.log"):
            with open(os.path.join(directory, file), "r") as f:
                results.append(f.readline())

    return results


def lossrate(directory):
    results = []
    for file in os.listdir(directory):
        if file.endswith("loss.log"):
            with open(os.path.join(directory, file), "r") as f:
                results.append((int(f.readline()) / 50.0) * 100)

    return results


def cpu(directory):
    results = []
    for file in os.listdir(directory):
        if file.endswith("cpu.log"):
            with open(os.path.join(directory, file), "r") as f:
                levels = []
                for line in f:
                    levels.append(float(line))
                
                results.append(sum(levels) / len(levels))
    
    return results


def mem(directory):
    results = []
    for file in os.listdir(directory):
        if file.endswith("mem.log"):
            with open(os.path.join(directory, file), "r") as f:
                levels = []
                for line in f:
                    levels.append(float(line) * 1000)
                
                results.append(sum(levels) / len(levels))
    
    return results


def convert_to_milliseconds(string):
    minutes, seconds = string.split("m")

    seconds = seconds[:-1]

    minutes_in_milliseconds = int(minutes) * 60000

    seconds_in_milliseconds = float(seconds) * 1000

    return minutes_in_milliseconds + seconds_in_milliseconds
