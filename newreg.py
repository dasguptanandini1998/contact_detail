from tkinter import *
import sqlite3
from tkinter import messagebox
import start
con=sqlite3.connect('database.db')
cur = con.cursor()
class NewReg(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        
        self.geometry("650x490+620+200")
        self.title("New Registration")
        self.resizable(False,False)
        self.grab_set()
        
        self.top = Frame(self, height=140, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=350, bg='#fcc324')
        self.bottomFrame.pack(fill=X)
       
        # Heading and image
        self.top_image = PhotoImage(file='icons/newreg.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=2)
        self.heading = Label(self.top, text='Registration', font='arial 15 bold', fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60) 

        ############################
        # Username
        self.lbl_uname=Label(self.bottomFrame,text=' Username*  ',font='arial 15 bold',fg='black',bg='#fcc324')
        self.lbl_uname.place(x=130,y=85)
        self.ent_uname=Entry(self.bottomFrame,width=24,font='Verdana 10 bold',bd=3)
        self.ent_uname.place(x=250,y=90)
        
        # Password
        self.lbl_pwd=Label(self.bottomFrame,text=' Password*  ',font='arial 15 bold',fg='black',bg='#fcc324')
        self.lbl_pwd.place(x=130,y=125)
        self.ent_pwd=Entry(self.bottomFrame,width=24,font='Verdana 10 bold',bd=3, show = '*')
        self.ent_pwd.place(x=250,y=130)
        
        # email
        self.lbl_mail=Label(self.bottomFrame,text='     Email  ',font='arial 15 bold',fg='black',bg='#fcc324')
        self.lbl_mail.place(x=130,y=165)
        self.ent_mail=Entry(self.bottomFrame,width=24,font='Verdana 10 bold',bd=3)
        self.ent_mail.place(x=250,y=170)

        #start.Application.regpersonBtn.destroy()
        # Login Button
        self.btn3Icon=PhotoImage(file='icons/signin.png')
        self.loginBtn=Button(self.bottomFrame,text='    Register      ',font='arial 12 bold',command=self.regst)
        self.loginBtn.config(image=self.btn3Icon,compound=LEFT)
        self.loginBtn.place(x=300, y=210)
        
        
        self.ent_uname.focus()
        
        
    def regst(self):
        self.attributes("-topmost", False)
        uname=self.ent_uname.get()
        pwd=self.ent_pwd.get()                
        umail = self.ent_mail.get()
        if umail=='':
            umail='optional'

    
        if(uname and pwd !=""):
            try:
                query="INSERT INTO 'users' (uname,pwd,umail) VALUES(?,?,?)"
                cur.execute(query,(uname,pwd,umail))
                con.commit()
                # Close the window bz record got inserted
                
                self.destroy()
                messagebox.showinfo("Success","Successfully added to database!",icon='info')
            except:
                messagebox.showerror("Error", "Cant add to database!", icon='warning')

        else:
            messagebox.showerror("Error","* Fields cant be empty!",icon='warning')
            self.attributes("-topmost", True)
            self.ent_uname.focus()
            # Bring the window back to Front
            #self.attributes("-topmost", True)
        
    