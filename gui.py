import tkinter as tk
import requests


file=open("api_key.txt","r")
api_key =str(file.read())

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

# Function to be called when the button is clicked
def on_button_click(event=None):
    # Get selected cities from the dropdown menus
    origin = origin_var.get()
    boarder_passage = boarder_passage_var.get()
    hamn = hamn_var.get()
    dest = dest_var.get()
    #boarder_passage = f"{51.016145},{15.065076}"

    
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
    print(to_int(distance1)+to_int(distance2))
    distance = to_int(distance1)+to_int(distance2)+to_int(distance3)

    # Set the text of the labels to display the distance and duration
    label_output1.config(text="Distance: " + str(distance) + " km")
    label_output2.config(text="Kostnad: " + str(round(distance*1.1+330)) +" euro")


# Create the main window
root = tk.Tk()
root.title("Viktor Distance Calculator")

# List of cities for the dropdown menus
cities = ["Habartice", "Bohumin","Ingen"]
hamn = ["Trelleborg", "Ystad"]

# Variables to store the selected cities
boarder_passage_var = tk.StringVar(root)
boarder_passage_var.set(cities[0])  # Set the default destination city

# Variables to store the selected hamn
hamn_var = tk.StringVar(root)
hamn_var.set(hamn[0])  # Set the default destination city

#Create and place the first input field
label1 = tk.Label(root, text="Start stad:")
label1.pack()
origin_var= tk.Entry(root)
origin_var.pack()

# Create and place the origin dropdown menu
label2 = tk.Label(root, text="Boarderpassage:")
label2.pack()
origin_menu = tk.OptionMenu(root, boarder_passage_var, *cities)
origin_menu.pack()

# Create and place the origin dropdown menu
label3 = tk.Label(root, text="Hamn i Sverige:")
label3.pack()
hamn_menu = tk.OptionMenu(root, hamn_var, *hamn)
hamn_menu.pack()

#Create and place the last input field
label4 = tk.Label(root, text="Destination:")
label4.pack()
dest_var= tk.Entry(root)
dest_var.pack()

# Create and place the button to trigger the function
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack()

# Create labels to display the distance and duration
label_output1 = tk.Label(root, text="")
label_output1.pack()
label_output2 = tk.Label(root, text="")
label_output2.pack()

# Enables the enter button to start the search
root.bind('<Return>', on_button_click)

# Start the tkinter main loop
root.mainloop()



