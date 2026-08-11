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

       Targeted Port Scanner
       Mode : Common & Important Ports
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
#
# port : (service, category, exploit hint, risk)
# =========================

PORT_INFO = {

    # Remote Access
    21: ("FTP", "Remote access", "Anonymous login / brute-force", "HIGH"),
    22: ("SSH", "Remote access", "Brute-force / weak credentials", "MED"),
    23: ("Telnet", "Remote access", "Cleartext credentials", "HIGH"),
    2222: ("SSH-ALT", "Remote access", "Alternative SSH service", "MED"),
    3389: ("RDP", "Remote access", "Remote access exposure", "HIGH"),
    5900: ("VNC", "Remote access", "Authentication exposure", "HIGH"),

    # Web
    80: ("HTTP", "Web service", "Web vulnerabilities", "MED"),
    443: ("HTTPS", "Web service", "Web vulnerabilities", "MED"),
    8000: ("HTTP-DEV", "Web service", "Development server exposure", "MED"),
    8008: ("HTTP-ALT", "Web service", "Admin panels", "MED"),
    8080: ("HTTP-ALT", "Web service", "Admin panels", "MED"),
    8443: ("HTTPS-ALT", "Web service", "Admin consoles", "MED"),
    8888: ("HTTP-ALT", "Web service", "Debug services", "MED"),

    # Windows / AD
    135: ("RPC", "Windows service", "Lateral movement", "HIGH"),
    139: ("NetBIOS", "Windows service", "SMB exposure", "HIGH"),
    445: ("SMB", "Windows service", "SMB security exposure", "CRITICAL"),
    389: ("LDAP", "Directory service", "User enumeration", "HIGH"),
    636: ("LDAPS", "Directory service", "Directory exposure", "MED"),
    3268: ("GC", "Directory service", "Forest enumeration", "MED"),

    # Mail
    25: ("SMTP", "Mail service", "Open relay / configuration", "MED"),
    110: ("POP3", "Mail service", "Cleartext credentials", "HIGH"),
    143: ("IMAP", "Mail service", "Cleartext credentials", "HIGH"),
    465: ("SMTPS", "Mail service", "Configuration issues", "MED"),
    587: ("SMTP-SUB", "Mail service", "Credential abuse", "MED"),
    993: ("IMAPS", "Mail service", "Credential abuse", "MED"),
    995: ("POP3S", "Mail service", "Credential abuse", "MED"),

    # Databases
    1433: ("MSSQL", "Database", "Database exposure", "HIGH"),
    1521: ("Oracle", "Database", "Default credentials", "HIGH"),
    2049: ("NFS", "File sharing", "Unauthorized file access", "HIGH"),
    3306: ("MySQL", "Database", "Weak credentials", "HIGH"),
    5432: ("PostgreSQL", "Database", "Weak credentials", "HIGH"),
    6379: ("Redis", "Database", "Unauthenticated access", "CRITICAL"),
    27017: ("MongoDB", "Database", "Authentication misconfiguration", "CRITICAL"),
    9200: ("Elastic", "Database", "Data exposure", "HIGH"),

    # Containers / DevOps
    2375: ("Docker", "Container service", "Docker API exposure", "CRITICAL"),
    2376: ("DockerTLS", "Container service", "TLS configuration", "MED"),
    6443: ("K8s API", "Orchestration", "Kubernetes API exposure", "CRITICAL"),
    10250: ("Kubelet", "Orchestration", "Kubelet exposure", "CRITICAL"),

    # Network / Infrastructure
    53: ("DNS", "Network service", "Zone transfer", "MED"),
    69: ("TFTP", "Network service", "Configuration disclosure", "HIGH"),
    123: ("NTP", "Network service", "NTP exposure", "LOW"),
    161: ("SNMP", "Network service", "Information disclosure", "HIGH"),
}


# =========================
# Output File
# =========================

output_file = f"scan_{target}.txt"

file = open(output_file, "w", encoding="utf-8")


# =========================
# Output Header
# =========================

header = (
    "PORT     STATE  SERVICE        CATEGORY            SECURITY HINT\n"
    "--------------------------------------------------------------------------\n"
)

print(header)
file.write(header)


# =========================
# Scan Logic
# =========================

for port, info in PORT_INFO.items():

    service, category, exploit, risk = info

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(0.5)

    result = sock.connect_ex(
        (target, port)
    )

    if result == 0:

        line = (
            f"{port:<8} "
            f"open   "
            f"{service:<14} "
            f"{category:<18} "
            f"{exploit}"
        )

        # Color output according to risk
        if risk in ["CRITICAL", "HIGH"]:
            print(f"{RED}{line}{RESET}")

        elif risk == "MED":
            print(f"{YELLOW}{line}{RESET}")

        else:
            print(f"{GREEN}{line}{RESET}")

        file.write(line + "\n")

    sock.close()


# =========================
# Finish
# =========================

file.close()

print("\n[✓] Scan completed")
print(f"[✓] Results saved to {output_file}")
