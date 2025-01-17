#from tkinter import *

from PIL import Image
from tkinter import ttk
from tkcalendar import *
from customtkinter import *
from customtkinter import CTkImage
from supabase import create_client, Client
from matplotlib.figure import Figure  # type: ignore
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from datetime import timedelta
import math
import re
import bcrypt

url: str ="https://wzzxpvdkqhyomheehkjt.supabase.co"
key: str ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enhwdmRrcWh5b21oZWVoa2p0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQxMzM4NjIsImV4cCI6MjA0OTcwOTg2Mn0.91tW7zUqoFKp8ozJBKBTM4Uw6llTTXJB511uFCg6ARU"
supabase: Client = create_client(url, key)
user_id = None
def exitBtnPressed():
    print("Exit button clicked")
    window.destroy()

def okButtonPressed():
    InputPage.tkraise()

def saveBtnPressed():
    print("Save button clicked")
    kategorijaValue = kategorija.get()
    datumValue = datum.get_date().strftime('%Y-%m-%d')
    iznosValue = iznos.get("1.0",'end-1c')
    opisValue = opis.get("1.0",'end-1c')
    if(iznosValue != "" and iznosValue.isnumeric and opisValue != ""):
        response = supabase.table("Transakcije").insert({
            "Kategorija": kategorijaValue,
            "Datum": datumValue,
            "Iznos": iznosValue,
            "Opis": opisValue,
            "user_id": user_id
        }).execute()
        print(response)
        iznos.delete('1.0', END)
        opis.delete('1.0', END)
    else:
        if (iznosValue == "" or not iznosValue.isnumeric):
            message.configure(text = "Iznos mora biti brojčana vrijednost!")
        else:
            message.configure(text = "Opis nemože biti prazan!")
        Alert.tkraise()

def inputBtnPressed():
    print("Main button clicked")
    InputPage.tkraise()

def graphBtnPressed():
    print("Graph button clicked")
    GraphPage.tkraise()

def tableBtnPressed():
    print("Table button clicked")
    filterBtnPressed()
    TablePage.tkraise()

