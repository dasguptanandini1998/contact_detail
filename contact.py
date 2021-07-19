from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import addpeople,updatepeople,myemail
import sqlite3
from PIL import Image, ImageTk
import os

con=sqlite3.connect('database.db')
cur = con.cursor()

class MyPeople(Toplevel):
    def __init__(self, user_id):
        Toplevel.__init__(self)
        self.user_id = user_id
        
        self.geometry("650x490+370+180")
        self.title("My Contact")
        self.resizable(False,False)     
        global person_id,size
        self.grab_set()
        query = ('SELECT * FROM users WHERE id =?')
        user = cur.execute(query,(self.user_id,))
        user_info = user.fetchall()
        #self.person_id=person_info[0][0]
        self.umail=user_info[0][3]
        
        
        #number of contacts
        query = ('SELECT * FROM persons WHERE user_id=?')
        user = cur.execute(query,[(self.user_id)])
        persons = user.fetchall()
        total=str(len(persons))
        
        # Frames
        self.top = Frame(self, height=140, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=350, bg='#fcc324')
        self.bottomFrame.pack(fill=X)
       
        # Heading and image
        self.top_image = PhotoImage(file='icons/person_icon.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=2)
        self.heading = Label(self.top, text='My Persons', font='arial 15 bold', fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)
        
        #totalcontact
        
        if(total!='0'):
            if(total=='1'):
                self.msg=Label(self.top, text='('+total+' Contact)',font='arial 15 bold',fg='#003f8a', bg='white')
            else:
                self.msg=Label(self.top, text='('+total+' Contacts)',font='arial 15 bold',fg='#003f8a', bg='white')
            self.msg.place(x=260, y=90)
        
        #listbox
        self.listBox=Listbox(self.bottomFrame,selectmode="multiple",width=45,height=30,font='Verdana 9 bold')
        self.listBox.grid(row=0, column=0,padx=(20,0))
        
        #ScrollBar
        self.sb1=Scrollbar(self.bottomFrame,orient=VERTICAL)
        self.sb1.config(command= self.listBox.yview)
        self.listBox.config(yscrollcommand=self.sb1.set)
        self.sb1.grid(row=0,column=1,sticky="ns")
        
        self.sb2=Scrollbar(self.bottomFrame,orient=HORIZONTAL)
        self.sb2.config(command= self.listBox.xview)
        self.listBox.config(xscrollcommand=self.sb2.set)
        self.sb2.grid(row=0,column=0,sticky="ew",pady=(230,0))
        
        count = 0
        if persons:
            for person in persons:
                self.listBox.insert(END,str(person[0])+"-"+person[1]+" "+person[2]+" "+person[3]+" "+person[6])
                count +=1
        
        self.listBox.bind('<<ListboxSelect>>', self.onselect)
        
        self.btnadd=Button(self.bottomFrame,text='Add',width=12,font='Sans 12 bold',command=self.add)
        self.btnadd.place(x=480,y=160)
        
        self.btnupdate = Button(self.bottomFrame, text='Update', width=12, font='Sans 12 bold',command=self.update)
        self.btnupdate.place(x=480,y=210)
        
        self.btndlt = Button(self.bottomFrame, text='Delete', width=12, font='Sans 12 bold',command=self.delete)
        self.btndlt.place(x=480,y=260)
        
        self.btnmail = Button(self.bottomFrame, text='Send Email', width=12, font='Sans 12 bold',command=self.mymail)
        self.btnmail.place(x=480,y=310)
        
        size=self.listBox.size()
        if size==0:
            self.btndlt['state'] = 'disabled'
            self.btnupdate['state'] = 'disabled'
        if self.umail=='optional':
            self.btnmail['state'] = 'disabled'
            
        
        
    def mymail(self):
        self.grab_set()
        top=Toplevel()
        top.geometry("350x150+500+300")
        top.title("Enter Password")
        top.resizable(False,False)
        top.attributes("-topmost", True)
        frame=Frame(top,height=250, bg='#fcc324')
        frame.pack(fill=X)
        pwdlbl = Label(frame,text='Password*',font='arial 15 bold',fg='white',bg='#fcc324')
        pwdlbl.place(x=10,y=40)
        pwdent=Entry(frame,width=30,bd=4,show = '*')
        pwdent.place(x=130,y=40)
        pwdent.focus()
        top.grab_set() #for modal window
        
        
        
        def send():        
            pwd=pwdent.get()
            top.destroy()
            if pwd!='':            
                selected_item=self.listBox.curselection()
                x=len(selected_item) 
                if (x==0 or x>1):
                    mail=myemail.SendMail("",self.umail,pwd)
                else:
                    mail=myemail.SendMail(self.person_id,self.umail,pwd)
                self.destroy()
                self.destroy()
            else:
                 
                messagebox.showerror('Error','Please enter your password!', icon='warning') 
                self.mymail()
        button = Button(frame, text='OK',font='arial 11 bold',command=send)
        button.place(x=200,y=80)
        top.mainloop()
        
        
            

    def add(self):
        addpage=addpeople.AddPeople(self.user_id)
        # Close the Current Window
        self.destroy()
    
    def update(self):
        selected_item=self.listBox.curselection()
        x=len(selected_item)
        if(x==1):                    
            updatepage=updatepeople.Update(self.person_id,self.user_id)
            self.destroy()   
        #self.attributes("-topmost", False)
    
    def delete(self):
        
        selected_item=self.listBox.curselection()
        x=len(selected_item)
        #print(selected_item)
        if(x!=0):
            self.btnmail['state'] = 'disabled'
            self.btnadd['state'] = 'disabled'
            self.btnupdate['state'] = 'disabled'
            self.btndlt['state'] = 'disabled'
            self.attributes("-topmost", False)
            if(x==1):
                mbox= messagebox.askquestion("Warning"," Delete Contact?\n"+str(x)+" contact will be deleted.",icon='warning')
                
            elif(x>=1):
                mbox= messagebox.askquestion("Warning"," Delete Contact?\n"+str(x)+" contacts will be deleted.",icon='warning')
                
            
            if mbox == 'yes':
                
                i=0
                try:
                    while(i<x):   
                        person=self.listBox.get(selected_item[i])
                        self.person_id=person.split("-")[0]
                        
                        person=cur.execute("SELECT * FROM persons WHERE id =?",(self.person_id,))
                        person_info = person.fetchall()
                        self.person_image=person_info[0][5]
                        if(self.person_image!='image/nooimage.png'):
                            os.remove(self.person_image)
                        
                        person=cur.execute("DELETE FROM persons WHERE id=?", (self.person_id,))
                        con.commit()
                                            
                        i+=1
                    self.destroy()
                    messagebox.showinfo("Success","Person has been deleted!")
                    
                    
                except:
                    messagebox.showinfo("Info","Person has not been deleted!")
            #self.attributes("-topmost", True)
            #self.btnmail['state'] = 'normal'
            self.btnadd['state'] = 'normal'
            self.btnupdate['state'] = 'normal'
            self.btndlt['state'] = 'normal'
            if self.umail!='optional':
                self.btnmail['state'] = 'normal'
    def onselect(self,evt):
        global selected_item
        val = evt.widget
        selected_item=val.curselection()
        person=val.get(selected_item)
        self.person_id=person.split("-")[0]
        
        person=cur.execute("SELECT * FROM persons WHERE id =?",(self.person_id,))
        person_info = person.fetchall()
        self.person_image=person_info[0][5]
        
        self.image_disp = Label(self.bottomFrame,height=120,width=120)
        self.image_disp.place(x=480,y=20)
        
        self.person_image_new=Image.open(self.person_image)
        self.person_image_new = ImageTk.PhotoImage(self.person_image_new)
        self.image_disp.config(image=self.person_image_new)
        
        person_id=self.person_id
        
    
        