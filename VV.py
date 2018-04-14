from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk

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
    cursor.execute("CREATE TABLE IF NOT EXISTS `MEDICINE_STOCK` (`ID`INTEGER NOT NULL, `batch_code` INTEGER, `expiry` DATE, `quantity` INTEGER, `price` REAL, PRIMARY KEY(ID,batch_code), FOREIGN KEY(`ID`) REFERENCES MEDICINE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS `TRANSACTION` (`T_ID` INTEGER PRIMARY KEY AUTOINCREMENT, `ID` INTEGER NOT NULL, `batch_code` INTEGER NOT NULL, `quantity` INTEGER, `price` REAL NOT NULL, FOREIGN KEY(`ID`) REFERENCES MEDICINE_STOCK, FOREIGN KEY(`batch_code`) REFERENCES MEDICINE_STOCK, FOREIGN KEY(`price`) REFERENCES MEDICINE_STOCK);")
    cursor.execute("SELECT * FROM `ADMIN` WHERE `user` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `ADMIN` (user, password) VALUES('admin', 'admin')")
        conn.commit()

def Exit():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to exit?', icon="warning")
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
    Home.title("Medical Stossre")
    width = 1024
    height = 720
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="Simple Inventory System", font=('arial', 20))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="#99ff99")

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

def DisplayData():
    Database()
    command = ("SELECT MEDICINE.name, MEDICINE_STOCK.ID,"
                "MEDICINE_STOCK.batch_code, MEDICINE_STOCK.orig_quantity,"
                "MEDICINE_STOCK.quantity, MEDICINE_STOCK.price, MEDICINE_STOCK.expiry "
                "FROM MEDICINE_STOCK "
                "INNER JOIN MEDICINE ON MEDICINE.ID = MEDICINE_STOCK.ID ")
    cursor.execute(command)
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

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

def parseDate (s):
        

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

def Logout():
    result = tkMessageBox.askquestion('Simple Inventory System', 'Are you sure you want to logout?', icon="warning")
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
        cursor.execute("SELECT * FROM `admin` WHERE `user` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `user` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
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
