import re
from collections import defaultdict
from app.models import Device

DEVICE_REGEX = re.compile(r"Device ([0-9A-F:]{17}) (.+)")

def parse_log(file_path: str):
    devices = defaultdict(int)
    names = {}

    with open(file_path, "r") as f:
        for line in f:
            match = DEVICE_REGEX.search(line)
            if match:
                mac, name = match.groups()
                devices[mac] += 1
                names[mac] = name

    return [
        Device(mac=mac, name=names.get(mac, "Unknown"), count=count)
        for mac, count in devices.items()
    ]
