# tasks.py
import asyncio
import json
import subprocess
from typing import Optional, Dict, Any, List
from datetime import datetime

from broker import broker


def parse_bluescan_output(output: str) -> Dict[str, Any]:
    """
    Parse the textual output from Bluescan.
    
    Bluescan typically outputs information about:
    - BR (Basic Rate) devices
    - LE (Low Energy) devices
    - LMP features
    - SDP services
    - GATT services
    - Vulnerabilities
    
    This parser extracts relevant fields into a structured dictionary.
    """
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "br_devices": [],
        "le_devices": [],
        "raw_output": output,
    }
    
    # Example parsing logic – adjust based on actual Bluescan output format
    lines = output.splitlines()
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if "BR Devices Found" in line:
            current_section = "br"
        elif "LE Devices Found" in line:
            current_section = "le"
        elif current_section == "br" and "BD_ADDR" in line:
            # Extract Bluetooth device address and info
            parts = line.split()
            if len(parts) >= 3:
                result["br_devices"].append({
                    "bd_addr": parts[0],
                    "name": parts[1] if len(parts) > 1 else None,
                    "class": parts[2] if len(parts) > 2 else None,
                })
        elif current_section == "le" and "Address" in line:
            # Extract LE device info
            parts = line.split()
            if len(parts) >= 2:
                result["le_devices"].append({
                    "address": parts[-1],
                    "rssi": parts[0] if parts[0].isdigit() else None,
                })
    
    return result


@broker.task
async def scan_bluetooth_air_state(
    scan_duration: int = 10,
    interface: Optional[str] = None,
    output_format: str = "json"
) -> Dict[str, Any]:
    """
    Taskiq task that runs Bluescan to collect the current Bluetooth "air state".
    
    Args:
        scan_duration: Duration of the scan in seconds.
        interface: Specific HCI interface to use (e.g., "hci0").
        output_format: Desired output format ("json" or "text").
    
    Returns:
        A dictionary containing parsed scan results and metadata.
    """
    cmd = ["bluescan"]
    
    if interface:
        cmd.extend(["-i", interface])
    
    # Add scan duration (Bluescan may not have a direct flag; adjust as needed)
    # cmd.extend(["--timeout", str(scan_duration)])
    
    # Optionally specify output format (if Bluescan supports JSON output)
    # cmd.extend(["--format", output_format])
    
    try:
        # Run Bluescan as a subprocess (async-friendly)
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        # Wait for the scan to complete or timeout
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=scan_duration + 5  # Add a small buffer
        )
        
        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")
        
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(
                proc.returncode, cmd, output=stdout_text, stderr=stderr_text
            )
        
        # Parse and structure the collected data
        scan_data = parse_bluescan_output(stdout_text)
        
        # Include execution metadata
        scan_data.update({
            "scan_duration": scan_duration,
            "interface": interface,
            "success": True,
            "error": None,
        })
        
        # You can optionally store results in a database or send to a webhook here
        # e.g., await store_scan_results(scan_data)
        
        return scan_data
        
    except asyncio.TimeoutError:
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "success": False,
            "error": f"Scan timed out after {scan_duration} seconds",
            "scan_duration": scan_duration,
            "interface": interface,
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "success": False,
            "error": str(e),
            "scan_duration": scan_duration,
            "interface": interface,
        }


@broker.task
async def process_scan_results(scan_data: Dict[str, Any]) -> None:
    """
    Optional post‑processing task (e.g., store in DB, trigger alerts).
    """
    if scan_data.get("success"):
        print(f"[{scan_data['timestamp']}] Found {len(scan_data.get('br_devices', []))} BR devices "
              f"and {len(scan_data.get('le_devices', []))} LE devices")
        # Add your storage/alerting logic here
    else:
        print(f"[{scan_data['timestamp']}] Scan failed: {scan_data.get('error')}")
        