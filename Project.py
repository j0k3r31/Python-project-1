from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import sqlite3
import requests
import bs4
import pandas as pd
import matplotlib.pyplot as plt


def f1():  # open add tab
    root.withdraw()
    add_stu.deiconify()


def f2():  # back out of add tab
    add_stu.withdraw()
    root.deiconify()
    add_stu_entRno.focus()
    add_stu_entRno.delete(0, END)
    add_stu_entName.focus()
    add_stu_entName.delete(0, END)
    add_stu_entMarks.focus()
    add_stu_entMarks.delete(0, END)


def f3():  # open view tab
    root.withdraw()
    view_stu.deiconify()
    view_stu_stdata.delete(1.0, END)
    con = None
    try:
        con = connect("studentdetails.db")
        cursor = con.cursor()
        sql = "select * from student order by rno"
        cursor.execute(sql)
        data = cursor.fetchall()
        info = " "
        for d in data:
            # print("rno ", d[0], "name", d[1], "marks", d[2])
            info = "RNo. = " + str(d[0]) + " Name= " + str(d[1]) + " Marks= " + str(d[2]) + "\n"
            view_stu_stdata.insert(INSERT, info)
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
    finally:
        if con is not None:
            con.close()


def f4():  # back out of the view tab
    view_stu.withdraw()
    root.deiconify()
    # view_stu_stdata.delete(0, END)
    # view_stu_stdata.focus()


def f5():  # go to update tab
    root.withdraw()
    update_stu.deiconify()


def f6():  # back out of update tab
    update_stu.withdraw()
    root.deiconify()
    update_stu_entRno.focus()
    update_stu_entRno.delete(0, END)
    update_stu_entName.focus()
    update_stu_entName.delete(0, END)
    update_stu_entMarks.focus()
    update_stu_entMarks.delete(0, END)


def f7():  # go to delete tab
    root.withdraw()
    delete_stu.deiconify()


def f8():  # back out of delete tab
    delete_stu.withdraw()
    root.deiconify()
    delete_stu_entRno.delete(0, END)
    delete_stu_entRno.focus()


def f9():  # go to charts
    con = None
    try:
        color_names = ['red', 'green', 'blue']
        con = sqlite3.connect("studentdetails.db")
        data = pd.read_sql_query("select * from student;", con)

        name = data['name'].tolist()
        marks = data['marks'].tolist()

        plt.bar(name, marks, color=color_names)
        plt.title("Batch Information!")
        plt.ylabel("Marks")

        plt.show()
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
    finally:
        if con is not None:
            con.close()


def f10():  # save changes in add tab
    con = None
    try:
        con = connect("studentdetails.db")
        rno = add_stu_entRno.get()
        name = add_stu_entName.get()
        marks = add_stu_entMarks.get()
        if len(rno) == 0 & len(name) == 0 & len(marks) == 0:
            showerror("Empty Feilds", "Enter Valid Credentials!")
        elif rno.isalpha():
            showerror("Integer Only", "Enter Rno in Numbers!")
        elif name.isdigit():
            showerror("Invalid Name", "Name can only contain Alphabets!")
        elif len(name) < 2:
            showerror("Invalid Name", "Name is too small!")
        elif marks.isalpha():
            showerror("Integer Only", "Enter Marks in Numbers!")

        else:
            cursor = con.cursor()
            rno = int(add_stu_entRno.get())
            name = add_stu_entName.get()
            marks = int(add_stu_entMarks.get())
            if rno < 0:
                showerror("Invalid roll number", "Roll number should be Positive!")
            elif marks < 0 or marks > 100:
                showerror("Invalid Marks", "Enter valid Marks!")
            else:
                sql = "insert into student values('%d', '%s', '%d')"
                cursor.execute(sql % (rno, name, marks))
                con.commit()
                showinfo("Sucess", "Record inserted")
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
            add_stu_entRno.focus()
            add_stu_entRno.delete(0, END)
            add_stu_entName.focus()
            add_stu_entName.delete(0, END)
            add_stu_entMarks.focus()
            add_stu_entMarks.delete(0, END)


