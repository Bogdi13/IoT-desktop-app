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