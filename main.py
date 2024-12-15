#from tkinter import *

from PIL import Image
from tkinter import  ttk
from tkcalendar import *
from customtkinter import *
from customtkinter import CTkImage
from supabase import create_client, Client
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

url: str ="https://wzzxpvdkqhyomheehkjt.supabase.co"
key: str ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind6enhwdmRrcWh5b21oZWVoa2p0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQxMzM4NjIsImV4cCI6MjA0OTcwOTg2Mn0.91tW7zUqoFKp8ozJBKBTM4Uw6llTTXJB511uFCg6ARU"
supabase: Client = create_client(url, key)

def saveBtnPressed():
    print("Save button clicked")
    kategorijaValue = kategorija.get()
    datumValue = datum.get_date().strftime('%Y-%m-%d')
    iznosValue = iznos.get("1.0",'end-1c')
    opisValue = opis.get("1.0",'end-1c')
    response = supabase.table("Transakcije").insert({
        "Kategorija": kategorijaValue,
        "Datum": datumValue,
        "Iznos": iznosValue,
        "Opis": opisValue
    }).execute()
    print(response)
    #provjeri da su dobre vrijednosti i spremi u bazu

def inputBtnPressed():
    print("Main button clicked")
    InputPage.tkraise()

def graphBtnPressed():
    print("Graph button clicked")
    GraphPage.tkraise()

def tableBtnPressed():
    print("Table button clicked")
    TablePage.tkraise()

def filterBtnPressed():
    print("Filter button clicked")
    kategorijaValue = filterKategorija.get()
    datumOdValue = filterDatumOd.get_date()
    datumDoValue = filterDatumDo.get_date()
    iznosOdValue = filterIznosOd.get("1.0",'end-1c')
    iznosDoValue = filterIznosDo.get("1.0",'end-1c')
    
def plot(): 
    datumOdValue = filterGrafDatumOd.get_date()
    datumDoValue = filterGrafDatumDo.get_date()
    od = dt.datetime.combine(datumOdValue, dt.datetime.now().time())
    do = dt.datetime.combine(datumDoValue, dt.datetime.now().time())
    days = mdates.drange(od,do,dt.timedelta(days=1))
    fig = Figure(figsize = (5, 5), dpi = 100) 
    
    y = np.random.rand(days.__len__())
  
    plot1 = fig.add_subplot(111) 

    fig.autofmt_xdate(rotation=90)

    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

    plot1.plot(days,y)
    
    canvas = FigureCanvasTkAgg(fig, master = graphHolder)
    canvas.draw()
  
    canvas.get_tk_widget().place(x=0, y=0) 
  
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

for frame in (InputPage, GraphPage, TablePage):
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)


#slike
home_icon = CTkImage(light_image=Image.open("mainicon.png"), size=(20, 20))
graph_icon = CTkImage(light_image=Image.open("graf.jpg"), size=(20, 20))
table_icon = CTkImage(light_image=Image.open("table.png"), size=(20, 20))







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


save = CTkButton(InputPage, width=10, text="Dodaj", command=saveBtnPressed)
save.place(x=700, y=598)


