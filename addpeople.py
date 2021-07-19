from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog 
from PIL import Image, ImageTk
import cv2
import time
import os
from tkcalendar import Calendar,DateEntry
import datetime
import re

con=sqlite3.connect('database.db')
cur=con.cursor()

class AddPeople(Toplevel):
    def __init__(self, user_id):
        Toplevel.__init__(self)
        self.user_id = user_id
        
        lastdate=datetime.datetime(1900,1,1)
        today = datetime.date.today()
        self.geometry("650x450+550+200")
        self.title("Add People")
        self.resizable(False,False)
        self.grab_set()
        self.times = time.time()
        # To keep the Window stay above all other windows
        self.attributes("-topmost", True)
        self.photo=0
        # Frames
        self.top = Frame(self, height=150, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=300, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/addperson.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='My Persons', font='arial 15 bold', fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        ##############################################################################

        #labels and entries
        #name
        self.lbl_name=Label(self.bottomFrame,text='Name*',font='arial 15 bold',fg='white',bg='#fcc324')
        self.lbl_name.place(x=40,y=40)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.focus()
        self.ent_name.place(x=150,y=45)

        #Phone Number
        self.lbl_phone = Label(self.bottomFrame, text='Phone*', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.place(x=150, y=85)
        
        #email
        self.lbl_email = Label(self.bottomFrame, text='Email', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_email.place(x=40, y=120)
        self.ent_email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_email.place(x=150, y=125)
        
        #bday
        self.lbl_bday = Label(self.bottomFrame, text='Birthday', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_bday.place(x=40, y=160)
        self.ent_bday = DateEntry(self.bottomFrame, width=28, bd=4,mindate=lastdate,maxdate=today,date_pattern='dd/mm/y')
        #DateEntry(root,width=30,bg="darkblue",fg="white")
        self.ent_bday.place(x=150, y=165)
        
        
        #Button
        self.btn2Icon = PhotoImage(file='icons/add.png')
        self.button=Button(self.bottomFrame,text='   Add Person  ', font='arial 11 bold',command=self.addPerson)
        self.button.config(image=self.btn2Icon, compound=LEFT)
        self.button.place(x=250,y=200)
        
        
        #image
        self.file='icons/noimage.png'
        #self.img=Image.open(self.file)
        self.img = PhotoImage(file=self.file)
        self.lbl_img_disp = Label(self.bottomFrame,height=120,width=120,image=self.img)
        self.lbl_img_disp.place(x=400,y=30)
        
        
        #BrowseButton
        #self.btn2Icon = PhotoImage(file='icons/add.png')
        self.button=Button(self.bottomFrame,text='   Browse...  ', font='arial 11 bold',command=self.open_file)
        self.button.config( compound=RIGHT)
        self.button.place(x=412,y=165)
        
        #RefreshButton
        self.btnrfsh = PhotoImage(file='icons/refresh.png')
        
        
    def addPerson(self):
        # Send window back bez U need to show Message Box
        self.attributes("-topmost", False)
        
        x=re.match("/^[0-9]*$/",self.ent_phone.get())
        
        name=self.ent_name.get()
        phone=self.ent_phone.get()
        email=self.ent_email.get()
        dates=self.ent_bday.get_date()
        print(dates)
        if(name and  phone !=""):
            
            if(self.photo==0 or self.photo==2): 
                self.imgs = cv2.imread(self.file,1)
                img_name="image/nooimage.png"
                cv2.imwrite(img_name,self.imgs)
                
                #image_obj = cv2.imread(img_name_new,1)
                print('no')                                       
            else:
                image_obj=cv2.imread(filename,1)
                image_obj=cv2.resize(image_obj,(120,120))
                img_name = "image\{}.jpg".format(self.times)
                cv2.imwrite(img_name,image_obj)
                #image_obj = cv2.imread(img_name,1)
                print('yes')
            print(img_name)
            
            try:
                query="INSERT INTO 'persons' (name,phone,email,user_id,image,date) VALUES(?,?,?,?,?,?)"
                cur.execute(query,(name,phone,email,self.user_id,img_name,dates))
                con.commit()
                # Close the window bz record got inserted
                self.destroy()
                messagebox.showinfo("Success","Successfully added to database!",icon='info')
            except:
                messagebox.showerror("Error", "Cant add to database!", icon='warning')

        else:
            messagebox.showerror("Error","* Fields cant be empty!",icon='warning')
            # Bring the window back to Front
            self.attributes("-topmost", True)
            self.ent_name.focus()
        
        
    def open_file(self): 
        global filename,imgg
        self.attributes("-topmost", False)
        a = filedialog.askopenfilename(filetype =(("jpeg files","*.jpg"),("PNG files","*.png")))
        self.attributes("-topmost", True)
        filename=a
        original = Image.open(filename)
        resized = original.resize((120, 120),Image.ANTIALIAS)
        imgg = ImageTk.PhotoImage(resized)
        
        
        self.lbl_img_disp.config(image=imgg)
        self.button.place(x=397,y=165)
        self.button['state'] = 'disabled'
        self.buttonrfsh=Button(self.bottomFrame,command=self.click_refresh)
        self.buttonrfsh.config(image=self.btnrfsh)
        self.buttonrfsh.place(x=501,y=165)
        self.photo=1
        
    def click_refresh(self):
        self.lbl_img_disp.config(image=self.img)
        self.buttonrfsh.destroy()
        self.button.place(x=412,y=165)
        self.button['state'] = 'normal'
        self.photo=2