from datetime import datetime


request_logs = []


def detect_attack(path):
    """
    Detect common attack patterns.
    """

    path = path.lower()

    if "/wp-admin" in path:
        return "High", "WordPress Scan"

    elif "/phpmyadmin" in path:
        return "High", "phpMyAdmin Scan"

    elif "/.env" in path:
        return "High", ".env File Probe"

    elif "union" in path or "select" in path or "or%201=1" in path:
        return "High", "SQL Injection"

    elif "<script>" in path or "%3cscript%3e" in path:
        return "High", "XSS Attempt"

    elif "../" in path or "..%2f" in path:
        return "High", "Directory Traversal"

    else:
        return "Low", "Normal Request"


def log_request(ip, method, path, user_agent):

    risk, attack = detect_attack(path)

    request_logs.append({

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "ip": ip,

        "method": method,

        "path": path,

        "user_agent": user_agent,

        "risk": risk,

        "attack": attack

    })


def get_statistics():

    total_requests = len(request_logs)

    high_risk = sum(
        1 for log in request_logs
        if log["risk"] == "High"
    )

    unique_ips = len(
        set(log["ip"] for log in request_logs)
    )

    wordpress_scans = sum(
        1 for log in request_logs
        if log["attack"] == "WordPress Scan"
    )

    return {
        "total_requests": total_requests,
        "high_risk": high_risk,
        "unique_ips": unique_ips,
        "wordpress_scans": wordpress_scans
    }