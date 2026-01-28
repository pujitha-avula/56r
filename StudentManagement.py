import  tkinter as tk
root = tk.Tk( ) 
root.title('project')
root.geometry('500x500')
import mysql.connector as sp
conn = sp.connect(password="pujitha@1amm",host="localhost",user="root",database="project",autocommit=False)
cur = conn.cursor()
print(conn.is_connected())

import csv
from tkinter import messagebox
from tkinter import filedialog
def csv_file_upload():
    filename=filedialog.askopenfilename(filetypes=[('CSV FILES','*.CSV')])
    # print("data.csv",filename)
    with open(filename,'r') as f:
        data = csv.reader(f)
        print(next(data))
        for row in data:
            cur.execute('''insert into project1 (name,age,grade,status) values (%s,%s,%s,%s)''',(row))
            print(row)
        conn.commit()
        messagebox.showinfo('INFO',"Data inserted to Database")
def show_grid():
    grid.configure(state=tk.NORMAL)
    grid.delete(1.0,tk.END)

    cur.execute('select * from project1')
    # print(cur.fetchall())
    for row in cur.fetchall():
       grid.insert(tk.END,f'iD:{row[0]},NAME:{row[1]},AGE:{row[2]},GRADE:{row[3]},STATUS:{row[4]}\n') 
    grid.configure(state=tk.DISABLED)
tk.Button(root,text='upload CSV',command=csv_file_upload).pack()
grid=tk.Text(root,height=15,width=60)
grid.pack(pady=10)
input_frame = tk.Frame(root)
input_frame.pack()
id_label = tk.Label(input_frame,text="ID").grid(row=0,column=0)
id_entry = tk.Entry(input_frame,width=2)
id_entry.grid(row=0,column=1,pady=5)
name_label = tk.Label(input_frame,text="NAME").grid(row=0,column=2)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0,column=3)
age_label = tk.Label(input_frame,text="AGE").grid(row=0,column=4)
age_entry = tk.Entry(input_frame,width=3)
age_entry.grid(row=0,column=5)
grade_label = tk.Label(input_frame,text="GRADE").grid(row=0,column=6)
grade_entry = tk.Entry(input_frame,width=3)
grade_entry.grid(row=0,column=7)
status_label = tk.Label(input_frame,text="STATUS").grid(row=0,column=8)
status_entry = tk.Entry(input_frame,width=6)
status_entry.grid(row=0,column=9)

# def add_record():
#     name = name_entry.get()
#     age = age_entry.get()
#     grade = grade_entry.get() 
#     status = status_entry.get()
#     if name and age and grade and status:
#         cur.execute(''' insert into project1 (NAME,AGE,GRADE,STATUS) values(%s,%s,%s,%s)''',(name,age,grade,status,))
#         conn.commit()
#         messagebox.showinfo('INFO',"your record added to database")
#         show_grid()
#     else:
#         messagebox.showwarning('WARNING',"Requied valid Data.")
def add_record():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    grade = grade_entry.get().strip().upper()
    status = status_entry.get().strip().lower()
    if not name:
        messagebox.showwarning('WARNING', 'Name is required')
        return
    if not name.replace(" ", "").isalpha():
        messagebox.showwarning('WARNING', 'Name should contain only letters')
        return
    if not age:
        messagebox.showwarning('WARNING', 'Age is required')
        return
    if not age.isdigit():
        messagebox.showwarning('WARNING', 'Age must be a number')
        return
    age_int = int(age)
    if age_int <= 0 or age_int > 120:  # you can adjust range
        messagebox.showwarning('WARNING', 'Enter a realistic age')
        return
    if not grade:
        messagebox.showwarning('WARNING','Grade is required!!')
        return
    allowed_grades = {"A", "B", "C", "D", "E", "F"}
    if grade not in allowed_grades:
        messagebox.showwarning('WARNING', f"Grade must be one of {allowed_grades}")
        return
    if not status:
        messagebox.showwarning('WARNING',"status required!!")
    allowed_status = {"pass", "fail"}
    if status not in allowed_status:
        messagebox.showwarning('WARNING', 'Status must be "pass" or "fail"')
        return
    try:
        cur.execute('''INSERT INTO project1 (NAME, AGE, GRADE, STATUS) VALUES (%s, %s, %s, %s)''',
            (name, age_int, grade, status))
        conn.commit()
        messagebox.showinfo('INFO', "Your record was added to the database")
        show_grid()
    except Exception as e:
        messagebox.showerror('ERROR', str(e))
