from tkinter import *
import threading
import time
import datetime
import sqlite3
import contact,newreg
from tkinter import ttk
from tkinter import messagebox


date = datetime.datetime.now().date()
con=sqlite3.connect('database.db')
cur=con.cursor()

user_id = 0


class Application(object):
    def __init__(self,master):
        self.master = master
                
        
        #Frames
        self.top=Frame(master,height=150,bg='white')
        self.top.pack(fill=X)
        self.bottom=Frame(master,height=250,bg='#adff2f')
        self.bottom.pack(fill=X)
        
        #Heading, image and date
        self.top_image= PhotoImage(file='icons/book.png')
        self.top_image_lbl=Label(self.top,image=self.top_image,bg='white')
        self.top_image_lbl.place(x=120,y=10)
        self.heading=Label(self.top,text=' Contact App',font='arial 15 bold', fg='#ffa500',bg='white')
        self.heading.place(x=260,y=60)
        

        #First Button
        self.btn1Icon=PhotoImage(file='icons/man.png')
        self.personBtn=Button(self.bottom,text='    My People   ',font='arial 12 bold', command=self.openMyPeople)
        self.personBtn.config(image=self.btn1Icon,compound=LEFT,state='disabled')
        self.personBtn.place(x=150, y=30)


        #Second Button
        self.btn2Icon = PhotoImage(file='icons/add.png')
        self.regpersonBtn = Button(self.bottom, text=' New Register ', font='arial 12 bold', command=self.funcRegPeople)
        self.regpersonBtn.config(image=self.btn2Icon, compound=LEFT)
        self.regpersonBtn.place(x=330, y=30)

        ############################
        # Username
        self.lbl_name=Label(self.bottom,text=' Username*  ',font='arial 15 bold',fg='black',bg='#adff2f')
        self.lbl_name.place(x=130,y=85)
        self.ent_uname=Entry(self.bottom,width=24,font='Verdana 10 bold',bd=3)
        #self.ent_uname.insert(0,'nandini')
        self.ent_uname.place(x=250,y=90)
        
        # Password
        self.lbl_pwd=Label(self.bottom,text=' Password*  ',font='arial 15 bold',fg='black',bg='#adff2f')
        self.lbl_pwd.place(x=130,y=125)
        self.ent_pwd=Entry(self.bottom,width=24,font='Verdana 10 bold',bd=3, show = '*')
        #self.ent_pwd.insert(0,'8910')
        self.ent_pwd.place(x=250,y=130)


        # Login Button
        self.btn3Icon=PhotoImage(file='icons/login_2.png')
        self.loginBtn=Button(self.bottom,text='    Login      ',font='arial 12 bold',command=self.login)
        self.loginBtn.config(image=self.btn3Icon,compound=LEFT)
        self.loginBtn.place(x=200, y=180)
        
        # Logout Button
        self.btn4Icon=PhotoImage(file='icons/logout.png')
        self.logoutBtn=Button(self.bottom,text='    Logout      ',font='arial 12 bold',command=self.logout)
        self.logoutBtn.config(image=self.btn4Icon,compound=LEFT,state='disabled')
        self.logoutBtn.place(x=330, y=180)
        
        ############################
        self.footerFrame=Frame(master,height=50,bg='black')
        self.footerFrame.pack(fill=X)
        
        ############################
        self.date_lbl=Label(self.footerFrame,text="Today's date: " +str(date),font='arial 12 bold', bg='black', fg='#ffa500')
        self.date_lbl.place(x=90,y=10)
        

        self.time_lbl=Label(self.footerFrame,font='arial 12 bold', bg='black', fg='#ffa500')
        self.time_lbl.place(x=350,y=10)
        
        self.t1 = threading.Thread(target=self.printTime)
        self.t1.start()
        
            
    def openMyPeople(self):
        contact.MyPeople(user_id)

    def funcRegPeople(self):
        reg=newreg.NewReg()
        
        
    def login(self):
        global user_id
        self.uname = self.ent_uname.get()
        self.pwd = self.ent_pwd.get()
        
        if( self.uname and self.pwd ==""):
            messagebox.showerror("Error","* Fields cant be empty!",icon='warning')
        else:
            
            try:
                query = ('SELECT * FROM users WHERE uname=? AND pwd=?')
                user = cur.execute(query,[(self.uname),(self.pwd)])
                user_info = user.fetchall()
                if user_info:
                    user_id = user_info[0][0]
                    self.personBtn['state'] = 'normal'
                    self.logoutBtn['state'] = 'normal'
                    self.regpersonBtn['state'] = 'disabled'
                    
                    self.ent_uname['state'] = 'disabled'
                    self.ent_pwd['state'] = 'disabled'
                    self.loginBtn['state'] = 'disabled'
                    self.lbl_wlcm=Label(self.bottom,text='Welcome   '+self.uname+'  \ud83d\ude03',font='arial 15 bold',fg='black',bg='#adff2f')
                    self.lbl_wlcm.place(x=235,y=220)
                    messagebox.showinfo("Success","Login Successful",icon='info')
                else:
                    messagebox.showerror("Error", "Login falied!", icon='warning')
            except:
                messagebox.showerror("Error", "Login falied!", icon='warning')
    
    def logout(self):
        self.ent_uname['state'] = 'normal'
        self.ent_pwd['state'] = 'normal'
        self.ent_uname.delete(0, "end")
        self.ent_pwd.delete(0, "end")
        self.ent_uname.focus()
        
        for widget in self.master.winfo_children():
            if isinstance(widget,Toplevel):
                widget.destroy()
        
        self.personBtn['state'] = 'disabled'
        self.logoutBtn['state'] = 'disabled'
        self.loginBtn['state'] = 'normal'
        self.regpersonBtn['state'] = 'normal'
        self.lbl_wlcm.destroy()
        self.t1.kill()
        

    def printTime(self): 
        while True:
            localtime = time.localtime()
            result = time.strftime("%I:%M:%S %p", localtime)
            time.sleep(1)
            self.time_lbl.config(text="Now: "+str(result))
        
def main():
    root = Tk()
    app = Application(root)
    root.title("  Contact App   ")
    root.iconbitmap(r'icons/appicon.ico')
    

    root.geometry("650x450+350+200")
    root.resizable(False,False)
    root.grab_set()
    root.mainloop()

if __name__ == '__main__':
    main()