main = CTkButton(InputPage, width=15, text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(InputPage, width=15, text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(InputPage, width=15, text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)







# Ekran za graf
title = CTkLabel(GraphPage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(GraphPage, width=15, text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(GraphPage, width=15, text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(GraphPage, width=15, text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)

filterGrafHolder = CTkFrame(GraphPage, width=200, height=600)
filterGrafHolder.pack()
filterGrafHolder.place(x=0, y=160)

filterGrafLabel1 = CTkLabel(filterGrafHolder, text="Filter", font=("Arial Bold", 16))
filterGrafLabel1.place(x=0, y=0)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Iznos", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=30)
filterGrafIznosOd = CTkTextbox(filterGrafHolder, height = 20, width = 50, font=("Arial Bold", 16))
filterGrafIznosOd.place(x=0, y=50)
filterGrafIznosDo = CTkTextbox(filterGrafHolder, height = 20, width = 50, font=("Arial Bold", 16))
filterGrafIznosDo.place(x=80, y=50)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Kategorija", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=80)
filterGrafKategorija = CTkComboBox(filterGrafHolder, height=20, width=200, font=("Arial Bold", 16), values=["Placa", "Hrana", "Racuni"])
filterGrafKategorija.place(x=0, y=110)

filterGrafLabel2 = CTkLabel(filterGrafHolder, text="Datum", font=("Arial Bold", 10))
filterGrafLabel2.place(x=0, y=140)
filterGrafDatumOd = DateEntry(filterGrafHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterGrafDatumOd.place(x=0, y=180)
filterGrafDatumDo = DateEntry(filterGrafHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterGrafDatumDo.place(x=0, y=220)

filterGrafBtn = CTkButton(filterGrafHolder, width=15, text="Filter", command=plot)
filterGrafBtn.place(x=0, y=250)

graphHolder = CTkFrame(GraphPage, width=650, height=600)
graphHolder.pack()
graphHolder.place(x=200, y=160)








# Ekran za tablicu
title = CTkLabel(TablePage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(TablePage, width=15, text="Main", image=home_icon, compound="left", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(TablePage, width=15, text="Prikaz Grafa", image=graph_icon, compound="left", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(TablePage, width=15, text="Prikaz transakcija", image=table_icon, compound="left", command=tableBtnPressed)
table.place(x=500, y=100)

filterHolder = CTkFrame(TablePage, width=200, height=600)
filterHolder.pack()
filterHolder.place(x=0, y=160)

filterLabel1 = CTkLabel(filterHolder, text="Filter", font=("Arial Bold", 16))
filterLabel1.place(x=0, y=0)

filterLabel2 = CTkLabel(filterHolder, text="Iznos", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=20)
filterLabel2 = CTkLabel(filterHolder, text="Od", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=45)
filterLabel2 = CTkLabel(filterHolder, text="Do", font=("Arial Bold", 10))
filterLabel2.place(x=80, y=45)
filterIznosOd = CTkTextbox(filterHolder, height = 1, width = 50, font=("Arial Bold", 16))
filterIznosOd.place(x=0, y=65)
filterIznosDo = CTkTextbox(filterHolder, height = 1, width = 50, font=("Arial Bold", 16))
filterIznosDo.place(x=80, y=65)

filterLabel2 = CTkLabel(filterHolder, text="Kategorija", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=100)
filterKategorija = CTkComboBox(filterHolder, height = 22, width = 200, font=("Arial Bold", 16),values = ["Placa", "Hrana", "Racuni","Auto","Stan","Ostalo"])
filterKategorija.place(x=0, y=130)

filterLabel2 = CTkLabel(filterHolder, text="Datum", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=170)
filterDatumOd = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumOd.place(x=0, y=200)
filterDatumDo = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumDo.place(x=0, y=240)

filterBtn = CTkButton(filterHolder, width=15, text="Filter", command=filterBtnPressed)
filterBtn.place(x=0, y=300)

tableHolder = CTkFrame(TablePage, width=650, height=600)
tableHolder.pack()
tableHolder.place(x=200, y=160)

tableColumns = ("Kategorija", "Datum", "Iznos", "Opis")

for j in range(4): #Columns
    b = CTkLabel(tableHolder, text=tableColumns[j], font=("Arial Bold", 16))
    b.grid(row=0, column=j)

response = supabase.table("Transakcije").select("*").execute()

if response.data:
    for i, row in enumerate(response.data, start=1): 
        CTkLabel(tableHolder, text=row['Kategorija'], font=("Arial", 16)).grid(row=i, column=0)
        CTkLabel(tableHolder, text=row['Datum'], font=("Arial", 16)).grid(row=i, column=1)
        CTkLabel(tableHolder, text=row['Iznos'], font=("Arial", 16)).grid(row=i, column=2)
        CTkLabel(tableHolder, text=row['Opis'], font=("Arial", 16)).grid(row=i, column=3)
else:
    CTkLabel(tableHolder, text="Nema podataka", font=("Arial", 16)).grid(row=1, column=0, columnspan=4)

InputPage.tkraise()

window.mainloop()