#edit  #name  
def edit_record():
    id_str = id_entry.get()
    if not id_str:
        messagebox.showerror('ERROR',f'Give valid id too!!')
        return
    if  not id_str.isdigit():
        messagebox.showwarning('WARNING',f'id should be integer!!')
        return
    name_str = name_entry.get()
    if name_str:

        if not name_str:
            messagebox.showwarning('WARNING',f'Enter a valid name')
            return
        if name_str.isdigit():
            messagebox.showerror('ERROR',f'name should not be only numbers!!')
            return
        try:
            cur.execute(''' select name from project1 where id=%s''',(id_str,))
            row = cur.fetchone( )
            if not row:
                messagebox.showerror('ERROR', 'No record found with that ID.')
                return
            cur.execute(''' update project1 set name=%s where id=%s''',(name_str,id_str))
            conn.commit()
            show_grid()
        except Exception as e:
            messagebox.ERROR('ERROR',f'{e}')
        else:
                if cur.rowcount == 0:
                    messagebox.showinfo('INFO', 'No record found with that ID.')
                else:
                    messagebox.showinfo('INFO','name updated')
# age
    age_str = age_entry.get().strip()
    if age_str:
        if not age_str:
            messagebox.showwarning('WARNING','Enter a valid age!!')
            return
        if  not age_str.isdigit():
            messagebox.showwarning('WARNGING','Age should be interger!!')
            return
        try:
            cur.execute(''' update project1 set age=%s where id=%s''',(age_str,id_str))
            conn.commit()
            show_grid()
            messagebox.showinfo('INFO',"Age updated successfully.")
        except Exception as e:
            messagebox.showerror('ERROR',f'{e}')
#grade
    grade_str = grade_entry.get().strip()
    if grade_str:
        if not grade_str:
            messagebox.showwarning('WARNING',"Give a valid Grade!!")
            return
        if grade_str.isdigit():
            messagebox.showwarning('WARNING',"Grade should not be integer!!")
            return 
        allowed = { "A","B","C","D","E","F"}
        if grade_str not in allowed:
            messagebox.showwarning("WARNING",f"Grade must be one of{allowed}")
            return
        try:
            cur.execute(''' update project1 set grade=%s where id = %s''',(grade_str,id_str))
            conn.commit() 
            updated = cur.rowcount
            if updated==0:
                messagebox.showinfo('INFO','No record found with ID') 
            else:
                messagebox.showinfo('INFO','Grade updated successfully!!')
            show_grid( )
        except Exception as e:
            messagebox.showerror('ERROR',f'{e}')
            
    status_str = status_entry.get().strip( )
    if status_str:
        if not status_str:
            messagebox.showwarning('WARNING','Enter a valid status')
            return
        if status_str.isdigit():
            messagebox.showwarning('WARNING',"status should not be integer!!")
            return 
        allowed = {"pass", "fail"}
        if status_str not in allowed:
                messagebox.showwarning('WARNING', 'Status must be either "pass" or "fail"')
                return
        try:
            cur.execute(''' update project1 set status=%s where id= %s''',(status_str,id_str))
            conn.commit()
            updated = cur.rowcount
            if updated ==0:
                 messagebox.showinfo('INFO','No record found with ID')
            else:
                messagebox.showinfo('INFO',"Status updated successfully!!")
            show_grid( )
        except Exception as e:
            messagebox.showerror('ERROR',f'{e}')
#delete
def delete_record():
    id_str = id_entry.get().strip()
    if not id_str:
        messagebox.showwarning('WARNING','Enter valid id!!')
        return
    try:
         if id != int(id_str):
             pass
    except Exception as e:
        messagebox.showerror('ERROR',f'id should be interger {e}')
        return
    try:
        cur.execute('''delete from project1 where id = (%s)''',(id_str,))
        conn.commit()
        deleted = cur.rowcount
        if deleted==0:
                messagebox.showinfo('INFO', f'No record found with ID')
        else:
                messagebox.showinfo('INFO','record successfully deleted!!')
        show_grid()
    except Exception as e:
        messagebox.showerror('ERROR',f'Given id not exists {e}')
tk.Button(input_frame,text='ADD',command=add_record).grid(row=1,column=0,pady=15)
tk.Button(input_frame,text='EDIT',command=edit_record).grid(row=1,column=1,pady=15)
tk.Button(input_frame,text='DELETE',command=delete_record).grid(row=1,column=2,pady=15)
show_grid( )
root.mainloop()