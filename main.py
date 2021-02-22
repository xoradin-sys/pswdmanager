
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import os


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    entry_password.delete(0, END)
    entry_password.clipboard_clear()
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    capitalized_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']
    password_list = [choice(letters) for _ in range(randint(6, 8))]
    password_list += [choice(capitalized_letters) for _ in range(randint(1, 2))]
    password_list += [choice(numbers) for _ in range(randint(1, 2))]
    password_list += [choice(symbols) for _ in range(randint(1, 1))]
    shuffle(password_list)
    password = "".join(password_list)
    entry_password.insert(0, password)
    entry_password.clipboard_append(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def password_save():
    save = False
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website:{
            "email": email,
            "password": password,
        }
    }
    if entry_website.get() == '' or entry_password.get() == '':
        messagebox.showinfo(title='', message='Fill out the fields pls!')
        pass
    else:
        global data
        msg = f'{entry_website.get()} | {entry_email.get()} | {entry_password.get()}'
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                if entry_website.get() in data:
                    is_ok = messagebox.askokcancel(title='WARNING!!', message='WEBSITE ALREADY IN FILE!\nOK TO OVERWRITE??')
                    if is_ok:
                        data.update(new_data)
                        save = True
                    else:
                        pass
                else:
                    data.update(new_data)
                    save = True
        except FileNotFoundError:
            data = new_data
        finally:
            with open("data.json", 'w') as file:
                json.dump(data, file, indent=4)
            entry_website.delete(0, END)
            entry_password.delete(0, END)

        if save:
            try:
                with open("PasswordManagerFile.txt", "w") as file:
                    file.write("")
                with open("data.json", "r") as file:
                    data = json.load(file)
                    for website in data:
                        key_item = data[website]
                        email_item = key_item["email"]
                        pswd_item = key_item["password"]
                        msg = f'{website} | {email_item} | {pswd_item}\n'
                        with open("PasswordManagerFile.txt", "a") as file:
                            file.write(msg)
            except:
                messagebox.showinfo(title='', message='There was an error writing to txtfile!')
                pass        
        drop()


# --------------------------- SHOW PASSWORD FILE ----------------------------#
def show_file():
    try:
        bashCommand = "mousepad PasswordManagerFile.txt &"
        os.system(bashCommand)
    except:
        bashCommand = "start notepad PasswordManagerFile.txt &"
        os.system(bashCommand)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    pass
    if entry_website.get() == '':
        messagebox.showinfo(title='', message='Fill out a website pls!')
        pass
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title='', message='No Datafile Found!')
        else:
            data_list = [website for website in data]
            if entry_website.get() in data_list:
                key_dict = data[entry_website.get()]
                entry_email.delete(0, END)
                entry_password.delete(0, END)
                entry_email.insert(0, key_dict["email"])
                entry_password.insert(0, key_dict["password"])
                entry_password.clipboard_clear()
                entry_password.clipboard_append(key_dict["password"])
            else:
                entry_password.delete(0, END)
                entry_email.delete(0, END)
                entry_password.clipboard_clear()
                messagebox.showinfo(title='', message='No Website Found!')


# ---------------------------- Other Setups --------------------------- #
def about():
    messagebox.showinfo(title='', message='Another XoraProduction')


def show_drop(value):
    entry_website.delete(0, END)
    entry_website.insert(0, value)
    drop()


class drop():
    def __init__(self):
        # Dropdown menu options
        with open("data.json", "r") as file:
            data = json.load(file)
            options = [item for item in data]
        # datatype of menu text
        dropVar = StringVar()
        # initial menu text
        dropVar.set("WebSites")
        # Create Dropdown menu
        drop = OptionMenu(window, dropVar, *options, command=show_drop)
        drop.config(padx=2, pady=2, bg='blue', fg='white', width=8)
        drop.grid(column=0, row=1)
        


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
menu = Menu(window)
menu.config(bg='blue', fg='white')
window.title("PASSWORD MANAGER")
window.minsize(width=500, height=360)
window.config(menu=menu, padx=20, pady=20, bg='white')
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)
# ###### Menu ######################
filemenu = Menu(menu)
menu.add_cascade(label="ShowFile", menu=filemenu)
filemenu.add_command(label="Open...", command=show_file)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=about)
# ##################################
# area 0,0
# area 0,1 drop_down_menu website
drop()
# area 0,2 label email/username
label_email = Label(text='Email/Username:')
label_email.config(padx=5, pady=4, bg='white')
label_email.grid(column=0, row=2)
# area 0,3 label password
label_password = Label(text='Password')
label_password.config(padx=5, pady=5, bg='white')
label_password.grid(column=0, row=3)
# area 0,4
# #################################
# area 1,0 canvas image
# area 1,1 entry website
entry_website = Entry(text='')
entry_website.config(bg='white', width=25)
entry_website.grid(column=1, row=1, columnspan=1)
entry_website.focus()
# area 1,2 entry email/username
entry_email = Entry(text='')
entry_email.config(bg='white', width=36)
entry_email.grid(column=1, row=2, columnspan=2)
entry_email.insert(0, "example@mail.com")
# area 1,3 entry password
entry_password = Entry(text='')
entry_password.config(bg='white', width=25)
entry_password.grid(column=1, row=3, columnspan=1)
# area 1,4 button add
button_add = Button(text='ADD', font='bold', command=password_save)
button_add.config(bg='yellow', fg='black', width=30)
button_add.grid(column=1, row=4, columnspan=2)
# #################################
# area 2,0
# area 2,1 search button
button_search = Button(text='Search', command=find_password)
button_search.config(bg='green', fg='white', width=8)
button_search.grid(column=2, row=1)
# area 2,2 span entry email/username
# area 2,3 button generate password
button_generate = Button(text='Generate', command=generate_password)
button_generate.config(fg='white', bg='red', width=8)
button_generate.grid(column=2, row=3)
# area 2,4 span button add
# ##################################

window.mainloop()