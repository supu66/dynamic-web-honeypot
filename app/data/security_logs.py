login_logs = [
    {"time": "09:11", "event": "Login Successful", "status": "Success"},
    {"time": "09:43", "event": "Dashboard Viewed", "status": "Info"},
    {"time": "10:05", "event": "Documents Accessed", "status": "Info"},
    {"time": "10:22", "event": "Failed Login Attempt", "status": "Failed"},
    {"time": "11:15", "event": "Session Expired", "status": "Warning"},
]

attack_logs = [
    {
        "ip": "185.77.18.44",
        "attack": "SQL Injection",
        "risk": "HIGH",
        "status": "Blocked",
    },
    {
        "ip": "103.91.44.21",
        "attack": "Brute Force",
        "risk": "MEDIUM",
        "status": "Monitoring",
    },
    {
        "ip": "45.88.20.111",
        "attack": "XSS Attempt",
        "risk": "HIGH",
        "status": "Blocked",
    },
    {
        "ip": "192.168.1.18",
        "attack": "Normal Login",
        "risk": "LOW",
        "status": "Allowed",
    },

]

security_stats = {
    "attacks_today": 19,
    "suspicious_ips": 7,
    "high_risk": 3,
    "honeypot_hits": 42
}