1. run usagelog.sh script with [attack_name] parameter **ON THE SERVER**
2. copy logs to local computer, in the /serverlogs/ folder
3. run python processextractor.py [process_name] where process name is the software running on the server, e.g. "nginx"
4. each file will be parsed into cpu and memory usage files

