import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, make_response
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import usd, login_required  # Import helpers
import csv
from io import StringIO, BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)  # Secure secret key generation
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route for the homepage
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    query = request.args.get("search")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Build the query with filters
    sql_query = "SELECT * FROM transactions WHERE user_id = :user_id"
    params = {"user_id": session["user_id"]}

    if start_date:
        sql_query += " AND timestamp >= :start_date"
        params["start_date"] = f"{start_date} 00:00:00"
    if end_date:
        sql_query += " AND timestamp <= :end_date"
        params["end_date"] = f"{end_date} 23:59:59"
    if query:
        sql_query += " AND (description LIKE :query OR category LIKE :query OR amount LIKE :query)"
        params["query"] = f"%{query}%"

    sql_query += " ORDER BY timestamp DESC"
    transactions = db.execute(sql_query, **params)

    # Calculate income, expenses, and balance
    income = sum(t["amount"] for t in transactions if t["category"] == "income")
    expenses = sum(t["amount"] for t in transactions if t["category"] == "expense")
    balance = income - expenses

    return render_template(
        "index.html",
        transactions=transactions,
        balance=balance,
        income=income,
        expenses=expenses,
        filters={"query": query, "start_date": start_date, "end_date": end_date}
    )





# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username exists
        user = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            flash("Invalid username and/or password", "danger")
            return redirect("/login")

        # Store user id in session
        session["user_id"] = user[0]["id"]
        flash("Logged in successfully!", "success")
        return redirect("/")

    return render_template("login.html")

# Route for the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear the session to ensure the user starts fresh
    session.clear()

    if request.method == "POST":
        # Get form inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for missing inputs and invalid values
        if not username:
            flash("Sorry, try to insert a valid username", "danger")
            return redirect("/register")
        elif not password or not confirmation:
            flash("Enter a valid password and confirm it", "danger")
            return redirect("/register")
        elif password != confirmation:
            flash("The passwords do not match", "danger")
            return redirect("/register")

        # Check if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            flash("Username already exists", "danger")
            return redirect("/register")

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hashed_password)

        # Retrieve the user from the database and log them in by storing their ID in the session
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # Redirect to the homepage after successful registration
        return redirect("/")
    else:
        return render_template("register.html")


# Route for history page to show transactions
@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC", user_id=user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add_transaction", methods=["GET", "POST"])
@login_required
def add_transaction():
    """Add a new transaction"""
    if request.method == "POST":
        # Get the form data
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        description = request.form.get("description")

        # Check for valid category
        if category not in ["income", "expense"]:
            flash("Invalid category", "danger")
            return redirect("/add_transaction")

        # Insert the transaction into the database
        db.execute("INSERT INTO transactions (user_id, category, amount, description) VALUES (?, ?, ?, ?)",
                   session["user_id"], category, amount, description)

        flash("Transaction added successfully!", "success")
        return redirect("/")

    return render_template("add_transaction.html")


@app.route("/export/csv")
@login_required
def export_csv():
    """Export transactions to a CSV file"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # Create a CSV file in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Description", "Category", "Amount", "Date"])
    for transaction in transactions:
        writer.writerow([
            transaction["description"],
            transaction["category"].capitalize(),
            transaction["amount"],
            transaction["timestamp"].split(" ")[0]
        ])

    # Return as a response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=transactions.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route("/export/pdf")
@login_required
def export_pdf():
    """Export transactions to a PDF file"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # Create a PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Transaction History")

    # Table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 80, "Description")
    c.drawString(200, height - 80, "Category")
    c.drawString(350, height - 80, "Amount")
    c.drawString(450, height - 80, "Date")

    # Transactions
    y = height - 100
    c.setFont("Helvetica", 10)
    for transaction in transactions:
        if y < 50:  # Start a new page if space is insufficient
            c.showPage()
            y = height - 50
        c.drawString(50, y, transaction["description"])
        c.drawString(200, y, transaction["category"].capitalize())
        c.drawString(350, y, f"{transaction['amount']:.2f}")
        c.drawString(450, y, transaction["timestamp"].split(" ")[0])
        y -= 20

    c.save()
    buffer.seek(0)

    # Return as a response
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=transactions.pdf"
    response.headers["Content-type"] = "application/pdf"
    return response


# Main entry point to start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
