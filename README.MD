# 🛡️ HomeProtector

**HomeProtector** is a local-first security and monitoring toolkit for home environments.
It passively observes wireless activity and uses local LLM analysis to detect anomalies, unknown devices, and potential threats.

---

## 🚀 Current Module: Bluetooth Analyzer

The Bluetooth Analyzer continuously scans nearby devices and produces intelligent daily summaries.

### Features

* ⏱️ Automatic scanning (cron/systemd)
* 📡 Device discovery (MAC + name)
* 📊 Frequency tracking (how often devices appear)
* 🧠 LLM-powered analysis (local)
* 🔒 Local-first (no cloud required)

---

## 🧠 Example Output

```
Summary:
12 unique devices detected. 3 persistent devices likely belong to the household.

Top devices:
- AA:BB:CC (iPhone) – 54 times
- DD:EE:FF (AirPods) – 49 times

Observations:
- Stable recurring devices → expected environment
- 2 transient devices → likely neighbors or passersby
- 1 unknown device with high frequency → requires attention

Risk level: Medium
```

---

## 🏗️ Architecture

```
bluetooth_analyzer/
 ├── analyzer.py     # main pipeline
 ├── parser.py       # log parsing
 ├── llm.py          # LLM integration
 ├── models.py       # data structures
 └── config.py       # configuration
```

---

## ⚙️ Installation

### 1. System dependencies

```
sudo apt install bluez python3-pip
```

### 2. Install Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

### 3. Python dependencies

```
pip install requests
```

---

## ▶️ Usage

### Run analyzer manually

```
python3 analyzer.py
```

### Schedule scans (cron example)

```
*/15 * * * * /home/$USER/bluetooth_scan.sh
```

### Daily summary

```
0 23 * * * python3 /home/$USER/bluetooth_analyzer/analyzer.py
```

---

## 📁 Output

Logs:

```
~/bluetooth_logs/scan_YYYY-MM-DD.log
```

Summaries:

```
~/bluetooth_logs/summary_YYYY-MM-DD.txt
```

---

## 🧩 Roadmap

### 📶 WiFi Analyzer (next)

* detect nearby networks
* track known vs unknown SSIDs
* monitor channel usage & signal strength
* identify rogue access points

### 🕵️ MITM / Network Inspection (experimental)

* local traffic observation
* ARP anomaly detection
* DNS spoofing detection
* suspicious routing patterns

Note: Active MITM techniques may be illegal depending on jurisdiction.
This project focuses on **defensive detection**, not offensive use.

---

## 🧱 Future Plans

* SQLite storage (history & trends)
* multi-day behavioral analysis
* “new device” alerts
* Telegram / email notifications
* RSSI-based distance estimation
* web dashboard

---

## 🔐 Philosophy

* **Local-first**: your data never leaves your machine
* **Transparent**: logs are readable and auditable
* **Extensible**: modular design
* **Practical**: built for real environments

---

## ⚠️ Limitations

* Bluetooth names can be spoofed
* MAC randomization reduces tracking accuracy
* Passive scanning is not exhaustive
* LLM analysis is heuristic, not guaranteed

---

## 🤝 Contributing

PRs and ideas welcome. Focus areas:

* anomaly detection improvements
* cross-day correlation
* performance optimization
* new analyzers (WiFi, network)

---

## 📌 Vision

HomeProtector evolves into a **personal home SIEM-lite system**:

* awareness of wireless activity around you
* early detection of anomalies
* zero dependency on external services

---
