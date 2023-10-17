from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Define available options for boarder_passage and hamn
BOARDER_PASSAGE_OPTIONS = ["Habartice", "Bohumin", "Ingen"]
HAMN_OPTIONS = ["Trelleborg", "Ystad"]

def get_distance_duration(origin, destination, api_key):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    params = {
        "origins": origin,
        "destinations": destination,
        "avoid": "highways",
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        print(data)
        element = data['rows'][0]['elements'][0]
        distance = element['distance']['text']
        duration = element['duration']['text']
        return distance, duration
    else:
        return "Error occurred: " + data['status']

@app.route('/', methods=['GET', 'POST'])
def index():

    def to_int(distance_string):
        try:
            # Attempt to convert the string to a floating-point number
            distance_float = float(distance_string.replace(' km', '').replace(',',''))
            # Convert the floating-point number to an integer (rounding to the nearest integer)
            distance_integer = int(round(distance_float))
            return distance_integer
        except ValueError:
            # Handle the case where conversion fails (e.g., invalid input)
            print("Invalid distance string")
            return None
    if request.method == 'POST':
        origin = request.form['origin']
        boarder_passage = request.form['boarder_passage']
        hamn = request.form['hamn']
        dest = request.form['dest']
        
        # Read API key from file
        with open("api_key.txt", "r") as file:
            api_key = file.read().strip()

        hamn_polen = "Swinoujscie"
 
        if boarder_passage == "Habartice":
            boarder_passage = "Habartice, 46373 Habartice u Frydlantu, Tjeckien"

        if boarder_passage=="Ingen":
            distance1, duration1 = get_distance_duration(origin, hamn_polen, api_key)
            distance2="0"
        else:
            distance1, duration1 = get_distance_duration(origin, boarder_passage, api_key)
            distance2, duration2 = get_distance_duration( boarder_passage, hamn_polen, api_key)
        
        distance3, duration3 = get_distance_duration(hamn, dest, api_key)
        distance = to_int(distance1)+to_int(distance2)+to_int(distance3)

        return render_template('index.html', distance=distance, cost=round(distance * 1.1 + 330), boarder_passage_options=BOARDER_PASSAGE_OPTIONS, hamn_options=HAMN_OPTIONS)
    return render_template('index.html', distance=None, cost=None, boarder_passage_options=BOARDER_PASSAGE_OPTIONS, hamn_options=HAMN_OPTIONS)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)