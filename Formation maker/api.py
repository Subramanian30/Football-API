from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def fetch_player_data(player_name):
    conn = sqlite3.connect('player_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Player_API WHERE FullName LIKE ?", (f"%{player_name}%",))

    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player/<player_name>', methods=['GET'])
def get_player(player_name):
    results = []

    players_data = fetch_player_data(player_name)

    for player in players_data:
        full_name, rating, country, club = player
        results.append({"full_name": full_name, "country": country, "club": club, "rating": rating})

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
