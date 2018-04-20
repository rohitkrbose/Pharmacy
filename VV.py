from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
from functools import partial
from Crypto.Hash import SHA256

root = Tk()
root.title("BM Pharmacy")

width = 480
height = 50
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="red")

#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_PRICE = IntVar()
PRODUCT_QTY = IntVar()
BATCH_DATE = StringVar()
EXPIRY_DATE = StringVar()
SEARCH = StringVar()
#========================================METHODS==========================================

def Database():
    global conn, cursor
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `ADMIN` (`user` TEXT,`password` TEXT,PRIMARY KEY(user));")
    cursor.execute("CREATE TABLE IF NOT EXISTS `MEDICINE` (`ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `name` INTEGER UNIQUE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS `MEDICINE_STOCK` (`ID`INTEGER NOT NULL, `batch_code` DATE NOT NULL, `expiry` DATE NOT NULL, `quantity` INTEGER NOT NULL, `price` REAL NOT NULL, PRIMARY KEY(ID,batch_code), FOREIGN KEY(`ID`) REFERENCES MEDICINE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS `TRANSACTION` (`T_ID` INTEGER NOT NULL,`t_stamp` TEXT NOT NULL, `ID` INTEGER NOT NULL, `batch_code` DATE NOT NULL,`quantity` INTEGER NOT NULL, `price` REAL NOT NULL, PRIMARY KEY(T_ID,ID,batch_code), FOREIGN KEY(`ID`) REFERENCES MEDICINE_STOCK, FOREIGN KEY(`batch_code`) REFERENCES MEDICINE_STOCK, FOREIGN KEY(`price`) REFERENCES MEDICINE_STOCK);")
    cursor.execute("SELECT * FROM `ADMIN`;")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `ADMIN` (user, password) VALUES('admin', ?)", (SHA256.new('admin'.encode('utf-8')).hexdigest(),))
        conn.commit()

def Exit():
    result = tkMessageBox.askquestion('BM Pharmacy', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Login")
    width = 300
    height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
    
def LoginForm():
    global lbl_result
    MidLoginForm = Frame(loginform, width=300)
    MidLoginForm.pack(side=TOP, pady=10)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 12), bd=1)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 12), bd=1)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 12))
    lbl_result.grid(row=3, columnspan=3)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 12), width=20)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 12), width=20, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 12), width=12, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=8)
    btn_login.bind('<Return>', Login)
    

def Home():
    global Home
    Home = Tk()
    Home.title("Pharmacy")
    width = 512
    height = 50
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="BM Pharmacy", font=('arial', 20))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu3 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New account", command=ShowNewAcc)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    filemenu3.add_command(label="Sell", command=ShowSell)
    filemenu3.add_command(label="History", command=ShowHistory)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    menubar.add_cascade(label="Transaction", menu=filemenu3)
    Home.config(menu=menubar)
    Home.config(bg="#99ff99")

def ShowNewAcc():
    global newaccform
    newaccform = Toplevel()
    newaccform.title("New Account")
    width = 300
    height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    newaccform.resizable(0, 0)
    newaccform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    NewAccForm()

def NewAccForm():
    global lbl_result
    MidLoginForm = Frame(newaccform, width=300)
    MidLoginForm.pack(side=TOP, pady=10)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 12), bd=1)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 12), bd=1)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 12))
    lbl_result.grid(row=3, columnspan=3)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 12), width=20)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 12), width=20, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Create", font=('arial', 12), width=12, command=Create)
    btn_login.grid(row=2, columnspan=2, pady=8)
    btn_login.bind('<Return>', Create)

def Create(event=None):
    global user_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        pass_hash = SHA256.new(PASSWORD.get().encode('utf-8')).hexdigest()
        cursor.execute("SELECT * FROM `admin` WHERE `user` = ? ;", (USERNAME.get(), ))
        if cursor.fetchone() is not None:
            print ('User already exists. Select different username.')
        else:
            cursor.execute("INSERT INTO `admin` (user, password) VALUES(?, ?)", (USERNAME.get(), pass_hash))
            conn.commit()
            data = cursor.fetchone()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            # ShowHome()
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Add Product")
    width = 400
    height = 200
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=400, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=8)
    lbl_text = Label(TopAddNew, text="Add Medicine to Stock", font=('arial', 12), width=400)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=400)
    MidAddNew.pack(side=TOP, pady=8)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('arial', 12), bd=1)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidAddNew, text="Product Quantity:", font=('arial', 12), bd=1)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Price:", font=('arial', 12), bd=1)
    lbl_price.grid(row=2, sticky=W)
    lbl_batch = Label(MidAddNew, text="Batch Date:", font=('arial', 12), bd=1)
    lbl_batch.grid(row=3, sticky=W)
    lbl_expiry = Label(MidAddNew, text="Expiry Date:", font=('arial', 12), bd=1)
    lbl_expiry.grid(row=4, sticky=W)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 12), width=15)
    productname.grid(row=0, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 12), width=15)
    productqty.grid(row=1, column=1)
    productprice = Entry(MidAddNew, textvariable=PRODUCT_PRICE, font=('arial', 12), width=15)
    productprice.grid(row=2, column=1)
    batchdate = Entry(MidAddNew, textvariable=BATCH_DATE, font=('arial', 12), width=15)
    batchdate.grid(row=3, column=1)
    expirydate = Entry(MidAddNew, textvariable=EXPIRY_DATE, font=('arial', 12), width=15)
    expirydate.grid(row=4, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 12), width=30, bg="#009ACD", command=AddNew)
    btn_add.grid(row=5, columnspan=2, pady=2)

