import os
from app.data.employees import employees
from app.security.logger import log_request
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

EMPLOYEE_ACCOUNT = {

    "username": "employee",

    "password": "Aetheris@2026"

}

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template(
        "pages/home.html"
    )


@main_bp.route("/about")
def about():
    return render_template(
        "pages/about.html"
    )


@main_bp.route("/services")
def services():
    return render_template(
        "pages/services.html"
    )


@main_bp.route("/careers")
def careers():
    return render_template(
        "pages/careers.html"
    )


@main_bp.route("/contact")
def contact():
    return render_template(
        "pages/contact.html"
    )


@main_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == EMPLOYEE_ACCOUNT["username"]
            and
            password == EMPLOYEE_ACCOUNT["password"]
        ):

            session["employee"] = username

            return redirect(
                url_for("main.dashboard")
            )

        return render_template(
            "pages/login.html",
            error="Invalid username or password."
        )

    return render_template(
        "pages/login.html"
    )


@main_bp.route("/dashboard")
def dashboard():

    if "employee" not in session:

        return redirect(
            url_for("main.login")
        )

    return render_template(
        "pages/dashboard.html",
        login_logs=login_logs,
        attack_logs=attack_logs,
        security_stats=security_stats
    )



@main_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("main.login")
    )

@main_bp.route("/documents")
def documents():

    if "employee" not in session:
        return redirect(url_for("main.login"))

    return render_template(
        "pages/documents.html"
    )

@main_bp.route("/directory")
def directory():

    if "employee" not in session:
        return redirect(url_for("main.login"))


    return render_template(
        "pages/directory.html",
        employees=employees
    )

@main_bp.route("/wp-admin")
def fake_wp_admin():

    return render_template(
        "pages/fake_wp_admin.html"
    )

@main_bp.route("/phpmyadmin")
def fake_phpmyadmin():

    return render_template(
        "pages/fake_phpmyadmin.html"
    )

@main_bp.route("/upload", methods=["GET", "POST"])
def fake_upload():

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if uploaded_file is None:
            return render_template(
                "pages/fake_upload.html",
                error="No file was submitted."
            )

        filename = uploaded_file.filename or "Unknown"

        return render_template(
            "pages/fake_upload.html",
            message=(
                f"File '{filename}' submitted successfully "
                "for security inspection."
            )
        )

    return render_template(
        "pages/fake_upload.html"
    )

@main_bp.route("/employee/<employee_id>")
def employee_profile(employee_id):

    if "employee" not in session:
        return redirect(url_for("main.login"))

    employee = next(

        (
            emp for emp in employees
            if emp["id"] == employee_id
        ),

        None

    )

    if employee is None:

        return "Employee not found", 404

    return render_template(

        "pages/employee_profile.html",

        employee=employee

    )

@main_bp.route("/secure/login", methods=["GET", "POST"])
def secure_login():

    if request.method == "POST":

        return render_template(
            "pages/secure_login.html",
            error="Invalid username or password."
        )

    return render_template(
        "pages/secure_login.html"
    )

@main_bp.route("/admin")
def fake_admin():
    return render_template("pages/fake_admin.html")


@main_bp.route("/administrator")
def fake_administrator():
    return render_template("pages/fake_admin.html")


@main_bp.route("/cpanel")
def fake_cpanel():
    return render_template("pages/fake_cpanel.html")


@main_bp.route("/webmail")
def fake_webmail():
    return render_template("pages/fake_webmail.html")


@main_bp.route("/.env")
def fake_env():
    return render_template("pages/fake_env.html")


@main_bp.route("/backup.zip")
def fake_backup():
    return render_template("pages/fake_backup.html")