def f11():  # save changes in update tab
    con = None
    try:
        con = connect("studentdetails.db")
        rno = update_stu_entRno.get()
        name = update_stu_entName.get()
        marks = update_stu_entMarks.get()
        if len(rno) == 0 & len(name) == 0 & len(marks) == 0:
            showerror("Empty Feilds", "Enter Valid Credentials!")
        elif rno.isalpha():
            showerror("Integer Only", "Enter Rno in Numbers!")
        elif name.isdigit():
            showerror("Invalid Name", "Name can only contain Alphabets!")
        elif len(name) < 2:
            showerror("Invalid Name", "Name is too small!")
        elif marks.isalpha():
            showerror("Integer Only", "Enter Marks in Numbers!")
        else:
            cursor = con.cursor()
            sql = "update student set name = '%s', marks = '%d' where rno = '%d'"
            rno = int(update_stu_entRno.get())
            name = update_stu_entName.get()
            marks = int(update_stu_entMarks.get())
            if rno < 0:
                showerror("Invalid roll number", "Roll number should be Positive!")
            elif marks < 0 or marks > 100:
                showerror("Invalid Marks", "Enter valid Marks")
            else:
                cursor.execute(sql % (name, marks, rno))
                if cursor.rowcount > 0:
                    showinfo("Success", "Record updated")
                    con.commit()
                else:
                    showerror('Error', "Roll number doesnot exist!")
    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
            update_stu_entRno.focus()
            update_stu_entRno.delete(0, END)
            update_stu_entName.focus()
            update_stu_entName.delete(0, END)
            update_stu_entMarks.focus()
            update_stu_entMarks.delete(0, END)


def f12():  # save changes in delete tab
    con = None
    try:
        con = connect("studentdetails.db")
        rno = delete_stu_entRno.get()
        if len(rno) == 0:
            showerror("Empty Feilds", "Enter a Roll NUmber!")
        elif rno.isalpha():
            showerror("Integer Only", "Enter Rno in Numbers only!")
        else:
            cursor = con.cursor()
            sql = "delete from student where rno = '%d'"
            rno = int(delete_stu_entRno.get())
            if rno < 0:
                showerror("Invalid roll number", "Roll Number should be positive!")
            else:
                cursor.execute(sql % rno)
                if cursor.rowcount > 0:
                    showinfo("Sucess", "Record deleted!")
                    con.commit()
                else:
                    showerror("Error", "Roll number doesnot exist!")

    except Exception as e:
        showerror("Issue", "No such database or table exists!  " + str(e))
        con.rollback()

    finally:
        if con is not None:
            con.close()
            delete_stu_entRno.delete(0, END)
            delete_stu_entRno.focus()


# ======================================================== Location =========================================================

try:
    web_address = "https://ipinfo.io/"
    res = requests.get(web_address)

    data1 = res.json()
    city_name = data1['city']

except Exception as e:
    print("issue ", e)

# ======================================================== Temperature ======================================================
try:
    a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
    a2 = "&q=" + city_name
    a3 = "&appid=c6e315d09197cec231495138183954bd"
    web_address = a1 + a2 + a3
    res = requests.get(web_address)
    data = res.json()

    main = data['main']
    temp = main['temp']

except Exception as e:
    print(e)

# ======================================================== QOTD =============================================================
try:
    web_address = "https://www.brainyquote.com/quote_of_the_day"
    res = requests.get(web_address)

    data3 = bs4.BeautifulSoup(res.text, "html.parser")

    info = data3.find('img', {'class': 'p-qotd'})

    quote = info['alt']


except Exception as e:
    print("issue", e)

# ======================================================== Main Window ======================================================
root = Tk()
root.title("S.M.S")
root.geometry("600x550+600+400")

btnAdd = Button(root, text="ADD", width=10, font=('Monaco', 18, 'bold'), command=f1)
btnView = Button(root, text="VIEW", width=10, font=('Monaco', 18, 'bold'), command=f3)
btnUpdate = Button(root, text="UPDATE", width=10, font=('Monaco', 18, 'bold'), command=f5)
btnDelete = Button(root, text="DELETE", width=10, font=('Monaco', 18, 'bold'), command=f7)
btnCharts = Button(root, text="CHARTS", width=10, font=('Monaco', 18, 'bold'), command=f9)
lblLocation = Label(root, text="Location : " + str(city_name), font=('Monaco', 18, 'bold'))
lblTemp = Label(root, text="Temperature : " + str(temp) + "°C", font=('Monaco', 18, 'bold'))
lblQotd = Label(root, text="QOTD : " + str(quote), wraplength=590, font=('Monaco', 18, 'bold'))

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnCharts.pack(pady=10)
lblLocation.place(x=10, y=400)
lblTemp.place(x=300, y=400)
lblQotd.place(x=10, y=450)

