import sys
all_notes = []

def create():
     title = input("Enter title: ")
     new_note = input("Enter: ")
     note = {
          "title":title,
          "content": new_note
     }
     all_notes.append(note)
    
def view():
     if len(all_notes) == 0:
          print("No notes available.")
          return

     for index, note in enumerate(all_notes):
          print(index + 1, "-", note["title"])

     try:
          number = int(input("Enter number of note to open: "))
          index = number - 1

          if index < 0 or index >= len(all_notes):
               print("Invalid note number.")
               return

          selected_note = all_notes[index]
          print("Title:", selected_note["title"])
          print("Content:", selected_note["content"])

     except ValueError:
          print("Please enter a valid number.")
    
def delete():
     if len(all_notes) == 0:
          print("No notes to delete.")
          return

     for index, note in enumerate(all_notes):
          print(index + 1, "-", note["title"])

     try:
          number = int(input("Enter number of note you'd like to delete: "))
          index = number - 1

          if index < 0 or index >= len(all_notes):
               print("Invalid note number.")
               return

          removed_note = all_notes.pop(index)
          print("Deleted:", removed_note["title"])

     except ValueError:
          print("Please enter a valid number.")
     
def main():
     while True:
          print("1 - Add, 2 - View, 3 - Delete, 0 - Quit")
          choice = int(input("Enter choice: "))
          if choice == 0:
               break
          elif choice == 1:
               create()
          elif choice == 2:
               view()
          elif choice == 3:
               delete()
          else:
               print("Please enter 1,2, or 3")

main()
               
