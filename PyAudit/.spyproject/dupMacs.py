#Useful source https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html

import argparse
from ipaddress import ip_address
import os
import sys

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
class mitmPacket:
    def __init__(self):
        #Other Info
        self.packet_id = None
        #Ethernet Info
        self.src_mac = None
        self.dst_mac = None

        #Ip Info
        self.src_ip = None
        self.dst_ip = None

        #Tcp Info
        self.src_port = None
        self.dst_port = None
    
    def showInfo(self):
        print('ID: {} | Src_Mac: {} | Src IP: {} | Src Port: {} | Dst Mac: {} | Dst Ip: {} | Dst Port: {}'.format(self.packet_id, self.src_mac, self.src_ip, self.src_port, self.dst_mac, self.dst_ip, self.dst_port ))

#Returns a list of my custom class that hold on to the following info: Src/Dst: IP, Mac, Ports
def extractDataFromRaw(file_name):

    packetMax = 2000
    count = 0
    mitmList = []
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1
        curr = mitmPacket()

        #Packet id will break if you ever count from anywhere other than packet 1..
        curr.packet_id = count

        if count > packetMax:  #Eventually I'll add a function that lets you read first x packets, last x packets or  range of packets
            break
        ether_pkt = Ether(pkt_data)

        curr.dst_mac = ether_pkt.dst
        curr.src_mac = ether_pkt.src

        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue

        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue

        ip_pkt = ether_pkt[IP]
        curr.dst_ip = ip_pkt.dst
        curr.src_ip = ip_pkt.src

        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue
        
        tcp_pkt = ip_pkt[TCP]
        curr.dst_port = tcp_pkt.dport
        curr.src_port = tcp_pkt.sport

        mitmList.append(curr)

    return mitmList

def duplicateMacs(mitmPacketList):

    #Macs will be stored in a dictionary that looks like this Mac:([list of ips: mitmpacket])
    #
    visitedDict = {}
    keysList = []
    for i in mitmPacketList:
        # every packet gives two combinations of a mac and ip
        # Adding the combos to a list of size 2 and iterating  will make it easier to program
        curr_mac_combo_1 = (i.src_mac, i.src_ip)
        curr_mac_combo_2 = (i.dst_mac, i.dst_ip)
        currList = []
        currList.append(curr_mac_combo_1)
        currList.append(curr_mac_combo_2)

        # If not  visited, add to visited set
        for i in currList:
            if i[0] not in visitedDict:
                visitedDict[i[0]] = [i[1]]
                continue
            
             
            else:
                #Ip mapping equal to other ip mappings, no change
                if i[1] in visitedDict[i[0]]:
                    continue
                #Duplicate Mac, add new ip to Mac Mapping
                else:
                    visitedDict[i[0]].append(i[1])
        
    for key in visitedDict:
        if len(visitedDict[key]) <= 1:
            keysList.append(key)
    
    for entry in keysList:
        visitedDict.pop(entry)
    return visitedDict

def process_pcap(file_name):

    print('Opening {}...'.format(file_name))

    mitmPacketList = []
    mitmPacketList = extractDataFromRaw(file_name)
    dupMacDict = duplicateMacs(mitmPacketList)
    for key in dupMacDict:
        count = len(dupMacDict[key])
        print("{} Duplicates Found for {}".format(count, key))
        print(dupMacDict[key])




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--pcap', metavar='<pcap file name>',
                        help='pcap file to parse', required=True)
    # If I ever store the mitm packets, I can use the following init option to avoid processing the same packets multiple times
    #parser.add_argument('--init', help='Converts raw packets into class objects. Use if mitm list is empty', required=False)
    args = parser.parse_args()
    
    file_name = args.pcap
    if not os.path.isfile(file_name):
        print('"{}" does not exist'.format(file_name), file=sys.stderr)
        sys.exit(-1)

    process_pcap(file_name)
    sys.exit(0)