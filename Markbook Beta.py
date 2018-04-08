
import tkinter as tk
import sqlite3

conn = sqlite3.connect('markbook.db')
cur = conn.cursor()
root = tk.Tk()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def classentry(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS classes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, class text)''')
        Classname = input("What is the class' name?")
        Classname = Classname.lower()
        cur.execute('''INSERT OR IGNORE INTO classes(class) VALUES(?)''', (Classname,))
        conn.commit()
        print("Class added successfully!")

    def reviewhw(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS reviewhw (class_id INTEGER NOT NULL, mark_id INTEGER NOT NULL, duedate TEXT, homework TEXT, score INTEGER)''')
        Classname = input('What class does this homework belong to?')
        Classname = Classname.lower()
        cur.execute('''SELECT id FROM classes WHERE class=?''', (Classname,))
        Classid = cur.fetchone()[0]
        DueDate = input('What date was this homework for?')
        cur.execute('''SELECT mark_id FROM students WHERE class_id=? ''', (Classid,))
        students = cur.fetchall()
        students = list(sum(students, ()))
        cur.execute('''SELECT name FROM students WHERE class_id=? ''', (Classid,))
        name = cur.fetchall()
        name = list(sum(name, ()))
        cur.execute('''SELECT homeworkset FROM sethw WHERE class_id=? AND duedate=? ''', (Classid,DueDate,))
        Homework = cur.fetchone()[0]
        for Students in students:
            Score = input("What is this student's score? (register order)")
            cur.execute('''INSERT INTO reviewhw(class_id, mark_id, duedate, homework, score) VALUES(?,?,?,?,?)''', (Classid, Students, DueDate, Homework, Score,))
            conn.commit()

    def addhw(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS sethw (class_id INTEGER NOT NULL, homeworkset TEXT, duedate TEXT) ''')
        Classname = input("What is the class to add homework to?")
        Classname = Classname.lower()
        cur.execute('''SELECT id FROM classes WHERE class=?''', (Classname,))
        Classid = cur.fetchone()[0]
        Hw2Set = input('Homework to add: ')
        Hw2Set = Hw2Set.lower()
        Duedate = input('What is the due date? ')
        cur.execute('''INSERT INTO sethw(class_id, homeworkset, duedate) VALUES(?, ?, ?)''', (Classid, Hw2Set, Duedate,))
        print("Homework Added Successfully!")
        conn.commit()

    def studentsadd(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS students (class_id INTEGER NOT NULL,mark_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT)''')
        Classname = input("What is the class to add students to?")
        Classname = Classname.lower()
        cur.execute('''SELECT id FROM classes WHERE class = ?''', (Classname,))
        Classid = cur.fetchone()[0]
        while True:
            StudentName = input("Student to add: ")
            StudentName = StudentName.lower()
            print("Type 'done' when done.")
            if StudentName == 'done':
                conn.commit()
                break
            else:
                cur.execute('''INSERT INTO students(class_id, name) VALUES(?, ?)''', (Classid, StudentName,))
                print(StudentName, " added into ", Classname)
                conn.commit()

    def seepoints(self):
        Classname = input('What class is the student in?')
        Classname = Classname.lower()
        Student = input('Which student is it?')
        Student = Student.lower()
        cur.execute('''SELECT mark_id FROM students WHERE name=? ''', (Student,))
        markid = cur.fetchone()[0]
        HW = input("What is the due date for the homework?")
        cur.execute('''SELECT score FROM reviewhw WHERE mark_id=? AND duedate=?''', (markid, HW,))
        toprint = cur.fetchall()
        toprint = list(sum(toprint, ()))
        print(Student,"in",Classname,"has achieved a",toprint,"on the homework due:",HW)

    def create_widgets(self):
        self.ClassCreate = tk.Button(self, text="Create a class", command=self.classentry)
        self.ClassCreate.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")
        self.StudentAdd = tk.Button(self, text="Add Students", command=self.studentsadd)
        self.StudentAdd.pack(side="top")
        self.HwAdd = tk.Button(self, text="Add Homework/Tests", command=self.addhw)
        self.HwAdd.pack(side="top")
        self.HwReview = tk.Button(self, text="Review Homework/Tests", command=self.reviewhw)
        self.HwReview.pack(side="top")
        self.PointReview = tk.Button(self, text="Check a student's homework/test score", command=self.seepoints)
        self.PointReview.pack(side="top")

app = Application(master=root)
app.mainloop()
