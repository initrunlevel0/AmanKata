from flask import Flask, request, render_template, redirect
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
import random
app = Flask(__name__)

# GLOBAL VARIABLE
# Data users[userId] = {}
users = {}

# Data chats
# Example: {"userId1": "wirama", "userId2": "ihe", ...} // Tambahi ihe kira2 opo ae seng perlu track untuk setiap sesi chat 
chats = {}

# APP CONFIGURATION
app.debug = True
socketio = SocketIO(app)

# DATA VARIABLE MANAGEMENT
def addUser(userName):
    users[userName] = {}

#def setSessIdofUser(userName, socket):
#    users[userName]['socket'] = socket

def isUserExist(username):
	return username in users

def addChat(username1, username2):
	if username1 in chats:
		if username2 in chats[username1]:
			return False
	
	if username2 in chats:
		if username1 in chats[username2]:
			return False
	
	chats[username1] = {}
	chats[username1][username2] = {}
	return True
	
def getSocketIdFromUser(username):
	return users[username]['sessId']


# HTML BASED ROUTE
@app.route("/")
def index():
    # Tampilkan laman Index
	return render_template("index.html")
	pass

@app.route("/chat", methods=['POST'])
def chatIndex():
    # Tampilkan laman utama chat
	your_username = request.form['your_username']
	partner_username = request.form['partner_username']
	
	if isUserExist(your_username):
		return redirect("/")
	else:
		addUser(your_username)
		return render_template("chat.html", your_username = your_username, partner_username = partner_username)

# SOCKET.IO Event
# Initialized after client connected to a chat
@socketio.on('connect', namespace='/sock')
def onChatConnect():
	emit("balasConnectTrigger")

@socketio.on('balasConnect', namespace='/sock')
def onBalasChatConnect(data):
	join_room(data["your_username"])
	if addChat(data["your_username"], data["partner_username"]):
		pass
	else:
		p = 46219
		q = 46451
		seed = 0
		while seed in [0, 1, p, q, p * q]:
			seed = random.getrandbits(31)
		print seed
		#key = random.getrandbits(128)
		#iv = random.getrandbits(128)
		#key_hex = hex(key)[2:34]
		#iv_hex = hex(iv)[2:34]
		#print key_hex
		#print iv_hex
		#emit("chatStart", {"key": key_hex, "iv": iv_hex})
		#emit("chatStart", {"key": key_hex, "iv": iv_hex}, room=data["partner_username"])
		emit("chatStart", {"seed": seed})
		emit("chatStart", {"seed": seed}, room=data["partner_username"])

@socketio.on('sendChatMessage', namespace='/sock')
def onSendChatMessage(data):
	print data
	emit("receiveMessage", {"message":data['message']}, room=data['destination_username'])

@socketio.on('disconnect', namespace='/sock')
def onDisconnect():
	print('Client disconnected')

# MAIN PROGRAM
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
