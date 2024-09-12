from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox as mb

contact=Tk()
contact.geometry('1200x650')
contact.resizable(0, 0)
contact.title("Contact Management System")
contact.configure(bg="darkgrey")
# contact.wm_iconbitmap("Contact.ico")
# database connectivity---------------------------------------
connector = sqlite3.connect('contact_management_system.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS contact_book_record (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, FIRSTNAME TEXT, LASTNAME TEXT, PHONE_NO TEXT, EMAIL TEXT, ADDRESS TEXT)"
)
# functions define--------------------------------------------------------------------


def display_records():

       tree.delete(*tree.get_children())
       curr = connector.execute('SELECT * FROM contact_book_record')
       data = curr.fetchall()
       for records in data:
           tree.insert('', END, values=records)



def save_record():
   global fname_v, lname_v, number_v, email_v, address_v
   fname = fname_v.get()
   lname = lname_v.get()
   contact = number_v.get()
   email = email_v.get()
   address = address_v.get()
   if not fname or not lname or not contact or not email or not address:
       mb.showerror('Error!', "Please fill all the missing fields!!")

   else:
       try:
           connector.execute(
           'INSERT INTO  contact_book_record(FIRSTNAME, LASTNAME, PHONE_NO, EMAIL, ADDRESS) VALUES (?,?,?,?,?)', (fname, lname, contact, email, address)
           )
           
           connector.commit()
           mb.showinfo('Record added', f"Contact Dtail of{fname} was successfully added!")
           reset()
           display_records()
       except ValueError:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def delete_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       tree.delete(current_item)
       connector.execute('DELETE FROM contact_book_record WHERE ID=%d' % selection[0])
       connector.commit()
       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
       display_records()

def reset():
   global  fname_v, lname_v, number_v, email_v, address_v
   for i in ['fname_v', 'lname_v', 'number_v', 'email_v', 'address_v']:
       exec(f"{i}.set('')")




def search():
     for child in tree.get_children():
        tree.delete(child)
     name_res = search_v.get()
     conn_db = sqlite3.connect('contact_management_system.db')
     cur_db = conn_db.cursor()
     queries = cur_db.execute("SELECT * FROM contact_book_record WHERE \
                     FIRSTNAME = (?)", (name_res,))
     list_res = []
     for result in queries:
         tree.insert('', END, values=result)
         list_res.append(result)

     # mb.showinfo("search item",f"Result : %s contact(s).' % (len(list_res))")
     # rslt_info.configure(text='Result : %s contact(s).' % (len(list_res)))
     conn_db.commit()
     cur_db.close()
     conn_db.close()








# fonts----------------------------------------------------------------------
heading_font = "Cambria 19 bold"
lableframe_font = "Cambria 14"
text_font = "Cambria 13 "
text_font2 = "Cambria 12 "
background_l = "darkgrey"
# login form---------------------------------------------------------




# heading-------------------------------------------------------------------

heading = Frame(contact, bg="gray", borderwidth=4, relief=GROOVE)
heading.pack(side=TOP, fill=X)
Label(heading, text="Contacts Book", font=heading_font, bg="gray").pack()

# variables--- --------------------------------------------------------
fname_v = StringVar()
lname_v = StringVar()
number_v = StringVar()
email_v = StringVar()
address_v = StringVar()
search_v = StringVar()

# contact information-----------------------------------
label_frame = LabelFrame(contact, bg=background_l, borderwidth=8)
label_frame.pack(expand='yes', fill='both', padx=12, pady=15, side=LEFT, anchor="nw")
label_frame2 = LabelFrame(label_frame, bg=background_l, borderwidth=4, text="Contact Info", font=lableframe_font)
label_frame2.pack(expand='yes', ipadx=210, ipady=270, anchor="nw", side=LEFT, pady=30, padx=30)

fname_l = Label(label_frame2, text='First Name*', font=text_font, bg=background_l)
fname_l.place(x=40, y=40)

lname_l = Label(label_frame2, text='Last Name*', font=text_font, bg=background_l)
lname_l.place(x=40, y=100)

email_l = Label(label_frame2, text='Mobile No*', font=text_font, bg=background_l)
email_l.place(x=40, y=160)
number_l = Label(label_frame2, text='Email*', font=text_font, bg=background_l)

number_l.place(x=40, y=220)

address_l = Label(label_frame2, text="Address*", font=text_font, bg=background_l)
address_l.place(x=40, y=280)


# entry-------------------------------------------------------

Entry(label_frame2, textvariable=fname_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=190, y=40, width=195)
Entry(label_frame2, textvariable=lname_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=190, y=100, width=195)
Entry(label_frame2, textvariable=number_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=190, y=160, width=195)
Entry(label_frame2, textvariable=email_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=190, y=220, width=195)

Entry(label_frame2, textvariable=address_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=190, y=280,width=195)

# button-----------------------------------------------------
Button(label_frame2, text="Save", width=13, borderwidth=5 , relief=GROOVE, fg="black", font="arial 10 bold", command=save_record).place(x=60, y=390)
Button(label_frame2,text="Reset", width=13, borderwidth=5, relief=GROOVE, fg="black", font="arial 10 bold",command=reset).place(x=205, y=390)



# RECORD------------------------------------------------------------------------
Label(label_frame, text="Contact Records !", bg=background_l, fg="navy").place(x=1015, y=14)
label_frame3 = LabelFrame(label_frame, bg=background_l, borderwidth=4, text="Search Bar", font=lableframe_font)
label_frame3.pack(expand='yes', ipadx=340 , ipady=270, anchor="s", pady=30, padx=18)

Entry(label_frame3, textvariable=search_v, font=text_font2, bg="white", borderwidth=2, relief=SUNKEN).place(x=21, y=10, width=280, height=29)
Button(label_frame3, text="Search", width=11, borderwidth=3, relief=GROOVE, fg="black", font="arial 10 bold", bg="gray",command=search).place(x=317, y=9)

Button(label_frame3, text="Delete", width=9, borderwidth=3, relief=GROOVE, fg="black", font="arial 10 bold", bg="gray",command=delete_record).place(x=430, y=9)


# scroll bar-----------------------------------------------------
tree = ttk.Treeview(label_frame3, height=55, selectmode=BROWSE,
                   columns=('ID', "FirstName", "LastName", "Contact", "Email", "Address"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('ID', text='ID', anchor=CENTER)
tree.heading('FirstName', text='First Name', anchor=CENTER)
tree.heading('LastName', text='Last Name', anchor=CENTER)
tree.heading('Contact', text='Phone No', anchor=CENTER)
tree.heading('Email', text='Email ID', anchor=CENTER)
tree.heading('Address', text='Address', anchor=CENTER)

tree.column('#0', width=0, stretch=NO,anchor=CENTER)
tree.column('#1', width=50, stretch=NO,anchor=CENTER)
tree.column('#2', width=90, stretch=NO,anchor=CENTER)
tree.column('#3', width=90, stretch=NO,anchor=CENTER)
tree.column('#4', width=140, stretch=NO,anchor=CENTER)
tree.column('#5', width=120, stretch=NO,anchor=CENTER)

tree.place(y=52, relwidth=1, relheight=0.86, relx=0.01)
display_records()



contact.mainloop()