from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar
from datetime import date, datetime
import sqlite3
from sqlite3 import Error
import random
import os, sys, subprocess
from os.path import exists
import json
import requests

cwd = os.getcwd()
db_file = cwd+"/client_data.db"

root = Tk()
root.title("Client Relationship Manager")
root.attributes('-fullscreen', True)
root.resizable(True, True)
root.call('source', 'forest-dark.tcl')
ttk.Style().theme_use('forest-dark')
style = ttk.Style()
style.configure('my.TButton', font=(None, 20))
style.configure('reset.TButton', font=(None, 15), bg="#639d7e")
style.configure('search.TButton', font=(None, 15), background="#639d7e")
style.configure('my.TLabel', font=(None, 50))
style.configure('TMenubutton', font=(None, 10))
style.configure('form.TMenubutton', font=(None, 20))


def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


# style.configure('my_button', font =
#                ('calibri', 10, 'bold', 'underline'),
#                 foreground = 'red')

homeFrame = Canvas(root, width=1920, height=1080)
homeFrame.pack()

clientsFrame = Canvas(root, width=1920, height=1080)

profileFrame = Canvas(root, width=1920, height=1080)

""" create a database connection to a SQLite database """

try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # cursor.execute('CREATE TABLE IF NOT EXISTS Clients (ID INTEGER PRIMARY KEY, Forename TEXT, Surname TEXT, Email TEXT, Phone TEXT, Address TEXT, Gender TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS Clients (ID INTEGER PRIMARY KEY, Forename TEXT, Surname TEXT, Email TEXT, Phone TEXT, Address TEXT, Birthday DATETIME, Gender TEXT, SignDate DATETIME)')
except Error as e:
    print(e)

def create_note(view, forename, surname):
   client_name = forename + surname

   current_directory = os.getcwd()
   final_directory = os.path.join(current_directory, client_name)
   if not os.path.exists(final_directory):
      os.makedirs(final_directory)

   filename = simpledialog.askstring("Create Note", "What would you like to name this note?", parent=view)
   if filename == None:
       pass
   else:
       filename = filename.replace(" ", "_")
       filename = filename.replace("/", "_")
       file = final_directory + "/" + filename + ".txt"
       while exists(file):
           filename = simpledialog.askstring("Note Already Exists", "A note with this name already exists. Please enter a new name.", parent=view)
           filename = filename.replace(" ", "_")
           filename = filename.replace("/", "_")
           file = final_directory + "/" + filename + ".txt"
           if filename == None:
               break
           elif exists(file) == False:
               break

   if filename != None:
       f = open(file, 'w')

       try:
           if sys.platform == "win32":
               os.startfile(file)
           else:
               opener = "open" if sys.platform == "darwin" else "xdg-open"
               subprocess.call([opener, file])
       except Error:
           pass

   else:
       pass

def edit_note(forename, surname):
    client_name = f"{forename} {surname}"
    current_directory = os.getcwd()
    initial_directory = os.path.join(current_directory, client_name)
    if os.path.isdir(initial_directory):
        file = askopenfilename(initialdir=initial_directory, title="Select file", filetypes=[("Text Files", "*.txt")])
        try:
            if sys.platform == "win32":
                os.startfile(file)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, file])
        except Error:
            pass
    else:
        messagebox.showerror(title="Error", message="No saved notes for this client.")

