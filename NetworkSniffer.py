from code import interact
from scapy.all import sniff, Ether, IP, TCP, UDP, Raw

def packet_callback(packet):
    # Check if the packet has an IP layer
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        proto = packet[IP].proto

        print(f"IP Packet: {ip_src} -> {ip_dst}")

        # Check if the packet has a TCP layer
        if TCP in packet:
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            print(f"TCP Segment: {ip_src}:{tcp_sport} -> {ip_dst}:{tcp_dport}")

            # Check if the packet has a Raw layer (payload)
            if Raw in packet:
                payload = packet[Raw].load
                print(f"Payload: {payload}")

        # Check if the packet has a UDP layer
        elif UDP in packet:
            udp_sport = packet[UDP].sport
            udp_dport = packet[UDP].dport
            print(f"UDP Segment: {ip_src}:{udp_sport} -> {ip_dst}:{udp_dport}")

            # Check if the packet has a Raw layer (payload)
            if Raw in packet:
                payload = packet[Raw].load
                print(f"Payload: {payload}")

    # Check if the packet has an Ethernet layer
    elif Ether in packet:
        eth_src = packet[Ether].src
        eth_dst = packet[Ether].dst
        print(f"Ethernet Frame: {eth_src} -> {eth_dst}")

    print("-" * 40)

def start_sniffing(interface=None):
    print("Starting packet sniffer...")
    # Start sniffing packets
    sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    # Specify the network interface to sniff on (e.g., 'eth0', 'wlan0')
    # If None, scapy will use the default interface
    start_sniffing(interact)