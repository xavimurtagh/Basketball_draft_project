import sqlite3
from flask import Flask, flash, redirect, render_template, request, session

conn = sqlite3.connect('players.db')
f = conn.cursor()
name = 'xavier'
p1 = 'p'

f.execute('INSERT INTO users (username, hash) VALUES(?, ?)', (name, p1))
rows = (f.execute("SELECT id FROM users WHERE username = ?", [name])).fetchone()
session["user_id"] = rows[0]
session["user_id"]
conn.close()