def scheduleAppointment(forename, surname):
    client_name = f"{forename} {surname}"
    data = []

    appointment = Toplevel(root)
    appointment.geometry("1920x1080")
    appointment.title("Schedule Appointment")

    todays_date = date.today()
    day = todays_date.day
    month = todays_date.month
    year = todays_date.year

    cal = Calendar(appointment, selectmode='day', font=(None, 40), year=year, month=month, day=day,
                   background="#313131", disabledbackground="#313131", bordercolor="#313131",
                   headersbackground="#313131", normalbackground="#313131", foreground='white',
                   normalforeground='white', headersforeground='white', weekendbackground="#639d7e",
                   othermonthbackground="#313131", othermonthwebackground="#90b9a3")
    cal.place(x=100, y=100)

    clicked_hour = StringVar()
    clicked_hour.set('00')
    hour_options = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                   '18', '19', '20', '21', '22', '23']
    hour_form = ttk.OptionMenu(appointment, clicked_hour, *hour_options, style='form.TMenubutton')
    hour_form.place(x=200, y=650)
    Label(appointment, text="Hour", font='None 20').place(x=200, y=700)

    clicked_minute = StringVar()
    clicked_minute.set('00')
    minute_options = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                   '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
                      '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54',
                      '55', '56', '57', '58', '59', '60']
    minute_form = ttk.OptionMenu(appointment, clicked_minute, *minute_options, style='form.TMenubutton')
    minute_form.place(x=300, y=650)
    Label(appointment, text="Minutes", font='None 20').place(x=300, y=700)


    ttk.Button(appointment, text="Submit", style='my.TButton', command=lambda: writeFile(data)).place(x=600, y=650)

    def writeFile(data):
        app_date = str(cal.selection_get())
        hour = clicked_hour.get()
        minute = clicked_minute.get()
        date = f"{app_date} {hour}:{minute}:00"

        current_directory = os.getcwd()
        file = current_directory + "/appointments.txt"
        if exists(file):
            with open(file, "r+") as f:
                size = os.path.getsize(file)
                if size != 0:
                    data = json.load(f)

                    print(app_date, type(app_date))
                    data.append([client_name, date])
                    data = sorted(data, key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"))
                    json.dump(data, open(file, 'r+'))

                    print(data)
                else:
                    pass
        else:
            f = open(file, 'w')

def database(forename_form, surname_form, email_form, phone_form, address_form, clicked_year, clicked_month, clicked_day, gender_radio, clicked_sign_year, clicked_sign_month, clicked_sign_day):

   cursor.row_factory = lambda cursor, row: row[0]
   cursor.execute("SELECT id FROM Clients")
   client_ids = cursor.fetchall()

   if len(client_ids) == 10001:
       print(client_ids)
       print("No more unique ids")
   else:
       id = random.randint(0, 10000)
       while id in client_ids:
           id = random.randint(0, 10000)

       forename = forename_form.get()
       surname = surname_form.get()
       email = email_form.get()
       phone = phone_form.get()
       address = address_form.get()
       birth_year_form = clicked_year.get()
       birth_month_form = clicked_month.get()
       birth_day_form = clicked_day.get()
       birthday = birth_year_form+'-'+birth_month_form+'-'+birth_day_form
       gender = gender_radio.get()
       if gender == 1:
           gender = "Female"
       elif gender == 2:
           gender = "Male"
       elif gender == 3:
           gender = "Other"
       elif gender == 4:
           gender = "Undisclosed"

       sign_year_form = clicked_sign_year.get()
       sign_month_form = clicked_sign_month.get()
       sign_day_form = clicked_sign_day.get()
       signdate = sign_year_form+'-'+sign_month_form+'-'+sign_day_form

       if forename == "" or surname == "" or email == "" or phone == "" or address == "":
           messagebox.showerror(title="Blank Fields", message="Please fill all fields to continue.")
       else:
           cursor.execute('INSERT INTO Clients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, forename, surname, email, phone, address, birthday, gender, signdate))
           conn.commit()

           forename_form.delete(0, "end")
           surname_form.delete(0, "end")
           email_form.delete(0, "end")
           phone_form.delete(0, "end")
           address_form.delete(0, "end")
           gender_radio.set(4)

def addNewClient():

    top = Toplevel(root)
    addClientFrame = Canvas(top, width=1920, height=1080)
    addClientFrame.pack()

    my_rectangle = round_rectangle(addClientFrame, 275, 190, 1200, 730, radius=50, outline="#207346", fill="")
    my_rectangle = round_rectangle(addClientFrame, 900, 25, 1500, 150, radius=50, outline="#207346", fill="#207346")
    text_canvas = addClientFrame.create_text(1170, 85, font="Mistral 50 bold", fill="black")
    addClientFrame.itemconfig(text_canvas, text="Add New Client")

    forename_form = ttk.Entry(addClientFrame, font=(None, 25), width=30)
    forename_form.focus()
    surname_form = ttk.Entry(addClientFrame, font=(None, 25), width=30)
    email_form = ttk.Entry(addClientFrame, font=(None, 25), width=30)
    phone_form = ttk.Entry(addClientFrame, font=(None, 25), width=30)
    address_form = ttk.Entry(addClientFrame, font=(None, 25), width=30)
    gender_radio = IntVar()
    r1 = ttk.Radiobutton(addClientFrame, text='Female', value=1, variable=gender_radio)
    r2 = ttk.Radiobutton(addClientFrame, text='Male', value=2, variable=gender_radio)
    r3 = ttk.Radiobutton(addClientFrame, text='Other', value=3, variable=gender_radio)
    r4 = ttk.Radiobutton(addClientFrame, text='Undisclosed', value=4, variable=gender_radio)
    gender_radio.set(4)


    box_x1 = 454
    box_x2 = 584
    box_y1 = 230
    box_y2 = 270
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1, box_x2, box_y2, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+60, box_x2, box_y2+60, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+120, box_x2, box_y2+120, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+180, box_x2, box_y2+180, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+240, box_x2, box_y2+240, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+300, box_x2, box_y2+300, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, box_x1, box_y1+360, box_x2, box_y2+360, radius=10, outline="#639d7e", fill="#639d7e")
    my_rectangle = round_rectangle(addClientFrame, 337, box_y1+420, box_x2, box_y2+420, radius=10, outline="#639d7e", fill="#639d7e")

    label_x = 520
    label_y = 250

    forename_label = addClientFrame.create_text(label_x, label_y, font="Mistral 25", fill="black")
    surname_label = addClientFrame.create_text(label_x, label_y+60, font="Mistral 25", fill="black")
    email_label = addClientFrame.create_text(label_x, label_y+120, font="Mistral 25", fill="black")
    phone_label = addClientFrame.create_text(label_x, label_y+180, font="Mistral 25", fill="black")
    address_label = addClientFrame.create_text(label_x, label_y+240, font="Mistral 25", fill="black")
    birthday_label = addClientFrame.create_text(label_x, label_y+300, font="Mistral 25", fill="black")
    gender_label = addClientFrame.create_text(label_x, label_y+360, font="Mistral 25", fill="black")
    signdate_label = addClientFrame.create_text(460, label_y+420, font="Mistral 25", fill="black")

    addClientFrame.itemconfig(forename_label, text="Forename")
    addClientFrame.itemconfig(surname_label, text="Surname")
    addClientFrame.itemconfig(email_label, text="Email")
    addClientFrame.itemconfig(phone_label, text="Phone")
    addClientFrame.itemconfig(address_label, text="Address")
    addClientFrame.itemconfig(birthday_label, text="Birthday")
    addClientFrame.itemconfig(gender_label, text="Gender")
    addClientFrame.itemconfig(signdate_label, text="Contract Sign Date")

    form_x = 640
    form_y = 230

    forename_form.place(x=form_x, y=form_y)
    surname_form.place(x=form_x, y=form_y+60)
    email_form.place(x=form_x, y=form_y+120)
    phone_form.place(x=form_x, y=form_y+180)
    address_form.place(x=form_x, y=form_y+240)
    r1.place(x=form_x, y=form_y+365)
    r2.place(x=form_x+140, y=form_y+365)
    r3.place(x=form_x+260, y=form_y+365)
    r4.place(x=form_x+390, y=form_y+365)

    clicked_day = StringVar()
    clicked_day.set('01')
    day_options = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    birth_day_form = ttk.OptionMenu(addClientFrame, clicked_day, *day_options, style='form.TMenubutton')
    birth_day_form.place(x=form_x, y=form_y+300)

    clicked_month = StringVar()
    clicked_month.set('01')
    month_options = ['01','02','03','04','05','06','07','08','09','10','11','12']
    birth_month_form = ttk.OptionMenu(addClientFrame, clicked_month, *month_options, style='form.TMenubutton')
    birth_month_form.place(x=form_x+115, y=form_y+300)

    clicked_year = StringVar()
    clicked_year.set('2022')
    year_options = []
    for i in range(1920, 2023):
        year_options.append(str(i))
    birth_year_form = ttk.OptionMenu(addClientFrame, clicked_year, *year_options, style='form.TMenubutton')
    birth_year_form.place(x=form_x+220, y=form_y+300)

    clicked_sign_day = StringVar()
    clicked_sign_day.set('01')
    sign_day_form = ttk.OptionMenu(addClientFrame, clicked_sign_day, *day_options, style='form.TMenubutton')
    sign_day_form.place(x=form_x, y=form_y+420)

    clicked_sign_month = StringVar()
    clicked_sign_month.set('01')
    sign_month_form = ttk.OptionMenu(addClientFrame, clicked_sign_month, *month_options, style='form.TMenubutton')
    sign_month_form.place(x=form_x+115, y=form_y+420)

    clicked_sign_year = StringVar()
    clicked_sign_year.set('2022')
    sign_year_form = ttk.OptionMenu(addClientFrame, clicked_sign_year, *year_options, style='form.TMenubutton')
    sign_year_form.place(x=form_x+220, y=form_y+420)

    ttk.Button(addClientFrame, text="Submit", style="my.TButton", command=lambda: database(forename_form, surname_form, email_form, phone_form, address_form, clicked_year, clicked_month, clicked_day, gender_radio, clicked_sign_year, clicked_sign_month, clicked_sign_day)).place(x=1045, y=780)

def displayData():

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    records = cursor.fetchall()

    global my_tree
    my_tree = ttk.Treeview(clientsFrame, show='headings', height=20)

    my_tree['columns'] = ("ID", "Forename", "Surname", "Email", "Phone", "Address", "Birthday", "Gender", "SignDate")
    my_tree.column("#0", width=100)
    my_tree.column("ID", width=135)
    my_tree.column("Forename", width=135)
    my_tree.column("Surname", width=135)
    my_tree.column("Email", width=135)
    my_tree.column("Phone", width=135)
    my_tree.column("Address", width=135)
    my_tree.column("Birthday", width=135)
    my_tree.column("Gender", width=135)
    my_tree.column("SignDate", width=135)

    my_tree.heading("ID", text="Customer ID")
    my_tree.heading("Forename", text="Forename")
    my_tree.heading("Surname", text="Surname")
    my_tree.heading("Email", text="Email Address")
    my_tree.heading("Phone", text="Phone Number")
    my_tree.heading("Address", text="Address")
    my_tree.heading("Birthday", text="Birthday")
    my_tree.heading("Gender", text="Gender")
    my_tree.heading("SignDate", text="Contract Sign Date")

    count = 0
    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))
        count += 1

    my_tree.place(x=42, y=200)

