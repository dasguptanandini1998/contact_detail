from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from tkinter import filedialog
import sqlite3
from tkinter.ttk import Progressbar
from tkinter import ttk
import threading

con=sqlite3.connect('database.db')
cur=con.cursor()

class SendMail(Toplevel):
    def __init__(self,person_id,umail,pwd):
        Toplevel.__init__(self)
        self.geometry("650x490+620+200")
        self.title("My Email")
        self.resizable(False,False)
        self.grab_set()
        self.counter=0
        global frm_email,password
        self.person_id = person_id
        frm_email=umail
        password=pwd
        self.top = Frame(self, height=140, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=350, bg='#fcc324')
        self.bottomFrame.pack(fill=X)
       
        # Heading and image
        self.top_image = PhotoImage(file='icons/email.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=2)
        self.heading = Label(self.top, text='Email', font='arial 15 bold', fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)
        
        #to
        self.lbl_to=Label(self.bottomFrame,text='To',font='arial 15 bold',fg='white',bg='#fcc324')
        self.lbl_to.place(x=40,y=20)
        self.ent_to=Entry(self.bottomFrame,width=60,bd=4)
        self.ent_to.focus()
        self.ent_to.place(x=150,y=25)
        
        if(self.person_id!=""): 
            person=cur.execute("SELECT * FROM persons WHERE id =?",(self.person_id,))
            person_info = person.fetchall()
            print(person_info)
            self.person_email=person_info[0][3]
            self.ent_to.insert(0,self.person_email)
        
        #subject
        self.lbl_subj = Label(self.bottomFrame, text='Subject', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_subj.place(x=40, y=60)
        self.ent_subj = Entry(self.bottomFrame, width=60, bd=4)
        self.ent_subj.place(x=150, y=65)
        
        #body
        self.lbl_body = Label(self.bottomFrame, text='Body', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_body.place(x=40, y=100)
        self.ent_body = Text(self.bottomFrame, width=50,height=8, bd=4)
        self.ent_body.place(x=150, y=105)
        
        #sendbutton
        button = Button(self.bottomFrame, text='Send',font='arial 11 bold',command=self.sendmail)
        button.place(x=450, y=290)
        
        #AttachmentButton
        self.btnatch = PhotoImage(file='icons/atch.png')
        self.buttonatch=Button(self.bottomFrame,command=self.attachbtn)
        self.buttonatch.config(image=self.btnatch)
        self.buttonatch.place(x=510,y=290)
        
        
        
        
    def sendmail(self):
        
        def mailthread():
            while True:
                progress = Progressbar(self.bottomFrame, orient=HORIZONTAL, length=200, mode='determinate')
                progress.place(x=235,y=220)
                progress['value'] = 50
        
        to_email=self.ent_to.get()        
        sub=self.ent_subj.get()
        message=self.ent_body.get(1.0,END)
        
        # self.email_thread = threading.Thread(target = mailthread)
        # self.email_thread.start()
        
        def Success():
            self.destroy()
            top = Toplevel(background="#fcc324")
            top.geometry("350x250+500+200")
            top.title('Success')
            msg=Message(top,text='\n\n\n\nMail Sent!'+'  \ud83d\ude03' ,font='arial 15 bold',fg='white',bg="#fcc324").pack()
            top.after(3000, top.destroy)
            
        def Failed():
            self.destroy()
            top = Toplevel(background="#fcc324")
            top.geometry("350x250+500+200")
            top.title('Failed')
            msg=Message(top,text='\n\n\n\nSomething wrong!',font='arial 15 bold',fg='white',bg="#fcc324")
            #msg.place(x=100,y=90)
            msg.pack()
            top.after(3000, top.destroy)
            
            
        if(to_email!=""):
            self.attributes("-topmost", True)
            if len(self.ent_body.get(1.0,END))==1:
                mbox= messagebox.askquestion("Warning"," Send this message without a subject or text in the body?",icon='warning')
                if mbox == 'yes':
                    pass
        
            msg=MIMEMultipart()
            msg['From']=frm_email
            msg['To']=to_email
            msg['Subject']=sub
            msg.attach(MIMEText(message,'plain'))
        
        
            try:
            
                if(self.counter!=0):
                    #print(filename)
                    self.attachment=open(filename,'rb')
                    part=MIMEBase('application','octet-stream')
                    part.set_payload((self.attachment).read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',"attachment; filename= "+filename)
                    msg.attach(part)
                server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                server.ehlo()
                server.login(frm_email,password)
                # msg.attach(part)
                server.sendmail(frm_email,to_email,msg.as_string())               
                Success()
                
                server.close()
                
                return True
                # print('True')
            except Exception as e:
                print('Something wrong'+str(e))
                Failed()
            
        else:
            self.attributes("-topmost", False)
            messagebox.showerror("Error","Add a recipient.",icon='warning') 
    def attachbtn(self):
        global filename
        filename = filedialog.askopenfilename(title="Choose A File")
        #print(filename)
        if filename!='':
            
            self.attach_ent=Entry(self.bottomFrame,width=60,bd=4)
            self.attach_ent.place(x=150,y=250)
            self.attach_ent.insert(0,filename)
            self.attach_ent.config(state="readonly")
        
            #filename=self.attach_ent.get()
            self.counter=+1
            
    
        
            
        