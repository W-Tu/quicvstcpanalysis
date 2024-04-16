while true; do (echo "%CPU %MEM ARGS $(date)" && ps -e -o pcpu,pmem,args --sort -pcpu | cut -d" " -f1-5 | head) >> logs/$1.log; sleep 0.5; done
