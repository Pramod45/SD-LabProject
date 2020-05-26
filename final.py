from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pymysql

root=Tk()

class login:
    def __init__(self, root):
        self.root=root
        self.root.title("Login page")
        self.root.geometry("1510x900+0+0")
        self.frame=Frame(self.root, bd=4, relief=RIDGE, bg="#221E1D")
        self.frame.place(x=500, y=100, width=500, height=408)

        self.username=StringVar()
        self.password=StringVar()

        title_lbl=Label(self.frame, text="Login to stone crushing's", bd=8, relief=RIDGE, font=("Times new roman", 30, "bold"), fg="white",  bg="#221E1D")
        title_lbl.pack(side=TOP, fill=X)

        #------------------------loginframe------------------------------
        self.frame1=Frame(self.frame, bg="#221E1D", bd=4,  relief=RIDGE)
        self.frame1.place(x=0, y=60, width=491.5, height=340)

        lbl_username=Label(self.frame1,  text="User name",bd=22, font=("arial", 20, "bold"), bg="#221E1D", fg="white")
        lbl_username.grid(row=1, columnspan=1,pady=10,padx=30, sticky="w")

        txt_username=Entry(self.frame1,textvariable=self.username,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_username.grid(row=1, columnspan=2,pady=20,padx=250, sticky="w")

        lbl_password=Label(self.frame1,  text="Password", bd=22, font=("arial", 20, "bold"), bg="#221E1D", fg="white")
        lbl_password.grid(row=2, columnspan=1,pady=10,padx=30, sticky="w")

        txt_password=Entry(self.frame1,textvariable=self.password,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE, show="*")
        txt_password.grid(row=2, columnspan=2,pady=20,padx=250, sticky="w")

        #====================================================================

        self.frame2=Frame(self.frame, bg="#221E1D", bd=4)
        self.frame2.place(x=6, y=280, width=480, height=100)

        login=Button(self.frame2, text="Login", width=15,height=2, relief=RAISED, command=self.login).grid(row=1, column=0, padx=20, pady=10)
        reset=Button(self.frame2, text="Reset", width=15,height=2, relief=RAISED, command=self.reset).grid(row=1, column=1, padx=25, pady=35)
        exit=Button(self.frame2, text="Exit", width=15,height=2, relief=RAISED).grid(row=1, column=2, padx=25, pady=35)


    def login(self):
        u=self.username.get()
        p=self.password.get()
        if u==str(12345) and p==str(12345) :
            messagebox.showinfo("Success", "Successfully logined...")
            self.newWindow = Toplevel(self.root)
            self.obj = stock(self.newWindow)

        else:
            messagebox.showerror("Error", "Invalid login details!!!")
            self.username.set("")
            self.password.set("")

    def reset(self):
        self.username.set("")
        self.password.set("")


obj=login(root)

class stock:
    def __init__(self, root):
        self.root=root
        self.root.title("Stock Details")
        self.root.geometry("1510x900+0+0")

        self.name=StringVar()
        self.qnt=IntVar()
        self.price=DoubleVar()
        self.calbnt=DoubleVar()

        Label(self.root, text="Stock Details",bd=10, relief=GROOVE, font=("Times new roman", 40, "bold"), bg="yellow", fg="red").pack(side=TOP,fill=X)


        #===========================root frame=========================

        self.frame1=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        self.frame1.place(x=20, y=100, width=1000, height=550)

        scroll_x=Scrollbar(self.frame1, orient=HORIZONTAL)
        scroll_y=Scrollbar(self.frame1, orient=VERTICAL)
        self.stk_tbl=ttk.Treeview(self.frame1, columns=("pname", "qnt","price", "amt"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.stk_tbl.xview)
        scroll_y.config(command=self.stk_tbl.yview)
        #self.stk_tbl.heading("sl", text="SL")
        self.stk_tbl.heading("pname", text="Product Name")
        self.stk_tbl.heading("qnt", text="Quantity")
        self.stk_tbl.heading("price", text="Price")
        self.stk_tbl.heading("amt", text="Total Amount")

        self.stk_tbl["show"]="headings"
        #self.stk_tbl.column("sl", width=120)
        self.stk_tbl.column("pname", width=250)
        self.stk_tbl.column("qnt", width=150)
        self.stk_tbl.column("price", width=200)
        self.stk_tbl.column("amt", width=150)
        self.stk_tbl.pack(fill=BOTH, expand=2)
        self.stk_tbl.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetchdata()

        #===========================root frame Buttons=========================

        self.frame2=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        self.frame2.place(x=20, y=670, width=1470, height=100)

        addbnt=Button(self.frame2, text="Purchase", width=30, height=2, command=self.add_prod).grid(row=1, column=2, padx=30, pady=25)
        upbnt=Button(self.frame2, text="Update",width=30, height=2, command=self.Update_prod).grid( row=1,column=4, padx=40, pady=25)
        delbnt=Button(self.frame2, text="Outward sales", width=30, height=2, command=self.delete_prod).grid( row=1, column=5,padx=40, pady=25)
        empbnt=Button(self.frame2, text="Emp_Details", width=30, height=2, command=self.emp_deatails).grid( row=1, column=6,padx=40, pady=25)
        clrbnt=Button(self.frame2, text="Quit", width=30, height=2, command=self.Quit1).grid( row=1, column=7, padx=40, pady=25)

    def Quit1(self):
        self.iexit=messagebox.askyesno("Exit", "Confirm if you want to exit")
        if self.iexit > 0 :
            self.root.destroy()

        else:
            command=self.stock(root)
            return


    #===========================cursor on Table frame=========================
    def get_cursor(self, ev):
        cursor_row=self.stk_tbl.focus()
        contents=self.stk_tbl.item(cursor_row)
        row=contents["values"]
        self.name.set(row[0])
        self.qnt.set(row[1])
        self.price.set(row[2])
        self.calbnt.set(row[3])

    #===========================Add products here=========================
    def add_prod(self):
        self.name=StringVar()
        self.qnt=IntVar()
        self.price=DoubleVar()
        self.calbnt1=DoubleVar()

        #===========================Add products frame=========================

        self.frame1=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        self.frame1.place(x=1030, y=120, width=460, height=500)

        m_title=Label(self.frame1, text="Sundrey Credito", font=("Times new roman", 30, "bold"), bg="crimson", fg="white")
        m_title.grid(row=0, pady=10, padx=150, sticky="w")


        lbl_dept=Label(self.frame1,  text="Item Name", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_dept.grid(row=1, columnspan=1,pady=10,padx=20, sticky="w")

        txt_dept=Entry(self.frame1,textvariable=self.name, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_dept.grid(row=1, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_mail=Label(self.frame1,  text="Quantity", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_mail.grid(row=2, columnspan=1,pady=10,padx=20, sticky="w")

        txt_mail=Entry(self.frame1, textvariable=self.qnt, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_mail.grid(row=2, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_contact=Label(self.frame1,  text="Price", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_contact.grid(row=3, columnspan=1,pady=10,padx=20, sticky="w")

        txt_contact=Entry(self.frame1, textvariable=self.price, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_contact.grid(row=3, columnspan=2,pady=20, padx=230, sticky="w")

        self.amtbnt=Button(self.frame1,  text="Amount", font=("Times new roman", 20, "bold"), bg="cadet blue", fg="white", command=self.calcbnt1).grid(row=4, columnspan=1,pady=10,padx=20, sticky="w")

        txt_netbnt=Entry(self.frame1, textvariable=self.calbnt1, font=("Times new roman", 15, "bold"), bd=5, width=20, relief=GROOVE, window=self.amtbnt)
        txt_netbnt.grid(row=4 , columnspan=2, pady=10, padx=230, sticky="w")

                #===================================button frame2==============================================

        self.frame2=Frame(self.frame1, bd=4, relief=RIDGE, bg="crimson")
        self.frame2.place(x=-4, y=410, width=460, height=85)

        addbnt=Button(self.frame2, text="Accept", width=20, command=self.add_item).grid(row=1, column=0, padx=40, pady=20)
        clearbnt=Button(self.frame2, text="Quit", width=20, command=self.Quit).grid(row=1, column=4, padx=40, pady=20)


    #===========================Add products functions=========================
    def calcbnt1(self):
        u=self.qnt.get()
        v=self.price.get()
        self.calbnt1.set(u*v)

    def Quit(self):
        self.iexit=messagebox.askyesno("Exit", "Confirm if you want to exit")
        if self.iexit > 0 :
            self.frame1.destroy()
        else:
            command=self.add_prod
            return


    def add_item(self):
        if self.name.get()=="" :
            messagebox.showerror("Error", "All fileds are required!!!")
        else:
            conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
            cur=conn.cursor()
            cur.execute("insert into prod values(%s,%s,%s,%s)", (self.name.get(),
                                                                self.qnt.get(),
                                                                self.price.get(),
                                                                self.calbnt1.get()))

            conn.commit()
            self.fetchdata()
                #self.clear()
            conn.close()
            messagebox.showinfo("Success", "Recorded successfully...")

    def fetchdata(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("select * from prod")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.stk_tbl.delete(*self.stk_tbl.get_children())
            for row in rows:
                self.stk_tbl.insert("", END, values=row)
            conn.commit()
        conn.close()

    def get_cursor(self, ev):
        cursor_row=self.stk_tbl.focus()
        contents=self.stk_tbl.item(cursor_row)
        row=contents["values"]
        self.name.set(row[0])
        self.qnt.set(row[1])
        self.price.set(row[2])
        self.calbnt.set(row[3])


    #===========================Upadate products here=========================

    def Update_prod(self):
        self.name=StringVar()
        self.price=IntVar()
        self.calbnt2=DoubleVar()
        self.a=IntVar()


        #===========================update products frame =========================

        self.frame1=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        self.frame1.place(x=1030, y=120, width=460, height=500)

        m_title=Label(self.frame1, text="Product", font=("Times new roman", 30, "bold"), bg="crimson", fg="white")
        m_title.grid(row=0, pady=10, padx=150, sticky="w")


        lbl_dept=Label(self.frame1,  text="Product Name", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_dept.grid(row=1, columnspan=1,pady=10,padx=20, sticky="w")

        txt_dept=Entry(self.frame1,textvariable=self.name, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_dept.grid(row=1, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_mail=Label(self.frame1,  text="Quantity", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_mail.grid(row=2, columnspan=1,pady=10,padx=20, sticky="w")

        txt_mail=Entry(self.frame1, textvariable=self.a, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_mail.grid(row=2, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_contact=Label(self.frame1,  text="Price", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_contact.grid(row=3, columnspan=1,pady=10,padx=20, sticky="w")

        txt_contact=Entry(self.frame1, textvariable=self.price, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_contact.grid(row=3, columnspan=2,pady=20, padx=230, sticky="w")

        self.amtbnt=Button(self.frame1,  text="Amount", font=("Times new roman", 20, "bold"), bg="cadet blue", fg="white", command=self.calcbnt).grid(row=4, columnspan=1,pady=10,padx=20, sticky="w")

        txt_netbnt=Entry(self.frame1, textvariable=self.calbnt2, font=("Times new roman", 15, "bold"), bd=5, width=20, relief=GROOVE, window=self.amtbnt)
        txt_netbnt.grid(row=4 , columnspan=2, pady=10, padx=230, sticky="w")

        #===================================update products button frame==============================================

        self.frame2=Frame(self.frame1, bd=4, relief=RIDGE, bg="crimson")
        self.frame2.place(x=-4, y=410, width=460, height=85)

        addbnt=Button(self.frame2, text="Update Item", width=20, command=self.Update_item).grid(row=1, column=0, padx=40, pady=20)
        clearbnt=Button(self.frame2, text="Quit", width=20, command=self.Quit).grid(row=1, column=4, padx=40, pady=20)


    #===========================update products function=========================
    def calcbnt(self):
        u=self.a.get()+self.qnt.get()
        v=self.price.get()
        self.calbnt2.set(u*v)


    def Update_item(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("update prod set  Quantity=%s, Price=%s, Amount=%s where Product_Name=%s", (
                                                                  self.a.get()+self.qnt.get(),
                                                                  self.price.get(),
                                                                  self.calbnt2.get(),
                                                                  self.name.get()))
        conn.commit()
        self.fetchdata()
        #self.clear()
        conn.close()


    #===========================remove products here=========================
    def delete_prod(self):
        self.name=StringVar()
        self.price=IntVar()
        self.calbnt3=DoubleVar()
        self.a=IntVar()


        #===========================delete products frame =========================

        self.frame1=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        self.frame1.place(x=1030, y=120, width=460, height=500)

        m_title=Label(self.frame1, text="Product", font=("Times new roman", 30, "bold"), bg="crimson", fg="white")
        m_title.grid(row=0, pady=10, padx=150, sticky="w")


        lbl_dept=Label(self.frame1,  text="Product Name", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_dept.grid(row=1, columnspan=1,pady=10,padx=20, sticky="w")

        txt_dept=Entry(self.frame1,textvariable=self.name, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_dept.grid(row=1, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_mail=Label(self.frame1,  text="Quantity", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_mail.grid(row=2, columnspan=1,pady=10,padx=20, sticky="w")

        txt_mail=Entry(self.frame1, textvariable=self.a, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_mail.grid(row=2, columnspan=2,pady=20,padx=230, sticky="w")

        lbl_contact=Label(self.frame1,  text="Price", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_contact.grid(row=3, columnspan=1,pady=10,padx=20, sticky="w")

        txt_contact=Entry(self.frame1, textvariable=self.price, font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_contact.grid(row=3, columnspan=2,pady=20, padx=230, sticky="w")

        self.amtbnt=Button(self.frame1,  text="Amount", font=("Times new roman", 20, "bold"), bg="cadet blue", fg="white", command=self.calcbnt2).grid(row=4, columnspan=1,pady=10,padx=20, sticky="w")

        txt_netbnt=Entry(self.frame1, textvariable=self.calbnt3, font=("Times new roman", 15, "bold"), bd=5, width=20, relief=GROOVE, window=self.amtbnt)
        txt_netbnt.grid(row=4 , columnspan=2, pady=10, padx=230, sticky="w")

        #===================================delete products button frame==============================================

        self.frame2=Frame(self.frame1, bd=4, relief=RIDGE, bg="crimson")
        self.frame2.place(x=-4, y=410, width=460, height=85)

        addbnt=Button(self.frame2, text="Sell Item", width=20, command=self.dle_Update_item).grid(row=1, column=0, padx=40, pady=20)
        clearbnt=Button(self.frame2, text="Quit", width=20, command=self.Quit).grid(row=1, column=4, padx=40, pady=20)


    #===========================remove products function=========================
    def calcbnt2(self):
        if (self.a.get() > self.qnt.get()):
            messagebox.showerror("Error", "Check product Quantity its moving out of stock")
        else:
            u=self.qnt.get()-self.a.get()
            v=self.price.get()
            self.calbnt3.set(u*v)

    def dle_Update_item(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("update prod set  Quantity=%s, Price=%s, Amount=%s where Product_Name=%s", (
                                                                          self.qnt.get()-self.a.get(),
                                                                          self.price.get(),
                                                                          self.calbnt3.get(),
                                                                          self.name.get()))
        conn.commit()
        self.fetchdata()
        #self.clear()
        conn.close()


    def emp_deatails(self):
        self.newWindow1 = Toplevel(self.root)
        self.obj = emp(self.newWindow1)

class emp:
    def __init__(self, root):
        self.root=root
        self.root.title("Employee Details")
        self.root.geometry("1510x900+0+0")

        Label(self.root, text="Employee Details",bd=10, relief=GROOVE, font=("Times new roman", 40, "bold"), bg="yellow", fg="red").pack(side=TOP,fill=X)

        self.emp_id_var = StringVar()
        self.emp_name_var=StringVar()
        self.emp_dept_var=StringVar()
        self.emp_mail_var=StringVar()
        self.emp_contact_var=StringVar()
        self.emp_gen_var=StringVar()

        self.search_by=StringVar()
        self.search_txt=StringVar()


                #------------------block1------------------------------
        frame1=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        frame1.place(x=20, y=100, width=450, height=650)

        m_title=Label(frame1, text="Employee", font=("Times new roman", 30, "bold"), bg="crimson", fg="white")
        m_title.grid(row=0, pady=10, padx=110, sticky="w")

        lbl_id=Label(frame1,  text="Emp ID", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_id.grid(row=1, columnspan=1,pady=10,padx=20, sticky="w")

        txt_id=Entry(frame1,textvariable=self.emp_id_var,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_id.grid(row=1, columnspan=2,pady=20,padx=200, sticky="w")

        lbl_name=Label(frame1,  text="Emp Name", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_name.grid(row=2, columnspan=1,pady=10,padx=20, sticky="w")

        txt_name=Entry(frame1,textvariable=self.emp_name_var,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_name.grid(row=2, columnspan=2,pady=20,padx=200, sticky="w")

        lbl_dept=Label(frame1,  text="Department", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_dept.grid(row=3, columnspan=1,pady=10,padx=20, sticky="w")

        txt_dept=Entry(frame1,textvariable=self.emp_dept_var,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_dept.grid(row=3, columnspan=2,pady=20,padx=200, sticky="w")

        lbl_mail=Label(frame1,  text="Mail ID", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_mail.grid(row=4, columnspan=1,pady=10,padx=20, sticky="w")

        txt_mail=Entry(frame1,textvariable=self.emp_mail_var,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_mail.grid(row=4, columnspan=2,pady=20,padx=200, sticky="w")

        lbl_contact=Label(frame1,  text="Contact No", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_contact.grid(row=5, columnspan=1,pady=10,padx=20, sticky="w")

        txt_contact=Entry(frame1,textvariable=self.emp_contact_var,font=("Times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_contact.grid(row=5, columnspan=2,pady=20,padx=200, sticky="w")

        lbl_gen=Label(frame1,  text="Gender", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_gen.grid(row=6, columnspan=1,pady=10,padx=20, sticky="w")

        gen=ttk.Combobox(frame1,textvariable=self.emp_gen_var, font=("Times new roman", 15, "bold"), state="readonly")
        gen['values']=("Male", "female", "other")
        gen.grid(row=6, column=0, padx=190, pady=10)

                #------------------block2------------------------------

        frame2=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        frame2.place(x=20, y=650, width=450, height=100)

        addbnt=Button(frame2, text="Add", width=10, command=self.add_data).grid(row=1, column=0, padx=25, pady=35)
        upbnt=Button(frame2, text="Update", width=10, command=self.Update_data).grid(row=1, column=1, padx=10, pady=35)
        delbnt=Button(frame2, text="Detele", width=10, command=self.delete_data).grid(row=1, column=2, padx=10, pady=35)
        clrbnt=Button(frame2, text="Clear", width=10, command=self.clear).grid(row=1, column=3, padx=10, pady=35)


                #------------------block3------------------------------
        frame3=Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        frame3.place(x=500, y=100, width=800, height=650)

        lbl_search=Label(frame3,  text="Search By", font=("Times new roman", 20, "bold"), bg="crimson", fg="white")
        lbl_search.grid(row=0, columnspan=1,pady=10,padx=20, sticky="w")

        search=ttk.Combobox(frame3,textvariable=self.search_by, font=("Times new roman", 15, "bold"), width=15, state="readonly")
        search['values']=("emp_id", "emp_Name", "emp_Contact")
        search.grid(row=0, column=2, padx=20, pady=10)

        txt_search=Entry(frame3, textvariable=self.search_txt, font=("Times new roman", 15, "bold"), width=15)
        txt_search.grid(row=0, column=3, padx=10, pady=10)

        searchbnt=Button(frame3, text="Search", width=10, command=self.search_data).grid(row=0, column=4, padx=25, pady=35)
        showallbnt=Button(frame3, text="Show all", width=10, command=self.fetchdata).grid(row=0, column=5, padx=10, pady=35)

                #--------------------Table frame-------------------------

        frame3=Frame(frame3, bd=4, relief=RIDGE, bg="crimson")
        frame3.place(x=15, y=70, width=760, height=550)

        scroll_x=Scrollbar(frame3, orient=HORIZONTAL)
        scroll_y=Scrollbar(frame3, orient=VERTICAL)
        self.emp_tbl=ttk.Treeview(frame3, columns=("emp_id", "name", "dept", "mail", "contact", "gender"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.emp_tbl.xview)
        scroll_y.config(command=self.emp_tbl.yview)
        self.emp_tbl.heading("emp_id", text="Emp ID")
        self.emp_tbl.heading("name", text="Emp Name")
        self.emp_tbl.heading("dept", text="Department")
        self.emp_tbl.heading("mail", text="Mail ID")
        self.emp_tbl.heading("contact", text="Contact No.")
        self.emp_tbl.heading("gender", text="Gender")
        self.emp_tbl["show"]="headings"
        self.emp_tbl.column("emp_id", width=120)
        self.emp_tbl.column("name")
        self.emp_tbl.column("dept")
        self.emp_tbl.column("mail")
        self.emp_tbl.column("contact")
        self.emp_tbl.column("gender")
        self.emp_tbl.pack(fill=BOTH, expand=2)
        self.emp_tbl.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetchdata()


    def add_data(self):
        if self.emp_id_var.get()=="" or self.emp_name_var.get()=="":
            messagebox.showerror("Error", "All fileds are required!!!")
        else:
            conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
            cur=conn.cursor()
            cur.execute("insert into emp values(%s,%s,%s,%s,%s,%s)", (self.emp_id_var.get(),
                                                                          self.emp_name_var.get(),
                                                                          self.emp_dept_var.get(),
                                                                          self.emp_mail_var.get(),
                                                                          self.emp_contact_var.get(),
                                                                          self.emp_gen_var.get()))
            conn.commit()
            self.fetchdata()
            self.clear()
            conn.close()
            messagebox.showinfo("Success", "Recorded successfully...")

    def fetchdata(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("select * from emp")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.emp_tbl.delete(*self.emp_tbl.get_children())
            for row in rows:
                self.emp_tbl.insert("", END, values=row)
            conn.commit()
        conn.close()

    def clear(self):
        self.emp_id_var.set("")
        self.emp_name_var.set("")
        self.emp_dept_var.set("")
        self.emp_mail_var.set("")
        self.emp_contact_var.set("")
        self.emp_gen_var.set("")

    def get_cursor(self, ev):
        cursor_row=self.emp_tbl.focus()
        contents=self.emp_tbl.item(cursor_row)
        row=contents["values"]
        self.emp_id_var.set(row[0])
        self.emp_name_var.set(row[1])
        self.emp_dept_var.set(row[2])
        self.emp_mail_var.set(row[3])
        self.emp_contact_var.set(row[4])
        self.emp_gen_var.set(row[5])

    def Update_data(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("update emp set  emp_name=%s, emp_dept=%s, emp_mail=%s, emp_contact=%s, emp_gender=%s where emp_id=%s", (
                                                                          self.emp_name_var.get(),
                                                                          self.emp_dept_var.get(),
                                                                          self.emp_mail_var.get(),
                                                                          self.emp_contact_var.get(),
                                                                          self.emp_gen_var.get(),
                                                                          self.emp_id_var.get()))
        conn.commit()
        elf.fetchdata()
        self.clear()
        conn.close()

    def delete_data(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()
        cur.execute("delete from emp where emp_id=%s", self.emp_id_var.get())
        conn.commit()
        conn.close()
        self.fetchdata()
        self.clear()

    def search_data(self):
        conn=pymysql.connect(host="localhost", user="root", password="", port=7000, database="pammu")
        cur=conn.cursor()

        cur.execute("select * from emp where"+str(self.search_by.get())+"IDLIKE '%2%''"+str(self.search_txt.get())+"'%2%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.emp_tbl.delete(*self.emp_tbl.get_children())
            for row in rows:
                self.emp_tbl.insert("", END, values=row)
            conn.commit()
        conn.close()




root.mainloop()
