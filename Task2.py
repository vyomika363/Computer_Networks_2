from mininet.net import Mininet
from mininet.node import Controller, OVSController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import time
import re
import os

def extract_domains(pcap_file):
    """Extracting domain names from a text-style PCAP file."""
    domains = []
    if not os.path.exists(pcap_file):
        print(f"[WARN] File not found: {pcap_file}")
        return domains

    with open(pcap_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Look for typical domain patterns
            match = re.search(r'([a-zA-Z0-9\-\.]+\.[a-z]{2,})', line)
            if match:
                domains.append(match.group(1))
    return list(set(domains))  # Return only unique domains

def resolve_and_measure(host, domains):
    """Perform DNS lookups using the host's default resolver."""
    success, fail = 0, 0
    total_time = 0.0

    for domain in domains:
        start = time.time()
        result = host.cmd(f'dig +short {domain}')
        latency = time.time() - start

        if result.strip():
            success += 1
            total_time += latency
        else:
            fail += 1

    avg_latency = total_time / success if success else 0
    throughput = success / total_time if total_time > 0 else 0

    return avg_latency, throughput, success, fail

def main():
    # Connect to existing Mininet network (already started with topology_1.py)
    net = Mininet(controller=OVSController, link=TCLink)
    net.start()

    # Folder where your shared files are (adjust name if needed)
    pcap_dir = "/media/sf_pcap_files"

    # Mapping of host to its respective PCAP file
    host_pcap_map = {
        'h1': 'PCAP_1_H1',
        'h2': 'PCAP_2_H2',
        'h3': 'PCAP_3_H3',
        'h4': 'PCAP_4_H4'
    }

    for hname, fname in host_pcap_map.items():
        host = net.get(hname)
        pcap_path = os.path.join(pcap_dir, fname)

        print(f"\n[INFO] Processing {hname} using {pcap_path}")
        domains = extract_domains(pcap_path)

        if not domains:
            print(f"[WARN] No domains found for {hname}. Skipping.")
            continue

        avg_latency, throughput, success, fail = resolve_and_measure(host, domains)

        print(f"\n=== {hname.upper()} Results ===")
        print(f"Average Latency: {avg_latency:.3f} s")
        print(f"Throughput: {throughput:.2f} queries/sec")
        print(f"Successful: {success}, Failed: {fail}")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()
