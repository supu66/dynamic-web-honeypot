from app.security.logger import request_logs
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


@admin_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(
            url_for("admin.login")
        )

    return render_template(
        "admin/dashboard.html",
        login_logs=login_logs,
        attack_logs=attack_logs,
        security_stats=security_stats
    )


@admin_bp.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(
        url_for("admin.login")
    )

@admin_bp.route("/monitor")
def monitor():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    return render_template(
        "admin/monitor.html",
        request_logs=request_logs
    )
