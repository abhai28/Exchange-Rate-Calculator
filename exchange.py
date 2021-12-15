#importing modules
from tkinter.constants import BOTTOM, CENTER, LEFT, TOP
import requests
import json
from datetime import date, datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo

#delcaring variables
url = 'https://v6.exchangerate-api.com/v6/e387ba33bc8873b856d25c41/latest/USD'
fileData = {}
fileFound = True

'''
    function creates file if it does not exist
    or if last time currency was updated is more then 6 hours
'''
def create_file():
    # Making our request
        response = requests.get(url)
        data = response.json()
        today = date.today()
        cur_date = today.strftime('%m/%d/%Y')
        now = datetime.now()
        cur_hour = now.strftime("%H") 
        #writing to json file
        data["date"]=cur_date
        data["hour"]=int(cur_hour)
        # Your JSON object
        with open('data.txt','w') as outfile:
            json.dump(data,outfile)
        return True

#function calculates the currency conversion
def currency_converter(first_cur, second_cur, first_rate, second_rate, amount):
    if(first_cur=="USD"):
        return(amount * second_rate)
    elif(second_cur=="USD"):
        return(amount/first_rate)
    else:
        return((amount/first_rate)*second_rate)

#retrieving data from file 
try:
    with open('data.txt') as json_file:
        fileData = json.load(json_file)
except:
    fileFound=False

if(fileFound==False):
    create_file()
    try:
        with open('data.txt') as json_file:
            fileData = json.load(json_file)
    except:
        fileFound=False
        
#checking if last time currencies were updates is more then 6 hours
cur_time = datetime.now()
cur_hour = int(cur_time.strftime("%H"))
if(cur_hour-fileData["hour"]>6 or cur_hour-fileData["hour"]<0):   
    fileFound = create_file()
    try:
        with open('data.txt') as json_file:
            fileData = json.load(json_file)
    except:
        fileFound=False
#getting all currency names 
currencies = list(fileData["conversion_rates"].keys())

#user interface
root = tk.Tk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo.png'))
#setting window size and title
root.geometry('600x400')
root.resizable(False,False)
root.title("Exchange Rate Calculator")

#function retries information from GUI and displays converted amount
def amount():
    first_cur = first_selected_cur.get()
    sec_cur = sec_selected_cur.get()
    amount = amount_text.get("1.0","end")
    first_rate = float(fileData["conversion_rates"][first_cur])
    sec_rate = float(fileData["conversion_rates"][sec_cur])
    if(first_cur==sec_cur):
        showinfo(
                message="Please select different currencies",
                title='Error'
            )
    elif(len(amount)<2):
        showinfo(
                message="Please enter value for amount",
                title="Error"
            )
    else:
        converted = "{:.2f}".format(currency_converter(first_cur,sec_cur,first_rate,sec_rate,float(amount)))
        showinfo(
                message="Amount = {}".format(converted),
                title="Calculation"
            )

#creating label
first_cur_label = ttk.Label(text="Please select Currency:")
first_cur_label.pack(fill=tk.X,padx=5,pady=5)

#creating combobox for user to select currency
first_selected_cur = tk.StringVar()
first_cur_box = ttk.Combobox(root, textvariable=first_selected_cur)
first_cur_box['values'] = currencies
first_cur_box['state'] = 'readonly'
first_cur_box.current(0)
first_cur_box.pack(fill=tk.X,padx=5,pady=5)

#function to get user selected value from combobox
def cur_changed(event):
    print(f'You selected {first_selected_cur.get()}!')

#binding function to combobox
first_cur_box.bind('<<ComboboxSelected>>',cur_changed)

#creating arrow image
arrow_img = Image.open("Down_Arrow_Icon.png")
arrow_img = arrow_img.resize((50,50),Image.ANTIALIAS)
arrow_img = ImageTk.PhotoImage(arrow_img)
arrow_label = tk.Label(image=arrow_img)
arrow_label.image = arrow_img
arrow_label.pack(fill=tk.X,padx=5,pady=5)

#creating label
sec_cur_label = ttk.Label(text="Please select Currency:")
sec_cur_label.pack(fill=tk.X,padx=5,pady=5)

#creating combobox for user to select currency
sec_selected_cur = tk.StringVar()
sec_cur_box = ttk.Combobox(root, textvariable=sec_selected_cur)
sec_cur_box['values'] = currencies
sec_cur_box['state'] = 'readonly'
sec_cur_box.current(0)
sec_cur_box.pack(fill=tk.X,padx=5,pady=5)

amount_label = ttk.Label(text="Enter amount:")
amount_label.pack(fill=tk.X,padx=5,pady=5,side=LEFT)

amount_text = tk.Text(root,height=1,width=30)
amount_text.config(wrap='none')
amount_text.pack(side=LEFT)

submit_btn = tk.Button(root,height=1,width=10,text="Convert",
                                        command=amount)
submit_btn.place(relx=0.5, rely=0.9, anchor=CENTER)

root.mainloop()