#!/usr/bin/env python3

import argparse
import binascii
import scapy
from scapy.all import *
import struct

class ClientIntercept:
    def __init__(self):
        pass
    
    def __call__(self, packet):
        # if self.args.verbose:
        #     packet.show()
        # else:

        if IP in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.bounce_back(packet)

    def bounce_back(self, packet):
        packet[TCP].sport, packet[TCP].dport = packet[TCP].dport, packet[TCP].sport
        packet[IP].src, packet[IP].dst = packet[IP].dst, packet[IP].src
        packet[Ether].src, packet[Ether].dst = packet[Ether].dst, packet[Ether].src
        del packet.chksum
        packet = packet.__class__(bytes(packet))
        sendp(packet, "enp6s0")

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)

class ServerIntercept:
    def __init__(self):
        pass
    
    def __call__(self, packet):
        # if self.args.verbose:
        #     packet.show()
        # else:

        if IP in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.52" and str(dst) == "192.168.100.51":
                self.bounce_back(packet)

    def bounce_back(self, packet):
        packet[TCP].sport, packet[TCP].dport = packet[TCP].dport, packet[TCP].sport
        packet[IP].src, packet[IP].dst = packet[IP].dst, packet[IP].src
        packet[Ether].src, packet[Ether].dst = packet[Ether].dst, packet[Ether].src
        del packet.chksum
        packet = packet.__class__(bytes(packet))
        sendp(packet, "enp6s0")

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)

class RandomServerImpersonation:
    def __init__(self):
        self.last_server_packet = []
    
    def __call__(self, packet):
        if IP in packet and TCP in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.52" and str(dst) == "192.168.100.51":
                self.record_server_packet(packet)
            elif str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.fake_server_reply(packet)

    def record_server_packet(self, packet):
        self.last_server_packet.append(packet)
            

    def fake_server_reply(self, client_packet):
        if len(self.last_server_packet) > 0:
            ind = random.randint(0, len(self.last_server_packet) - 1)
            server_packet = self.last_server_packet[ind]
            server_packet = self.copy_port(client_packet, server_packet)
            if server_packet:
                sendp(server_packet, "enp6s0")
                print(server_packet.summary())


    def copy_port(self, src, dst):
        dst[TCP].sport, dst[TCP].dport = src[TCP].dport, src[TCP].sport
        dst[IP].src, dst[IP].dst = src[IP].dst, src[IP].src
        dst[Ether].src, dst[Ether].dst = src[Ether].dst, src[Ether].src
        del dst.chksum
        dst = dst.__class__(bytes(dst))
        return dst

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)


class ServerImpersonation:
    def __init__(self):
        self.last_server_packet = []
    
    def __call__(self, packet):
        if IP in packet and TCP in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.52" and str(dst) == "192.168.100.51":
                self.record_server_packet(packet)
            elif str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.fake_server_reply(packet)

    def record_server_packet(self, packet):
        self.last_server_packet.append(packet)
            

    def fake_server_reply(self, client_packet):
        if len(self.last_server_packet) > 0:
            server_packet = self.last_server_packet[-1]
            server_packet = self.copy_port(client_packet, server_packet)
            if server_packet:
                sendp(server_packet, "enp6s0")
                print(server_packet.summary())


    def copy_port(self, src, dst):
        dst[TCP].sport, dst[TCP].dport = src[TCP].dport, src[TCP].sport
        dst[IP].src, dst[IP].dst = src[IP].dst, src[IP].src
        dst[Ether].src, dst[Ether].dst = src[Ether].dst, src[Ether].src
        del dst.chksum
        dst = dst.__class__(bytes(dst))
        return dst

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)


if __name__ == "__main__":
    #sniffer = ClientIntercept()
    #sniffer = ServerIntercept()
    #sniffer = RandomServerImpersonation()
    sniffer = ServerImpersonation()
    sniffer.run_forever()

    