import tkinter as tk
from tkinter import *
import psycopg2


# functions for user authentication
def createUser(username, email, password, contact, birthDate):
    global myConnection, myCursor, issueTable, bookTable, userTable

    print(username)
    print(email)
    print(password)
    print(contact)
    print(birthDate)

    status = 'user'
    userList = []
    query1 = "select * from "+userTable+" where email = "+email+" and password = "+password+";"
    try:
        myCursor.execute(query1)
        myConnection.commit()
        print(myCursor)
        for i in myCursor:
            userList.append(i[0])
        print(userList)
        if email in userList:
            userList.clear()
            messageWindow("Error : User already exists. Login instead.")
            return
    except:
        userList.clear()
        messageWindow("Error : Couldn't connect to database")
        return

    query2 = "insert into "+userTable+" values('"+username+"','"+email+"','"+password+"','"+contact+"','"+birthDate+"','"+status+"');"
    try:
        myCursor.execute(query2)
        myConnection.commit()
        messageWindow("Success : user created successfully!!!")
        print("User created successfully!!!")
    except:
        messageWindow("Error : Couldn't connect to database")


def signUp():
    global myConnection, myCursor, issueTable, bookTable, userTable
    signWin = tk.Toplevel()
    signWin.title("Library Management System")
    signWin.geometry("770x500")

    # Define background image
    bg = PhotoImage(file="login_background.png")

    # Create a Canvas
    signCanvas = Canvas(signWin)
    signCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Set the image in output window
    signCanvas.create_image(0, 0, image=bg, anchor="nw")

    signCanvas.create_text(400, 40, text="Personal Details", font=("Helvetica", 20, "bold"), fill="black")
    # Book ID to Delete
    signCanvas.create_text(200, 120, text="Username", font=("Helvetica", 12), fill="black")
    Entry1 = Entry(signWin, font=("Helvetica", 12), width=30)
    signCanvas.create_window(290, 105, anchor="nw", window=Entry1)

    signCanvas.create_text(200, 160, text="Email ID", font=("Helvetica", 12), fill="black")
    Entry2 = Entry(signWin, font=("Helvetica", 12), width=30)
    signCanvas.create_window(290, 145, anchor="nw", window=Entry2)

    signCanvas.create_text(200, 200, text="Password", font=("Helvetica", 12), fill="black")
    Entry3 = Entry(signWin, font=("Helvetica", 12), width=30)
    signCanvas.create_window(290, 185, anchor="nw", window=Entry3)

    signCanvas.create_text(200, 240, text="Contact No.", font=("Helvetica", 12), fill="black")
    Entry4 = Entry(signWin, font=("Helvetica", 12), width=30)
    signCanvas.create_window(290, 225, anchor="nw", window=Entry4)

    signCanvas.create_text(180, 280, text="Date of birth (YYYY-MM-DD)", font=("Helvetica", 12), fill="black")
    Entry5 = Entry(signWin, font=("Helvetica", 12), width=30)  # speed
    signCanvas.create_window(290, 265, anchor="nw", window=Entry5)

    # button to submit info
    Create_btn = Button(signWin, text="Create Account", bg='black', fg='cyan', height=1, width=25,
                        command=lambda: createUser(Entry1.get(), Entry2.get(), Entry3.get(), Entry4.get(), Entry5.get()))
    signCanvas.create_window(300, 350, anchor="nw", window=Create_btn)

    back_Btn = Button(signWin, text="Back", bg='black', fg='cyan', height=1, width=5, font=("Helvetica", 6),
                      command=lambda: signWin.destroy())
    signCanvas.create_window(10, 7, anchor="nw", window=back_Btn)
    signCanvas.create_text(380, 450, text="Project Developed by Anthony D'souza", font=("Helvetica", 8), fill="black")

    signWin.mainloop()


def authenticate(email, password):
    global myConnection, myCursor, issueTable, bookTable, userTable

    userList = []
    passwordList = []
    query1 = "select * from "+userTable+" where email = "+email
    try:
        myCursor.execute(query1)
        myConnection.commit()
        for i in myCursor:
            userList.append(i[0])
            passwordList.append(i[1])

        if email in userList:
            if password in passwordList:
                query2 = "select status from "+userTable+" where email = "+email+" and password = "+password
                print(f"query2 = {query2}")
                myCursor.execute(query2)
                print("dick...")
                myConnection.commit()
                print("dick...")

            for i in myCursor:
                check = i[0]
            print(check)
            if check == 'admin':
                optionsPage(True)
            elif check == 'user':
                optionsPage(False)
        else:
            messageWindow("Error : Invalid username or password")
    except:
        messageWindow("Error : Can't connect to Database")


