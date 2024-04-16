from grapher import *
import parsers

DELAY = "./delay/logs"
LOSS = "./loss/logs"
CPU = "./serverutil/serverlogs/cpu"
MEM = "./serverutil/serverlogs/mem"
FLOODING = "/flooding"
ECHO = "/impersonation/echo"
RANDOM = "/impersonation/random"
SLOWLORIS = "/slowloris"
QUIC = "/quic"
TCP = "/tcp"

to_plot = {
    "quicfloodingdelay" : (
        plot_data, 
        [
            parsers.delay, 
            DELAY+FLOODING+QUIC, 
            "QUIC Flooding Attack", 
            "Number of Connection Handshakes (s$^{-1}$)",
            "Estimated Handshake Overhead (ms)",
            range(0, 101, 25), 
            2500
        ]
    ),
    "tcpfloodingdelay" : (
        plot_data, 
        [
            parsers.delay, 
            DELAY+FLOODING+TCP, 
            "TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Estimated Handshake \nOverhead (ms)",
            range(0, 101, 25), 
            2500
        ]
    ),
    "tcpfloodingrescaleddelay" : (
        plot_data, 
        [
            parsers.delay, 
            DELAY+FLOODING+TCP, 
            "TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Estimated Handshake \nOverhead (ms)",
            range(0, 101, 25), 
            15000
        ]
    ),
    "quicvstcpfloodingdelay" : (
        dual_plot_data,
        [
            [parsers.delay, parsers.delay],
            [DELAY+FLOODING+QUIC, DELAY+FLOODING+TCP],
            "QUIC vs TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Estimated Handshake \nOverhead (ms)",
            range(0, 101, 25), 
            15000,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpfloodinglossrate" : (
        dual_plot_data,
        [
            [parsers.lossrate, parsers.lossrate],
            [LOSS+FLOODING+QUIC, LOSS+FLOODING+TCP],
            "QUIC vs TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Lost Packets (%)",
            range(0, 101, 25), 
            100,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpfloodingcpu" : (
        dual_plot_data,
        [
            [parsers.cpu, parsers.cpu],
            [CPU+FLOODING+QUIC, CPU+FLOODING+TCP],
            "QUIC vs TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Mean CPU Utilisation (%)",
            range(0, 101, 25), 
            100,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpfloodingmem" : (
        dual_plot_data,
        [
            [parsers.mem, parsers.mem],
            [MEM+FLOODING+QUIC, MEM+FLOODING+TCP],
            "QUIC vs TCP Flooding Attack", 
            "Number of Connection \nHandshakes (s$^{-1}$)",
            "Mean Memory Utilisation (KB)",
            range(0, 101, 25), 
            1000,
            ["QUIC", "TCP"]
        ]
    ),
    ######################
    "quicslowlorisdelay" : (
        plot_data, 
        [
            parsers.delay, 
            DELAY+SLOWLORIS+QUIC, 
            "QUIC Slowloris Attack", 
            "Number of Active Connections",
            "Estimated Connection \nOverhead (ms)",
            range(0, 1001, 250), 
            2500
        ]
    ),
    "tcpslowlorisdelay" : (
        plot_data, 
        [
            parsers.delay, 
            DELAY+SLOWLORIS+TCP, 
            "TCP Slowloris Attack", 
            "Number of Active Connections",
            "Estimated Connection \nOverhead (ms)",
            range(0, 1001, 250), 
            2500
        ]
    ),
    "quicvstcpslowlorisdelay" : (
        dual_plot_data,
        [
            [parsers.delay, parsers.delay],
            [DELAY+SLOWLORIS+QUIC, DELAY+SLOWLORIS+TCP],
            "QUIC vs TCP Slowloris Attack", 
            "Number of Active Connections",
            "Estimated Connection \nOverhead (ms)",
            range(0, 1001, 250), 
            2500,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpslowlorislossrate" : (
        dual_plot_data,
        [
            [parsers.lossrate, parsers.lossrate],
            [LOSS+SLOWLORIS+QUIC, LOSS+SLOWLORIS+TCP],
            "QUIC vs TCP Slowloris Attack", 
            "Number of Active Connections",
            "Lost Packets (%)",
            range(0, 1001, 250), 
            100,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpslowloriscpu" : (
        dual_plot_data,
        [
            [parsers.cpu, parsers.cpu],
            [CPU+SLOWLORIS+QUIC, CPU+SLOWLORIS+TCP],
            "QUIC vs TCP Slowloris Attack", 
            "Number of Active Connections",
            "Mean CPU Utilisation (%)",
            range(0, 1001, 250), 
            100,
            ["QUIC", "TCP"]
        ]
    ),
    "quicvstcpslowlorismem" : (
        dual_plot_data,
        [
            [parsers.mem, parsers.mem],
            [MEM+SLOWLORIS+QUIC, MEM+SLOWLORIS+TCP],
            "QUIC vs TCP Slowloris Attack", 
            "Number of Active Connections",
            "Mean Memory Utilisation (KB)",
            range(0, 1001, 250), 
            1000,
            ["QUIC", "TCP"]
        ]
    ),
    ################
    "quicvstcpechodelay" : (
        dual_bar_data,
        [
            [parsers.delay, parsers.delay],
            [DELAY+ECHO+QUIC, DELAY+ECHO+TCP],
            "QUIC vs TCP Immediate \nClient Echo Attack", 
            "Protocol",
            "Estimated Echo Delay (ms)",
            ["QUIC", "TCP"],
            50000
        ]
    ),
    "quicvstcprandomdelay" : (
        dual_bar_data,
        [
            [parsers.delay, parsers.delay],
            [DELAY+RANDOM+QUIC, DELAY+RANDOM+TCP],
            "QUIC vs TCP Random \nServer Replay Attack", 
            "Protocol",
            "Estimated Replay Delay (ms)",
            ["QUIC", "TCP"],
            50000
        ]
    ),
    "quicvstcpecholossrate" : (
        dual_bar_data,
        [
            [parsers.lossrate, parsers.lossrate],
            [LOSS+ECHO+QUIC, LOSS+ECHO+TCP],
            "QUIC vs TCP Immediate \nClient Echo Attack", 
            "Protocol",
            "Lost Packets (%)",
            ["QUIC", "TCP"],
            100
        ]
    ),
    "quicvstcprandomlossrate" : (
        dual_bar_data,
        [
            [parsers.lossrate, parsers.lossrate],
            [LOSS+RANDOM+QUIC, LOSS+RANDOM+TCP],
            "QUIC vs TCP Random \nServer Replay Attack", 
            "Protocol",
            "Lost Packets (%)",
            ["QUIC", "TCP"],
            100
        ]
    ),
    "quicvstcpechocpu" : (
        dual_bar_data,
        [
            [parsers.cpu, parsers.cpu],
            [CPU+ECHO+QUIC, CPU+ECHO+TCP],
            "QUIC vs TCP Immediate \nClient Echo Attack",
            "Protocol",
            "Mean CPU Utilisation (%)",
            ["QUIC", "TCP"],
            100
        ]
    ),
    "quicvstcpechomem" : (
        dual_bar_data,
        [
            [parsers.mem, parsers.mem],
            [MEM+ECHO+QUIC, MEM+ECHO+TCP],
            "QUIC vs TCP Immediate \nClient Echo Attack",
            "Protocol",
            "Mean Memory Utilisation (KB)",
            ["QUIC", "TCP"],
            1000
        ]
    ),
    "quicvstcprandomcpu" : (
        dual_bar_data,
        [
            [parsers.cpu, parsers.cpu],
            [CPU+ECHO+QUIC, CPU+ECHO+TCP],
            "QUIC vs TCP Random \nServer Replay Attack",
            "Protocol",
            "Mean CPU Utilisation (%)",
            ["QUIC", "TCP"],
            100
        ]
    ),
    "quicvstcprandommem" : (
        dual_bar_data,
        [
            [parsers.mem, parsers.mem],
            [MEM+ECHO+QUIC, MEM+ECHO+TCP],
            "QUIC vs TCP Random \nServer Replay Attack",
            "Protocol",
            "Mean Memory Utilisation (KB)",
            ["QUIC", "TCP"],
            1000
        ]
    )
}

for plot in to_plot:
    print(plot)