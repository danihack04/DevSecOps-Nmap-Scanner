import sys
import subprocess
from datetime import datetime


def scan_target(target):
    print(f"[+] Iniciando escaneo contra {target}...\n")

    try:
        result = subprocess.run(
            ["nmap", "-sS", "-Pn", target],
            capture_output=True,
            text=True
        )
    except Exception as e:
        print(f"[!] Error ejecutando nmap: {e}")
        sys.exit(1)

    return result.stdout


def extract_open_ports(nmap_output):
    open_ports = []

    for line in nmap_output.split("\n"):
        if "open" in line and "/" in line:
            open_ports.append(line.strip())

    return open_ports


def save_results(target, ports):
    filename = f"scan_{target}.txt"

    with open(filename, "w") as f:
        f.write(f"Scan report for {target}\n")
        f.write(f"Date: {datetime.now()}\n\n")

        if ports:
            f.write("Open ports:\n")
            for port in ports:
                f.write(port + "\n")
        else:
            f.write("No open ports found.\n")

    print(f"\n[+] Resultados guardados en {filename}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scanner.py <IP>")
        sys.exit(1)

    target = sys.argv[1]

    raw_output = scan_target(target)
    open_ports = extract_open_ports(raw_output)

    print("[+] Puertos abiertos:\n")

    if open_ports:
        for port in open_ports:
            print(port)
    else:
        print("No se encontraron puertos abiertos.")

    save_results(target, open_ports)

    if open_ports:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()