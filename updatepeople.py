from tkinter import *
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import time
import os
from tkcalendar import Calendar,DateEntry
from datetime import date
import datetime

con=sqlite3.connect('database.db')
cur=con.cursor()

class Update(Toplevel):
    def __init__(self, person_id,user_id):
        Toplevel.__init__(self)
        self.geometry("550x450+550+200")
        self.title("Update Person")
        self.resizable(False,False)
        self.grab_set()
        
        self.times = time.time()
        today = date.today()
        lastdate=date(1900,1,1)
        
        self.user_id = user_id
        
        # To keep the Window stay above all other windows
        self.attributes("-topmost", True)
        # Get person from database
        self.person_id = person_id

        person=cur.execute("SELECT * FROM persons WHERE id =?",(self.person_id,))
        person_info = person.fetchall()
        print(person_info)
        #self.person_id=person_info[0][0]
        self.person_name=person_info[0][1]
        self.person_phone=person_info[0][2]
        self.person_email=person_info[0][3]
        self.person_image=person_info[0][5]
        
        dob=person_info[0][6]
        self.person_dob=datetime.datetime.strptime(dob,'%Y-%m-%d')
        #self.person_dob=dob
        
        
        
        # Frames
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/addperson.png')
        self.top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.topFrame, text='My Persons', font='arial 15 bold', fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)
        
        # labels and entries
        # Name
        self.lbl_name = Label(self.bottomFrame, text='*Name', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, self.person_name)
        self.ent_name.place(x=150, y=40)

        # Phone Number
        self.lbl_phone = Label(self.bottomFrame, text='*Phone', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, self.person_phone)
        self.ent_phone.place(x=150, y=85)
        
        # email
        self.lbl_email = Label(self.bottomFrame, text='Email', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_email.place(x=40, y=120)
        self.ent_email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_email.insert(0, self.person_email)
        self.ent_email.place(x=150, y=125)
       
        
       #bday
        self.lbl_bday = Label(self.bottomFrame, text='Birthday', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_bday.place(x=40, y=160)
        self.ent_bday = DateEntry(self.bottomFrame, width=28, bd=4,maxdate=today,mindate=lastdate,date_pattern='dd/mm/y')
        self.ent_bday.set_date(self.person_dob)
        #DateEntry(root,width=30,bg="darkblue",fg="white")
        self.ent_bday.place(x=150, y=165)
        
       #image
        self.lbl_image = Label(self.bottomFrame,height=120,width=120)
        self.lbl_image.place(x=400,y=30)
        self.person_image_new=Image.open(self.person_image)
        self.person_image_new = ImageTk.PhotoImage(self.person_image_new)
        self.lbl_image.config(image=self.person_image_new)
        self.photo=0
        
       
        # Button
        button = Button(self.bottomFrame, text='Update Person',font='arial 11 bold',command=self.updatePerson)
        button.place(x=280, y=200)
        
        #BrowseButton
        self.button=Button(self.bottomFrame,text='   Browse...  ', font='arial 11 bold',command=self.open_file)
        #RefreshButton
        self.btnrfsh = PhotoImage(file='icons/refresh.png')
        
        if(self.person_image!='image/nooimage.png'):
            self.button.place(x=398,y=165)
            self.buttonrfsh=Button(self.bottomFrame,command=self.click_refresh)
            self.buttonrfsh.config(image=self.btnrfsh)
            self.buttonrfsh.place(x=500,y=165)
            self.button['state'] = 'disabled'
        else:
            self.button.place(x=415,y=165)
        
        # Close the Window after the User click's the button and 
        # update operation complete's
        self.lift()
        
    def updatePerson(self):
        # Send window back bez U need to show Message Box
        self.attributes("-topmost", False)
        global person_image
        person_id = self.person_id
        person_name = self.ent_name.get()
        person_email = self.ent_email.get()
        person_phone = self.ent_phone.get()
        date=self.ent_bday.get_date()
        
        
        if(person_name and person_phone !=""):
            try:
                
                if(self.photo==0):
                    self.person_image_new= self.person_image
                elif(self.person_image=="image/nooimage.png" and self.photo==1):
                    image_obj=cv2.imread(filename,1)
                    image_obj=cv2.resize(image_obj,(120,120))
                    self.person_image_new = "image\{}.jpg".format(self.times)
                    cv2.imwrite(self.person_image_new,image_obj)
                elif(self.photo==1):
                    os.remove(self.person_image)
                    image_obj=cv2.imread(filename,1)
                    image_obj=cv2.resize(image_obj,(120,120))
                    #self.person_image_new = "image\{}.jpg".format(self.times)
                    cv2.imwrite(self.person_image,image_obj)                   
                    self.person_image_new=self.person_image
                elif(self.photo==2):                    
                    if(self.person_image!="image/nooimage.png"):
                        os.remove(self.person_image)
                    self.person_image_new=self.person_image_new
                person_im=self.person_image_new
                
                query= "UPDATE persons set name=?, email=?, phone=?,image=?,date=? WHERE id=? and user_id=?"
                cur.execute(query,(person_name,person_email,person_phone,person_im,date,person_id,self.user_id))
                con.commit()
                # Close the window bz record got updated
                
                self.destroy()
                messagebox.showinfo("Success","Person has been updated")
                #self.destroy()
            except:
                messagebox.showinfo("Warning", "Person has not been updated",icon='warning')
                # Bring the window back to Front
                #self.attributes("-topmost", True)
            #self.destroy() 
        else:
            messagebox.showerror("Error","* Fields cant be empty!",icon='warning')
    def open_file(self): 
        global filename,imgg
        self.attributes("-topmost", False)
        a = filedialog.askopenfilename(filetype =(("jpeg files","*.jpg"),("PNG files","*.png")))
        self.attributes("-topmost", True)
        filename=a
        original = Image.open(filename)
        resized = original.resize((120, 120),Image.ANTIALIAS)
        imgg = ImageTk.PhotoImage(resized)
        
        self.button.place(x=398,y=165)
        self.button['state'] = 'disabled'
        self.buttonrfsh=Button(self.bottomFrame,command=self.click_refresh)
        self.buttonrfsh.config(image=self.btnrfsh)
        self.buttonrfsh.place(x=500,y=165)
        
        self.lbl_image.config(image=imgg)
        self.photo=1
    def click_refresh(self):
        self.no_im='icons/noimage.png'
        self.no_img=Image.open(self.no_im)
        self.no_img = ImageTk.PhotoImage(self.no_img)
        self.lbl_image.config(image=self.no_img)
        self.buttonrfsh.destroy()
        self.button.place(x=415,y=165)
        self.button['state'] = 'normal'
        self.person_image_new='image/nooimage.png'
        self.photo=2
        
