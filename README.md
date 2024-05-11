<<<<<<< HEAD
Repository-ul contine doua proiecte C#, un proiect C++, un proiect Java si doua proiecte de IoT (la unul dintre ele s-a folosit Python)
=======
# IoT - Android Things - Team Project - Moldovan Bogdana 235/1 - Filipas Razvan 233/1

## Monitorizarea temperaturii si a umiditatii intr-o incapere | Analizarea datelor colectate

Programul colectează constant date despre temperatura și umiditate și le stochează într-o bază de date. Apoi, calculează media temperaturii și umidității pentru ultimele 24 de ore și pentru ultima oră. Aceste date pot fi utilizate ulterior pentru a analiza și monitoriza nivelurile de temperatură și umiditate într-o anumita locație. De aemenea, programul semnaleaza atunci cand temperatura sau umiditatea nu se incadreaza in diferiti parametrii.

Am stabilit ca temperatura standard intr-o incapere sa fie cuprinsa intre 18 si 24 grade Celsius, iar umiditatea intre 30% si 60%.

## Short demo

https://user-images.githubusercontent.com/100224995/230480193-18ea0c15-bcef-4e45-8401-7b1876a4cbe4.mp4

<img width="421" alt="pic" src="https://user-images.githubusercontent.com/117570113/230485451-235acfd6-b453-4c21-95ca-fb13fbd4af76.png">



## Schematics Plan

