#from tkinter import *
from tkinter import ttk
from tkcalendar import *
from customtkinter import *

def saveBtnPressed():
    print("Save button clicked")
    kategorijaValue = kategorija.get()
    datumValue = datum.get_date()
    iznosValue = iznos.get("1.0",'end-1c')
    opisValue = opis.get("1.0",'end-1c')

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
iznos = CTkTextbox(InputPage, height = 1, width = 20, font=("Arial Bold", 16))
iznos.place(x=200, y=230)

label5 = CTkLabel(InputPage, text="Opis", font=("Arial Bold", 16))
label5.place(x=50, y=260)
opis = CTkTextbox(InputPage, height = 15, width = 40, font=("Arial Bold", 16))
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

for i in range(1, 10): #Rows
    for j in range(4): #Columns
        b = CTkLabel(tableHolder, text="12313123", font=("Arial", 16))
        b.grid(row=i, column=j)






window.mainloop()