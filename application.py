from flask import Flask, request, render_template, redirect
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
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
		emit("chatStart")
		emit("chatStart", room=data["partner_username"])
	

	
@socketio.on('sendChatMessage', namespace='/sock')
def onSendChatMessage(data):
	print data
	emit("receiveMessage", {"message":data['message']}, room=data['destination_username'])

# MAIN PROGRAM
if __name__ == "__main__":
    socketio.run(app)
