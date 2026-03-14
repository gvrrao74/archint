from flask import Flask, render_template, request, jsonify
import requests
import random
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# REAL News Key provided by user for live data
NEWS_KEY = 'pub_125551f32e6b4554a9ed40b87b37dadc'

@app.route('/')
def home():
    return render_template('index.html')

# --- SIMULATION ENGINES (STOCKS) ---
def generate_simulated_candles(count=40):
    """Generates synthetic OHLC data for the simulation."""
    candles = []
    price = random.uniform(100, 500)
    for _ in range(count):
        o = price
        c = o + random.uniform(-12, 12)
        candles.append({
            'o': o, 
            'h': max(o, c) + random.uniform(0, 5), 
            'l': min(o, c) - random.uniform(0, 5), 
            'c': c
        })
        price = c
    return candles

def draw_chart(candles, rows=10):
    """Renders a professional ASCII candlestick chart."""
    if not candles: return ""
    vals = [c['h'] for c in candles] + [c['l'] for c in candles]
    min_v, max_v = min(vals), max(vals)
    rng = (max_v - min_v) or 1
    grid = [[" " for _ in range(len(candles))] for _ in range(rows)]
    for x, c in enumerate(candles):
        y_o = int(((c['o']-min_v)/rng)*(rows-1))
        y_c = int(((c['c']-min_v)/rng)*(rows-1))
        char = "█" if c['c'] >= c['o'] else "░"
        for y in range(min(y_o, y_c), max(y_o, y_c) + 1):
            grid[rows-1-y][x] = char
    return "\n".join(["".join(row) for row in grid])

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    user_input = data.get('command', '').strip().split()
    if not user_input: return jsonify({"output": ""})
    
    cmd = user_input[0].upper()
    args = user_input[1:]

    # --- 01: REAL NEWS LOGIC ---
    if cmd in ['NEWS', '01']:
        query = " ".join(args) if args else "business"
        url = f"https://newsdata.io/api/1/latest?apikey={NEWS_KEY}&q={query}&language=en"
        try:
            r = requests.get(url).json()
            articles = r.get('results', [])[:3]
            output = f"[ REAL-TIME INTEL UPLINK: {query.upper()} ]\n"
            output += "--------------------------------------------------------------\n"
            if not articles:
                output += "[-] NO LIVE NEWS FOUND FOR THIS QUERY."
            else:
                for art in articles:
                    output += f"» {art['title']}\n"
                    output += f"  SRC: {art.get('source_id', 'Unknown').upper()}\n"
                    output += f"  LNK: {art.get('link', 'N/A')}\n\n"
            output += "--------------------------------------------------------------\n"
            output += "[!] DISCLAIMER: The news presented here is REAL and LEGIT.\n"
            return jsonify({"output": output})
        except:
            return jsonify({"output": "ERROR: NEWS UPLINK TIMEOUT."})

    # --- 02: SIMULATED STOCKS (WITH CANDLESTICK GRAPH) ---
    if cmd in ['STOCKS', '02']:
        symbol = args[0].upper() if args else "SIM_TKR"
        candles = generate_simulated_candles()
        chart = draw_chart(candles)
        change = candles[-1]['c'] - candles[0]['o']
        return jsonify({"output": f"""
[ SIMULATED MARKET BRIEF: {symbol} ]
--------------------------------------------------------------
{chart}
--------------------------------------------------------------
LAST: ${candles[-1]['c']:.2f} | 24H DELTA: {change:+.2f}
ACTION: {'STRONG BUY' if change > 0 else 'STRONG SELL'}

[!] SIMULATION NOTICE: This stock data is SYNTHETIC. 
It is generated locally for entertainment purposes.
--------------------------------------------------------------
"""})

    # --- 03: IP LOOKUP (REAL DATA FROM VIDEO LOGIC) ---
    if cmd in ['IP', '03']:
        target_ip = args[0] if args else ""
        try:
            # Logic inspired by the provided video: Fetching from ip-api
            response = requests.get(f"http://ip-api.com/json/{target_ip}").json()
            
            if response.get('status') == 'fail':
                msg = response.get('message', 'Invalid IP')
                if msg == "private range":
                    return jsonify({"output": "[-] ERROR: TARGET IS A PRIVATE IP. CANNOT LOCATE ON PUBLIC WEB."})
                return jsonify({"output": f"[-] LOOKUP FAILED: {msg}"})
            
            return jsonify({"output": f"""
[ IP TARGETING UPLINK: {target_ip if target_ip else 'YOUR_IP'} ]
--------------------------------------------------------------
COUNTRY:   {response.get('country', 'UNKNOWN')}
REGION:    {response.get('regionName', 'UNKNOWN')}
CITY:      {response.get('city', 'UNKNOWN')}
TIMEZONE:  {response.get('timezone', 'UNKNOWN')}
ISP:       {response.get('isp', 'UNKNOWN')}
LAT/LON:   {response.get('lat')}, {response.get('lon')}
--------------------------------------------------------------
[!] DATA SOURCE: VERIFIED IP GEOLOCATION UPLINK.
"""})
        except:
            return jsonify({"output": "ERROR: IP UPLINK TIMEOUT."})

    # --- NEW 04: DEVELOPER INFO ---
    if cmd in ['DEV', '04']:
        return jsonify({"output": """
[ CLASSIFIED DEVELOPER PROFILE ]
--------------------------------------------------------------
...............:..:.:..::::::::::::::::::::::::::::::...:......:.:.:.......:...:
.....................................::..::....................................:
.............................:-=*#%%%%%%%%%%##+=-::............................:
..........................-*%%%@@@@@@@@@@@@@@@@%%%#=::.........................:
.......................:=#%@@@@@@@@@@@@@@@@@@@@@@@@@%%+-:......................:
.....................:*%@@@@@@%%%%%%@@@@@@@@@@%%@@@@@@@%*-:....................:
...................:+%@@@@@@%#######%%%@@@@@@%@@@@@@@@@@@%=:...................:
..................:*%@@@@%%#*++=++++++**#%%%%%##%%%%%%@@@@%=:..................:
.................:#%@@@%%#+===============++===+++***##%@@@*:..................:
.................=%%%%%*+===-=------------===-=====++*#%%@@%:..................:
.................+%%%%*+=====-----------------=====+++*#%@@%-..................:
.................+%%%#*=====------------------=====+++*#%%%%:..................:
.................+%%%*+=====--------------------=====++*%%%%:..................:
.................=%%#+=====+=++*++=--------=+++==++====+#%%%:..................:
.................:%#+-==***+++++++==------==+***#***#*==*%%+:..................:
.................:+#+-====++**####*+=---=+*#######*+====+%#::..................:
.................--*+-==+*###%@%++*+=====+**+#@@%*%#*+==+#+++-.................:
................:==++--=====+++++=========+++*+*+++=====++==+-:................:
................:====--------=--=---=--==================+*+=:.................:
.................-==---------------=----====------=--=====++=::................:
.................-==--------------------======------==-==+*+=:.................:
.................:--=-=--=--------=++===+*+==------======+==:..................:
.................:-=+=------------========+===----=========-:..................:
...................::---=-------======++++++===========-::::...................:
.....................:-========*#*+=====++*##*+=======-::::....................:
......................:-=================+++=+========:::::....................:
.......................:-===========-========+==+++==:::.......................:
........................:=+++======---========+++**++#-::::....................:
.......................-#*+++++++====++++++++*******%@%*:::..:.................:
....................::*%%+-=++**********************@@@%%#*=-:::...............:
.................:-+##%%%=:-===+***########***++++=:=@@%%%%%%%*-::::::.:....:..:
............::=*####%%%%%+::-+====+++******+++====::-%@%%%%%%%%%#=:::::::::.:.::
........:-=*%%%%%%%%%%%%%#:.:-*+====++++++++====+::::#%%%%%%%%%%%@%%#+-:::::::::
...::-+##%%%%%%%%%%%%%%%%%+::.:+*+======++=+==+*-::::*%%%%%%%%%%%%%%%%%%#*+-::::
-+*##%%%%%%%%%%%%%%%%%%%%%#-:.::-***+++++++++**-::::-#%%%%%%%%%%%%%%%%@@@%%%%#*+
#%%%%@@@@@@%%%%%%%%@@@%%%%%#:...::-***+++++***=:::::*%%%@%%%%%%%%%%%@@@@%%%%%%%#
#%%%%@@%%%@@@@@@@@@@@%%%%%%%+:.....:-********-:::::-%%%%%%@@@@@@@@@@@@@%%%%%%%%#
#%%%%%%%%%@@%%%%%%@@%%%%%%%%#-......::=#####=::.:::=%%%%%%%@@@@@%%%@@@@%%@%%%%%#
#%%%%%%%%@@@@%%%%@@%%%%%%%%%%*:........-*%#-:::.:::*%%%%%%%%@@@@@%%%@@@@%%%%%%%#
#%%%%%%%%@@@%%%%%%%%%%%%%%%%%%-......:::::::-::.::-%%%%%%%%%@@@@@%@@@@@%%%%%%%%#
#%%%%%%%%@@%%%%%%%%%%%%%%%%%%%*:...::::..::.:--:::*%%%%%%%%%%@%%%@@%@@@@@%@@%%%#
#%%%%%%%%@%%@%%%@%%%%%%%%%%%%%%=:::::.......:-:::-#%%%%%%%@%%%%%%%@@@@@@%%@@%%%%
#%%%%%%%%@%%%%%%%@@%%%%%%%%%%%%*-::..........:::--#%%%%%%@%@%@%%@@@%@@@@%%@@%%%%
#%%%%%%%%@%%%%%%%%@%%%%%%%%%%%%%+-:..........:::-=%%%%%%%%%%%@%@@@%%%%@@%@@@%@%%
#%%%%%%%%%%%%%%%%%@@@%%%%%%%%%%%#=:..........:::-#%%%%%%%%%@%%@@@%%%@%%%%@@@%@%%
#%%%%%%%%%%%%%%%%%%%@@%%%%%%%%%%%*::.........::-+%%%%%%%%%%%@@@%%%%@%%%%%@@@@@%%
#%%%%%%%%%%%%%%%%%%%%@@%@%%%%%%%%#=:.:......:.:-*%%%%%%%%%%@@@%%%%%%%%%%%@@@@@%%
#%%%@%%%%%%%%%%%%%%%%%@@@%%%%%%%%%*:::.......::=%%%%%%%%%%@@@%%%%%%%%%%%@@@@@@@%
#%%%%%%%%%%%%%%%%%%%%%%%@@%%%%%%%%%::::......::*%%%%%%%%%%@@%%%%%%%%%%%@%@@@@@@%
#%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%%=::.:.....:-#%%%%%%%%@@%%%%%%%%%%%%%%@@@@@@@%
##%%%%%%%%%%%%@%%%%%%%%%%%@@%%%%%%%#::.::...::+%%%%%%%%@@%%%%%%%%%%%%@%%%@@@@@@%
##%%%%%%%%%%%%%%%%%%%%%%%%%%@%%%%%%%=:::::.:::*%%%%%%%@@%@%%%%%%%%%%%%%%%%@@@@%%

--------------------------------------------------------------
This is GVR, a hackclubber who wants to build exciting projects for the world. 
Im also into Sport Shooting, and I have a passion for learning new things.

STATUS: ACTIVE
CLEARANCE: **********
--------------------------------------------------------------
"""})

    # --- CC: CORE COMMANDS MENU ---
    if cmd in ['CC', '04', 'HELP']:
        return jsonify({"output": """
[ CORE COMMANDS ]
--------------------------------------------------------------
[ 01 ] NEWS [query]   - Global news uplink (REAL)
[ 02 ] STOCKS [sym]   - Market simulation (FAKE)
[ 03 ] IP [address]   - Target geolocation lookup (REAL)
[ 04 ] DEV            - View developer profile (REAL)
[ CLS ]               - Clear terminal buffer
--------------------------------------------------------------
"""})

    if cmd == 'CLS': return jsonify({"output": "SYSTEM_SIGNAL_CLEAR"})
    return jsonify({"output": "COMMAND NOT RECOGNIZED. TYPE 'CC'."})

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
