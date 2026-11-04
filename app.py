
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_connection(): #this function ay para makapag connect sa database
    return mysql.connector.connect(host="localhost", 
                                   user="root", 
                                   password="041006", 
                                   database="hotel_db")


#this function naman ay para sa READ FUNCTION ibigsabihin lahat ng ginagawamong paaadd ng reservation
#pag update at pag delete also yung mga previous record... eto yung function na gagana para i reload lahat yun
def fetch_records():   
    
    tree.delete(*tree.get_children())
    try:
         #connection to the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        rows = cursor.fetchall()
       
        for row in rows:
            # Insert each row into the Tkinter Treeview table grid
            tree.insert("", tk.END, values=row)  
        # Close the database connection
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


# CREATE OPERATION 
def add_reservation():
   
    name = entry_name.get()
    room = entry_room.get()
    rtype = combo_type.get()
    cin = entry_in.get()
    cout = entry_out.get()
    # Validate IF may blangko sa mga form mag popo up yung input error
    if not (name and room and rtype and cin and cout):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # SQL query pa mag insert ng reservation record sa datbase tapos ginamitan naten ng place holder
        query = "INSERT INTO reservations (guest_name, room_number, room_type, check_in, check_out) VALUES (%s, %s, %s, %s, %s)"
        #tapos ipapass na nya yung laman sa place holder
        cursor.execute(query, (name, room, rtype, cin, cout))
        #i commit naten para masave sa database yung transaction
        conn.commit()
        conn.close()
        
        # Notify the user of successful addition
        messagebox.showinfo("Success", "Reservation added successfully!")
        
        # Clear the input form boxes
        clear_fields()
        # Refresh the table display to show the new record
        fetch_records()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add reservation: {e}")



# UPDATE OPERATION
def update_reservation():
   
    selected = tree.selection()
    if not selected:    
        messagebox.showwarning("Select Error", "Please select a record from the table to update.")
        return

      #to extract the unique ID from the selected table row pagkatapos i click
    res_id = tree.item(selected[0])['values'][0]
    
    #Get the updated text values na ginawa ni user
    name = entry_name.get()
    room = entry_room.get()
    rtype = combo_type.get()
    cin = entry_in.get()
    cout = entry_out.get()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        #SQL query to kukunin nya yung primary id sa database ng c-nlick mo kanina tapos iupdate nya
        query = """UPDATE reservations 
                   SET guest_name=%s, room_number=%s, room_type=%s, check_in=%s, check_out=%s 
                   WHERE id=%s"""           
        #ineexcicute nya yung query passing sa placeholder tapos ang ikakabit nya yung mga ginawa nating variable sa taas
        cursor.execute(query, (name, room, rtype, cin, cout, res_id))
        #i commit para mag update sa database
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Reservation updated successfully!")
        clear_fields()
        fetch_records()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update reservation: {e}")




# DELETE OPERATION
def delete_reservation():

    selected = tree.selection() 
    if not selected:
        messagebox.showwarning("Select Error", "Please select a record to delete.")
        return

    #to extract the unique ID from the selected table row pagkatapos i click
    res_id = tree.item(selected[0])['values'][0]
    
    # may poop up message nah pipili ka ng YES or NO para ma prevent naten yung accidentally madelete
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to cancel this reservation?")
    
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # SQL query to kukunin nya yung primary id sa database ng c-nlick mo kanina tapos idelete nya
            cursor.execute("DELETE FROM reservations WHERE id=%s", (res_id,))
            
            #para i save yung final commit at i close yung connection sa database
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Reservation deleted successfully!")
            clear_fields()
            fetch_records()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete reservation: {e}")
            

# Ang functioon na ere inaallow nya yung user na mag click sa mga data naten at pag katapos mong i click yung sempre
# SEmpree mag aapear yung mga info doon sa form para manavigate naten sya ulit like ma edit naten sya ulit like ma update or delete
def on_tree_select(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])['values']
        clear_fields()
        
        entry_name.insert(0, item[1])
        entry_room.insert(0, item[2])
        combo_type.set(item[3])
        entry_in.insert(0, item[4])
        entry_out.insert(0, item[5])

