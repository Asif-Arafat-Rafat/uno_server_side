from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_socketio import SocketIO, emit, join_room
import secrets
import string
from classes.game_play import Game

app = Flask(__name__)
socketio = SocketIO(app)


lobbies = {}  # Dictionary to store lobby information

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_lobby/<int:size>")
def create_lobby(size):
    lobby_code = generate_code()
    lobbies[lobby_code] = {"player_count": 0, "players": [], "size": size}
    return redirect(url_for("add_player", lobby_code=lobby_code))

@app.route("/add_player/<lobby_code>")
def add_player(lobby_code):
    player_id = generate_code(8)  
    if len(lobbies[lobby_code]["players"]) >= lobbies[lobby_code]["size"]:
        return jsonify({"error": "Lobby is full."}), 400
    # Generate a unique player ID
    lobbies[lobby_code]["players"].append(player_id)
    lobbies[lobby_code]["player_count"] += 1

    return jsonify({"lobby_code": lobby_code, "player_id": player_id})

@app.route("/monitor_lobby/<lobby_code>/<player_id>")
def monitor_lobby_route(lobby_code, player_id):
    if lobby_code in lobbies:
        return render_template("monitor.html", lobby_code=lobby_code, player_id=player_id)
    else:
        return "Lobby not found.", 404
player_data={}

@socketio.on("monitor_lobby")
def monitor_lobby(data):
    socket_id = request.sid

    lobby_code = data.get("lobby_code")
    player_id = data.get("player_id")
    player_data[player_id] = {
        "socket_id": socket_id,
        "lobby_code": lobby_code
    }
    join_room(lobby_code)
    if lobbies[lobby_code]["player_count"]> 2:
        emit("error", {"message": "Lobby is full. "})
        return
    if lobby_code in lobbies:
        if player_id not in lobbies[lobby_code]["players"]:
            emit("error", {"message": "You are not in this lobby."})
            
        else:
            emit("lobby_update", {
                "player_count": lobbies[lobby_code]["player_count"],
                "on_socket_count": len(player_data),
                "players": player_data,
                "lobby_data": lobbies[lobby_code],
                "lobbies": lobbies
            },to=lobby_code
)
    else:
        emit("error", {"message": "Lobby not found."})    

@socketio.on("disconnect")
def handle_disconnect():
    socket_id = request.sid
    for player_id,data in player_data.items():
        if data['socket_id']==socket_id:
            lobby_code=data['lobby_code']
            if lobby_code in lobbies:
                lobbies[lobby_code]["player_count"] -= 1
                lobbies[lobby_code]["players"].remove(player_id)
                del player_data[player_id]
                emit("lobby_update", {
                    "player_count": lobbies[lobby_code]["player_count"],
                    "on_socket_count": len(player_data),
                    "players": player_data
                },to=lobby_code)
            break
def generate_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
# Listen for a click event from any client



# @socketio.on("game_start")
# def handle_game_start(data):

#     lobby_code = data.get("lobby_code")
#     player_id = data.get("player_id")

#     print(f"Game start requested for lobby: {lobby_code} by player: {player_id}")

#     if lobby_code not in lobbies:
#         emit("error", {
#             "message": "Lobby not found"
#         })
#         return

#     if player_id not in lobbies[lobby_code]["players"]:
#         emit("error", {
#             "message": "Player not in lobby"
#         })
#         return

#     game = Game(
#         lobby_id=lobby_code,
#         players=lobbies[lobby_code]["players"]
#     )

#     game_data = game.start_game()

#     emit("game_data", {
#         "current_card": game_data["current_card"],
#         "direction": game_data["direction"],
#         "turn": game_data["turn"],
#         "data": game_data["deck"][player_id]
#     })


@app.route("/game/<lobby_code>/<player_id>")
def game(lobby_code, player_id):
    if lobby_code in lobbies:
        return render_template("game.html", lobby_code=lobby_code, 
                               player_id=player_id,
                               players=lobbies[lobby_code]["players"])
    else:
        return "Lobby not found.", 404

@socketio.on("game_start")
def handle_game_start(data):
    lobby_code = data.get("lobby_code")
    player_id = data.get("player_id")
    print(f"Game start requested for lobby: {lobby_code} by player: {player_id}")
    game = Game(lobby_id=lobby_code, players=lobbies[data["lobby_code"]]["players"])
    game_data=game.start_game()
    emit("game_data",{
        "current_card":game_data["current_card"],
        "direction":game_data["direction"],
        "turn":game_data["turn"],
        "data":game_data["deck"][data["player_id"]]
    })


if __name__ == "__main__":
    import os

    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        allow_unsafe_werkzeug=True
    )