def search(search_entry, menu_selection):
    cursor = conn.cursor()
    searching = search_entry.get()
    option = menu_selection.get()

    if option == "By Forename":
        cursor.execute("SELECT * FROM Clients WHERE forename like ?", (searching,))
    elif option == "By Surname":
        cursor.execute("SELECT * FROM Clients WHERE surname like ?", (searching,))
    elif option == "By ID":
        cursor.execute("SELECT * FROM Clients WHERE id like ?", (searching,))

    records = cursor.fetchall()

    for record in my_tree.get_children():
        my_tree.delete(record)

    count = 0
    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))
        count += 1

def viewClient(view_entry):

    cursor = conn.cursor()
    if isinstance(view_entry, Entry):
        client_id = view_entry.get()
    else:
        client_id = view_entry


    cursor.execute("SELECT * FROM Clients WHERE id like ?", (client_id,))
    records = cursor.fetchall()

    if len(records) == 0:
        messagebox.showerror(title="No Existing Customer", message="There is no customer with this ID in your records.")
        view_entry.delete(0, "end")
    else:
        top = Toplevel(root)
        view = Canvas(top, width=1920, height=1080)
        view.pack()

        client_id = records[0][0]
        birthday = records[0][6]
        birthday_values = birthday.split("-")

        signdate = records[0][8]
        signdate_values = signdate.split("-")

        text_canvas = view.create_text(240, 85, font="Mistral 30 bold", fill="black")
        view.itemconfig(text_canvas, text="Upcoming Appointments:")
        my_rectangle = round_rectangle(view, 900, 15, 1500, 90, radius=50, outline="#207346", fill="#207346")
        text_canvas = view.create_text(1170, 51, font="Mistral 50 bold", fill="black")
        view.itemconfig(text_canvas, text=f"{records[0][1]} {records[0][2]}")
        my_rectangle = round_rectangle(view, 500, 110, 1400, 710, radius=50, outline="#207346", fill="")
        my_rectangle = round_rectangle(view, 40, 110, 450, 710, radius=50, outline="#207346", fill="")

        appointments = Text(view, height=20, width=25)
        appointments.place(x=75, y=150)
        appointments.configure(font='None, 20')

        current_directory = os.getcwd()
        file = current_directory + "/appointments.txt"
        if exists(file):
            with open(file, "r+") as f:
                size = os.path.getsize(file)
                if size != 0:
                    data = json.load(f)

                    today = date.today()
                    today = today.strftime("%Y-%m-%d %H:%M:%S")
                    user_apps = []
                    for i in data:
                        if i[0] == f"{records[0][1]} {records[0][2]}":
                            if i[1] > today:
                                user_apps.append(i)

                    for i in range(len(user_apps)):
                        position = f'{i}.0'
                        appointments.insert(position, f'{(user_apps[i][1])[0:10]} - {(user_apps[i][1])[11:16]}\n');
                    scrollbar = ttk.Scrollbar(view, orient='vertical', command=appointments.yview)
                    scrollbar.place(x=400, y=155)
                    appointments['yscrollcommand'] = scrollbar.set
                else:
                    pass

        box_x1 = 650
        box_x2 = 780
        box_y1 = 150
        box_y2 = 190
        my_rectangle = round_rectangle(view, box_x1, box_y1, box_x2, box_y2, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 60, box_x2, box_y2 + 60, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 120, box_x2, box_y2 + 120, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 180, box_x2, box_y2 + 180, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 240, box_x2, box_y2 + 240, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 300, box_x2, box_y2 + 300, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 360, box_x2, box_y2 + 360, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, box_x1, box_y1 + 420, box_x2, box_y2 + 420, radius=10, outline="#639d7e", fill="#639d7e")
        my_rectangle = round_rectangle(view, 530, box_y1 + 480, box_x2, box_y2 + 480, radius=10, outline="#639d7e", fill="#639d7e")

        label_x = 715
        label_y = 170
        id_label = view.create_text(label_x, label_y, font="Mistral 25", fill="black")
        forename_label = view.create_text(label_x, label_y +60, font="Mistral 25", fill="black")
        surname_label = view.create_text(label_x, label_y + 120, font="Mistral 25", fill="black")
        email_label = view.create_text(label_x, label_y + 180, font="Mistral 25", fill="black")
        phone_label = view.create_text(label_x, label_y + 240, font="Mistral 25", fill="black")
        address_label = view.create_text(label_x, label_y + 300, font="Mistral 25", fill="black")
        birthday_label = view.create_text(label_x, label_y + 360, font="Mistral 25", fill="black")
        gender_label = view.create_text(label_x, label_y + 420, font="Mistral 25", fill="black")
        signdate_label = view.create_text(655, label_y + 480, font="Mistral 25", fill="black")

        view.itemconfig(id_label, text="ID")
        view.itemconfig(forename_label, text="Forename")
        view.itemconfig(surname_label, text="Surname")
        view.itemconfig(email_label, text="Email")
        view.itemconfig(phone_label, text="Phone")
        view.itemconfig(address_label, text="Address")
        view.itemconfig(birthday_label, text="Birthday")
        view.itemconfig(gender_label, text="Gender")
        view.itemconfig(signdate_label, text="Contract Sign Date")

        label_x = 830
        label_y = 150
        id_value = Label(view, text=records[0][0], font=('Verdana', 25))
        id_value.place(x=label_x, y=label_y)
        forename_value = Label(view, text=records[0][1], font=('Verdana', 25))
        forename_value.place(x=label_x, y=label_y + 60)
        surname_value = Label(view, text=records[0][2], font=('Verdana', 25))
        surname_value.place(x=label_x, y=label_y + 120)
        email_value = Label(view, text=records[0][3], font=('Verdana', 25))
        email_value.place(x=label_x, y=label_y + 180)
        phone_value = Label(view, text=records[0][4], font=('Verdana', 25))
        phone_value.place(x=label_x, y=label_y + 240)
        address_value = Label(view, text=records[0][5], font=('Verdana', 25))
        address_value.place(x=label_x, y=label_y + 300)
        birthday_value = Label(view, text=records[0][6], font=('Verdana', 25))
        birthday_value.place(x=label_x, y=label_y + 360)
        gender_value = Label(view, text=records[0][7], font=('Verdana', 25))
        gender_value.place(x=label_x, y=label_y + 420)
        signdate_value = Label(view, text=records[0][8], font=('Verdana', 25))
        signdate_value.place(x=label_x, y=label_y + 480)

        def deleteClient():
            confirm = messagebox.askquestion(title="Delete Client Record", message="This action cannot be undone. Are you sure you wish to delete this record?", icon="warning")
            if confirm == 'yes':
                cursor.execute(('''DELETE FROM Clients WHERE id = ?'''), (client_id,))
                conn.commit()
                view.destroy()
                top.destroy()
            else:
                pass

        def editClient():
            forename_value.destroy()
            surname_value.destroy()
            email_value.destroy()
            phone_value.destroy()
            address_value.destroy()

            label_y = 205
            forename_entry = ttk.Entry(view, font=('Verdana', 25))
            forename_entry.place(x=825, y=label_y)
            surname_entry = ttk.Entry(view, font=('Verdana', 25))
            surname_entry.place(x=825, y=label_y + 60)
            email_entry = ttk.Entry(view, font=('Verdana', 25))
            email_entry.place(x=825, y=label_y + 120)
            phone_entry = ttk.Entry(view, font=('Verdana', 25))
            phone_entry.place(x=825, y=label_y + 180)
            address_entry = ttk.Entry(view, font=('Verdana', 25))
            address_entry.place(x=825, y=label_y + 240)

            forename_entry.insert(0, records[0][1])
            surname_entry.insert(0, records[0][2])
            email_entry.insert(0, records[0][3])
            phone_entry.insert(0, records[0][4])
            address_entry.insert(0, records[0][5])
            #
            # gender_radio = IntVar()
            # r1 = ttk.Radiobutton(view, text='Female', value=1, variable=gender_radio)
            # r2 = ttk.Radiobutton(view, text='Male', value=2, variable=gender_radio)
            # r3 = ttk.Radiobutton(view, text='Other', value=3, variable=gender_radio)
            # r4 = ttk.Radiobutton(view, text='Undisclosed', value=4, variable=gender_radio)
            #
            # gender = records[0][7]
            #
            # if gender == "Female":
            #     gender_radio.set(1)
            # elif gender == "Male":
            #     gender_radio.set(2)
            # elif gender == "Other":
            #     gender_radio.set(3)
            # elif gender == "Undisclosed":
            #     gender_radio.set(4)
            #
            # r1.place(x=825, y=label_y + 370)
            # r2.place(x=965, y=label_y + 370)
            # r3.place(x=1085, y=label_y + 370)
            # r4.place(x=1215, y=label_y + 370)
            #
            # clicked_day = StringVar()
            # clicked_day.set(birthday_values[2])
            # day_options = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
            #                '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
            # birth_day_form = ttk.OptionMenu(view, clicked_day, *day_options, style='form.TMenubutton')
            # birth_day_form.place(x=825, y=label_y + 305)
            #
            # clicked_month = StringVar()
            # clicked_month.set(birthday_values[1])
            # month_options = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            # birth_month_form = ttk.OptionMenu(view, clicked_month, *month_options, style='form.TMenubutton')
            # birth_month_form.place(x=943, y=label_y + 305)
            #
            # clicked_year = StringVar()
            # clicked_year.set(birthday_values[0])
            # year_options = []
            # for i in range(1920, 2023):
            #     year_options.append(str(i))
            # birth_year_form = ttk.OptionMenu(view, clicked_year, *year_options, style='form.TMenubutton')
            # birth_year_form.place(x=1052, y=label_y + 305)
            #
            # birth_year_form = clicked_year.get()
            # birth_month_form = clicked_month.get()
            # birth_day_form = clicked_day.get()
            #
            # clicked_sign_day = StringVar()
            # clicked_sign_day.set(signdate_values[2])
            # sign_day_form = ttk.OptionMenu(view, clicked_sign_day, *day_options, style='form.TMenubutton')
            # sign_day_form.place(x=825, y=label_y + 425)
            #
            # clicked_sign_month = StringVar()
            # clicked_sign_month.set(signdate_values[1])
            # sign_month_form = ttk.OptionMenu(view, clicked_sign_month, *month_options, style='form.TMenubutton')
            # sign_month_form.place(x=943, y=label_y + 425)
            #
            # clicked_sign_year = StringVar()
            # clicked_sign_year.set(signdate_values[0])
            # sign_year_form = ttk.OptionMenu(view, clicked_sign_year, *year_options, style='form.TMenubutton')
            # sign_year_form.place(x=1052, y=label_y + 425)
            #
            # sign_year_form = clicked_sign_year.get()
            # sign_month_form = clicked_sign_month.get()
            # sign_day_form = clicked_sign_day.get()

            def update_db():
                new_forename = forename_entry.get()
                new_surname = surname_entry.get()
                new_email = email_entry.get()
                new_phone = phone_entry.get()
                new_address = address_entry.get()
                # new_birthday = birth_year_form + '-' + birth_month_form + '-' + birth_day_form
                # new_signdate = sign_year_form + '-' + sign_month_form + '-' + sign_day_form

                if new_forename != "" and new_forename != records[0][1]:
                    cursor.execute(('''UPDATE Clients
                                    SET Forename = ?
                                    WHERE id = ?'''), (new_forename, client_id))
                if new_surname != "" and new_surname != records[0][2]:
                    cursor.execute(('''UPDATE Clients
                                    SET Surname = ?
                                    WHERE id = ?'''), (new_surname, client_id))
                if new_email != "" and new_email != records[0][3]:
                    cursor.execute(('''UPDATE Clients
                                    SET Email = ?
                                    WHERE id = ?'''), (new_email, client_id))
                if new_phone != "" and new_phone != records[0][4]:
                    cursor.execute(('''UPDATE Clients
                                    SET Phone = ?
                                    WHERE id = ?'''), (new_phone, client_id))
                if new_address != "" and new_address != records[0][5]:
                    cursor.execute(('''UPDATE Clients
                                    SET Address = ?
                                    WHERE id = ?'''), (new_address, client_id))
                # if new_birthday != "" and new_birthday != records[0][6]:
                #     confirm = messagebox.askquestion(title="Changing Client Birthday", message="Dates don't usually change \nAre you sure you want to change the birthdate of the client?", icon="warning")
                #     if confirm == 'yes':
                #         cursor.execute(('''UPDATE Clients
                #                         SET Birthday = ?
                #                         WHERE id = ?'''), (new_birthday, client_id))
                #     else:
                #         pass
                # if new_signdate != "" and new_signdate != records[0][8]:
                #     confirm = messagebox.askquestion(title="Changing Client Sign Date", message="Dates don't usually change \nAre you sure you want to change the sign date of the client?", icon="warning")
                #     if confirm == 'yes':
                #         cursor.execute(('''UPDATE Clients
                #                         SET SignDate = ?
                #                         WHERE id = ?'''), (new_signdate, client_id))
                #     else:
                #         pass

                conn.commit()
                view.destroy()
                top.destroy()
                viewClient(client_id)

            ttk.Button(view, text="Submit Changes", style="my.TButton", command=lambda: update_db()).place(x=550, y=800)

        ttk.Button(view, text="Edit Client Details", style="my.TButton", command=lambda: editClient()).place(x=550, y=750)
        ttk.Button(view, text="Delete Client", style="my.TButton", command=lambda: deleteClient()).place(x=785, y=750)
        ttk.Button(view, text="Create Note", style="my.TButton", command=lambda: create_note(view, records[0][1], records[0][2])).place(x=990, y=750)
        ttk.Button(view, text="Edit Note", style="my.TButton", command=lambda: edit_note(records[0][1], records[0][2])).place(x=1200, y=750)
        ttk.Button(view, text="Schedule Appointment", style="my.TButton", command=lambda: scheduleAppointment(records[0][1], records[0][2])).place(x=120, y=750)