def optionsPage(flag):
    global background

    optWindow = Tk()
    optWindow.title('Library Management System')
    optWindow.geometry("400x500")

    # Define background image
    background = PhotoImage(file="Library1.png")

    # Create a Canvas
    optCanvas = Canvas(optWindow)
    optCanvas.pack(side=LEFT, fill=BOTH, expand=1)
    optCanvas.create_image(0, 0, image=background, anchor="nw")

    optCanvas.create_text(200, 50, text="Welcome to Central Library", font=("Helvetica", 20, "bold"),
                          fill="black")

    if flag is True:
        button1 = Button(optCanvas, text="Add Book Details", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: insert())
        optCanvas.create_window(90, 120, anchor="nw", window=button1)

        button2 = Button(optCanvas, text="View Book List", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: view())
        optCanvas.create_window(90, 200, anchor="nw", window=button2)

        button3 = Button(optCanvas, text="Issue Book to Student", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: issue())
        optCanvas.create_window(90, 280, anchor="nw", window=button3)

        button4 = Button(optCanvas, text="Return Book", bg='black', fg='cyan', height=1, width=25,
                         command=lambda: returnBook())
        optCanvas.create_window(90, 360, anchor="nw", window=button4)

        button5 = Button(optCanvas, text="Delete Book", bg='black', fg='cyan', height=1, width=25,
                         command=lambda: delete())
        optCanvas.create_window(90, 420, anchor="nw", window=button5)

        optCanvas.create_text(200, 485, text="Project Developed by Anthony D'souza", font=("Helvetica", 10),
                              fill="white")
        optWindow.mainloop()

    elif flag is False:
        button1 = Button(optCanvas, text="View Book List", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: view())
        optCanvas.create_window(90, 150, anchor="nw", window=button1)

        button2 = Button(optCanvas, text="Issue Book to Student", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: issue())
        optCanvas.create_window(90, 230, anchor="nw", window=button2)

        button3 = Button(optCanvas, text="Return Book", bg='black', fg='cyan', height=2, width=30,
                         command=lambda: returnBook())
        optCanvas.create_window(90, 310, anchor="nw", window=button3)
        optWindow.mainloop()


# Start of success/error window
def messageWindow(message):
    global background
    popup = tk.Toplevel()
    popup.geometry("400x150")
    popup.title("Error/Success Window")

    # Create a Canvas
    myCanvas = Canvas(popup)
    myCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    myCanvas.create_image(0, 0, image=background, anchor="nw")

    myCanvas.create_text(250, 50, text=f'{message}', font=("Helvetica", 15), fill="white")

    closeButton = Button(popup, text='Exit', width=10, height=1, bg='black', fg='cyan', command=lambda: popup.destroy())
    myCanvas.create_window(270, 100, anchor="nw", window=closeButton)
    popup.mainloop()


# GUI Window to Add Books to the Library -> Starts Here
def Register(bookId, title, author, status):
    global myConnection, myCursor, bookTable

    allBid = []
    status = status.lower()

    # printing values entered by user(for verification)
    print(bookId)
    print(title)
    print(author)
    print(status)

    query1 = "select title from "+bookTable+" where bid = "+bookId+";"
    try:
        myCursor.execute(query1)
        myConnection.commit()
        for i in myCursor:
            allBid.append(i[0])
        print(allBid)
        if title in allBid:
            messageWindow("Error : Book already exists in library")
            return
    except:
        messageWindow("Error : Can't connect to Database")
        return

    query2 = "insert into "+bookTable+" values('"+bookId+"','"+title+"','"+author+"','"+status+"')"
    print(query2)
    try:
        myCursor.execute(query2)
        myConnection.commit()
        # messagebox.showinfo('Success', "Book added successfully")
        messageWindow('Success : New Book Added Successfully')
    except:
        # messagebox.showinfo("Error", "Can't add data into Database")
        messageWindow("Error : Addition of a New Book was Unsuccessful")