# ======================================================== Add Stu tab =============================================================
add_stu = Toplevel(root)
add_stu.title("Add Student Details")
add_stu.geometry("600x550+600+400")

add_stu_lblRno = Label(add_stu, text="Enter the Students Roll Number: ", font=('Monaco', 18, 'bold'))
add_stu_entRno = Entry(add_stu, bd=5, font=('Monaco', 18, 'bold'))
add_stu_lblName = Label(add_stu, text="Enter the Students Name: ", font=('Monaco', 18, 'bold'))
add_stu_entName = Entry(add_stu, bd=5, font=('Monaco', 18, 'bold'))
add_stu_lblMarks = Label(add_stu, text="Enter the Students Marks: ", font=('Monaco', 18, 'bold'))
add_stu_entMarks = Entry(add_stu, bd=5, font=('Monaco', 18, 'bold'))
add_stu_btnSave = Button(add_stu, text="Save", width=10, font=('Monaco', 18, 'bold'), command=f10)
add_stu_btnBack = Button(add_stu, text="Back", width=10, font=('Monaco', 18, 'bold'), command=f2)

add_stu_lblRno.pack(pady=5)
add_stu_entRno.pack(pady=5)
add_stu_lblName.pack(pady=5)
add_stu_entName.pack(pady=5)
add_stu_lblMarks.pack(pady=5)
add_stu_entMarks.pack(pady=5)
add_stu_btnSave.pack(pady=5)
add_stu_btnBack.pack(pady=5)

add_stu.withdraw()

# ======================================================== View Stu Tab ==============================================================

view_stu = Toplevel(root)
view_stu.title("View Student Details")
view_stu.geometry("600x550+600+400")

view_stu_stdata = ScrolledText(view_stu, width=35, height=10, font=('Monaco', 18, 'bold'))
view_stu_btnBack = Button(view_stu, text="Back", width=10, font=('Monaco', 18, 'bold'), command=f4)

view_stu_stdata.pack(pady=5)
view_stu_btnBack.pack(pady=5)

view_stu.withdraw()

# ======================================================== Update Stu Tab ============================================================

update_stu = Toplevel(root)
update_stu.title("Update Student Details")
update_stu.geometry("600x550+600+400")

update_stu_lblRno = Label(update_stu, text="Enter the Students Roll Number: ", font=('Monaco', 18, 'bold'))
update_stu_entRno = Entry(update_stu, bd=5, font=('Monaco', 18, 'bold'))
update_stu_lblName = Label(update_stu, text="Enter the Students Name: ", font=('Monaco', 18, 'bold'))
update_stu_entName = Entry(update_stu, bd=5, font=('Monaco', 18, 'bold'))
update_stu_lblMarks = Label(update_stu, text="Enter the Students Marks: ", font=('Monaco', 18, 'bold'))
update_stu_entMarks = Entry(update_stu, bd=5, font=('Monaco', 18, 'bold'))
update_stu_btnSave = Button(update_stu, text="Save", width=10, font=('Monaco', 18, 'bold'), command=f11)
update_stu_btnBack = Button(update_stu, text="Back", width=10, font=('Monaco', 18, 'bold'), command=f6)

update_stu_lblRno.pack(pady=5)
update_stu_entRno.pack(pady=5)
update_stu_lblName.pack(pady=5)
update_stu_entName.pack(pady=5)
update_stu_lblMarks.pack(pady=5)
update_stu_entMarks.pack(pady=5)
update_stu_btnSave.pack(pady=5)
update_stu_btnBack.pack(pady=5)

update_stu.withdraw()

# ================================================= Delete Stu Tab =========================================================

delete_stu = Toplevel(root)
delete_stu.title("Delete Student Details")
delete_stu.geometry("600x550+600+400")

delete_stu_lblRno = Label(delete_stu, text="Enter the Students Rno: ", font=('Monaco', 18, 'bold'))
delete_stu_entRno = Entry(delete_stu, bd=5, font=('Monaco', 18, 'bold'))
delete_stu_btnSave = Button(delete_stu, text="Delete", width=10, font=('Monaco', 18, 'bold'), command=f12)
delete_stu_btnBack = Button(delete_stu, text="Back", width=10, font=('Monaco', 18, 'bold'), command=f8)

delete_stu_lblRno.pack(pady=5)
delete_stu_entRno.pack(pady=5)
delete_stu_btnSave.pack(pady=5)
delete_stu_btnBack.pack(pady=5)

delete_stu.withdraw()

root.mainloop()