![tp](https://user-images.githubusercontent.com/117570113/230478170-6a943e1d-965c-4250-bbe5-2caa54fbf0e6.png)


## Pre-requisites
- Android Things compatible board - Arduino Uno
- 3 x jumper wires
- breadborad
- 1 x temperature and humidity sensor
- Power supply cable

## Setup and build
### Configurare hardware
Montajul este realizat urmand uramtorii pasi:
  1. se plaseaza modulul sensor de temperatura si umididate DHT11 pe breadboard
  2. se fac conexiunile cu placa Arduino UNO, folosind fire de tip "tata-tata", astfel:
        a. pinul VCC al modulului se conecteaza la pinul 5V al placii Arduino (in acest caz, am folosit unul de culoare rosie)
        b. pinul Signal al modulului se conecteaza la pinul Digital 7 al placii Arduino (in acest caz, am folosit unul  de culoare maro)
        c. pinul GND al modulului se conecteaza la pinul GND al placii Arduino (in acest caz, am folosit unul de culoare neagra)
  3. se face conexiunea cu un computer folosind un cablu de alimentare (in acest caz, am folosit un cablu cu mufa USB 3.0 pentru conectarea la computer si mufa USB B pentru conectarea la placa)

### Configurare software
Pentru testarea montajului la nivel software se foloseste Arduino IDE 2.x unde se selecteaza tipul placii folosite (Arduino Uno) si tipul portului utilizat (COM4)

Pentru dezvoltarea aplicatiei desktop se foloseste ca IDE PyCharm si ca limbaj de programare Python. Datele sunt stocate intr-o baza de date SQLite. Pentru furnizarea unei interfete s-a folosit biblioteca Tinker din Python.

Aplicatia face analiza valorilor umiditatii si temperaturii, afisand in fereastra temperatura curenta, umiditatea curenta, temperatura medie din ultima ora, umiditatea medie din ultima ora si temperatura, respectiv umiditatea medie din ultimele 24 de ore. Daca umididatea are valori cuprinse intre 30% si 60% se afiseaza mesajul "Umiditate optima", iar daca temperatura are valori cuprinse intre 24 si 18 grade se afiseaza mesajul "Temperatura optima". Pentru temperaturi cu valoari mai mari de 24 de grade se afiseaza "Temperatura mare", iar pentru temperaturi cu valori mai mici de 18 grade se afiseaza "Temperatura mica". Asemenea si pentru umiditate: daca umiditatea depaseste 60%, se afiseaza "Umiditate mare", iar daca are valoare mai mica decat 30%, se afieaza "Umiditate mica".

## Cod sursa Arduino

```
#include <dht.h>

dht DHT;

#define DHT11_PIN 7                     // Set pin 7 for reading

void setup() {
  Serial.begin(9600);                   // Set the serial begin
  pinMode(DHT11_PIN, INPUT);            // Set the pin to input for reading data
}

void loop() {
  DHT.read11(DHT11_PIN);                // Read the values of temperature and humidity from sensor
  Serial.print(DHT.temperature);        // Print the temperature value
  Serial.print(",");
  Serial.print(DHT.humidity);           // Print the humidity value
  Serial.println();
  delay(1000);                          // Detect the values every 1 sec
}
```

## Cod sursa Python

```
import serial
import tkinter as tk

from media import medii_24h, medii_1h
from adddata import add_data

arduino_port = 'COM4'
baud_rate = 9600


def read_from_arduino():
    # deschidem portul serial
    ser = serial.Serial(arduino_port, baud_rate)
    # citim datele
    data = ser.readline().decode().strip()
    # inchidem portul serial
    ser.close()
    # returnam datele sub forma de tuplu (temperatura, umiditate)
    return tuple(map(float, data.split(',')))

# functie pentru actualizarea etichetei cu valorile citite de la Arduino
def update_label():

    temperature, humidity = read_from_arduino()
    #temperature, humidity = 20,45
    add_data(temperature, humidity)

    temperature_label.config(font='TNR',bg="grey", text=f"Temperatura: {temperature:.2f} °C", anchor="w")
    humidity_label.config(font='TNR',bg="grey", text=f"Umiditate: {humidity:.2f}%", anchor="w")

    media_temp_24h, media_umid_24h = medii_24h()
    temperature_label_24h.config(font='TNR',bg="grey", anchor='w', text=f"Temperatura medie in ultimele 24h: {media_temp_24h:.2f} °C")
    humidity_label_24h.config(font='TNR',bg="grey", anchor='w', text=f"Umiditate medie in ultimele 24h: {media_umid_24h:.2f}%")

    media_temp_1h, media_umid_1h = medii_1h()
    temperature_label_1h.config(font='TNR',bg="grey", anchor='w', text=f"Temperatura medie in ultima ora: {media_temp_1h:.2f} °C")
    humidity_label_1h.config(font='TNR',bg="grey", anchor='w', text=f"Umiditate medie in ultima ora: {media_umid_1h:.2f}%")


    if humidity>60:
        umiditate_mare_label.pack()
        umiditate_mica_label.pack_forget()
        umiditate_optima_label.pack_forget()
    else:
        if humidity<30:
            umiditate_mare_label.pack_forget()
            umiditate_mica_label.pack()
            umiditate_optima_label.pack_forget()
        else:
            umiditate_mare_label.pack_forget()
            umiditate_mica_label.pack_forget()
            umiditate_optima_label.pack()

    if temperature>24:
        temperatura_mare_label.pack()
        temperatura_mica_label.pack_forget()
        temperatura_optima_label.pack_forget()
    else:
        if temperature<18:
            temperatura_mare_label.pack_forget()
            temperatura_mica_label.pack()
            temperatura_optima_label.pack_forget()
        else:
            temperatura_mare_label.pack_forget()
            temperatura_mica_label.pack_forget()
            temperatura_optima_label.pack()

    root.after(100, update_label)

root = tk.Tk()
root.title("Temperature and humidity from Arduino")
root.configure(bg='grey',border=5)

title_label= tk.Label(root,bg="grey",font='TNR', text="Monitorizarea temperaturii si a umiditatii", fg='lightblue')
title_label.pack(pady=20)


temperature_label = tk.Label(root,bg="grey",font='TNR', text="Temperatura: N/A °C", anchor="w")
temperature_label.pack()
humidity_label = tk.Label(root,bg="grey",font='TNR', text="Umiditate: N/A %", anchor='w')
humidity_label.pack()


temperature_label_24h = tk.Label(root,bg="grey", anchor='w',font='TNR', highlightcolor='grey', text="Temperatura medie in ultimele 24h: N/A °C")
temperature_label_24h.pack()
humidity_label_24h = tk.Label(root,bg="grey",font='TNR', anchor='w', text="Umiditate medie in ultimele 24h: N/A %")
humidity_label_24h.pack()

temperature_label_1h = tk.Label(root,bg="grey", anchor='w',font='TNR', highlightcolor='grey', text="Temperatura medie in ultima ora: N/A °C")
temperature_label_1h.pack()
humidity_label_1h = tk.Label(root,bg="grey",font='TNR', anchor='w', text="Umiditate medie in ultima ora: N/A %")
humidity_label_1h.pack()


umiditate_mare_label = tk.Label(root,bg="grey",font='TNR', text="Umiditate mare!", anchor='w', fg='orange')
umiditate_mare_label.pack_forget()
umiditate_mica_label = tk.Label(root,bg="grey",font='TNR', text="Umiditate mica!", anchor='w', fg='orange')
umiditate_mica_label.pack_forget()
umiditate_optima_label = tk.Label(root,bg="grey",font='TNR', text="Umiditate optima", anchor='w', fg='lightblue')
umiditate_optima_label.pack_forget()

temperatura_mare_label = tk.Label(root,bg="grey",font='TNR', text="Temperatura mare!", anchor='w', fg='orange')
temperatura_mare_label.pack_forget()
temperatura_mica_label = tk.Label(root,bg="grey",font='TNR', text="Temperatura mica!", anchor='w', fg='orange')
temperatura_mica_label.pack_forget()
temperatura_optima_label = tk.Label(root,bg="grey",font='TNR', text="Temperatura optima", anchor='w', fg='lightblue')
temperatura_optima_label.pack_forget()


root.after(1000, update_label)

root.mainloop()
```

```
import sqlite3
from datetime import datetime, timedelta

def medii_24h():
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    cursor.execute('SELECT * FROM parametrii WHERE timp BETWEEN ? AND ?', (start_time, end_time,))
    rows = cursor.fetchall()
    sum_temp = 0
    sum_umid = 0
    count = len(rows)
    for row in rows:
        sum_temp += row[1]
        sum_umid += row[2]

    media_temp = sum_temp / count
    media_umid = sum_umid / count

    conn.close()

    return media_temp, media_umid


def medii_1h():
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    cursor.execute('SELECT * FROM parametrii WHERE timp BETWEEN ? AND ?', (start_time, end_time,))
    rows = cursor.fetchall()
    sum_temp = 0
    sum_umid = 0
    count = len(rows)
    for row in rows:
        sum_temp += row[1]
        sum_umid += row[2]

    media_temp = sum_temp / count
    media_umid = sum_umid / count

    conn.close()

    return media_temp, media_umid
```
```
import sqlite3
import datetime

def add_data(temperatura, umiditate):
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parametrii (
            id INTEGER PRIMARY KEY,
            temperatura REAL,
            umiditate REAL,
            timp TEXT
        )
    ''')

    timp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO parametrii (temperatura, umiditate, timp) VALUES (?, ?, ?)', (temperatura, umiditate, timp))
    conn.commit()
    conn.close()

```
>>>>>>> 455be2b73eaf81535b1b63a8f905c6650ee1a4bd