# function para mag clear ng form kung sakaling mag bago isip mo diba i clear mo lang
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_room.delete(0, tk.END)
    combo_type.set("Single")  # magreset yung combobox_dropdown to default value which is SINGLE ako
    entry_in.delete(0, tk.END)
    entry_out.delete(0, tk.END)


#-----  GUI  -------
#TAKE note DITO PO MAG UUMPISA LAHAT NG EXCUTION NATEN SA PROGRAM kung anong gagawin ng mga function sa taas naka base LAHAT DITO
#mag simula po dito hanggang baba nandito po yung mga GUI naten eto yung pinaka user interface naten
#at gumawa tayo ng dalawang frame kase ngani isang frame sa from at frame sa BUTOns
root = tk.Tk()  
root.title("Hotel Room Reservation System")
root.geometry("780x520") 

frame_form = tk.LabelFrame(root, text=" Reservation Details ", padx=10, pady=10)
frame_form.pack(fill="x", padx=15, pady=10)

tk.Label(frame_form, text="Guest Name:").grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(frame_form, width=25)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Room No:").grid(row=0, column=2, sticky="w", pady=5)
entry_room = tk.Entry(frame_form, width=15)
entry_room.grid(row=0, column=3, padx=10, pady=5)

tk.Label(frame_form, text="Room Type:").grid(row=1, column=0, sticky="w", pady=5)
combo_type = ttk.Combobox(frame_form, values=["Single", "Double", "Deluxe", "Suite"], width=22)
combo_type.set("Single")
combo_type.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Check-In (YYYY-MM-DD):").grid(row=1, column=2, sticky="w", pady=5)
entry_in = tk.Entry(frame_form, width=15)
entry_in.grid(row=1, column=3, padx=10, pady=5)

tk.Label(frame_form, text="Check-Out (YYYY-MM-DD):").grid(row=2, column=2, sticky="w", pady=5)
entry_out = tk.Entry(frame_form, width=15)
entry_out.grid(row=2, column=3, padx=10, pady=5)


#dito gumawa tayo ng 4 na button for there functionality sempre
#at gumawA MUNA po tayo ng frame para pag lagyan ng mga BUTOns
frame_buttons = tk.Frame(root)
frame_buttons.pack(fill="x", padx=15, pady=5)
# Button to trigger the CREATE function
btn_add = tk.Button(frame_buttons, text="Add Reservation", bg="#4CAF50", fg="white", command=add_reservation, width=15)
btn_add.pack(side="left", padx=5)
# Button to trigger the UPDATE function
btn_update = tk.Button(frame_buttons, text="Update Selection", bg="#2196F3", fg="white", command=update_reservation, width=15)
btn_update.pack(side="left", padx=5)
# Button to trigger the DELETE function
btn_delete = tk.Button(frame_buttons, text="Delete Selection", bg="#f44336", fg="white", command=delete_reservation, width=15)
btn_delete.pack(side="left", padx=5)
# Button to clear input boxes
btn_clear = tk.Button(frame_buttons, text="Clear Form", command=clear_fields, width=12)
btn_clear.pack(side="left", padx=5)

# dito gumamit ako ng treeview class eto ay builtin class na sa ttk tatawagin mo sya pag kaylanagn
#yung nakikita nating data table sa baba tapos nandon lahat ng updates or information eto po gumagagawa non
columns = ("ID", "Guest Name", "Room", "Type", "Check-In", "Check-Out")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.column("ID", width=40)
tree.column("Guest Name", width=180)
tree.column("Room", width=80)
tree.column("Type", width=100)
tree.column("Check-In", width=110)
tree.column("Check-Out", width=110)

tree.pack(fill="both", expand=True, padx=15, pady=10)
tree.bind("<<TreeviewSelect>>", on_tree_select)

#as you can see dito po mag uumpisa yung code dito po mag uumpisa yung exicution :>
fetch_records()
root.mainloop()