def clientsPage(currentFrame):

    currentFrame.pack_forget()
    clientsFrame.pack()
    displayData()

    my_rectangle = round_rectangle(clientsFrame, 900, 25, 1600, 150, radius=50, outline="#207346", fill="#207346")
    text_canvas = clientsFrame.create_text(1170, 85, font="Mistral 50 bold", fill="black")
    clientsFrame.itemconfig(text_canvas, text="Clients")

    options = ["By Forename", "By Surname", "By ID"]
    menu_selection = StringVar()

    menu_button = ttk.OptionMenu(clientsFrame, menu_selection, "By Forename", *options, style='TMenubutton')
    menu_button.place(x=360, y=135)

    search_entry = ttk.Entry(clientsFrame, font=(None, 20))
    view_entry = ttk.Entry(clientsFrame, font=(None, 20))

    def temp_text_search(e):
        search_entry.delete(0, "end")

    def temp_text_view(e):
        view_entry.delete(0, "end")

    search_entry.insert(0, "Name / ID")
    search_entry.place(x=70, y=130)
    search_entry.bind("<FocusIn>", temp_text_search)

    view_entry.insert(0, "Customer ID")
    view_entry.place(x=100, y=750)
    view_entry.bind("<FocusIn>", temp_text_view)

    ttk.Button(clientsFrame, text="Search", style="search.TButton", command=lambda: search(search_entry, menu_selection)).place(x=470, y=130)
    ttk.Button(clientsFrame, text="Refresh", style="reset.TButton", command=lambda: displayData()).place(x=1171, y=680)
    ttk.Button(clientsFrame, text="View Client Profile", style="my.TButton", command=lambda: viewClient(view_entry)).place(x=400, y=750)

    home_button = ttk.Button(clientsFrame, text="Home", style="my.TButton", command=lambda: homePage(clientsFrame))
    home_button.place(x=65, y=50)
    ttk.Button(clientsFrame, text="Add New Client", style="my.TButton", command=lambda: addNewClient()).place(x=600, y=750)

