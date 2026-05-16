
import tkinter as tk
import ttkbootstrap as tb
import requests
from ttkbootstrap.constants import *

editing_note_id = None
filtered_notes = []

# global variables
token = None
notes_cache = []

API_URL = "http://127.0.0.1:5000"

# FUNCTIONS

def load_notes():
    global notes_cache, filtered_notes

    response = requests.get(
        f"{API_URL}/api/notes/",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        notes_cache = response.json()
    else:
        notes_cache = []

    filtered_notes = notes_cache

    listbox.delete(0, END)

    for note in filtered_notes:
        listbox.insert(END, note["title"])

    listbox.selection_clear(0, END)


def add_note():
    global editing_note_id

    title = title_entry.get()
    content = content_text.get("1.0", END).strip()

    if not title or not content:
        return

    headers = {"Authorization": f"Bearer {token}"}

    if editing_note_id:
        requests.patch(
            f"{API_URL}/api/notes/{editing_note_id}",
            json={"title": title, "content": content},
            headers=headers
        )
        editing_note_id = None

    else:
        requests.post(
            f"{API_URL}/api/notes/",
            json={"title": title, "content": content},
            headers=headers
        )

    title_entry.delete(0, END)
    content_text.delete("1.0", END)

    load_notes()


def show_note(event):
    selection = listbox.curselection()

    if not selection:
        return

    index = selection[0]

    if index >= len(filtered_notes):
        return

    note = filtered_notes[index]

    title_entry.delete(0, END)
    title_entry.insert(0, note["title"])

    content_text.delete("1.0", END)
    content_text.insert("1.0", note["content"])


def delete_note():
    if not listbox.curselection():
        return

    index = listbox.curselection()[0]
    note_id = filtered_notes[index]["id"]

    requests.delete(
        f"{API_URL}/api/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    title_entry.delete(0, END)
    content_text.delete("1.0", END)

    load_notes()


def edit_note():
    global editing_note_id

    if not listbox.curselection():
        return

    index = listbox.curselection()[0]
    note = filtered_notes[index]

    editing_note_id = note["id"]

    title_entry.delete(0, END)
    title_entry.insert(0, note["title"])

    content_text.delete("1.0", END)
    content_text.insert("1.0", note["content"])


def new_note():
    global editing_note_id

    editing_note_id = None

    title_entry.delete(0, END)
    content_text.delete("1.0", END)

    listbox.selection_clear(0, END)


def search_notes():
    global filtered_notes

    query = search_entry.get().lower()

    listbox.delete(0, END)

    filtered_notes = [
        note for note in notes_cache
        if query in note["title"].lower()
        or query in note["content"].lower()
    ]

    for note in filtered_notes:
        listbox.insert(END, note["title"])

    listbox.selection_clear(0, END)


def login():
    global token

    username = login_user_entry.get()
    password = login_pass_entry.get()

    response = requests.post(
        f"{API_URL}/api/login",
        json={"username": username, "password": password}
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        status_label.config(text="Logged in!", foreground="green")

        login_frame.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)

        load_notes()

    else:
        status_label.config(text="Login failed", foreground="red")


def register():
    username = login_user_entry.get()
    password = login_pass_entry.get()

    response = requests.post(
        f"{API_URL}/api/register",
        json={"username": username, "password": password}
    )

    if response.status_code == 201:
        status_label.config(
            text="User created! Now login.",
            foreground="green"
        )
    else:
        status_label.config(
            text="Registration failed",
            foreground="red"
        )


def logout():
    global token, notes_cache, filtered_notes

    token = None
    notes_cache = []
    filtered_notes = []

    listbox.delete(0, END)

    title_entry.delete(0, END)
    content_text.delete("1.0", END)

    search_entry.delete(0, END)

    main_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=True)

    login_user_entry.delete(0, END)
    login_pass_entry.delete(0, END)

    status_label.config(text="Logged out", foreground="green")


# WINDOW

app = tb.Window(themename="darkly")
app.title("Notes App")
app.geometry("1000x650")

# LOGIN FRAME

login_frame = tb.Frame(app)
login_frame.pack(fill=BOTH, expand=True)

tb.Label(
    login_frame,
    text="Notes App",
    font=("Segoe UI", 22, "bold")
).pack(pady=(50, 25))

tb.Label(
    login_frame,
    text="Username",
    font=("Segoe UI", 11, "bold")
).pack()

login_user_entry = tb.Entry(login_frame, width=30)
login_user_entry.pack(pady=(0, 15))

tb.Label(
    login_frame,
    text="Password",
    font=("Segoe UI", 11, "bold")
).pack()

login_pass_entry = tb.Entry(login_frame, show="*", width=30)
login_pass_entry.pack(pady=(0, 20))

tb.Button(
    login_frame,
    text="Login",
    command=login,
    bootstyle=PRIMARY,
    width=20
).pack(pady=5)

tb.Button(
    login_frame,
    text="Register",
    command=register,
    bootstyle=SECONDARY,
    width=20
).pack()

status_label = tb.Label(login_frame, text="")
status_label.pack(pady=15)

# MAIN APP LAYOUT

main_frame = tb.Frame(app)

# SIDEBAR

sidebar_frame = tb.Frame(main_frame, padding=15)
sidebar_frame.pack(side=LEFT, fill=Y)

tb.Label(
    sidebar_frame,
    text="My Notes",
    font=("Segoe UI", 18, "bold")
).pack(pady=(0, 15))

search_entry = tb.Entry(sidebar_frame)
search_entry.pack(fill=X, pady=(0, 10))

tb.Button(
    sidebar_frame,
    text="Search",
    command=search_notes,
    bootstyle=PRIMARY
).pack(fill=X, pady=(0, 5))

tb.Button(
    sidebar_frame,
    text="Reset",
    command=load_notes,
    bootstyle=SECONDARY
).pack(fill=X, pady=(0, 10))

listbox = tk.Listbox(
    sidebar_frame,
    bg="#2b2b2b",
    fg="white",
    selectbackground="#375a7f",
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 11)
)

listbox.pack(fill=BOTH, expand=True)

listbox.bind("<<ListboxSelect>>", show_note)

tb.Button(
    sidebar_frame,
    text="+ New Note",
    command=new_note,
    bootstyle=SUCCESS
).pack(fill=X, pady=(10, 5))

tb.Button(
    sidebar_frame,
    text="Delete Note",
    command=delete_note,
    bootstyle=DANGER
).pack(fill=X, pady=(0, 5))

tb.Button(
    sidebar_frame,
    text="Logout",
    command=logout,
    bootstyle=SECONDARY
).pack(fill=X)

# EDITOR AREA

editor_frame = tb.Frame(main_frame, padding=20)
editor_frame.pack(side=LEFT, fill=BOTH, expand=True)

tb.Label(
    editor_frame,
    text="Title",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

title_entry = tb.Entry(
    editor_frame,
    font=("Segoe UI", 16)
)

title_entry.pack(fill=X, pady=(0, 20))

tb.Label(
    editor_frame,
    text="Content",
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

content_text = tk.Text(
    editor_frame,
    wrap="word",
    font=("Segoe UI", 12),
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    relief="flat",
    padx=10,
    pady=10
)

content_text.pack(fill=BOTH, expand=True, pady=(0, 20))

tb.Button(
    editor_frame,
    text="Save Note",
    command=add_note,
    bootstyle=SUCCESS
).pack(anchor="e")

# RUN

app.mainloop()