import ipaddress
import sys
import argparse


def prefix_diff(a: bytes, b: bytes) -> int:
    same_bits = 0
    last_i = None
    for i in range(4):
        last_i = i
        if a[i] != b[i]:
            break
        same_bits += 8

    if same_bits < 32:
        n = a[last_i] ^ b[last_i]
        for i in reversed(range(8)):
            if n & (1 << i) != 0:
                break
            same_bits += 1
    return 32 - same_bits


net_list = []

parser = argparse.ArgumentParser(description=f"Merge IP addresses from stdin into subnets with a given maximum prefix")

parser.add_argument('--max-prefix', type=int, action='store', required=False, help="max subnet prefix", default=24)
args = parser.parse_args()

for line in sys.stdin.readlines():
    try:
        a = ipaddress.ip_address(line.strip())
    except:
        print(f"{line} is not valid IP address", file=sys.stderr)
        continue
    found = False
    if len(net_list) > 0:
        for i in range(len(net_list)):
            n = net_list[i]
            if a in n:
                found = True
                break
            na = n.network_address
            pd = prefix_diff(a.packed, na.packed)
            if pd > 32 - args.max_prefix:
                continue
            n = n.supernet(pd + n.prefixlen - 32)
            if n.prefixlen < args.max_prefix:
                continue
            net_list[i] = n
            found = True
            break
    if not found:
        net_list.append(ipaddress.ip_network(a))

for n in net_list:
    print(n.compressed)
