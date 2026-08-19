from app.database import (
    get_recent_requests,
    get_attack_logs,
    get_attack_summary,
    get_security_stats
)

from app.data.security_logs import (
    login_logs,
    attack_logs,
    security_stats
)

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

ADMIN_ACCOUNT = {
    "username": "admin",
    "password": "AetherisAdmin@2026"
}


# ============================================================
# ADMIN LOGIN
# ============================================================

@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_ACCOUNT["username"]
            and
            password == ADMIN_ACCOUNT["password"]
        ):

            session["admin"] = username

            return redirect(
                url_for("admin.dashboard")
            )

        return render_template(
            "admin/login.html",
            error="Invalid administrator credentials."
        )

    return render_template(
        "admin/login.html"
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@admin_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:

        return redirect(
            url_for("admin.login")
        )

    # Get security statistics
    stats = get_security_stats()

    # Get real attack events from SQLite
    real_attack_logs = get_attack_logs(100)

    # Get attack counts grouped by attack type
    attack_summary = get_attack_summary()

    return render_template(
        "admin/dashboard.html",

        login_logs=login_logs,

        attack_logs=real_attack_logs,

        security_stats=stats,

        attack_summary=attack_summary
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@admin_bp.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(
        url_for("admin.login")
    )


# ============================================================
# LIVE REQUEST MONITOR
# ============================================================

@admin_bp.route("/monitor")
def monitor():

    if "admin" not in session:

        return redirect(
            url_for("admin.login")
        )

    # --------------------------------------------------------
    # Get the latest 100 requests from SQLite
    # --------------------------------------------------------

    database_logs = get_recent_requests(100)

    # --------------------------------------------------------
    # Calculate risk statistics
    # --------------------------------------------------------

    high_risk = sum(
        1
        for log in database_logs
        if log["risk"] == "High"
    )

    medium_risk = sum(
        1
        for log in database_logs
        if log["risk"] == "Medium"
    )

    normal_requests = sum(
        1
        for log in database_logs
        if log["risk"] == "Low"
    )


    # --------------------------------------------------------
    # Send database records to monitor.html
    # --------------------------------------------------------

    return render_template(
        "admin/monitor.html",

        request_logs=database_logs,

        high_risk=high_risk,

        medium_risk=medium_risk,

        normal_requests=normal_requests
    )

