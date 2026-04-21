import os
from datetime import datetime
from app.parser import parse_log
from app.llm import generate_summary
from app.config import LOG_DIR, MODEL, SUMMARY_TEMPLATE


def format_devices(devices):
    lines = []
    for d in sorted(devices, key=lambda x: x.count, reverse=True):
        lines.append(f"{d.count}x {d.mac} ({d.name})")
    return "\n".join(lines)


def main():
    today = datetime.now().strftime("%Y-%m-%d")

    log_file = os.path.join(LOG_DIR, f"scan_{today}.log")
    summary_file = os.path.join(LOG_DIR, f"summary_{today}.txt")

    if not os.path.exists(log_file):
        print("No log file for today")
        return

    devices = parse_log(log_file)
    formatted = format_devices(devices)

    prompt = SUMMARY_TEMPLATE.format(data=formatted)

    summary = generate_summary(prompt, MODEL)

    with open(summary_file, "w") as f:
        f.write(summary)

    print(f"Saved summary: {summary_file}")


if __name__ == "__main__":
    main()
