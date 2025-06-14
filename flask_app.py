import flask
import json
import os
import imgcompar

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path + '/templates', 'media')

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
    for i in newboard:
        try:
            newboard[i].remove(name)
        except:
            pass
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
    for k in range(len(players)):
        if players[k][0:4]=="nigg" and players[k][-3:] == "ers":
            players[k] = "Idiots"
        elif players[k] == "Kundi Soothans":
            players[k] = "Handsome Devil"
    return flask.render_template("frontend/leaderboard.html",players=players,playerlen=len(players), stages=stages)
@app.route("/parabellum")
def parabellum():
    #check user agent header
    user_agent = flask.request.headers.get('User-Agent')
    if "Antikythera" in user_agent and "JupiterOS" in user_agent:
        return flask.render_template("frontend/parabellum.html",access=True)
    #find Operating System
    if "Windows" in user_agent:
        os = "Windows"
    elif "Linux" in user_agent and "Android" not in user_agent:
        os = "Linux"
    elif "Mac" in user_agent:
        os = "Mac"
    elif "Android" in user_agent:
        os = "Android"
    elif "iPhone OS" in user_agent:
        os = "iOS"
    else:
        os= "Unknown"
    
    return flask.render_template("frontend/parabellum.html",access=False,os=os)

@app.route("/akmechanism")
def akmechanism():
    return flask.render_template('/frontend/akmechanism.html')
@app.route("/akforgot")
def akforgot():
    return flask.render_template('/frontend/akforgot.html')

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
        data[username] = {"password": password, "count": 0, "levels":[0,0,0,0,0,0,0,0,0]}
        updateData(data)
        return json.dumps({"status": "success", "message": "User registered successfully"})

@app.route("/api/check", methods=["POST"])
def check():
    data= flask.request.get_json()
    img= data.get("image")
    username = data.get("username")
    password = data.get("password")
    udata= getData()
    for i in range(9):
        chocked = imgcompar.chock(i, img)
        if chocked[0] == 0 and chocked[1] >= 0.9 and udata[username]["levels"][i] == 0:
            #check if user is in data.json
            if username in udata:
                if udata[username]["password"] == password:
                    #update count
                    udata[username]["count"] += 1
                    #update levels
                    udata[username]["levels"][i] = 1
                    updateData(udata)
                    #update leaderboard
                    updateLeaderboard(udata[username]["count"], username)
                    return json.dumps({"status": "success", "message": "Image found"})
                else:
                    return json.dumps({"status": "error", "message": "Invalid password"})
            else:
                return json.dumps({"status": "error", "message": "User not found"})
    return json.dumps({"status": "wrongimg", "message": ":):):):)"})


@app.route('/api/verifymarketplace', methods=['POST', 'OPTIONS'])
def verify_marketplace():
    data = json.loads(str(flask.request.data)[2:-1])
    print(data)
    code = data.get('code')

    if code == "glory to domus":
        print("yay")
        return flask.make_response("valid", 200)
    else:
        return flask.make_response("invalid", 200)

@app.route('/locuscognitionis/gangsofrome')
def gangs():
    return flask.render_template('frontend/locuscognitionis.html')

@app.route('/mercatus')
def market():
    return flask.render_template('frontend/mercatusromanus.html')

@app.route('/contents')
def retContent():
    content = ['''<h3>Lucilla of Capua</h3>
        <p>Daughter of noble merchant Gaius Aemilius Varro</p>
        <p class="location">Location: Stored in Forum Boarium</p>''', '''<h3>Tiberius Drusus</h3>
        <p>Former Tribune’s heir</p>
        <p class="location">Location: Captured on the Appian Way</p>''', '''<h3>Marcellus Rufus</h3>
        <p>Senator's son</p>
        <p class="location">Location: Seized outside the Curia</p>''','''<h3>Claudia Vestina</h3>
        <p>Priestess of Vesta</p>
        <p class="location">Location: Disappeared from Temple District</p>''']
    ind = flask.request.args.get("index")
    print(ind)
    return content[int(ind) - 1]

@app.route('/totallylegitmarket')
def gang():
    return flask.render_template('frontend/domusobscura.html')

@app.route('/<path:filename>')
def media(filename):
    return flask.send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

@app.route("/missing")
def missing():
    return flask.render_template("frontend/missing.html")

@app.route('/report')
def reported():
    msg = flask.request.args.get("message")
    if "forum" in msg.lower() and "boarium" in msg.lower():
        return flask.render_template("frontend/thankyou.html")
    else:
        return "<script>alert('She was not found there, you will be hanged for misinformation!')</script>"

app.run(port=5000)