def filterBtnPressed():
    print("Filter button clicked")

    for widget in tableHolder.winfo_children():
        widget.destroy()

    tableColumns = ("Kategorija", "Datum", "Iznos", "Opis")

    for j in range(4): 
        b = CTkLabel(tableHolder, text=tableColumns[j], font=("Arial Bold", 16))
        b.grid(row=0, column=j)

    datumOdValue = filterDatumOd.get_date()
    datumDoValue = filterDatumDo.get_date()
    iznosOdValue = filterIznosOd.get("1.0",'end-1c')
    iznosDoValue = filterIznosDo.get("1.0",'end-1c')

    categoryTableFilterArray = []
    if(placaTableCheck.get() == 1):
        categoryTableFilterArray.append("Placa")
    if(hranaTableCheck.get() == 1):
        categoryTableFilterArray.append("Hrana")
    if(racuniTableCheck.get() == 1):
        categoryTableFilterArray.append("Racuni")
    if(autoTableCheck.get() == 1):
        categoryTableFilterArray.append("Auto")
    if(stanTableCheck.get() == 1):
        categoryTableFilterArray.append("Stan")
    if(ostaloTableCheck.get() == 1):
        categoryTableFilterArray.append("Ostalo")

    if(datumOdValue == datumDoValue):
        if(iznosOdValue != "" and iznosDoValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte("Iznos", iznosDoValue).gte("Iznos", iznosOdValue).execute()
        elif(iznosOdValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).gte("Iznos", iznosOdValue).execute()
        elif(iznosDoValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte("Iznos", iznosDoValue).execute()
        else:
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).execute()

        if response.data:
            databaseData = list(response.data)
            databaseData.sort(key=lambda x: x['Datum'])

            filteredData = [row for row in databaseData if row['user_id'] == user_id]

            if filteredData:
                for i, row in enumerate(filteredData, start=1):
                    CTkLabel(tableHolder, text=row['Kategorija'], font=("Arial", 16), width=100).grid(row=i, column=0)
                    CTkLabel(tableHolder, text=row['Datum'], font=("Arial", 16), width=100).grid(row=i, column=1)
                    CTkLabel(tableHolder, text=row['Iznos'], font=("Arial", 16), width=70).grid(row=i, column=2)
                    CTkLabel(tableHolder, text=row['Opis'], font=("Arial", 16), width=330).grid(row=i, column=3)
            else:
                CTkLabel(tableHolder, text="Nema podataka za ovog korisnika", font=("Arial", 16)).grid(row=1, column=0, columnspan=4)
        else:
            CTkLabel(tableHolder, text="Nema podataka", font=("Arial", 16)).grid(row=1, column=0, columnspan=4)

    else:
        if(iznosOdValue != "" and iznosDoValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte('Datum', datumDoValue).gte('Datum', datumOdValue).lte("Iznos", iznosDoValue).gte("Iznos", iznosOdValue).execute()
        elif(iznosOdValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte('Datum', datumDoValue).gte('Datum', datumOdValue).gte("Iznos", iznosOdValue).execute()
        elif(iznosDoValue != ""):
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte('Datum', datumDoValue).gte('Datum', datumOdValue).lte("Iznos", iznosDoValue).execute()
        else:
            response = supabase.table("Transakcije").select("*").in_("Kategorija", categoryTableFilterArray).lte('Datum', datumDoValue).gte('Datum', datumOdValue).execute()

        if response.data:
            databaseData = list(response.data)
            databaseData.sort(key=lambda x: x['Datum'])
            filteredData = [row for row in databaseData if row['user_id'] == user_id]

            if filteredData:
                for i, row in enumerate(filteredData, start=1):
                    CTkLabel(tableHolder, text=row['Kategorija'], font=("Arial", 16), width=100).grid(row=i, column=0)
                    CTkLabel(tableHolder, text=row['Datum'], font=("Arial", 16), width=100).grid(row=i, column=1)
                    CTkLabel(tableHolder, text=row['Iznos'], font=("Arial", 16), width=70).grid(row=i, column=2)
                    CTkLabel(tableHolder, text=row['Opis'], font=("Arial", 16), width=330).grid(row=i, column=3)
            else:
                CTkLabel(tableHolder, text="Nema podataka za ovog korisnika", font=("Arial", 16)).grid(row=1, column=0, columnspan=4)
        else:
            CTkLabel(tableHolder, text="Nema podataka", font=("Arial", 16)).grid(row=1, column=0, columnspan=4)

    
def promjenaGrafa(event):
    if (filterGrafKategorija.get() == "Stanje"):
        filterGrafIznosOd.delete('1.0', END)
        filterGrafIznosDo.delete('1.0', END)
        placaCheck.set(0)
        hranaCheck.set(0)
        racuniCheck.set(0)
        autoCheck.set(0)
        stanCheck.set(0)
        ostaloCheck.set(0)

        filterGrafIznosOd.configure(state = DISABLED)
        filterGrafIznosDo.configure(state = DISABLED)
        Button1.configure(state = DISABLED)
        Button2.configure(state = DISABLED)
        Button3.configure(state = DISABLED)
        Button4.configure(state = DISABLED)
        Button5.configure(state = DISABLED)
        Button6.configure(state = DISABLED)
    else:
        filterGrafIznosOd.configure(state = NORMAL)
        filterGrafIznosDo.configure(state = NORMAL)
        Button1.configure(state = NORMAL)
        Button2.configure(state = NORMAL)
        Button3.configure(state = NORMAL)
        Button4.configure(state = NORMAL)
        Button5.configure(state = NORMAL)
        Button6.configure(state = NORMAL)

def plot(): 
    datumOdValue = filterGrafDatumOd.get_date()
    datumDoValue = filterGrafDatumDo.get_date()

    if (filterGrafKategorija.get() == "Stanje"):
        ax.clear()

        if(datumOdValue == datumDoValue):
            response = supabase.table("Transakcije").select("Datum").order("Datum").execute()
            dates = []
            for i, row in enumerate(response.data, start=1):
                dates.append(dt.datetime.strptime(row["Datum"], "%Y-%m-%d"))
            dates = sorted(set(dates))
            response = supabase.table("Transakcije").select("Datum").order("Datum").execute()
        else:
            response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).gte('Datum', datumOdValue).order("Datum").execute()
            dates = []
            dates.append(dt.datetime.combine(datumOdValue, dt.datetime.min.time()))
            for i, row in enumerate(response.data, start=1):
                dates.append(dt.datetime.strptime(row["Datum"], "%Y-%m-%d"))
            dates.append(dt.datetime.combine(datumDoValue, dt.datetime.min.time()))
            dates = sorted(set(dates))
            response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).order("Datum").execute()
        
        datesAll = []

        for i, row in enumerate(response.data, start=1):
            datesAll.append(dt.datetime.strptime(row["Datum"], "%Y-%m-%d"))

        datesAll.append(dt.datetime.combine(datumOdValue, dt.datetime.min.time()))
        datesAll.append(dt.datetime.combine(datumDoValue, dt.datetime.min.time()))

        datesAll = sorted(set(datesAll))

        values = []

        sum = 0
        oldSum = 0

        for date in datesAll:
            response = supabase.table("Transakcije").select("*").eq("Datum", date).execute()

            if response.data:
                for i, row in enumerate(response.data, start=1):
                    if row['Kategorija'] == "Placa":
                        sum += row['Iznos']
                    else:
                        sum -= row['Iznos']
                
                if (date in dates):
                    if date - dt.timedelta(days=1) in dates:
                        values.append(sum)
                    else:
                        dates.append(date - dt.timedelta(days=1))
                        values.append(oldSum)
                        values.append(sum)
            else:
                values.append(sum)

            oldSum = sum

        dates = sorted(set(dates))

        fig.autofmt_xdate(rotation=90)

        print(dates)

        a = dates[dates.__len__()-1]
        b = dates[0]
        dayVar = a-b

        fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=math.ceil((dates[dates.__len__()-1]-dates[0]).days/30)))

        ax.grid(True, color="dimgrey", zorder=0)

        ax.plot(dates,values, zorder=3, linewidth=2)
        ax.fill_between(dates, values, alpha=0.5)

        canvas.draw()

    else:
        ax.clear()

        categoryFilterArray = []
        if(placaCheck.get() == 1):
            categoryFilterArray.append("Placa")
        if(hranaCheck.get() == 1):
            categoryFilterArray.append("Hrana")
        if(racuniCheck.get() == 1):
            categoryFilterArray.append("Racuni")
        if(autoCheck.get() == 1):
            categoryFilterArray.append("Auto")
        if(stanCheck.get() == 1):
            categoryFilterArray.append("Stan")
        if(ostaloCheck.get() == 1):
            categoryFilterArray.append("Ostalo")

        print(categoryFilterArray)

        if(datumOdValue == datumDoValue):
            if (filterGrafIznosOd.get("1.0",'end-1c') != "" and filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").in_("Kategorija", categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).order("Datum").execute()
            elif (filterGrafIznosOd.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").in_("Kategorija", categoryFilterArray).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).order("Datum").execute()
            elif (filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").in_("Kategorija", categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).order("Datum").execute()
            else:
                response = supabase.table("Transakcije").select("Datum").in_("Kategorija", categoryFilterArray).order("Datum").execute()

            dates = []
            for i, row in enumerate(response.data, start=1):
                dates.append(dt.datetime.strptime(row["Datum"], "%Y-%m-%d"))
            dates = sorted(set(dates))
            
        else:
            if (filterGrafIznosOd.get("1.0",'end-1c') != "" and filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).gte('Datum', datumOdValue).in_("Kategorija", categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).order("Datum").execute()
            elif (filterGrafIznosOd.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).gte('Datum', datumOdValue).in_("Kategorija", categoryFilterArray).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).order("Datum").execute()
            elif (filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).gte('Datum', datumOdValue).in_("Kategorija", categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).order("Datum").execute()
            else:
                response = supabase.table("Transakcije").select("Datum").lte('Datum', datumDoValue).gte('Datum', datumOdValue).in_("Kategorija", categoryFilterArray).order("Datum").execute()

            dates = []
            dates.append(dt.datetime.combine(datumOdValue, dt.datetime.min.time()))
            for i, row in enumerate(response.data, start=1):
                dates.append(dt.datetime.strptime(row["Datum"], "%Y-%m-%d"))
            dates.append(dt.datetime.combine(datumDoValue, dt.datetime.min.time()))
            dates = sorted(set(dates))

        values = []
        colors = []

        for date in dates:
            if (filterGrafIznosOd.get("1.0",'end-1c') != "" and filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("*").eq("Datum", date).in_('Kategorija', categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).execute()
            elif (filterGrafIznosOd.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("*").eq("Datum", date).in_('Kategorija', categoryFilterArray).gte("Iznos", filterGrafIznosOd.get("1.0",'end-1c')).execute()
            elif (filterGrafIznosDo.get("1.0",'end-1c') != ""):
                response = supabase.table("Transakcije").select("*").eq("Datum", date).in_('Kategorija', categoryFilterArray).lte("Iznos", filterGrafIznosDo.get("1.0",'end-1c')).execute()
            else:
                response = supabase.table("Transakcije").select("*").eq("Datum", date).in_('Kategorija', categoryFilterArray).execute()
        
            print(response.data)

            if response.count:
                print("aaaaaaaaaaaaaaaaaaaaaaaa")

            filteredData = [row for row in response.data if row['user_id'] == user_id]

            if filteredData:
                print("Filtered data found!")
                sum = 0
                for i, row in enumerate(filteredData, start=1):
                    if row['Kategorija'] == "Placa":
                        sum += row['Iznos']
                    else:
                        sum -= row['Iznos']

                values.append(sum)
                if sum >= 0:
                    colors.append("green")
                else:
                    colors.append("red")
            else:
                values.append(0)
                colors.append("gray")

        fig.autofmt_xdate(rotation=90)

        print(dates)

        a = dates[dates.__len__()-1]
        b = dates[0]
        dayVar = a-b

        fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=math.ceil((dates[dates.__len__()-1]-dates[0]).days/30)))

        ax.grid(True, color="dimgrey", zorder=0)

        ax.bar(dates,values, color=colors, zorder=3)

        canvas.draw()


        # creating the Matplotlib toolbar
        #toolbar = NavigationToolbar2Tk(canvas, window) 
        #toolbar.update() 
    
        # placing the toolbar on the Tkinter window 
        #canvas.get_tk_widget().pack() 


#Kreiranje windowa
window = CTk()
window.title("Transaction Master")


##centriranje
window_width = 850
window_height = 700
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)
window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

#Kreiranje frameova
InputPage = CTkFrame(window, width=850, height=700)
GraphPage = CTkFrame(window, width=850, height=700)
TablePage = CTkFrame(window, width=850, height=700)
Alert = CTkFrame(window, width=200, height=150)

for frame in (InputPage, GraphPage, TablePage, Alert):
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


#slike
home_icon = CTkImage(light_image=Image.open("mainicon.png"), size=(20, 20))
graph_icon = CTkImage(light_image=Image.open("graf.png"), size=(20, 20))
table_icon = CTkImage(light_image=Image.open("table.png"), size=(20, 20))




# Ekran za login
LoginPage = CTkFrame(window, width=850, height=700)
LoginPage.place(relx=0.5, rely=0.5, anchor=CENTER)
def registerBtnPressed():
    global user_id
    usernameValue = username.get()
    if not usernameValue or not password.get():
        loginMessage.configure(text="Username and password cannot be empty")
        return
    passwordValue = password.get()
    hashed_password = bcrypt.hashpw(passwordValue.encode('utf-8'), bcrypt.gensalt())
    supabase.table("Users").insert({
        "Username": usernameValue,
        "Password": hashed_password.decode('utf-8')
    }).execute()
    user_id = getUserId(username.get())
    print(f"User ID: {user_id}")
    InputPage.tkraise()

def loginBtnPressed():
    global user_id
    usernameValue = username.get()
    passwordValue = password.get()
    response = supabase.table("Users").select("Password").eq("Username", usernameValue).execute()
    if response.data:
        stored_hashed_password = response.data[0]['Password']
        if bcrypt.checkpw(passwordValue.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            user_id = getUserId(username.get())
            print(f"User ID: {user_id}")
            InputPage.tkraise()
        else:
            loginMessage.configure(text="Invalid credentials")
    else:
        loginMessage.configure(text="Invalid credentials")

loginTitle = CTkLabel(LoginPage, text="Login", font=("Arial Bold", 40))
loginTitle.place(relx=0.5, y=50, anchor=CENTER)

usernameLabel = CTkLabel(LoginPage, text="Username", font=("Arial Bold", 16))
usernameLabel.place(x=200, y=200)
username = CTkEntry(LoginPage, width=200, font=("Arial Bold", 16))
username.place(x=350, y=200)

passwordLabel = CTkLabel(LoginPage, text="Password", font=("Arial Bold", 16))
passwordLabel.place(x=200, y=250)
password = CTkEntry(LoginPage, width=200, font=("Arial Bold", 16), show="*")
password.place(x=350, y=250)

loginButton = CTkButton(LoginPage, width=70, height=40, text="Login", command=loginBtnPressed)
loginButton.place(x=350, y=300)

registerButton = CTkButton(LoginPage, width=70, height=40, text="Register", command=registerBtnPressed)
registerButton.place(x=450, y=300)

loginMessage = CTkLabel(LoginPage, text="", font=("Arial Bold", 16))
loginMessage.place(x=350, y=350)

def getUserId(username):
    response = supabase.table("Users").select("id").eq("Username", username).execute()
    if response.data:
        return response.data[0]['id']
    else:
        return None

LoginPage.tkraise()

# Logout button
def clearFields():
    username.delete(0, END)
    password.delete(0, END)
    loginMessage.configure(text="")

logoutButton = CTkButton(InputPage, width=70, height=40, text="Logout", command=lambda: [clearFields(), LoginPage.tkraise()])
logoutButton.place(x=600, y=600)

# Ekran za unos
title = CTkLabel(InputPage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)


label2 = CTkLabel(InputPage, text="Kategorija", font=("Arial Bold", 16))
label2.place(x=50, y=170)
kategorija = CTkComboBox(InputPage, height = 22, width = 200, font=("Arial Bold", 16),values = ["Placa", "Hrana", "Racuni","Auto","Stan","Ostalo"])
kategorija.place(x=200, y=170)

label3 = CTkLabel(InputPage, text="Datum", font=("Arial Bold", 16))
label3.place(x=50, y=205)
datum = DateEntry(InputPage, height = 1, width = 20, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024,)
datum.place(x=200, y=205)

label4 = CTkLabel(InputPage, text="Iznos(€)", font=("Arial Bold", 16))
label4.place(x=50, y=240)
iznos = CTkTextbox(InputPage, height = 1, width = 200, font=("Arial Bold", 16))
iznos.place(x=200, y=240)


label5 = CTkLabel(InputPage, text="Opis", font=("Arial Bold", 16))
label5.place(x=50, y=280)
opis = CTkTextbox(InputPage, height = 300, width = 400, font=("Arial Bold", 16))
opis.place(x=200, y=280)


save = CTkButton(InputPage, width=70,height=40, text="Dodaj", command=saveBtnPressed)
save.place(x=200, y=600)

exit = CTkButton(InputPage, width=70,height=40, text="Exit", command=exitBtnPressed)
exit.place(x=500, y=600)


main = CTkButton(InputPage, width=120,height=50, text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(InputPage, width=15,height=50,text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(InputPage, width=15,height=50,text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)



# Ekran za graf
title = CTkLabel(GraphPage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(GraphPage, width=120,height=50,text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(GraphPage, width=15,height=50, text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(GraphPage, width=15,height=50, text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)

filterGrafHolder = CTkFrame(GraphPage, width=200, height=600)
filterGrafHolder.pack()
filterGrafHolder.place(x=0, y=160)

filterGrafLabel1 = CTkLabel(filterGrafHolder, text="Filter", font=("Arial Bold", 16))
filterGrafLabel1.place(x=0, y=0)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Graf", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=30)
filterGrafKategorija = CTkComboBox(filterGrafHolder, height=20, width=200, font=("Arial Bold", 16), values=["Promet", "Stanje"], command=promjenaGrafa)
filterGrafKategorija.place(x=0, y=50)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Iznos", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=80)
filterGrafIznosOd = CTkTextbox(filterGrafHolder, height = 20, width = 75, font=("Arial Bold", 16))
filterGrafIznosOd.place(x=0, y=110)
filterGrafIznosDo = CTkTextbox(filterGrafHolder, height = 20, width = 75, font=("Arial Bold", 16))
filterGrafIznosDo.place(x=80, y=110)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Kategorija", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=140)
placaCheck = IntVar() 
hranaCheck = IntVar() 
racuniCheck = IntVar() 
autoCheck = IntVar() 
stanCheck = IntVar() 
ostaloCheck = IntVar() 
Button1 = ttk.Checkbutton(filterGrafHolder, text = "Placa", variable = placaCheck, onvalue = 1, offvalue = 0, width = 10) 
Button2 = ttk.Checkbutton(filterGrafHolder, text = "Hrana", variable = hranaCheck, onvalue = 1, offvalue = 0, width = 10) 
Button3 = ttk.Checkbutton(filterGrafHolder, text = "Racuni", variable = racuniCheck, onvalue = 1, offvalue = 0, width = 10) 
Button4 = ttk.Checkbutton(filterGrafHolder, text = "Auto", variable = autoCheck, onvalue = 1, offvalue = 0, width = 10) 
Button5 = ttk.Checkbutton(filterGrafHolder, text = "Stan", variable = stanCheck, onvalue = 1, offvalue = 0, width = 10) 
Button6 = ttk.Checkbutton(filterGrafHolder, text = "Ostalo", variable = ostaloCheck, onvalue = 1, offvalue = 0, width = 10) 
Button1.place(x=0, y=170)
Button2.place(x=0, y=190)
Button3.place(x=0, y=210)
Button4.place(x=0, y=230)
Button5.place(x=0, y=250)
Button6.place(x=0, y=270)

placaCheck.set(1)
hranaCheck.set(1)
racuniCheck.set(1)
autoCheck.set(1)
stanCheck.set(1)
ostaloCheck.set(1)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Datum", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=300)
filterGrafDatumOd = DateEntry(filterGrafHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterGrafDatumOd.place(x=0, y=340)
filterGrafDatumDo = DateEntry(filterGrafHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterGrafDatumDo.place(x=0, y=380)

filterGrafBtn = CTkButton(filterGrafHolder, width=15, text="Plot", command=plot)
filterGrafBtn.place(x=0, y=420)

graphHolder = CTkFrame(GraphPage, width=650, height=600)
graphHolder.pack()
graphHolder.place(x=200, y=160)

fig, ax = plt.subplots()

ax.set_facecolor("#333333")
ax.figure.set_facecolor("#333333")

ax.spines['top'].set_color("w")
ax.spines['bottom'].set_color("w")
ax.spines['left'].set_color("w")
ax.spines['right'].set_color("w")

ax.tick_params(axis='x', colors='w')
ax.tick_params(axis='y', colors='w')

ax.grid(True, color="dimgrey", zorder=0)

canvas = FigureCanvasTkAgg(fig, master = graphHolder)
canvas.get_tk_widget().place(x=0, y=0)








# Ekran za tablicu
title = CTkLabel(TablePage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(TablePage, width=120,height=50, text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(TablePage, width=120,height=50, text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(TablePage, width=120,height=50, text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)

filterHolder = CTkFrame(TablePage, width=200, height=600)
filterHolder.pack()
filterHolder.place(x=0, y=160)

filterLabel1 = CTkLabel(filterHolder, text="Filter", font=("Arial Bold", 16))
filterLabel1.place(x=90, y=0)

filterLabel2 = CTkLabel(filterHolder, text="Iznos", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=20)
filterLabel2 = CTkLabel(filterHolder, text="Od", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=45)
filterLabel2 = CTkLabel(filterHolder, text="Do", font=("Arial Bold", 10))
filterLabel2.place(x=80, y=45)
filterIznosOd = CTkTextbox(filterHolder, height = 1, width = 75, font=("Arial Bold", 16))
filterIznosOd.place(x=0, y=65)
filterIznosDo = CTkTextbox(filterHolder, height = 1, width = 75, font=("Arial Bold", 16))
filterIznosDo.place(x=80, y=65)

filterLabel2 = CTkLabel(filterHolder, text="Kategorija", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=140)

placaTableCheck = IntVar() 
hranaTableCheck = IntVar() 
racuniTableCheck = IntVar() 
autoTableCheck = IntVar() 
stanTableCheck = IntVar() 
ostaloTableCheck = IntVar() 
ButtonTable1 = ttk.Checkbutton(filterHolder, text = "Placa", variable = placaTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable2 = ttk.Checkbutton(filterHolder, text = "Hrana", variable = hranaTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable3 = ttk.Checkbutton(filterHolder, text = "Racuni", variable = racuniTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable4 = ttk.Checkbutton(filterHolder, text = "Auto", variable = autoTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable5 = ttk.Checkbutton(filterHolder, text = "Stan", variable = stanTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable6 = ttk.Checkbutton(filterHolder, text = "Ostalo", variable = ostaloTableCheck, onvalue = 1, offvalue = 0, width = 10) 
ButtonTable1.place(x=0, y=170)
ButtonTable2.place(x=0, y=190)
ButtonTable3.place(x=0, y=210)
ButtonTable4.place(x=0, y=230)
ButtonTable5.place(x=0, y=250)
ButtonTable6.place(x=0, y=270)

placaTableCheck.set(1)
hranaTableCheck.set(1)
racuniTableCheck.set(1)
autoTableCheck.set(1)
stanTableCheck.set(1)
ostaloTableCheck.set(1)

filterLabel2 = CTkLabel(filterHolder, text="Datum", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=300)
filterDatumOd = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumOd.place(x=0, y=330)
filterDatumDo = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumDo.place(x=0, y=370)

filterBtn = CTkButton(filterHolder, width=15, text="Filter", command=filterBtnPressed)
filterBtn.place(x=0, y=430)

tableHolder = CTkScrollableFrame(master=TablePage, width=620, height=520)
tableHolder.pack()
tableHolder.place(x=200, y=160)

LoginPage.tkraise()

window.mainloop()