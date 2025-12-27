from flask import Flask, render_template, request, abort, redirect, session
from dotenv import load_dotenv
import sqlite3
from werkzeug.utils import secure_filename
import csv
import os
import uuid
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = "smart_city_secret_key"


UPLOAD_FOLDER = "uploads"
CSV_FILE = "issues.csv"

ADMIN_EMAIL = "pillabalu1@gmail.com"  


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_IMAGE_SIZE_MB = 30

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_SIZE_MB * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ReferenceID",
            "City",
            "Area",
            "Street",
            "Issue",
            "CitizenEmail",
            "Phone",
            "ImageFile",
            "SubmittedAt"
        ])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_indian_phone(phone):
    """
    Valid formats:
    9876543210
    +919876543210
    """
    pattern = r"^(?:\+91)?[6-9]\d{9}$"
    return re.match(pattern, phone)

def get_db():
    return sqlite3.connect("database.db")


def send_email(to, subject, body, sender_name):
    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{SENDER_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)


def send_email_with_attachment(to, subject, body, sender_name, attachment_path):
    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{SENDER_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        data = f.read()

    msg.add_attachment(
        data,
        maintype="image",
        subtype="jpeg",
        filename=os.path.basename(attachment_path)
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)



@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT password FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        db.close()

        if user and check_password_hash(user[0], password):
            session["user"] = email
            return redirect("/report")
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password, created_at) VALUES (?,?,?,?)",
                (name, email, hashed_password, created_at)
            )
            db.commit()
            db.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Account already exists")

    return render_template("register.html")

@app.route("/report")
def report():
    if "user" not in session:
        return redirect("/login")
    return render_template("report.html")

@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect("/login")

    ref_id = "SV-" + uuid.uuid4().hex[:6].upper()

    name = request.form["name"]
    city = request.form["city"]
    area = request.form["area"]
    street = request.form["street"]
    issue = request.form["issue"]
    email = request.form["email"]
    phone = request.form["phone"] 

    if not is_valid_indian_phone(phone):
        abort(400, "Invalid Indian phone number")

    if "image" not in request.files:
        abort(400, "No image uploaded")

    image = request.files["image"]

    if image.filename == "":
        abort(400, "No selected image")

    if not allowed_file(image.filename):
        abort(400, "Only image files allowed")

    safe_name = secure_filename(image.filename)
    image_filename = f"{ref_id}_{safe_name}"
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
    image.save(image_path)

    submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            ref_id,
            city,
            area,
            street,
            issue,
            email,
            phone,
            image_filename,
            submitted_time
        ])

    send_email(
        to=email,
        subject="Issue Reported Successfully | Smart Village System",
        sender_name="CyberTech Solutions",
        body=f"""Dear {name},
        
Your infrastructure issue has been successfully reported.

Reference ID: {ref_id}
Location: {city}, {area}, {street}
Issue Reported: {issue}

Our CyberTech Solutions team will verify and resolve the issue at the earliest.

Thank you for contributing towards building a smarter and better village.

Thank you,
CyberTech Solutions
"""
    )

    send_email_with_attachment(
        to=ADMIN_EMAIL,
        subject="New Village Issue Submitted (Image + Location)",
        sender_name="Smart Village Reporting System",
        attachment_path=image_path,
        body=f"""New infrastructure issue reported.

Reference ID: {ref_id}

City   : {city}
Area   : {area}
Street : {street}

Issue:
{issue}

Citizen Details:
Name  : {name}
Email : {email}
Phone : {phone}

Submitted At:
{submitted_time}
"""
    )

    return render_template("success.html", ref_id=ref_id)

@app.errorhandler(413)
def file_too_large(e):
    return "Image size exceeds 30 MB limit", 413

@app.errorhandler(400)
def bad_request(e):
    return "Bad Request", 400

if __name__ == "__main__":
    app.run(debug=True)
