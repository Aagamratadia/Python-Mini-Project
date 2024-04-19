import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime, timedelta
import mysql.connector
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aagam@03',
    'database': 'parkinglot',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS parking_rec(
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    vehicle_type VARCHAR(20),
    checkin_date DATE,
    checkin_time Time
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
Cars = 250
bicycles = 78


def save_to_database(vehicle_number, vehicle_type,checkin_date,checkin_time):
    insert_query = """
    INSERT INTO parking_rec (vehicle_number, vehicle_type,checkin_date,checkin_time)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (vehicle_number, vehicle_type,checkin_date,checkin_time))
    connection.commit()


def submit_form():
    # Get values from the entry widgets
    number_value = number_entry.get()
    type_value = type_entry.get()
    Spots_value=100
    entry_exit_value = entry_exit_var.get()
    current_datetime = datetime.now()
    Date.append(current_datetime.strftime("%y-%m-%d"))
    Time.append(current_datetime.strftime("%H:%M:%S"))
    
    # Convert time difference to hours
    if entry_exit_value=='Entry':
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result_label.config(text=f" - - - - - - - - - Details- - - - - - - - - \n\nNumber Plate: {number_value}\nTime of Entry: {current_time}\nEntry/Exit: {entry_exit_value}\nPrediction on {future_date}: {predicted_available_spaces[0]}")
        save_to_database(number_value,type_value,Date[-1],Time[-1])

    if entry_exit_value=='Exit': 
        check_in_time, check_out_time = calculate_check_times(entry_exit_value)
        checkout_time=datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
        print('checkout_time')
        checkin_time=datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
        time_difference = checkout_time - checkin_time
        # Convert time difference to hours
        hours_parked = time_difference.total_seconds() / 3600
        if type_value == "CYCLE":
                            rate_per_hour = 20
        elif type_value == "BIKE":
                            rate_per_hour = 40
        elif type_value == "CAR":
                            rate_per_hour = 60
        amt = float(hours_parked)*rate_per_hour
        result_label.config(text=f" - - - - - - - - - Details- - - - - - - - - \n\nNumber Plate: {number_value}\nType: {type_value}\nAmount: {amt} rps\nHours Parked: {hours_parked}\nTime of Exit: {checkout_time}\nEntry/Exit: {entry_exit_value}")
        save_to_database(number_value,type_value,Date[-1],Time[-1])


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

def get_available_spaces():
    # Fetch the count of each type of vehicle from the database
    cursor.execute("SELECT COUNT(*) FROM parking_rec WHERE vehicle_type='CYCLE'")
    available_cycles = bicycles - cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM parking_rec WHERE vehicle_type='BIKE'")
    available_bikes = bikes - cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM parking_rec WHERE vehicle_type='CAR'")
    available_cars = Cars - cursor.fetchone()[0]

    return available_cycles, available_bikes, available_cars



def open_list_gui():
    list_gui = tk.Toplevel(root)
    list_gui.title("List of Parked Vehicles")
    list_gui.geometry("800x300")

    label = ttk.Label(list_gui, text="Parked Vehicles:")
    label.grid(row=0, column=0, columnspan=2, pady=10)
    close_button = ttk.Button(list_gui, text="Close", command=list_gui.destroy)
    close_button.grid(row=1, column=0)

    # Create headers
    headers = ["Vehicle No.", "Vehicle Type", "Date", "Time"]
    for col, header in enumerate(headers):
        header_label = ttk.Label(list_gui, text=header)
        header_label.grid(row=1, column=col, padx=5, pady=5)

    # Fetch records from the database
    cursor.execute("SELECT vehicle_number, vehicle_type, checkin_date, checkin_time FROM parking_rec")
    records = cursor.fetchall()

    for row, record in enumerate(records, start=2):
        for col, value in enumerate(record):
            value_label = ttk.Label(list_gui, text=str(value))
            value_label.grid(row=row, column=col, padx=5, pady=5)

    available_cycles, available_bikes, available_cars = get_available_spaces()

    available_label = ttk.Label(list_gui, text=f"Available Spaces:\nCYCLE: {available_cycles}\nBIKE: {available_bikes}\nCAR: {available_cars}")
    available_label.grid(row=row + 1, column=0, columnspan=len(headers), pady=10)


    close_button = ttk.Button(list_gui, text="Close", command=list_gui.destroy)
    close_button.grid(row=row + 2, column=0, columnspan=len(headers), pady=10)
    






root = tk.Tk()
root.title("Parking Details")
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


submit_button = ttk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=6, column=0, columnspan=1,padx=60, pady=5)

refresh_button = ttk.Button(root, text="Refresh", command=refresh_form)
refresh_button.grid(row=6, column=1, columnspan=1,padx=60   , pady=5)

list_button = ttk.Button(root, text="List", command=open_list_gui)
list_button.grid(row=7, column=0, columnspan=2, pady=10)

# Create and place the label for displaying the result
result_label = ttk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=4, pady=10)

query = "SELECT checkin_date, available_cars FROM parking_rec"
df = pd.read_sql_query(query, connection)

connection.close()

df['checkin_date'] = pd.to_datetime(df['checkin_date'])

df['day_of_week'] = df['checkin_date'].dt.day_name()
df['month'] = df['checkin_date'].dt.month

df = pd.get_dummies(df, columns=['day_of_week'])

X = df.drop(['checkin_date', 'available_cars'], axis=1)
y = df['available_cars']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

plt.scatter(X_test['month'], y_test, color='black', label='Actual')
plt.scatter(X_test['month'], y_pred, color='blue', label='Predicted')
plt.xlabel('Month')
plt.ylabel('Available Spaces')
plt.legend()
# plt.show()




future_date = datetime.strptime('2023-12-15', '%Y-%m-%d')
future_day_of_week = future_date.strftime('%A')
future_month = future_date.month
future_data = pd.get_dummies(pd.DataFrame({
    'month': [future_month],
    'day_of_week': [future_day_of_week]
}), columns=['day_of_week'])
missing_columns = set(X_train.columns) - set(future_data.columns)
for col in missing_columns:
    future_data[col] = 0

# Re-order columns to match the order in X_train
future_data = future_data[X_train.columns]

predicted_available_spaces = model.predict(future_data)
print(f"Predicted Available Spaces on {future_date}: {predicted_available_spaces[0]}")


root.mainloop()