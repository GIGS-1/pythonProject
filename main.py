#from tkinter import *
from tkinter import ttk
from tkcalendar import *
from customtkinter import *
import os
from supabase import create_client, Client

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

#Kreiranje windowa
window = CTk()
window.title("Transaction Master")
window.geometry('850x700')

#Kreiranje frameova
InputPage = CTkFrame(window, width=850, height=700)
GraphPage = CTkFrame(window, width=850, height=700)
TablePage = CTkFrame(window, width=850, height=700)

InputPage.place(x=0, y=0)
GraphPage.place(x=0, y=0)
TablePage.place(x=0, y=0)


# Ekran za unos
title = CTkLabel(InputPage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

label1 = CTkLabel(InputPage, text="Dodaj novi zapis", font=("Arial Bold", 18))
label1.place(x=50, y=130)

label2 = CTkLabel(InputPage, text="Kategorija", font=("Arial Bold", 16))
label2.place(x=50, y=170)
kategorija = ttk.Combobox(InputPage, height = 1, width = 20, font=("Arial Bold", 16))
kategorija['values'] = ("Placa", "Hrana", "Racuni")
kategorija.place(x=200, y=170)

label3 = CTkLabel(InputPage, text="Datumm", font=("Arial Bold", 16))
label3.place(x=50, y=200)
datum = DateEntry(InputPage, height = 1, width = 20, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
datum.place(x=200, y=200)

label4 = CTkLabel(InputPage, text="Iznos", font=("Arial Bold", 16))
label4.place(x=50, y=230)
iznos = CTkTextbox(InputPage, height = 1, width = 100, font=("Arial Bold", 16))
iznos.place(x=200, y=230)

label5 = CTkLabel(InputPage, text="Opis", font=("Arial Bold", 16))
label5.place(x=50, y=260)
opis = CTkTextbox(InputPage, height = 100, width = 400, font=("Arial Bold", 16))
opis.place(x=200, y=260)

save = CTkButton(InputPage, width=10, text="Spremi", command=saveBtnPressed)
save.place(x=700, y=598)

main = CTkButton(InputPage, width=15, text="Main", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(InputPage, width=15, text="Prikaz grafa", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(InputPage, width=15, text="Prikaz transakcija", command=tableBtnPressed)
table.place(x=500, y=100)


# Ekran za graf
title = CTkLabel(GraphPage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(GraphPage, width=15, text="Main", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(GraphPage, width=15, text="Prikaz grafa", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(GraphPage, width=15, text="Prikaz transakcija", command=tableBtnPressed)
table.place(x=500, y=100)


# Ekran za tablicu
title = CTkLabel(TablePage, text="Transaction Master", font=("Arial Bold", 40))
title.place(relx=0.5, y=50, anchor=CENTER)

main = CTkButton(TablePage, width=15, text="Main", command=inputBtnPressed)
main.place(x=200, y=100)

graph = CTkButton(TablePage, width=15, text="Prikaz grafa", command=graphBtnPressed)
graph.place(x=350, y=100)

table = CTkButton(TablePage, width=15, text="Prikaz transakcija", command=tableBtnPressed)
table.place(x=500, y=100)

filterHolder = CTkFrame(TablePage, width=200, height=600)
filterHolder.pack()
filterHolder.place(x=0, y=160)

filterLabel1 = CTkLabel(filterHolder, text="Filter", font=("Arial Bold", 16))
filterLabel1.place(x=0, y=0)

filterLabel2 = CTkLabel(filterHolder, text="Iznos", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=30)
filterIznosOd = CTkTextbox(filterHolder, height = 1, width = 5, font=("Arial Bold", 16))
filterIznosOd.place(x=0, y=50)
filterIznosDo = CTkTextbox(filterHolder, height = 1, width = 5, font=("Arial Bold", 16))
filterIznosDo.place(x=80, y=50)

filterLabel2 = CTkLabel(filterHolder, text="Kategorija", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=80)
filterKategorija = ttk.Combobox(filterHolder, height = 1, width = 10, font=("Arial Bold", 16))
filterKategorija['values'] = ("Placa", "Hrana", "Racuni")
filterKategorija.place(x=0, y=110)

filterLabel2 = CTkLabel(filterHolder, text="Datum", font=("Arial Bold", 10))
filterLabel2.place(x=0, y=140)
filterDatumOd = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumOd.place(x=0, y=180)
filterDatumDo = DateEntry(filterHolder, height = 1, width = 10, font=("Arial Bold", 16), date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=4, Calendar =2024)
filterDatumDo.place(x=0, y=220)

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


window.mainloop()