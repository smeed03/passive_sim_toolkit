import argparse
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt


def make_payload(mode: str) -> dict:
    payload = {
        "device": "simulated_iot",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "mode": mode,
        "temperature_c": round(20 + random.random() * 3, 2),
        "humidity": round(35 + random.random() * 10, 2),
    }

    if mode == "active":
        payload.update({
            "event": random.choice(
                ["user_command", "state_change", "interaction"]
            ),
            "target_temperature_c": round(21 + random.random() * 3, 1),
        })

    return payload


def main():
    parser = argparse.ArgumentParser(description="MQTT traffic simulator")
    parser.add_argument("--host", required=True, help="MQTT broker host (WSL IP)")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--topic", default="dams/sim/telemetry")
    parser.add_argument("--mode", choices=["passive", "active"], default="passive")
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--passive-interval", type=float, default=5.0)
    parser.add_argument("--active-interval", type=float, default=0.3)
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()

    interval = (
        args.passive_interval
        if args.mode == "passive"
        else args.active_interval
    )

    end_time = time.time() + args.seconds
    sent = 0

    while time.time() < end_time:
        payload = make_payload(args.mode)
        client.publish(
            args.topic,
            json.dumps(payload),
            qos=0,
            retain=False,
        )
        sent += 1
        time.sleep(interval)

    client.loop_stop()
    client.disconnect()

    print(
        f"Done. Sent {sent} messages "
        f"to mqtt://{args.host}:{args.port} "
        f"topic={args.topic} mode={args.mode}"
    )


if __name__ == "__main__":
    main()
