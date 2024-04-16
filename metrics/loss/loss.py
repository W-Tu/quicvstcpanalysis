import sys
import glob

threshold = float(sys.argv[1]) or 60
logs = glob.glob("logs/*/*/*[!loss].log")

for log in logs:
    lost_packets = 0
    with open(log) as f:
        for line in f:
            time = line.rstrip().split("\t")[1]
            time = time.rstrip("s").split("m")
            seconds = int(time[0]) * 60 + float(time[1])
            if seconds >= threshold:
                lost_packets += 1
    new_log = log[:-4] + "loss" + log[-4:]
    with open(new_log, "w+") as f:
        f.write(str(lost_packets))