def insert():
    global background
    # Initializing the GUI Window
    insert_Book_Window = tk.Toplevel()
    insert_Book_Window.title("Library Management System")
    insert_Book_Window.geometry("400x450")

    # Create a Canvas
    insert_Canvas = Canvas(insert_Book_Window)
    insert_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # set image as background in GUI
    insert_Canvas.create_image(0, 0, image=background, anchor="nw")

    insert_Canvas.create_text(200, 40, text="Add Books", font=("Helvetica", 20, "bold"), fill="white")

    # Input Box for Book ID
    insert_Canvas.create_text(120, 100, text="Book ID (BID)", font=("Helvetica", 15), fill="white")
    Info1 = Entry(insert_Book_Window, font=("Helvetica", 10), width=20)
    insert_Canvas.create_window(220, 90, anchor="nw", window=Info1)
    # Input Box for Title
    insert_Canvas.create_text(120, 140, text="Book Title", font=("Helvetica", 15), fill="white")
    Info2 = Entry(insert_Book_Window, font=("Helvetica", 10), width=20)
    insert_Canvas.create_window(220, 130, anchor="nw", window=Info2)
    # Input Box for Book Author
    insert_Canvas.create_text(120, 180, text="Author of Book", font=("Helvetica", 15), fill="white")
    Info3 = Entry(insert_Book_Window, font=("Helvetica", 10), width=20)
    insert_Canvas.create_window(220, 170, anchor="nw", window=Info3)
    # Input Box for Book Status
    insert_Canvas.create_text(120, 220, text="Status(Avail/issued)", font=("Helvetica", 15), fill="white")
    Info4 = Entry(insert_Book_Window, font=("Helvetica", 10), width=20)
    insert_Canvas.create_window(220, 210, anchor="nw", window=Info4)
    # Input Box for Date Book was Added
    insert_Canvas.create_text(120, 260, text="Date of Addition", font=("Helvetica", 15), fill="white")
    Info4 = Entry(insert_Book_Window, font=("Helvetica", 10), width=20)
    insert_Canvas.create_window(220, 250, anchor="nw", window=Info4)

    # Checking if all entries are of the expected data type

    # Buttons
    addButton = Button(insert_Book_Window, text="Insert", bg='black', fg='cyan', height=1, width=10,
                       command=lambda: Register(Info1.get(), Info2.get(), Info3.get(), Info4.get()))
    insert_Canvas.create_window(80, 320, anchor="nw", window=addButton)
    quitButton = Button(insert_Book_Window, text="Quit", bg='black', fg='cyan', height=1, width=10,
                        command=lambda: insert_Book_Window.destroy())
    insert_Canvas.create_window(220, 319, anchor="nw", window=quitButton)

    insert_Book_Window.mainloop()


