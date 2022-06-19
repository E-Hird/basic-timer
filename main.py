#Imports//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from tkinter import *
from tkinter import messagebox
from math import *
import winsound as win
import time
import sys
import os
#Framework////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
##Variables
global info;    # List of the lines in info.tim
info = []
global day;     # Top line of info.tim, checks wether new day or not
day = 0
global tasks;   # 2nd line of info.tim, list of tasks
global times;   # 3rd line of info.tim is starting times, 4th line is progress
tasks = []
times = []
global on;      # List of which timers are active
on = []
global alarm;   # Wether or not the alarm is active
alarm = False
global t;       # List of timer instances
t = []
##Objects
class Timer:                            #Timer Widget
    def onoff(self):                    # Toggles the timer on and off
        if not on[self.index]:
            on[self.index] = True
            self.button.config(text="Pause")
        elif on[self.index]:
            on[self.index] = False
            self.button.config(text="Play")
    
    def __init__(self, frame, index):   # Creates the timer gui itself
        self.index = index
        box = Frame(frame)
        l_task = Label(box, text=tasks[index], font="Helevicta 20")                         #Task name
        self.l_timer = Label(box, text=str(convert_time(times[index], True)), font="Verdana 20")  #Task time
        self.button = Button(box, text="Play", command=self.onoff, width=6)                 #Start/stop timer
        l_task.grid(column=0, row=0)
        self.l_timer.grid(column=0, row=1)
        self.button.grid(column=0, row=2)
        box.grid(column=index%3, row=index//3)

class Table:                            #Row of Table Widget
    def remove(self):                   #Removes row from the table
        temp_times.pop(temp_tasks.index(self.name))
        temp_tasks.remove(self.name)
        self.e_task.destroy()
        self.e_time.destroy()
        self.button.destroy()

    def __init__(self, frame, index):   #Create the table itself
        self.name = temp_tasks[index]
        self.e_task = Entry(frame, width=40)        #Task name
        self.e_time = Entry(frame, width=20)        #Task time
        self.e_task.grid(column=0, row=index+1)
        self.e_time.grid(column=1, row=index+1)
        self.e_task.insert(0, temp_tasks[index])    #Remove the task
        self.e_time.insert(0, str(convert_time(temp_times[index], True)))

        self.button = Button(frame, text="Remove", command=self.remove, width=6)
        self.button.grid(column=2, row=index+1)
##Scripts
def convert_time(length, num_to_str):   # Puts time in hr:min:sec format 
    if num_to_str:
        secs = length % 60
        time_mins = length // 60
        mins = time_mins % 60
        time_hrs = time_mins // 60
        hrs = time_hrs % 60
        if len(str(secs)) == 1:
            secs = "0" + str(secs)
        if len(str(mins)) == 1:
            mins = "0" + str(mins)
        if len(str(hrs)) == 1:
            hrs = "0" + str(hrs)
        string = (str(hrs) + ":" + str(mins) + ":" + str(secs))
        return string
    else:
        parts = length.split(":")
        num = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return num

def check_time_format(read_entry):        # Checks that time in format hr:min:sec
    correct_format = True
    try:
        int(read_entry.get().replace(":", ""))
    except ValueError:
        correct_format = False
        messagebox.showerror("Error", "Use numbers for time")
        return correct_format;
    if not (len(read_entry.get())==8 and read_entry.get()[2]==":" and read_entry.get()[5]==":"):
        correct_format = False
        messagebox.showerror("Error", "Put time in format hr:min:sec where hrs < 99")
        return correct_format;
    if (int((read_entry.get()).split(":")[1]) > 59 or int((read_entry.get()).split(":")[2]) > 59):
        correct_format = False
        messagebox.showerror("Error", "Make sure that mins are secs are < 99")
        return correct_format;
    if ((len(read_entry.get())<=0)):
        correct_format = False
        messagebox.showerror("Error", "Input a time")
        return correct_format;
    return correct_format;

def alarm_onoff():          # Toggles the alarm
    global alarm;
    if(check_time_format(alarm_entry)):
        if not alarm:
            alarm = True
            button_alarm.config(text="Turn Off")
            alarm_entry.config(state=DISABLED)
        elif alarm:
            alarm = False
            button_alarm.config(text="Turn On")
            alarm_entry.config(state=NORMAL)

def time_update():          # Ticks the clock down every second
    global alarm;
    time_num = time.time()
    time_num = floor(time_num)
    tim = time.localtime(time_num)
    tim = time.strftime('%H:%M:%S', tim)
    clock.config(text=(str(tim)))

    if (alarm) and (str(tim)==alarm_entry.get()):   #Checks if alarm should activate
        win.Beep(1000, 1500)
        alarm = False
        button_alarm.config(text="Turn On")
        alarm_entry.config(state=NORMAL)

    for i in range(len(tasks)):                     #Checks if timer is done
        if (on[i]):
            if times[i] <= 0:
                on[i] = False
                t[i].button.config(text="Done")
                win.Beep(1000, 1500)
            else:
                times[i] -= 1
                t[i].l_timer.config(text=convert_time(times[i], True))
            
    
    clock.after(1000, time_update)                  #Reiterates the clock

def settings():
    global temp_tasks;                          #Creates temp lists for editing
    global temp_times;
    win_settings = Toplevel()                   #Creates settings window
    win_settings.title("Settings")
    win_settings.resizable(False, False)
    ttle_frame = Frame(win_settings)            #Creates frames for settings window
    table = Frame(win_settings, bg="#353a42")
    add_frame = Frame(win_settings)
    save_frame = Frame(win_settings)
    ttle_frame.pack()
    table.pack()
    add_frame.pack()
    save_frame.pack()
    
    l_title = Label(ttle_frame, text="Schedule for today", font="Arial 15 bold")        #Title widget
    l_title.pack()

    l_task_header = Label(table, text="Tasks", anchor="w", width=40, bg="#666666", fg="#ffffff", relief=RAISED)                 #Table headers
    l_time_header = Label(table, text="Times (hr:min:sec)", anchor="w", width=20, bg="#666666", fg="#ffffff", relief=RAISED)
    l_task_header.grid(column=0,row=0)
    l_time_header.grid(column=1,row=0)

    rows = []
    temp_tasks = tasks.copy()
    temp_times = eval(info[2])

    for i in range(len(tasks)):             #Creates table
        rows.append(Table(table, i))

    def add():                                  #Add timer to the editing list
        valid = check_time_format(add_time)     #Check that the entries are valid
        if ((len(add_task.get())<=0)):
            valid = False
            messagebox.showerror("Error", "Tasks need a name")
        elif (temp_tasks.count(add_task.get())>0):
            valid = False
            messagebox.showerror("Error", "Cannot have more than one task of the same name")
        
        if valid:
              temp_tasks.append(add_task.get())                         #Add the task
              temp_times.append(convert_time(add_time.get(), False))
              rows.append(Table(table, len(temp_tasks)-1))
              add_task.delete(0, last=len(add_task.get()))
              add_time.delete(0, last=len(add_time.get()))
            
    
    add_task = Entry(add_frame, width=40)                               #Buttons for adding tasks
    add_time = Entry(add_frame, width=20)
    add_button = Button(add_frame, text="Add", command=add, width=6)
    add_task.grid(column=0, row=0)
    add_time.grid(column=1, row=0)
    add_button.grid(column=2, row=0)

    def save():                                                         #Save the edited list of tasks
        global tasks;
        global times;
        tasks = temp_tasks.copy()
        times = temp_times.copy()
        info[2] = temp_times.copy()
        messagebox.showinfo("Saved", "Timers updated: Please reload the program.")
        leave()                                                         #Leave to finalise the save
        

    save_button = Button(save_frame, text="Save", command=save, width=6)    #Buttons for saving the list of tasks
    exit_button = Button(save_frame, text="Back", command=win_settings.destroy, width=6)
    save_button.grid(column=0, row=0)
    exit_button.grid(column=1, row=0)
        

def leave():
    save_str = ""                           #Format the info for saving
    info[0] = day
    info[1] = tasks.copy()
    info[3] = times.copy()
    f = open("info.tim", "w")
    for i in range(len(info)):
        save_str = save_str + str(info[i])
        if (i != (len(info)-1)):
            save_str += "\n"
    f.write(save_str)                       #Save the info save string
    f.close()
    main.destroy()                          #Destroy the GUI
#File check///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
try:
    f = open("info.tim", "r")
    info = f.read()
    info = info.split("\n")
    while info.count("") > 0:
        info.remove("")
    for i in range(len(info)-2):    #Checks the lists are the same length
        if(len(eval(info[1])) != len(eval(info[i+2]))):
            main = Tk()
            main.geometry("1x1+940+540")
            messagebox.showerror("Error", "File corruption: \nInconsistent amount of tasks")
            main.destroy()
            sys.exit()
except IOError:                     #Checks the file exists
    info = ["0", "[]", "[]", "[]"]
    f = open("info.tim", "w")
    f.write("0\n[]\n[]\n[]")
finally:
    f.close()
#Setup////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
day = floor(time.time())            #Find the current day
day = time.localtime(day)
day = time.strftime('%D', day)
last_day = info[0]
if last_day != day:                 #Assign timers based on the day
    tasks = eval(info[1])
    times = eval(info[2])
    for i in range(len(tasks)):
        on.append(False)
else:
    tasks = eval(info[1])
    times = eval(info[3])
    for i in range(len(tasks)):
        on.append(False)
#GUI//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
main = Tk()                         #Create the main window
main.title("Schedule")
main.geometry("+600+300")
main.resizable(False, False)

title = Frame(main)                 #Create the main window frames
time_frame = Frame(main)
alarm_frame = Frame(main)
timers = Frame(main)
exit_frame = Frame(main)
title.pack()
time_frame.pack()
alarm_frame.pack()
timers.pack()
exit_frame.pack()

l_title = Label(title, text="Schedule for today", font="Arial 25 bold")
l_title.pack()

clock = Label(time_frame, text="thing", font="Verdana 25")  #Create the clock
clock.pack()
clock.after(1000, time_update)

l_alarm = Label(alarm_frame, text="Alarm", font="Helevicta 20 bold")    #Create the alarm
l_alarm.pack()
alarm_manage = Frame(alarm_frame)
alarm_manage.pack()
alarm_entry = Entry(alarm_manage, width=60)
button_alarm = Button(alarm_manage, text="Turn On", command=alarm_onoff, width=8)
alarm_entry.grid(column=0, row=0)
button_alarm.grid(column=1, row=0)

for i in range(len(tasks)):         #Create the timers
    t.append(Timer(timers, i))

button_settings = Button(exit_frame, text="Configure", command=settings, width=8)   #Buttons for navigating the program
button_settings.grid(column=0, row=0)
button_exit = Button(exit_frame, text="Exit", command=leave, width=8)
button_exit.grid(column=1, row=0)

main.protocol("WM_DELETE_WINDOW", leave)        #Save the times if the window closes at all
main.mainloop()
