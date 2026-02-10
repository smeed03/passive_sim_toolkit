import argparse
import time

from scapy.all import IP, UDP, Raw, send


SSDP_MULTICAST_IP = "239.255.255.250"
SSDP_PORT = 1900


def build_msearch(st: str = "ssdp:all") -> bytes:
    # Minimal SSDP M-SEARCH request (discovery traffic)
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
    ap = argparse.ArgumentParser(description="Simulate LAN discovery traffic (SSDP)")
    ap.add_argument("--mode", choices=["passive", "active"], default="passive")
    ap.add_argument("--seconds", type=int, default=60)

    # Passive: occasional discovery probe
    ap.add_argument("--passive-interval", type=float, default=30.0)

    # Active: bursts of discovery probes (more like “device waking up / scanning”)
    ap.add_argument("--active-burst-size", type=int, default=15)
    ap.add_argument("--active-burst-gap", type=float, default=0.05)   # gap within burst
    ap.add_argument("--active-interval", type=float, default=2.0)     # time between bursts

    ap.add_argument("--st", default="ssdp:all", help="SSDP search target (e.g., ssdp:all)")
    args = ap.parse_args()

    payload = build_msearch(args.st)
    pkt = IP(dst=SSDP_MULTICAST_IP) / UDP(dport=SSDP_PORT, sport=1901) / Raw(load=payload)

    end = time.time() + args.seconds
    sent = 0

    if args.mode == "passive":
        while time.time() < end:
            send(pkt, verbose=False)
            sent += 1
            time.sleep(args.passive_interval)
    else:
        while time.time() < end:
            for _ in range(args.active_burst_size):
                send(pkt, verbose=False)
                sent += 1
                time.sleep(args.active_burst_gap)
            time.sleep(args.active_interval)

    print(f"Done. Sent {sent} SSDP packets. mode={args.mode}")


if __name__ == "__main__":
    main()
