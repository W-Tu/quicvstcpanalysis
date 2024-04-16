import sys
import glob

process_target = sys.argv[1] or "nginx"
logs = glob.glob("serverlogs/*[!cpu|!mem].log")

for log in logs:
    cpu_usage = []
    memory_usage = []

    with open(log) as f:
        lines = f.readlines()
        data_points = len(lines) // 9
        for i in range(data_points):
            c = "0"
            m = "0"
            line = lines[i * 9:(i + 1) * 9][-2]
            line = ' '.join(line.split())
            line = line.split(" ")
            if process_target in line[-1]:
                print(line)
                c = line[8]
                m = line[9]
                    
            cpu_usage.append(f"{c}\n")
            memory_usage.append(f"{m}\n")
    
    cpu_log = log[:-4] + "cpu" + log[-4:]
    memory_log = log[:-4] + "mem" + log[-4:]

    with open(cpu_log, "w+") as f:
        f.writelines(cpu_usage)

    with open(memory_log, "w+") as f:
        f.writelines(memory_usage)