# GUI Window to View All Books in the Library -> Starts Here
def view():
    global myConnection, myCursor, issueTable, bookTable, userTable

    view_Window = Tk()
    view_Window.title("Library")
    view_Window.geometry("600x500")

    viewCanvas = Canvas(view_Window)
    viewCanvas.config(bg="#12a4d9")
    viewCanvas.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(view_Window, bg="#FFBB00", bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Books", bg='black', fg='white', font=('Courier', 15))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(view_Window, bg='black')
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    y = 0.25

    Label(labelFrame, text="%-10s%-40s%-30s%-20s" % ('BID', 'Title', 'Author', 'Status'), bg='black', fg='white').place(
        relx=0.07, rely=0.1)
    Label(labelFrame, text="----------------------------------------------------------------------------", bg='black',
          fg='white').place(relx=0.05, rely=0.2)
    # Enter Table Names here
    bookTable = "books"

    getBooks = "select * from " + bookTable
    try:
        myCursor.execute(getBooks)
        print(getBooks)
        print(myCursor)
        myConnection.commit()
        print(myConnection)
        for i in myCursor:
            Label(labelFrame, text="%-10s%-30s%-30s%-20s" % (i[0], i[1], i[2], i[3]), bg='black', fg='white').place(
                relx=0.07, rely=y)
            y += 0.1
    except:
        messageWindow("Error : Failed to fetch files from database")
        # messagebox.showinfo("Failed to fetch files from database")

    view_Window.mainloop()


# GUI Window to Issue Books to Student -> Starts Here
def issueBook(bookID, userID, period, date):
    global myConnection, myCursor, bookTable, issueTable

    allBid = []
    flag = None
    query1 = "select bid from " + bookTable
    print(f"query1 = {query1}")

    try:
        myCursor.execute(query1)
        print("Hi!!!")
        myConnection.commit()
        print(myCursor)
        for i in myCursor:
            allBid.append(i[0])
        print(allBid)
        print(bookID)
        if bookID in allBid:
            query2 = "select status from " + bookTable + " where bid = '" + bookID + "'"
            print(f"query2 = {query2}")
            myCursor.execute(query2)
            print("dick...")
            myConnection.commit()
            print("dick...")

            for i in myCursor:
                check = i[0]
            print(check)
            if check == 'avail':
                flag = True
            else:
                flag = False

        else:
            allBid.clear()
            messageWindow("Error : Book not present in Library")
            # messagebox.showinfo("Error", "Book ID not present")
            return
    except:
        allBid.clear()
        messageWindow("Error : Can't fetch Book IDs")
        # messagebox.showinfo("Error", "Can't fetch Book IDs")
        return
    query3 = "insert into "+issueTable+" values('"+bookID+"','"+userID+"','"+period+"','"+date+"')"
    print(f"query3 = {query3}")
    # show = "select * from "+issueTable

    query5 = "update " + bookTable + " set status = 'issued' where bid = '" + bookID + "'"
    print(f"query5 = {query5}")
    try:
        if bookID in allBid and flag is True:
            print("Fuck you1...")
            myCursor.execute(query3)
            print("Fuck you2...")
            myConnection.commit()
            print("Fuck you3...")
            myCursor.execute(query5)
            print("Fuck you4...")
            myConnection.commit()
            print("Fuck you5...")
            messageWindow("Success : Book Issued Successfully")
            print("Success : Book Issued Successfully")
            # messagebox.showinfo('Success', "Book Issued Successfully")
        else:
            messageWindow("Error : Book Already Issued")
            print("Error : Book Already Issued")
            # messagebox.showinfo('Message', "Book Already Issued")
            return
    except:
        messageWindow("Error : value entered is Invalid")
        print("Error : value entered is Invalid")
        # messagebox.showinfo("Search Error", "The value entered is wrong, Try again")
        return

    print(bookID)
    print(userID)
    print(period)
    print(date)

    allBid.clear()


def issue():
    # global issueInfo1, issueInfo2, issueInfo3, issueInfo3
    global background
    # Initializing the GUI Window
    bookIssue_Window = tk.Toplevel()
    bookIssue_Window.title("Library Management System")
    bookIssue_Window.geometry("403x400")

    # Define background image
    background = PhotoImage(file="Library1.png")

    # Create a Canvas
    bookIssue_Canvas = Canvas(bookIssue_Window)
    bookIssue_Canvas.pack(side=LEFT, fill=BOTH, expand=1)
    bookIssue_Canvas.create_image(0, 0, image=background, anchor="nw")

    bookIssue_Canvas.create_text(220, 30, text="Book Issue Details", font=("Helvetica", 20, "bold"), fill="white")

    # Input Boxes for the GUI Design
    bookIssue_Canvas.create_text(150, 100, text="Book ID (BID)", font=("Helvetica", 15), fill="white")
    Info1 = Entry(bookIssue_Window, font=("Helvetica", 10), width=12)
    bookIssue_Canvas.create_window(250, 90, anchor="nw", window=Info1)
    bookIssue_Canvas.create_text(150, 150, text="User ID (UID)", font=("Helvetica", 15), fill="white")
    Info2 = Entry(bookIssue_Window, font=("Helvetica", 10), width=12)  # speed
    bookIssue_Canvas.create_window(250, 140, anchor="nw", window=Info2)
    bookIssue_Canvas.create_text(150, 200, text="Period (Days)", font=("Helvetica", 15), fill="white")
    Info3 = Entry(bookIssue_Window, font=("Helvetica", 10), width=12)  # speed
    bookIssue_Canvas.create_window(250, 190, anchor="nw", window=Info3)
    bookIssue_Canvas.create_text(125, 250, text="Issued Date (YYYY-MM-DD)", font=("Helvetica", 15), fill="white")
    Info4 = Entry(bookIssue_Window, font=("Helvetica", 10), width=12)  # speed
    bookIssue_Canvas.create_window(250, 240, anchor="nw", window=Info4)

    # Submit button to end the input
    submitButton = Button(bookIssue_Window, text="Issue", bg='black', fg='cyan', height=1, width=6,
                          command=lambda: issueBook(Info1.get(), Info2.get(), Info3.get(), Info4.get()))
    bookIssue_Canvas.create_window(120, 320, anchor="nw", window=submitButton)
    quitButton = Button(bookIssue_Window, text="Exit", bg='black', fg='cyan', height=1, width=6,
                        command=lambda: bookIssue_Window.destroy())
    bookIssue_Canvas.create_window(230, 320, anchor="nw", window=quitButton)

    bookIssue_Window.mainloop()


# GUI Window to Return Books to Library-> Start Here
def updateReturn(bookID):
    global myConnection, myCursor, bookTable, issueTable

    allBid = []
    flag = None
    query1 = "select bid from " + issueTable
    print(f"query1 = {query1}")

    try:
        myCursor.execute(query1)
        print("myCursor = \n" + myCursor)
        myConnection.commit()
        for i in myCursor:
            allBid.append(i[0])

        if bookID in allBid:
            query2 = "select status from " + bookTable + " where bid = '" + bookID + "'"
            print(f"query2 = {query2}")
            myCursor.execute(query2)
            myConnection.commit()
            for i in myCursor:
                check = i[0]

            if check == 'issued':
                flag = True
            else:
                flag = False

        else:
            messageWindow("Error : Book not present in Library")
            allBid.clear()
            return
            # messagebox.showinfo("Error", "Book ID not present")
    except:
        messageWindow("Error : Can't fetch Book IDs")
        # messagebox.showinfo("Error", "Can't fetch Book IDs")

    query3 = "delete from " + issueTable + " where bid = '" + bookID + "'"
    print(f"query3 = {query3}")

    print(bookID in allBid)
    print(flag)

    query4 = "update " + bookTable + " set status = 'avail' where bid = '" + bookID + "'"
    print(f"query4 = {query4}")
    try:
        if bookID in allBid and flag is True:
            myCursor.execute(query3)
            myConnection.commit()
            myCursor.execute(query4)
            myConnection.commit()
            messageWindow("Success : Book Returned Successfully")
            # messagebox.showinfo('Success', "Book Returned Successfully")
        else:
            messageWindow("Error : Please check the book ID")
            # messagebox.showinfo('Message', "Please check the book ID")
    except:
        messageWindow("Error : The value entered is wrong")
        # messagebox.showinfo("Search Error", "The value entered is wrong, Try again")

    allBid.clear()


def returnBook():
    global background
    return_Window = tk.Toplevel()
    return_Window.title("Library Management System")
    return_Window.geometry("400x250")

    # Define background image
    background = PhotoImage(file="Library1.png")

    returnCanvas = Canvas(return_Window)
    returnCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    returnCanvas.create_image(0, 0, image=background, anchor="nw")

    returnCanvas.create_text(200, 40, text="Book Return Details", font=("Helvetica", 20, "bold"), fill="white")

    # Book ID to Delete
    returnCanvas.create_text(120, 100, text="Book ID (BID)", font=("Helvetica", 12), fill="white")
    Info1 = Entry(return_Window, font=("Helvetica", 12), width=18)
    returnCanvas.create_window(200, 90, anchor="nw", window=Info1)

    # Submit Button & Quit Button
    submitButton = Button(return_Window, text="Return", bg='black', fg='cyan',
                          command=lambda: updateReturn(Info1.get()))
    returnCanvas.create_window(130, 150, anchor="nw", window=submitButton)
    quitButton = Button(return_Window, text="Quit", bg='black', fg='cyan', command=return_Window.destroy)
    returnCanvas.create_window(230, 150, anchor="nw", window=quitButton)

    return_Window.mainloop()


# GUI Window to Delete Books -> Starts Here
def removeBook(bookID):
    global myConnection, myCursor, bookTable, issueTable

    availability = None
    allBid = []
    query1 = "select status from " + bookTable + " where Bid = '" + bookID + "'"
    query2 = "select bid from" + bookTable

    try:
        myCursor.execute(query2)
        myConnection.commit()
        for i in myCursor:
            allBid.append(i[0])

        if bookID in allBid:
            myCursor.execute(query1)
            myConnection.commit()
            for i in myCursor:
                availability = i[0]

        else:
            allBid.clear()
            messageWindow("Error : Book not present in library")
            return
    except:
        allBid.clear()
        messageWindow("Error : Can't Fetch Book ID")
        return

    query3 = "delete from " + bookTable + " where Bid = '" + bookID + "'"
    query4 = "delete from " + issueTable + " where Bid = '" + bookID + "'"

    try:
        if bookID in allBid and availability == 'avail':
            myCursor.execute(query3)
            myConnection.commit()
            myCursor.execute(query4)
            myConnection.commit()
        else:
            messageWindow("Error : Can't delete the Book as it is currently issused")

        messageWindow("Success : Book Record Deleted Successfully")
        # messagebox.showinfo('Success', "Book Record Deleted Successfully")
    except:
        messageWindow("Error : Incorrect Book ID entered")
        # messagebox.showinfo("Please check Book ID")

    print(bookID)


def delete():
    global background

    delete_Window = tk.Toplevel()
    delete_Window.title("Library Management System")
    delete_Window.geometry("400x200")

    # Create a Canvas
    remove_Canvas = Canvas(delete_Window)
    remove_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # Set the image in output window
    remove_Canvas.create_image(0, 0, image=background, anchor="nw")

    remove_Canvas.create_text(220, 40, text="Book Deletion Details", font=("Helvetica", 20, "bold"), fill="white")
    # Book ID to Delete
    remove_Canvas.create_text(150, 100, text="Book ID (BID)", font=("Helvetica", 12), fill="white")
    Info1 = Entry(delete_Window, font=("Helvetica", 12), width=12)
    remove_Canvas.create_window(220, 90, anchor="nw", window=Info1)

    # Submit Button
    deleteButton = Button(delete_Window, text="Delete", bg='black', fg='cyan', command=removeBook(Info1.get()))
    remove_Canvas.create_window(150, 150, anchor="nw", window=deleteButton)

    # Exit Button
    quitButton = Button(delete_Window, text="Quit", bg='black', fg='cyan', command=delete_Window.destroy)
    remove_Canvas.create_window(250, 150, anchor="nw", window=quitButton)

    delete_Window.mainloop()


# Main Program
myConnection = psycopg2.connect(host="localhost", user="postgres", password="r00t1@3$", database="library")
myCursor = myConnection.cursor()

# Enter Table Names here
issueTable = "issued"
bookTable = "books"
userTable = "users"

mainWin = Tk()
mainWin.title("Library Management System")
mainWin.geometry("770x500")

# Define background image
background = PhotoImage(file="login_background.png")

# Create a Canvas
mainCanvas = Canvas(mainWin)
mainCanvas.pack(side=LEFT, fill=BOTH, expand=1)

# Set the image in output window
mainCanvas.create_image(0, 0, image=background, anchor="nw")

mainCanvas.create_text(400, 70, text="User Credentials", font=("Helvetica", 20, "bold"), fill="black")
# Book ID to Delete
mainCanvas.create_text(180, 160, text="Email ID", font=("Helvetica", 15), fill="black")
mainEntry1 = Entry(mainWin, font=("Helvetica", 15), width=30)
mainCanvas.create_window(270, 145, anchor="nw", window=mainEntry1)

mainCanvas.create_text(180, 220, text="Password", font=("Helvetica", 15), fill="black")
mainEntry2 = Entry(mainWin, font=("Helvetica", 15), width=30)
mainCanvas.create_window(270, 205, anchor="nw", window=mainEntry2)

mainCanvas.create_text(390, 325, text="To create a new account. Click Sign UP.", font=("Helvetica", 10), fill="black")
# Sign up for new user
newUser = Button(mainWin, text="Sign Up", bg='black', fg='cyan', height=1, width=25, command=lambda: signUp())
mainCanvas.create_window(150, 345, anchor="nw", window=newUser)
# Submit Button
Enter = Button(mainWin, text="Login", bg='black', fg='cyan', height=1, width=25,
               command=lambda: authenticate(mainEntry1.get(), mainEntry2.get()))
mainCanvas.create_window(450, 345, anchor="nw", window=Enter)

mainCanvas.create_text(380, 450, text="Project Developed by Anthony D'souza", font=("Helvetica", 8), fill="black")

mainWin.mainloop()
