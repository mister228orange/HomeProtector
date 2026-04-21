from dataclasses import dataclass

@dataclass
class Device:
    mac: str
    name: str
    count: int
