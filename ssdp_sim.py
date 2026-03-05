import argparse
import time

from scapy.all import Ether, IP, UDP, Raw, sendp


SSDP_MULTICAST_IP = "239.255.255.250"
SSDP_PORT = 1900

SSDP_MULTICAST_MAC = "01:00:5e:7f:ff:fa"


def build_msearch(st: str = "ssdp:all") -> bytes:
    msg = (
        "M-SEARCH * HTTP/1.1\r\n"
        f"HOST: {SSDP_MULTICAST_IP}:{SSDP_PORT}\r\n"
        'MAN: "ssdp:discover"\r\n'
        "MX: 1\r\n"
        f"ST: {st}\r\n"
        "\r\n"
    )
    return msg.encode("ascii")


def main():
    ap = argparse.ArgumentParser(description="Simulate LAN discovery traffic (SSDP) via L2 sendp")
    ap.add_argument("--iface", required=True, help='Interface name (ex: "Intel(R) Wi-Fi 6 AX201 160MHz")')
    ap.add_argument("--mode", choices=["passive", "active"], default="passive")
    ap.add_argument("--seconds", type=int, default=10)
    ap.add_argument("--passive-interval", type=float, default=2.0)
    ap.add_argument("--active-burst-size", type=int, default=20)
    ap.add_argument("--active-burst-gap", type=float, default=0.05)
    ap.add_argument("--active-interval", type=float, default=1.0)
    ap.add_argument("--st", default="ssdp:all")
    args = ap.parse_args()

    payload = build_msearch(args.st)

    pkt = (
        Ether(dst=SSDP_MULTICAST_MAC)
        / IP(dst=SSDP_MULTICAST_IP)
        / UDP(dport=SSDP_PORT, sport=1901)
        / Raw(load=payload)
    )

    end = time.time() + args.seconds
    sent = 0

    if args.mode == "passive":
        while time.time() < end:
            sendp(pkt, iface=args.iface, verbose=False)
            sent += 1
            time.sleep(args.passive_interval)
    else:
        while time.time() < end:
            for _ in range(args.active_burst_size):
                sendp(pkt, iface=args.iface, verbose=False)
                sent += 1
                time.sleep(args.active_burst_gap)
            time.sleep(args.active_interval)

    print(f"Done. Sent {sent} SSDP packets via sendp on iface='{args.iface}'. mode={args.mode}")


if __name__ == "__main__":
    main()