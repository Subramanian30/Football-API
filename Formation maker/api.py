from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def fetch_players_data(query=None):
    conn = sqlite3.connect('player_database.db')
    cursor = conn.cursor()

    if query:
        # cursor.execute("SELECT * FROM Player_API WHERE FullName LIKE ? OR ClubName LIKE ?", (f"%{query}%", f"%{query}%"))
        cursor.execute("SELECT * FROM Player_API WHERE FullName LIKE ? OR FullName LIKE ?",
               (f"{query}%", f"% {query}%"))

    else:
        cursor.execute("SELECT * FROM Player_API")

    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "Please provide a query parameter"}), 400

    results = []

    players_data = fetch_players_data(query)
    
    for player in players_data:
        player_name, rating, country, club = player
        results.append({"player_name": player_name, "country": country, "club": club, "rating": rating})

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