def homePage(currentFrame):

    if currentFrame != None:
        currentFrame.pack_forget()
    homeFrame.pack()

    my_rectangle = round_rectangle(homeFrame, 900, 25, 1600, 150, radius=50, outline="#207346", fill="#207346")
    text_canvas = homeFrame.create_text(1170, 85, font="Mistral 50 bold", fill="black")
    homeFrame.itemconfig(text_canvas, text="Your Dashboard")

    todays_date = date.today()
    today = todays_date.strftime("%Y-%m-%d %H:%M:%S")
    year = todays_date.year
    month = todays_date.month
    day = todays_date.day
    cal = Calendar(homeFrame, selectmode='day', font=(None, 40), year=year, month=month, day=day,
                   background="#313131", disabledbackground="#313131", bordercolor="#313131",
                   headersbackground="#313131", normalbackground="#313131", foreground='white',
                   normalforeground='white', headersforeground='white', weekendbackground="#639d7e",
                   othermonthbackground="#313131", othermonthwebackground="#90b9a3")
    cal.place(x=565, y=240)

    text_canvas = homeFrame.create_text(245, 55, font="Mistral 30 bold", fill="black")
    homeFrame.itemconfig(text_canvas, text="Upcoming Public Holidays:")
    my_rectangle = round_rectangle(homeFrame, 40, 30, 450, 430, radius=50, outline="#207346", fill="")

    holidays = Text(homeFrame, height=13, width=30)
    holidays.place(x=80, y=85)
    holidays.configure(font='None, 18')

    response = requests.get(url="https://date.nager.at/api/v3/publicholidays/2022/AT")
    all_holidays = response.json()

    upcoming_holidays = []
    for i in all_holidays:
        if i['date']>today:
            upcoming_holidays.append(i)


    for i in range(len(upcoming_holidays)):
        position = f'{i}.0'
        holidays.insert(position, f"{(upcoming_holidays[i])['date']} - {(upcoming_holidays[i])['name']}\n")

    text_canvas = homeFrame.create_text(245, 475, font="Mistral 30 bold", fill="black")
    homeFrame.itemconfig(text_canvas, text="Upcoming Appointments:")
    my_rectangle = round_rectangle(homeFrame, 40, 450, 450, 850, radius=50, outline="#207346", fill="")

    appointments = Text(homeFrame, height=13, width=25)
    appointments.place(x=80, y=505)
    appointments.configure(font='None, 20')

    current_directory = os.getcwd()
    file = current_directory + "/appointments.txt"
    if exists(file):
        with open(file, "r+") as f:
            size = os.path.getsize(file)
            if size != 0:
                data = json.load(f)

                apps = []
                for i in data:
                    if i[1] > today:
                        apps.append(i)

                for i in range(len(apps)):
                    position = f'{i}.0'
                    appointments.insert(position, f'{(apps[i][1])[0:10]} - {(apps[i][1])[11:16]} - {apps[i][0]}\n')
                scrollbar = ttk.Scrollbar(homeFrame, orient='vertical', command=appointments.yview)
                scrollbar.place(x=400, y=510)
                appointments['yscrollcommand'] = scrollbar.set
            else:
                pass


    ttk.Button(homeFrame, text="Clients", style="my.TButton", command=lambda:clientsPage(homeFrame)).place(x=1100, y=750)


def main():
    homePage(None)

if __name__ == "__main__":
    main()

root.mainloop()
conn.commit()
conn.close()