import socket
from datetime import datetime

# =========================
# Colors (ANSI)
# =========================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# =========================
# Banner
# =========================
banner = r"""
██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝   ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║
██║     ╚██████╔╝██║  ██║   ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝

   Targeted Port Scanner (nmap-style)
   Mode : Common & Important Ports Only
   Use  : Educational / Lab Purpose
"""
print(banner)

# =========================
# Target Input
# =========================
target = input("Enter target IP: ").strip()
print(f"\n[*] Starting scan on {target}")
print(f"[*] Scan time: {datetime.now()}\n")

# =========================
# Port Information
# port : (service, category, exploit hint, risk)
# =========================
PORT_INFO = {
    # Remote Access
    21:   ("FTP", "Remote access", "Anonymous login / brute-force", "HIGH"),
    22:   ("SSH", "Remote access", "Brute-force / weak creds", "MED"),
    23:   ("Telnet", "Remote access", "Cleartext credentials", "HIGH"),
    2222: ("SSH-ALT", "Remote access", "Hidden SSH service", "MED"),
    3389: ("RDP", "Remote access", "BlueKeep / brute-force", "HIGH"),
    5900: ("VNC", "Remote access", "No authentication", "HIGH"),

    # Web
    80:   ("HTTP", "Web service", "Web vulnerabilities", "MED"),
    443:  ("HTTPS", "Web service", "Web vulnerabilities", "MED"),
    8000: ("HTTP-DEV", "Web service", "Dev server exposure", "MED"),
    8008: ("HTTP-ALT", "Web service", "Admin panels", "MED"),
    8080: ("HTTP-ALT", "Web service", "Admin panels", "MED"),
    8443: ("HTTPS-ALT", "Web service", "Admin consoles", "MED"),
    8888: ("HTTP-ALT", "Web service", "Debug services", "MED"),

    # Windows / AD
    135:  ("RPC", "Windows service", "Lateral movement", "HIGH"),
    139:  ("NetBIOS", "Windows service", "SMB relay", "HIGH"),
    445:  ("SMB", "Windows service", "EternalBlue (MS17-010)", "CRITICAL"),
    389:  ("LDAP", "Directory service", "User enumeration", "HIGH"),
    636:  ("LDAPS", "Directory service", "AD attacks", "MED"),
    3268: ("GC", "Directory service", "Forest enumeration", "MED"),

    # Mail
    25:   ("SMTP", "Mail service", "Open relay", "MED"),
    110:  ("POP3", "Mail service", "Cleartext creds", "HIGH"),
    143:  ("IMAP", "Mail service", "Cleartext creds", "HIGH"),
    465:  ("SMTPS", "Mail service", "Misconfiguration", "MED"),
    587:  ("SMTP-SUB", "Mail service", "Credential abuse", "MED"),
    993:  ("IMAPS", "Mail service", "Credential abuse", "MED"),
    995:  ("POP3S", "Mail service", "Credential abuse", "MED"),

    # Databases
    1433: ("MSSQL", "Database", "xp_cmdshell abuse", "HIGH"),
    1521: ("Oracle", "Database", "Default credentials", "HIGH"),
    2049: ("NFS", "File sharing", "No authentication", "HIGH"),
    3306: ("MySQL", "Database", "Weak credentials", "HIGH"),
    5432: ("PostgreSQL", "Database", "Weak credentials", "HIGH"),
    6379: ("Redis", "Database", "Unauthenticated RCE", "CRITICAL"),
    27017:("MongoDB", "Database", "No authentication", "CRITICAL"),
    9200: ("Elastic", "Database", "Data exposure", "HIGH"),

    # Containers / DevOps
    2375: ("Docker", "Container service", "Root takeover", "CRITICAL"),
    2376: ("DockerTLS", "Container service", "TLS misconfig", "MED"),
    6443: ("K8s API", "Orchestration", "Cluster takeover", "CRITICAL"),
    10250:("Kubelet", "Orchestration", "Remote code execution", "CRITICAL"),

    # Network / Infra
    53:   ("DNS", "Network service", "Zone transfer", "MED"),
    69:   ("TFTP", "Network service", "Config leak", "HIGH"),
    123:  ("NTP", "Network service", "Amplification", "LOW"),
    161:  ("SNMP", "Network service", "Information disclosure", "HIGH"),
}

# =========================
# Output File (nmap-style)
# =========================
output_file = f"scan_{target}.txt"
file = open(output_file, "w")

header = (
    "PORT     STATE  SERVICE        CATEGORY            EXPLOIT HINT\n"
    "--------------------------------------------------------------------------\n"
)
print(header)
file.write(header)

# =========================
# Scan Logic
# =========================
for port, info in PORT_INFO.items():
    service, category, exploit, risk = info

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    if s.connect_ex((target, port)) == 0:
        line = f"{port:<8} open   {service:<14} {category:<18} {exploit}"

        # Color by risk
        if risk in ["CRITICAL", "HIGH"]:
            print(f"{RED}{line}{RESET}")
        else:
            print(f"{GREEN}{line}{RESET}")

        file.write(line + "\n")

    s.close()

file.close()

print(f"\n[✓] Scan completed")
print(f"[✓] Results saved to {output_file}")
