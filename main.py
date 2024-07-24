import requests
import json
import tkinter as tk
from tkinter import ttk
from threading import Thread
from tkinter import messagebox

# Function to get all the latest currency rates from the API.
def fetch_latest_currency_rates():
    # Checking if there is Internet connection using try except block.
    try:
        latest_currency_rate_response = requests.get("https://api.currencyapi.com/v3/latest",headers=headers)
        if latest_currency_rate_response.status_code==200:
            latest_currency_rate_obj = json.loads(latest_currency_rate_response.content)
            currency_data = latest_currency_rate_obj["data"]
            currency_data_keys = currency_data.keys()
            for every_currency_code in currency_data_keys:
                currency_rates_dict.update({every_currency_code:currency_data.get(every_currency_code).get("value")})
        elif latest_currency_rate_response.status_code==500:
            messagebox.showinfo("Internal error","Try again later!")
    except:
        messagebox.showwarning("No Internet connection","Please check your Internet connection!")
def thread_fetch_latest_currency_rates():
    thread_var = Thread(target=fetch_latest_currency_rates())
    thread_var.start()

# Function to get all the currency names and its equivalent currency code from the CurrencyAPI.
def fetch_currency_name_with_code():
    try:
        response = requests.get("https://api.currencyapi.com/v3/currencies",headers=headers)
        if response.status_code==200:
            response_obj = json.loads(response.content)
            for curr_code in response_obj["data"]:
                currency_names_to_code_dict.update({response_obj["data"].get(curr_code).get("name"):curr_code})
        elif response.status_code==429:
            messagebox.showinfo("Access limit exceeded","You have exceeded your free limit to access.\n Try again from next month.")
        else:
            messagebox.showinfo("Some error occurred","Try again after some time.\nPlease check you have a stable Internet connection")
    except:
        messagebox.showinfo("No Internet connection","Your device is not connected to the Internet")

# Function to check if the given string 'value' is a valid currency with only digits, and not other characters.
def check_if_valid_amount(value):
    count_dot = value.count(".")
    if count_dot>1:
        return False
    for ch in value:
        if ch!="." and str(ch).isdigit()==False:
            return False
    return True

# Function to perform the currency conversion based on the rates fetched from the API.
def convert_amount_to_specific_currency():
    if user_entered.get()=="" or user_entered.get().isspace() or check_if_valid_amount(user_entered.get())==False:
        converted_answer.config(text="Invalid input entered! Please enter any number")
    else:
        if len(currency_rates_dict) == 0:
            thread_fetch_latest_currency_rates()
        amount = float(user_entered.get())
        if from_currency.get()==n.get():
            converted_answer.config(text="")
            messagebox.showerror("Error","Same currency! Could not convert\nPlease choose different currency to convert.")
        else:
            from_code = currency_names_to_code_dict.get(currency_names_list[cbbx_from.current()])
            value_of_1usd_in_from_currency = currency_rates_dict.get(from_code)
            value_of_1_from_currency = 1/value_of_1usd_in_from_currency
            value_of_1_to_currency = currency_rates_dict.get(currency_names_to_code_dict.get(n.get()))
            # Multiply the 'amount' value with the value of the 1 currency to convert.
            answer = amount*(value_of_1_from_currency*value_of_1_to_currency)
            answer = str(answer)[:str(answer).find(".")+3]
            converted_answer.config(text=f"{amount} {from_code} = {answer} {currency_names_to_code_dict.get(n.get())}")

# Thread function to conver the currencies.
def thread_convert_amount_to_specific_currency():
    thread_var = Thread(target=convert_amount_to_specific_currency())
    thread_var.start()

# GUI creation
root = tk.Tk()
root.title("Currency Converter")
root.geometry("650x300")
color_primary = "#82ccdd"
root.config(bg=color_primary)
app_icon = tk.PhotoImage(file="currency-exchange.png")
my_api_key = "YOUR_CURRENCYAPI_API_KEY"
currency_rates_dict = {}
# Dictionary containing currency names to currency codes.
# US Dollar => USD
currency_names_to_code_dict = {}
# Initializing the headers for calling the CurrencyAPI.
headers = {
    'apikey': my_api_key
}
user_entered = tk.StringVar()
tk.Label(root,text="Enter the amount to convert",font=("Times New Roman",16),bg=color_primary,fg="#000000").pack(pady=15)
entry1 = tk.Entry(root,textvariable=user_entered,font=("Arial",15))
entry1.pack(pady=1)
# Fetch the list of currency names and currency codes.
fetch_currency_name_with_code()
n = tk.StringVar()
currency_names_list = list(currency_names_to_code_dict.keys())
# Frame
frame1 = tk.Frame(root,background=color_primary)
frame1.pack(pady=17)
from_currency = tk.StringVar()
# Combobox to set the initial currency.
cbbx_from = ttk.Combobox(frame1,width=30,textvariable=from_currency,font=("Arial",12))
cbbx_from['values'] = currency_names_list
cbbx_from.insert(0,currency_names_list[0])
cbbx_from.grid(row=0,column=0,padx=10)
# Combobox to set the final currency to convert to.
combobox_to = ttk.Combobox(frame1, width=30, textvariable=n,font=("Arial",12))
combobox_to['values'] = currency_names_list
combobox_to.grid(row=0,column=1,padx=10)
combobox_to.insert(0,currency_names_list[65])
# Button
convert_btn = tk.Button(root,text="Convert",command=thread_convert_amount_to_specific_currency,bg="#0000FF",fg="#ffffff",font=("Arial",13),activebackground="#0000FF")
convert_btn.pack()
# Label to display the conversion result.
converted_answer = tk.Label(root,font=("Arial",14),bg=color_primary)
converted_answer.pack(pady=16)
# Setting icon of app
root.iconphoto(True,app_icon)
root.mainloop()
