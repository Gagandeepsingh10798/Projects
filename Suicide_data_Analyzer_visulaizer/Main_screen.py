# import libraries
from tkinter import *
from tkinter import ttk
import pandas as pd
from PIL import ImageTk
import tkinter.messagebox as mb
import matplotlib.style as style
import functions
# import libraries

style.use("ggplot")

# data-frame + states,year,cause,age-groups list
df = pd.read_csv("data.csv")
STATES = sorted(list(set(df["STATE/UT"])))
YEAR = sorted(list(set(df["Year"])))
CAUSE = sorted(list(set(df["CAUSE"])))
AGE = sorted(list(set(df.columns[3:16])))


# data-frame + states,year,cause,age-groups list

# Functions
# quit application function


def quite():
    box = mb.askquestion('Exit Application', 'Are you sure you want to exit the application',
                         icon='warning')
    if box == 'yes':
        master.destroy()


# quit application function
# suicides number


def show_data_frame():
    df1 = pd.read_csv("data.csv")
    df1 = df1[(df1["STATE/UT"] == state_list.get())]
    df1 = df1[(df1["Year"] == int(year_list.get()))]
    df1 = df1[(df1["CAUSE"] == cause_list.get())]
    result_ans = list(df1[df1.columns[df1.columns.get_loc(age_list.get())]].values)
    Result.delete(0, END)
    Result.insert(0, result_ans[0:2])

# suicides number
# Functions
# gui window start
master = Tk()
master.wm_attributes('-fullscreen', 'true')  # to hide title bar
master.state('zoomed')  # to make window open as full screen
background_image = PhotoImage(file="images\\background.png")  # to set image at background of window
background_label = Label(master, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# drop down lists
state_list = StringVar(master)
state_list.set(STATES[0])  # default value

state2_list = StringVar(master)
state2_list.set(STATES[0])  # default value

year_list = StringVar(master)
year_list.set(YEAR[0])  # default value

year2_list = StringVar(master)
year2_list.set(YEAR[0])  # default value

cause_list = StringVar(master)
cause_list.set(CAUSE[0])  # default value

age_list = StringVar(master)
age_list.set(AGE[0])  # default value

drop_down_1 = ttk.OptionMenu(master, state_list, *STATES).place(x=254, y=157)
drop_down_5 = ttk.OptionMenu(master, state2_list, *STATES).place(x=420, y=157)
drop_down_2 = ttk.OptionMenu(master, year_list, *YEAR).place(x=254, y=265)
drop_down_6 = ttk.OptionMenu(master, year2_list, *YEAR).place(x=420, y=265)
drop_down_3 = ttk.OptionMenu(master, cause_list, *CAUSE).place(x=254, y=390)
drop_down_4 = ttk.OptionMenu(master, age_list, *AGE).place(x=254, y=485)
Result = ttk.Entry(master)
Result.place(x=254, y=589)

# create buttons here
q = Button(master, text='Quit', command=lambda: quite(), bg="black", relief=FLAT)
q_image = ImageTk.PhotoImage(file="images\\quit.png")
q.config(image=q_image)
q.image = q_image
q.place(x=1210, y=75)

calculate = Button(master, text='Show Data',
                   command=lambda: show_data_frame(), bg="black", relief=FLAT)
calculate_image = ImageTk.PhotoImage(file="images\\calculate.png")
calculate.config(image=calculate_image, )
calculate.image = calculate_image
calculate.place(x=410, y=570)

one = Button(master, text='Show Data',
             command=lambda: functions.all_year_shw(state_list.get(), cause_list.get()),
             bg="black", relief=FLAT)
one_image = ImageTk.PhotoImage(file="images\\one.png")
one.config(image=one_image)
one.image = one_image
one.place(x=1210, y=160)

two = Button(master, text='Show Data',
             command=lambda: functions.cmp_two_states(state_list.get(), state2_list.get(), int(year_list.get())),
             bg="black", relief=FLAT)
two_image = ImageTk.PhotoImage(file="images\\two.png")
two.config(image=two_image)
two.image = two_image
two.place(x=1210, y=250)

three = Button(master, text='Show Data',
               command=lambda: functions.shw_data_all_state(int(year_list.get()), cause_list.get(), age_list.get()),
               bg="black", relief=FLAT)
three_image = ImageTk.PhotoImage(file="images\\three.png")
three.config(image=three_image)
three.image = three_image
three.place(x=1210, y=340)

four = Button(master, text='Show Data',
              command=lambda: functions.shw_data_all_cause(state_list.get(), age_list.get(), int(year_list.get())),
              bg="black", relief=FLAT)
four_image = ImageTk.PhotoImage(file="images\\four.png")
four.config(image=four_image)
four.image = four_image
four.place(x=1210, y=430)

five = Button(master, text='Show Data',
              command=lambda: functions.shw_data_all_year(state_list.get()),
              bg="black", relief=FLAT)
five_image = ImageTk.PhotoImage(file="images\\five.png")
five.config(image=five_image)
five.image = five_image
five.place(x=1210, y=520)

six = Button(master, text='Show Data',
             command=lambda: functions.sme_state_growth(int(year_list.get()), int(year2_list.get()), state_list.get(),
                                              age_list.get()),
             bg="black", relief=FLAT)
six_image = ImageTk.PhotoImage(file="images\\six.png")
six.config(image=six_image)
six.image = six_image
six.place(x=1210, y=610)

seven = Button(master, text='Show Data',
               command=lambda: functions.pie_state(int(year_list.get()), state_list.get()),
               bg="black", relief=FLAT)
seven_image = ImageTk.PhotoImage(file="images\\seven.png")
seven.config(image=seven_image)
seven.image = seven_image
seven.place(x=1279, y=160)

eight = Button(master, text='Show Data',
               command=lambda: functions.sme_plotting(int(year_list.get()), state_list.get(), cause_list.get()),
               bg="black", relief=FLAT)
eight_image = ImageTk.PhotoImage(file="images\\eight.png")
eight.config(image=eight_image)
eight.image = eight_image
eight.place(x=1279, y=250)
mainloop()
# gui window end