def AddNew():
    Database()

    comm_insert = "INSERT INTO `MEDICINE_STOCK` (ID,batch_code,expiry,orig_quantity,quantity,price) VALUES (?,?,?,?,?,?)"
    prod_name = str(PRODUCT_NAME.get())

    # check if new product is there in database
    cursor.execute("SELECT * FROM `MEDICINE` WHERE name = ?", (prod_name,))
    if cursor.fetchone() is None:
        # if not present, add an entry
        cursor.execute("INSERT INTO MEDICINE (name) VALUES (?)",(prod_name,))
        conn.commit()

    # fetch ID
    cursor.execute("SELECT * FROM `MEDICINE` WHERE name = ?", (prod_name,))
    data = cursor.fetchone()
    id_code = data[0]

    cursor.execute(comm_insert, (id_code, str(BATCH_DATE.get()), str(EXPIRY_DATE.get()), int(PRODUCT_QTY.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get())))
    conn.commit()

    # Reset fields

    PRODUCT_NAME.set("")
    PRODUCT_PRICE.set("")
    PRODUCT_QTY.set("")
    BATCH_DATE.set("")
    EXPIRY_DATE.set("")

    cursor.close()
    conn.close()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Medicine Stock", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("name", "ID", "batch_code", "orig_quantity", "quantity", "price", "expiry"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('name', text="Med",anchor=W)
    tree.heading('ID', text="ID",anchor=W)
    tree.heading('batch_code', text="Batch",anchor=W)
    tree.heading('orig_quantity', text="Original Qty",anchor=W)
    tree.heading('quantity', text="Current Qty",anchor=W)
    tree.heading('price', text="Price",anchor=W)
    tree.heading('expiry', text="Expiry",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=20)
    tree.column('#2', stretch=NO, minwidth=0, width=120)
    tree.column('#3', stretch=NO, minwidth=0, width=120)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.column('#5', stretch=NO, minwidth=0, width=120)
    tree.column('#6', stretch=NO, minwidth=0, width=120)
    tree.column('#7', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def HistoryForm():
    global htree
    TopViewForm = Frame(historyform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(historyform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(historyform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Transaction History", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text=" ", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    htree = ttk.Treeview(MidViewForm, columns=("T_ID", "ts", "ID", "batch_code", "quantity", "price"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=htree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=htree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    htree.heading('T_ID', text="Transaction ID",anchor=W)
    htree.heading('ts', text="Timestamp",anchor=W)
    htree.heading('ID', text="Med ID",anchor=W)
    htree.heading('batch_code', text="Batch",anchor=W)
    htree.heading('quantity', text="Qty",anchor=W)
    htree.heading('price', text="Price",anchor=W)
    htree.column('#0', stretch=NO, minwidth=0, width=0)
    htree.column('#1', stretch=NO, minwidth=0, width=20)
    htree.column('#2', stretch=NO, minwidth=0, width=120)
    htree.column('#3', stretch=NO, minwidth=0, width=120)
    htree.column('#4', stretch=NO, minwidth=0, width=120)
    htree.column('#5', stretch=NO, minwidth=0, width=120)
    htree.column('#6', stretch=NO, minwidth=0, width=120)
    htree.pack()
    DisplayDataT()

def getOptVal (sb,value):
    Database ()
    command = ("SELECT SUM (MEDICINE_STOCK.quantity) "
                "FROM MEDICINE_STOCK, MEDICINE "
                "WHERE MEDICINE.name = ? AND MEDICINE.ID = MEDICINE_STOCK.id")
    cursor.execute(command, (value,))
    data = cursor.fetchone()
    optval = data[0]
    sb.config(to=int(optval))

def SellForm():

    TopViewForm = Frame(sellform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(sellform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(sellform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Medicine Stock", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)

    global N

    N = 5

    OPTIONS = getInfo()
    med_vars = []
    med_opts = []
    med_quants = []
    quant_vars = []

    for i in range(N):
        med_vars.append(StringVar())
        quant_vars.append(StringVar())
        med_quants.append(Spinbox(LeftViewForm,textvariable=quant_vars[i],to=0))
        med_opts.append(OptionMenu(LeftViewForm, med_vars[i], *OPTIONS,command = partial(getOptVal,med_quants[i]) ))
        med_opts[i].grid(row=i, column=2)
        med_quants[i].grid(row=i, column=3)

    ### Get the algorithm in python to update.

    # Step1: Find the existing quantities



    btn_submit = Button(LeftViewForm, text="Submit", command=partial(SubmitBill,med_vars,quant_vars))
    # btn_submit.pack(side=TOP, padx=50, pady=10, fill=X)
    btn_submit.grid(row=N,column=2)

def getInfo ():
    Database()
    command = ("SELECT DISTINCT MEDICINE.name " 
                    "FROM MEDICINE "
                    "INNER JOIN MEDICINE_STOCK ON MEDICINE.ID = MEDICINE_STOCK.ID "
                    "WHERE MEDICINE_STOCK.quantity > 0")
    cursor.execute(command)
    fetch = cursor.fetchall()
    dd_list = []
    for data in fetch:
        dd_list.append(data[0])
    return dd_list

def DisplayData():
    Database()
    command = ("SELECT MEDICINE.name, MEDICINE_STOCK.ID,"
                "MEDICINE_STOCK.batch_code, MEDICINE_STOCK.orig_quantity,"
                "MEDICINE_STOCK.quantity, MEDICINE_STOCK.price, MEDICINE_STOCK.expiry " "FROM MEDICINE_STOCK "
                "INNER JOIN MEDICINE ON MEDICINE.ID = MEDICINE_STOCK.ID ")
    cursor.execute(command)
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def DisplayDataT():
    Database()
    command = ("SELECT * FROM `TRANSACTION` ORDER BY T_ID DESC;")
    cursor.execute(command)
    fetch = cursor.fetchall()
    for data in fetch:
        htree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitBill (opt,quant):
    Database()

    # Get last transaction ID... it represents a bill
    cursor.execute("SELECT * FROM `TRANSACTION`")
    D = cursor.fetchall()
    tid = 1
    if (len(D) != 0):
        tid = D[-1][0] + 1

    cursor.execute("SELECT CURRENT_TIMESTAMP;")
    ts = cursor.fetchall()[0][0]
    print (ts)

    names, quantities = [], []
    for i in range (N):
        t1 = opt[i].get()
        t2 = quant[i].get()
        if t1 != '':
            names.append(t1)
            quantities.append(t2)
            command = ("SELECT MEDICINE_STOCK.ID, MEDICINE_STOCK.batch_code, MEDICINE_STOCK.quantity, MEDICINE_STOCK.expiry, MEDICINE_STOCK.price "
               "FROM MEDICINE, MEDICINE_STOCK " 
               "WHERE MEDICINE.ID = MEDICINE_STOCK.ID AND MEDICINE.name = ? "
               "ORDER BY MEDICINE_STOCK.expiry ")
            cursor.execute(command, (t1,))
            fetch = cursor.fetchall()
            rem = int(t2)
            for ent in fetch:
                q = int(ent[2]) # quantity
                if (rem >= q):
                    cursor.execute("INSERT INTO `TRANSACTION` VALUES (?,?,?,?,?,?) ;", (tid,ts,int(ent[0]),str(ent[1]),q,float(ent[4])) )
                    conn.commit()
                    rem = rem - q
                    q = 0
                else:
                    cursor.execute("INSERT INTO `TRANSACTION` VALUES (?,?,?,?,?,?) ;", (tid,ts,int(ent[0]),str(ent[1]),rem,float(ent[4])))
                    conn.commit()
                    q = q - rem
                    rem = 0
                command = ("UPDATE MEDICINE_STOCK "
                           "SET quantity = ? "
                           "WHERE MEDICINE_STOCK.ID = ? AND MEDICINE_STOCK.batch_code = ?")
                cursor.execute(command, (int(q), int(ent[0]), str(ent[1])))
                conn.commit()


def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        command = ("SELECT MEDICINE.name, MEDICINE_STOCK.ID,"
                "MEDICINE_STOCK.batch_code, MEDICINE_STOCK.orig_quantity,"
                "MEDICINE_STOCK.quantity, MEDICINE_STOCK.price, MEDICINE_STOCK.expiry "
                "FROM MEDICINE_STOCK "
                "INNER JOIN MEDICINE ON MEDICINE.ID = MEDICINE_STOCK.ID "
                "WHERE MEDICINE.name LIKE ?")
        cursor.execute(command, ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('BM Pharmacy', 'You sure?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM MEDICINE_STOCK WHERE ID = ? AND batch_code = ?" ,(selecteditem[1], selecteditem[2])) 
            conn.commit()
            cursor.close()
            conn.close()

def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("View Stock")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()


def ShowHistory():
    global historyform
    historyform = Toplevel()
    historyform.title("View Transaction History")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    historyform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    historyform.resizable(0, 0)
    HistoryForm()

def ShowSell():
    global sellform
    sellform = Toplevel()
    sellform.title("Sell Medicine")
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    sellform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    sellform.resizable(0, 0)
    SellForm()

def Logout():
    result = tkMessageBox.askquestion('BM Pharmacy', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()
  
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        pass_hash = SHA256.new(PASSWORD.get().encode('utf-8')).hexdigest()
        cursor.execute("SELECT * FROM `admin` WHERE `user` = ? AND `password` = ?", (USERNAME.get(), pass_hash))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `user` = ? AND `password` = ?", (USERNAME.get(), pass_hash))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()

#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Account", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

#========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)

#========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="BM Pharmacy", font=('arial', 20))
lbl_display.pack()

#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
