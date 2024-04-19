import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import mysql.connector
import re
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aagam@03',
    'database': 'parkinglot',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS parking_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    vehicle_type VARCHAR(20),
    vehicle_name VARCHAR(50),
    owner_name VARCHAR(50),
    checkin_date DATE,
    checkin_time TIME
);
"""
cursor.execute(create_table_query)
connection.commit()

Vehicle_Number = ['']
Vehicle_Type = ['']
vehicle_Name = ['']
Owner_Name = ['']
Date = ['']
Time = ['']
bikes = 100
cars = 250
bicycles = 78


def save_to_database(vehicle_number, vehicle_type, vehicle_name, owner_name, checkin_date, checkin_time):
    insert_query = """
    INSERT INTO parking_records (vehicle_number, vehicle_type, vehicle_name, owner_name, checkin_date, checkin_time)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (vehicle_number, vehicle_type, vehicle_name, owner_name, checkin_date, checkin_time))
    connection.commit()


def submit_form():
    # Get values from the entry widgets
    number_value = number_entry.get()
    type_value = type_entry.get()
    Spots_value=100
    entry_exit_value = entry_exit_var.get()
    
    # Convert time difference to hours
    if entry_exit_value=='Entry':
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Spots_value=100
        result_label.config(text=f"Number Plate: {number_value}\nTime of Entry: {current_time}\nEntry/Exit: {entry_exit_value}\nSpots Left: {Spots_value}")
    if entry_exit_value=='Exit': 
        check_in_time, check_out_time = calculate_check_times(entry_exit_value)
        checkout_time=datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
        checkin_time=datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
        time_difference = checkout_time - checkin_time
            # Convert time difference to hours
        hours_parked = time_difference.total_seconds() / 3600
        if type_value == "Bicycle":
                            rate_per_hour = 20
        elif type_value == "Bike":
                            rate_per_hour = 40
        elif type_value == "Car":
                            rate_per_hour = 60
        amt = float(hours_parked)*rate_per_hour
        result_label.config(text=f"Number Plate: {number_value}\nType: {type_value}\nAmount: {amt} rps\nHours Parked: {hours_parked}\nTime of Exit: {checkout_time}\nEntry/Exit: {entry_exit_value}")
        save_to_database(number_value,type_value,amt,entry_exit_value,hours_parked)


def refresh_form():
    # Clear entry fields
    number_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)

    # Clear radio button selection
    entry_exit_var.set("")

    # Clear the result label
    result_label.config(text="")

def calculate_check_times(entry_exit_value):
        current_time = datetime.now()
        check_in_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if entry_exit_value == "Exit":
     
            current_time += timedelta(minutes=100)

        check_out_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        return check_in_time, check_out_time
def open_list_gui():
    list_gui = tk.Toplevel(root)
    list_gui.title("List GUI")
    list_gui.geometry("300x200")

    label = ttk.Label(list_gui, text="This is the List GUI.")
    label.grid(row=0, column=0, pady=20)
    close_button = ttk.Button(list_gui, text="Close", command=list_gui.destroy)
    close_button.grid(row=1, column=0)

# Create the main window
root = tk.Tk()
root.title("Parking Details")

# Create and place entry widgets
number_label = ttk.Label(root, text="Number Plate:")
number_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

number_entry = ttk.Entry(root)
number_entry.grid(row=0, column=1, pady=5)

type_label = ttk.Label(root, text="Vehicle Type:")
type_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

type_entry = ttk.Entry(root)
type_entry.grid(row=2, column=1,rowspan=2, pady=5)

entry_exit_var = tk.StringVar()
entry_radio = ttk.Radiobutton(root, text="Entry", variable=entry_exit_var, value="Entry")
entry_radio.grid(row=5, column=0, padx=75, pady=5, sticky=tk.W)

exit_radio = ttk.Radiobutton(root, text="Exit", variable=entry_exit_var, value="Exit")
exit_radio.grid(row=5, column=1, padx=85, pady=5, sticky=tk.W)

# Create and place the submit button
submit_button = ttk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=6, column=0, columnspan=1,padx=60, pady=5)

refresh_button = ttk.Button(root, text="Refresh", command=refresh_form)
refresh_button.grid(row=6, column=1, columnspan=1,padx=60   , pady=5)

list_button = ttk.Button(root, text="List", command=open_list_gui)
list_button.grid(row=7, column=0, columnspan=2, pady=10)

# Create and place the label for displaying the result
result_label = ttk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=4, pady=10)



# Start the main loop
root.mainloop()
