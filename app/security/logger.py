from datetime import datetime
from urllib.parse import unquote
from app.database import get_connection

LOG_FILE = "honeypot.log"


# In-memory request history
# Used by the Admin Live Monitor.
request_logs = []


def detect_attack(path, user_agent=""):
    """
    Detect common web attack patterns.
    Returns:
        (risk_level, attack_type)
    """

    # Decode URL-encoded characters before checking for attacks
    path = unquote(path).lower()
    user_agent = unquote(user_agent).lower()

    # --------------------------------
    # HIGH RISK — SQL INJECTION
    # --------------------------------

    if any(x in path for x in [
        "union select",
        "union+select",
        "select ",
        "or 1=1",
        "or+1=1",
        "and 1=1",
        "' or '1'='1",
        "' or 1=1",
        "'--",
        "information_schema",
        "sleep(",
        "benchmark(",
        "xp_cmdshell",
        "into outfile",
        "into dumpfile"
    ]):
        return "High", "SQL Injection"

    # --------------------------------
    # HIGH RISK — CROSS SITE SCRIPTING
    # --------------------------------

    elif any(x in path for x in [
        "<script",
        "</script>",
        "javascript:",
        "alert(",
        "prompt(",
        "confirm(",
        "onerror=",
        "onload=",
        "onclick=",
        "onmouseover="
    ]):
        return "High", "Cross Site Scripting"

    # --------------------------------
    # HIGH RISK — DIRECTORY TRAVERSAL
    # --------------------------------

    elif any(x in path for x in [
        "../",
        "..\\",
        "..%2f",
        "..%5c",
        "etc/passwd",
        "etc/shadow",
        "windows/system32",
        "boot.ini"
    ]):
        return "High", "Directory Traversal"

    # --------------------------------
    # HIGH RISK — COMMAND INJECTION
    # --------------------------------

    elif any(x in path for x in [
        "cmd.exe",
        "powershell",
        "whoami",
        "wget ",
        "curl ",
        "&&",
        "||",
        "|",
        ";"
    ]):
        return "High", "Command Injection"

    # --------------------------------
    # HIGH RISK — SENSITIVE FILE PROBE
    # --------------------------------

    elif any(x in path for x in [
        ".env",
        ".git/",
        ".git/config",
        "config.php",
        "database.sql",
        "backup.zip",
        "backup.sql",
        "wp-config.php",
        "id_rsa",
        ".htpasswd"
    ]):
        return "High", "Sensitive File Probe"

    # --------------------------------
    # HIGH RISK — WORDPRESS SCAN
    # --------------------------------

    elif any(x in path for x in [
        "/wp-admin",
        "/wp-login",
        "/xmlrpc.php",
        "/wp-content/",
        "/wp-includes/"
    ]):
        return "High", "WordPress Scan"

    # --------------------------------
    # HIGH RISK — PHPMYADMIN SCAN
    # --------------------------------

    elif any(x in path for x in [
        "/phpmyadmin",
        "/phpmyadmin/",
        "/pma"
    ]):
        return "High", "phpMyAdmin Scan"

    # --------------------------------
    # HIGH RISK — WEB SHELL PROBE
    # --------------------------------

    elif any(x in path for x in [
        "shell.php",
        "cmd.php",
        "webshell",
        "c99.php",
        "r57.php"
    ]):
        return "High", "Web Shell Probe"

    # --------------------------------
    # MEDIUM RISK — ADMIN ENUMERATION
    # --------------------------------

    elif any(x in path for x in [
        "/admin",
        "/administrator",
        "/login.php",
        "/signin",
        "/cpanel",
        "/webmail"
    ]):
        return "Medium", "Admin Enumeration"

    # --------------------------------
    # MEDIUM RISK — SECURITY SCANNER
    # --------------------------------

    elif any(x in user_agent for x in [
        "sqlmap",
        "nikto",
        "nmap",
        "masscan",
        "dirbuster",
        "gobuster",
        "burpsuite",
        "zaproxy",
        "wpscan",
        "curl",
        "wget",
        "python-requests"
    ]):
        return "Medium", "Security Scanner"


    # File Upload Honeypot
    elif "/upload" in path or "/file-upload" in path:
        return "High", "File Upload Probe"
    
    # Suspicious file upload probing
    elif any(x in path for x in [
        "shell.php",
        "cmd.php",
        "webshell.php",
        "backdoor.php",
        "malware.exe",
        "ransomware.exe",
        ".php",
        ".phtml",
        ".jsp",
        ".asp",
        ".aspx"
    ]):
        return "High", "Suspicious File Upload"

    return "Low", "Normal Request"


def log_request(ip, method, path, user_agent):
    """
    Record an incoming HTTP request.

    The request is:
    1. Classified by detect_attack()
    2. Added to the in-memory request_logs list
    3. Written to honeypot.log
    """

    risk, attack = detect_attack(path, user_agent)

    # Create structured log entry for Live Monitor
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip or "Unknown",
        "method": method,
        "path": path,
        "risk": risk,
        "attack": attack,
        "user_agent": user_agent or "Unknown"
    }

    # Add newest request to memory
    request_logs.append(log_entry)

    # Prevent unlimited memory growth
    # Keep the latest 500 requests.
    if len(request_logs) > 500:
        request_logs.pop(0)

    # Also save request to honeypot.log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{log_entry['time']}] "
            f"IP={log_entry['ip']} | "
            f"METHOD={log_entry['method']} | "
            f"PATH={log_entry['path']} | "
            f"RISK={log_entry['risk']} | "
            f"ATTACK={log_entry['attack']} | "
            f"USER_AGENT={log_entry['user_agent']}\n"
        )

    # Save request permanently to SQLite
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO request_logs (
            timestamp,
            ip,
            method,
            path,
            risk,
            attack,
            user_agent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        log_entry["time"],
        log_entry["ip"],
        log_entry["method"],
        log_entry["path"],
        log_entry["risk"],
        log_entry["attack"],
        log_entry["user_agent"]
    ))

    connection.commit()
    connection.close()
    
def get_security_stats():
    """
    Calculate security statistics from captured requests.
    """

    attacks_today = len(request_logs)

    suspicious_ips = len({
        log["ip"]
        for log in request_logs
        if log["risk"] in ["High", "Medium"]
    })

    high_risk = sum(
        1
        for log in request_logs
        if log["risk"] == "High"
    )

    honeypot_hits = sum(
        1
        for log in request_logs
        if log["attack"] != "Normal Request"
    )

    return {
        "attacks_today": attacks_today,
        "suspicious_ips": suspicious_ips,
        "high_risk": high_risk,
        "honeypot_hits": honeypot_hits
    }

def get_attack_logs():
    """
    Return only requests classified as actual attacks.
    """

    return [
        log
        for log in request_logs
        if log["attack"] != "Normal Request"
    ]

def get_attack_summary():
    """
    Count detected attacks by attack type.
    """

    summary = {}

    for log in request_logs:

        attack = log["attack"]

        if attack == "Normal Request":
            continue

        if attack not in summary:
            summary[attack] = 0

        summary[attack] += 1

    return summary
