import os
import sqlite3

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, dp

import pandas as pd

from sqlalchemy import create_engine

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"


#conn = sqlite3.connect('players.db')


@app.route("/")
@login_required
def index():
    """Goes to homepage"""
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    rows = (c.execute('SELECT * FROM players, favourites WHERE favourites.userid = ? AND players.id = favourites.playerid',[session["user_id"]])).fetchall()
    #if not rows:
        #conn.close()
        #return render_template("portfolio.html")
    conn.close()
    return render_template("index.html", rows=rows)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search for player"""
    if request.method == "POST":
        s = request.form.get("name")
        conn = sqlite3.connect('players.db')
        a = conn.cursor()
        names = (a.execute("SELECT player_name, id FROM players WHERE player_name LIKE ?", ('%'+s+'%',))).fetchall()
        conn.close()
        output = []
        for name in names:
            if name not in output:
                output.append(name)
        return render_template("searched.html", names=output)
    else:
        return render_template("search.html")


@app.route('/profile/<int:player_id>')
@login_required
def profile(player_id):
    # Retrieve the player's information from the database
    conn = sqlite3.connect('players.db')
    b = conn.cursor()
    player = (b.execute('SELECT * FROM players WHERE id = ?', [player_id])).fetchall()
    name = (b.execute('SELECT player_name FROM players WHERE id = ?', [player_id])).fetchone()
    # Render the players's profile page
    conn.close()
    return render_template('profile.html', player=player, name=name)


@app.route('/profile/<int:player_id>/favourite', methods=['GET'])
@login_required
def favourite(player_id):
    # Remove row from the database if it exists
    conn = sqlite3.connect('players.db')
    d = conn.cursor()
    if (d.execute('SELECT * FROM favourites WHERE playerid = ? AND userid = ?', [player_id, session['user_id']])).fetchall():
        d.execute('DELETE FROM favourites WHERE playerid = ? AND userid = ?', [player_id, session['user_id']])
    # Else add it to the database
    #player = c.execute('SELECT * FROM players WHERE id = ?', player_id)
    else:
        d.execute('INSERT INTO favourites (playerid, userid) VALUES (?, ?)', [player_id, session['user_id']])
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/rankings")
@login_required
def ryears():
    """Return all years"""
    return render_template("ryears.html")


@app.route("/rankings/<int:year>")
@login_required
def rankings(year):
    """Search for player"""
    conn = sqlite3.connect('players.db')
    a = conn.cursor()
    guards = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY guard_score DESC LIMIT 30", (year,))).fetchall()
    forwards = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY forward_score DESC LIMIT 30", (year,))).fetchall()
    centres = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY centre_score DESC LIMIT 30", (year,))).fetchall()
    conn.close()
    return render_template("rankings.html", guards=guards, forwards=forwards, centres=centres)



@app.route("/draft", methods=["GET", "POST"])
@login_required
def dyears():
    """Draft years"""
    return render_template("dyears.html")


@app.route("/draft/<int:year>")
@login_required
def draft(year):
    """Drafts for each year"""
    conn = sqlite3.connect('players.db')
    a = conn.cursor()
    guards = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY guard_score DESC LIMIT 30", (year,))).fetchall()
    forwards = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY forward_score DESC LIMIT 30", (year,))).fetchall()
    centres = (a.execute("SELECT * FROM players WHERE year = ? ORDER BY centre_score DESC LIMIT 30", (year,))).fetchall()
    conn.close()
    players = []
    p = []
    for guard in guards:
        best = guard[-4]
        best_pos = 'Guard'
        if guard[-3] > best:
            best = guard[-3]
            best_pos = 'Forward'
        if guard[-2] > best:
            best = guard[-2]
            best_pos = 'Centre'
        players.append([guard[3], guard[1], best_pos, best, guard[-1], guard[0]])
        p.append(guard[3])

    for forward in forwards:
        if forward[3] not in p:
            best = forward[-4]
            best_pos = 'Forward'
            if forward[-3] > best:
                best = forward[-3]
                best_pos = 'Forward'
            if forward[-2] > best:
                best = forward[-2]
                best_pos = 'Centre'
            players.append([forward[3], forward[1], best_pos, best, forward[-1], forward[0]])
            p.append(forward[3])

    for centre in centres:
        if centre[3] not in p:
            best = centre[-4]
            best_pos = 'Forward'
            if centre[-3] > best:
                best = centre[-3]
                best_pos = 'Forward'
            if centre[-2] > best:
                best = centre[-2]
                best_pos = 'Centre'
            players.append([centre[3], centre[1], best_pos, best, centre[-1], centre[0]])
            p.append(centre[3])

    players = sorted(players,key=lambda x: x[3], reverse=True)
    return render_template("draft.html", players=players)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        conn = sqlite3.connect('players.db')
        e = conn.cursor()
        rows = (e.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])).fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        conn = sqlite3.connect('players.db')
        f = conn.cursor()
        name = request.form.get("username")
        p1 = request.form.get("password")
        p2 = request.form.get("confirmation")
        if p1 != p2 or not p1 or not name:
            return apology("invalid username and/or password", 400)
        elif (f.execute("SELECT * FROM users WHERE username = ?", (name,))).fetchone():
            return apology("username already exists", 400)
        f.execute('INSERT INTO users (username, hash) VALUES(?, ?)', (name,generate_password_hash(p1)))
        rows = (f.execute("SELECT id FROM users WHERE username = ?", [name])).fetchone()
        session["user_id"] = rows[0]
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Get stock quote."""
    if request.method == "POST":
        conn = sqlite3.connect('players.db')
        g = conn.cursor()
        op = request.form.get("password")
        np = request.form.get("npassword")
        if not request.form.get("password") or not request.form.get("npassword"):
            return apology("must provide password", 400)
        rows = (g.execute("SELECT * FROM users WHERE id = ?", [session['user_id']])).fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2], op):
            return apology("old password is incorrect", 400)
        g.execute('UPDATE users SET hash = ? WHERE id = ?', [generate_password_hash(np), session['user_id']])
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return render_template('change_password.html')

