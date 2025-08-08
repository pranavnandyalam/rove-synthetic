import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from recommender import recommend_best_redemptions
from sql_lite import insert_feedback
from value_calc import example_calculations

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "dev")


@app.get("/")
def index():
    examples = example_calculations()
    return render_template("index.html", results=None, examples=examples)


@app.post("/recommend")
def recommend():
    origin = request.form.get("origin", "").upper().strip()
    destination = request.form.get("destination", "").upper().strip()
    departure_date = request.form.get("departure_date", "").strip()
    miles_available = int(request.form.get("miles_available", "0"))
    results = recommend_best_redemptions(origin, destination, departure_date, miles_available)
    examples = example_calculations()
    return render_template(
        "index.html",
        results=results,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        miles_available=miles_available,
        examples=examples,
    )


@app.post("/feedback")
def feedback():
    origin = request.form.get("origin", "")
    destination = request.form.get("destination", "")
    departure_date = request.form.get("departure_date", "")
    miles_available = int(request.form.get("miles_available", "0"))
    rating = int(request.form.get("rating", "0"))
    comments = request.form.get("comments", "")
    insert_feedback(origin, destination, departure_date, miles_available, rating, comments)
    flash("Thanks for your feedback!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True) 