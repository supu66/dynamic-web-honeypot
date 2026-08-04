from datetime import datetime

LOG_FILE = "honeypot.log"


def detect_attack(path, user_agent=""):
    """
    Detect common web attacks.
    """

    path = path.lower()
    user_agent = user_agent.lower()

    # WordPress
    if any(x in path for x in [
        "/wp-admin",
        "/wp-login",
        "/xmlrpc.php"
    ]):
        return "High", "WordPress Scan"

    # phpMyAdmin
    elif any(x in path for x in [
        "/phpmyadmin",
        "/pma"
    ]):
        return "High", "phpMyAdmin Scan"

    # Sensitive Files
    elif any(x in path for x in [
        ".env",
        ".git",
        "config.php",
        "database.sql",
        "backup.zip"
    ]):
        return "High", "Sensitive File Probe"

    # SQL Injection
    elif any(x in path for x in [
        "union",
        "select",
        "or 1=1",
        "or%201=1",
        "'--",
        "information_schema"
    ]):
        return "High", "SQL Injection"

    # Cross Site Scripting
    elif any(x in path for x in [
        "<script>",
        "%3cscript%3e",
        "alert(",
        "onerror="
    ]):
        return "High", "Cross Site Scripting"

    # Directory Traversal
    elif any(x in path for x in [
        "../",
        "..%2f",
        "..\\",
        "etc/passwd"
    ]):
        return "High", "Directory Traversal"

    # Command Injection
    elif any(x in path for x in [
        ";",
        "&&",
        "|",
        "cmd.exe",
        "whoami"
    ]):
        return "High", "Command Injection"

    # Web Shell
    elif any(x in path for x in [
        "shell.php",
        "cmd.php",
        "webshell"
    ]):
        return "High", "Web Shell Probe"

    # Admin Enumeration
    elif any(x in path for x in [
        "/admin",
        "/administrator",
        "/login.php"
    ]):
        return "Medium", "Admin Enumeration"

    # Security Scanners
    elif any(x in user_agent for x in [
        "sqlmap",
        "nikto",
        "curl",
        "wget",
        "python-requests"
    ]):
        return "Medium", "Security Scanner"

    return "Low", "Normal Request"


def log_request(ip, method, path, user_agent):

    risk, attack = detect_attack(path, user_agent)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now()}] "
            f"IP={ip} | "
            f"METHOD={method} | "
            f"PATH={path} | "
            f"RISK={risk} | "
            f"ATTACK={attack} | "
            f"USER_AGENT={user_agent}\n"
        )