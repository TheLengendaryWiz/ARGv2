import flask
import json
app = flask.Flask(__name__)


def roman_numerals(num):
    #convert numbers from 1 t 9 to roman numerals
    roman_numerals = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        5: 'V',
        6: 'VI',
        7: 'VII',
        8: 'VIII',
        9: 'IX'}
    return roman_numerals.get(num)
def getData():
    with open('data.json', 'r') as r:
        return json.loads(r.read())


def updateData(data):
    with open('data.json', "w") as d:
        d.write(json.dumps(data))
def getLeaderboard():
    with open('leaderboard.json', 'r') as r:
        return json.loads(r.read())
def updateLeaderboard(stage, name):
    newboard = getLeaderboard()
    data= getData()
    lastLevel = data[name]['count']
    newboard[str(lastLevel)].remove(name) if lastLevel else None
    newboard[str(stage)].append(name)

    with open('leaderboard.json', 'w') as l:
        l.write(json.dumps(newboard))

@app.route('/')
def hello():
    return flask.redirect('/instructions')
@app.route('/instructions')
def instructions():
    return open("templates/frontend/instructions.html").read()
@app.route("/login")
def login():
    return open("templates/frontend/login.html").read()
@app.route("/register")
def register():
    return open("templates/frontend/register.html").read()
@app.route("/dashboard")
def dashboard():
    return flask.render_template("frontend/dashboard.html")
@app.context_processor
def utility_processor():
    def printRoman(num):
 
        # Storing roman values of digits from 0-9
        # when placed at different places
        m = ["", "M", "MM", "MMM"]
        c = ["", "C", "CC", "CCC", "CD", "D",
            "DC", "DCC", "DCCC", "CM "]
        x = ["", "X", "XX", "XXX", "XL", "L",
            "LX", "LXX", "LXXX", "XC"]
        i = ["", "I", "II", "III", "IV", "V",
            "VI", "VII", "VIII", "IX"]
    
        # Converting to roman
        thousands = m[num // 1000]
        hundreds = c[(num % 1000) // 100]
        tens = x[(num % 100) // 10]
        ones = i[num % 10]
    
        ans = (thousands + hundreds +
            tens + ones)
    
        return ans
    return dict(printRoman=printRoman)
@app.route("/leaderboard")
def leaderboard():
    players = []
    stages = []
    lb = getLeaderboard()
    for i in lb.keys():
        [stages.append(roman_numerals(int(i))) for j in range(len(lb[i]))]
        players = players + lb[i]
    if len(players) == 0:
        return flask.render_template("frontend/leaderboard_copy.html")
    return flask.render_template("frontend/leaderboard.html",players=players,playerlen=len(players), stages=stages)

#API CALLS
@app.route("/api/login", methods=["POST"])
def api_login():
    data = flask.request.get_json()
    username = data.get("username")
    password = data.get("password")
    data= getData()
    if username in data:
        if data[username]["password"] == password:
            return json.dumps({"status": "success", "message": "Login successful"})
        else:
            return json.dumps({"status": "error", "message": "Invalid password"})
    else:
        return json.dumps({"status": "error", "message": "User not found"})



@app.route("/api/register", methods=["POST"])
def api_reg():
    data = flask.request.get_json()
    username = data.get("username")
    password = data.get("password")
    data = getData()
    if username in data:
        return json.dumps({"status": "error", "message": "Username already exists"})
    else:
        data[username] = {"password": password , "count": 0}
        updateData(data)
        return json.dumps({"status": "success", "message": "User registered successfully"})



app.run(port=5000)