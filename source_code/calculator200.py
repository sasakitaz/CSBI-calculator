import tkinter as tk
from tkinter import *
from tkinter import ttk
import CSBICalculation_Module
import CSBICalcModule
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from tkinter import messagebox

def quit_me(root_window):
        root_window.quit()
        root_window.destroy()

class Timer:
    def __init__(self, master):
        self.master = master
        self.hours = 1
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0
        self.timer_running = False


        self.timer_frame = tk.Frame(master)
        self.timer_frame.pack(side=tk.LEFT)

        self.label = tk.Label(self.timer_frame, text="Estimated calculation time : ", font=("Helvetica", 16), background="#CFDAED")
        self.label.pack(side=tk.LEFT)

        self.hours_label = tk.Label(self.timer_frame, text="00", font=("Helvetica", 16), background="#CFDAED")
        self.hours_label.pack(side=tk.LEFT)


        self.separator1_label = tk.Label(self.timer_frame, text=":", font=("Helvetica", 16), background="#CFDAED")
        self.separator1_label.pack(side=tk.LEFT)


        self.minutes_label = tk.Label(self.timer_frame, text="00", font=("Helvetica", 16), background="#CFDAED")
        self.minutes_label.pack(side=tk.LEFT)


        self.separator2_label = tk.Label(self.timer_frame, text=":", font=("Helvetica", 16), background="#CFDAED")
        self.separator2_label.pack(side=tk.LEFT)


        self.seconds_label = tk.Label(self.timer_frame, text="00", font=("Helvetica", 16), background="#CFDAED")
        self.seconds_label.pack(side=tk.LEFT)


        self.separator3_label = tk.Label(self.timer_frame, text=".", font=("Helvetica", 16), background="#CFDAED")
        self.separator3_label.pack(side=tk.LEFT)

        
        self.milliseconds_label = tk.Label(self.timer_frame, text="00", font=("Helvetica", 16), background="#CFDAED")
        self.milliseconds_label.pack(side=tk.LEFT)
        

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.LEFT)

        
        #self.hours_button = tk.Button(self.button_frame, text="時", command=self.increment_hours, font=("Helvetica", 16))
        #self.hours_button.pack(side=tk.LEFT)


        #self.minutes_button = tk.Button(self.button_frame, text="分", command=self.increment_minutes, font=("Helvetica", 16))
        #self.minutes_button.pack(side=tk.LEFT)


        #self.seconds_button = tk.Button(self.button_frame, text="秒", command=self.increment_seconds, font=("Helvetica", 16))
        #self.seconds_button.pack(side=tk.LEFT)


        #self.reset_button = tk.Button(self.button_frame, text="リセット", command=self.reset_timer, font=("Helvetica", 16))
        #self.reset_button.pack(side=tk.LEFT)
        
        
        #self.start_stop_button = tk.Button(self.button_frame, text="スタート", command=self.start_stop_timer, font=("Helvetica", 16))
        #self.start_stop_button.pack(side=tk.LEFT)


    def increment_hours(self):
        if not self.timer_running:
            self.hours += 1
            self.update_labels()


    def increment_minutes(self):
        if not self.timer_running:
            self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1
            self.update_labels()


    def increment_seconds(self):
        if not self.timer_running:
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes == 60:
                    self.minutes = 0
                    self.hours += 1
            self.update_labels()


    def reset_timer(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0
        self.update_labels()


    def update_labels(self):
        self.hours_label.config(text=str(self.hours).zfill(2))
        self.minutes_label.config(text=str(self.minutes).zfill(2))
        self.seconds_label.config(text=str(self.seconds).zfill(2))
        self.milliseconds_label.config(text=str(self.milliseconds).zfill(2))


    def start_stop_timer(self):
        if not self.timer_running:
            self.timer_running = True
            #self.start_stop_button.config(text="ストップ")
            self.countdown()
        else:
            self.timer_running = True
            #self.start_stop_button.config(text="スタート")


    def countdown(self):
        if self.hours == 0 and self.minutes == 0 and self.seconds == 0 and self.milliseconds == 0:
            self.timer_running = False
            #self.start_stop_button.config(text="スタート")
            return


        if self.milliseconds == 0:
            self.milliseconds = 99
            if self.seconds == 0:
                self.seconds = 59
                if self.minutes == 0:
                    self.minutes = 59
                    self.hours -= 1
                else:
                    self.minutes -= 1
            else:
                self.seconds -= 1
        else:
            self.milliseconds -= 1


        self.update_labels()


        if self.timer_running:
            self.master.after(10, self.countdown)



class PlaceholderEntry(tk.Entry):
    def __init__(self, container, placeholder, *args, fg1="#d5d5d5", fg2="black", **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.fg1 = fg1
        self.fg2 = fg2

        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self["fg"] = fg1

    def _clear_placeholder(self, e):
        if hasattr(self, "placeholder"):
            self.delete("0", "end")
            self["fg"] = self.fg2

    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["fg"] = self.fg2


def estimated_time(dimension):
    time = 0.00001835*dimension**2
    return time

def dimension(n0, npls, nmns, j, m):
    dim = [0]
    allowl = [0]
    allowmB = [0]
    for ll in range(- nmns, npls + 1):
        for mB in range(- j, j + 1):
            
            jdim = []
            for num in range(0, j + 1):
                jd = (2 * abs(num) + 1)
                jdim.append(jd)
                
            mminus = []
            for mm in range(0, abs(mB) + 1):
                if mm == 0:
                    a = 0
                else:
                    a = (2 * (abs(mm) - 1) + 1)
                mminus.append(a)
                
            if ll + mB == m:
                d = (npls + 1 - abs(ll))*(sum(jdim)-sum(mminus))
                dim.append(d)
                allowl.append(ll)
                allowmB.append(mB)
    dimension = sum(dim)*(n0 + 1)
    return dimension

baseGround = tk.Tk()
# メインウィンドウを作成

baseGround.geometry('960x600')
# ウィンドウのサイズを設定

baseGround.title('Coupled-Stretch-Bend-Internal-Rotation Model Calculator')
# ウィンドウのタイトルを設定

#ラベル
label1 = tk.Label(text='Coupled-Stretch-Bend-Internal-Rotation Model Calculator', font=("Helvetica", "18", "bold"), width = "800", height = "2", foreground='#5881C1', background='#3F3F3F')
label1.pack()

# Notebookウィジェットの作成
notebook = ttk.Notebook(baseGround)

# タブの作成
tab_one = tk.Frame(notebook, bg='#CFDAED')
tab_two = tk.Frame(notebook, bg='#CFDAED')
tab_thr = tk.Frame(notebook, bg='#CFDAED')

# notebookにタブを追加
notebook.add(tab_one, text="Molecular Parameters")
notebook.add(tab_two, text="Matrix size and Potential parameters")
notebook.add(tab_thr, text="Results")


label = ttk.Label(tab_one, text="Molecular Parameter", font=("Helvetica", "16", "bold"), foreground = "#28487c", background="#CFDAED")
label.place(x= 5, y=5)


# tab_oneに配置するウィジェットの作成
label = ttk.Label(tab_one, text="Symmetry of Small Molecule", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 20, y=20 + 30)




"""
combobox_max_LB = ttk.Combobox(tab_two, values="0  1  2  3  4  5", width = 10, state="readonly", style="office.TCombobox")
combobox_max_LB.place(x=225, y=285 + 10)
label = ttk.Label(tab_two, text="m_cpl, Angular momentum coupling: ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 10, y=310 + 10)
combobox_max_mcpl = ttk.Combobox(tab_two, values="0  1  2  3", width = 10, state="readonly", style="office.TCombobox")
combobox_max_mcpl.place(x=225, y=310 + 10)
label = ttk.Label(tab_two, text="R^n, R dependence of Angular term: ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 10, y=335 + 10)
combobox_max_n = ttk.Combobox(tab_two, values="0  6  8  10", width = 10, state="readonly", style="office.TCombobox")
combobox_max_n.place(x=225, y=335 + 10)
"""






style = ttk.Style(tab_one)
style.configure("Placeholder.TEntry", foreground="#d5d5d5", width=10)

label = ttk.Label(tab_one, text="Small Molecule", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5 + 15, y=65 + 30 + 30)
label = ttk.Label(tab_one, text="Rotational Constants [float]", font=("Helvetica", "10",), background="#CFDAED")
label.place(x= 5 + 15, y=65 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="A = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 15, y=90 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="cm\u207B\u00B9", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 15, y=90 + 20 + 40 + 30)
txtBox_A_small = ttk.Entry(tab_one, width=15)
txtBox_A_small.place(x=50 + 15, y=90 + 20 + 40 + 30)

label = ttk.Label(tab_one, text="B = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 15, y=115 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="cm\u207B\u00B9", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 15, y=115 + 20 + 40 + 30)
txtBox_B_small = ttk.Entry(tab_one, width=15)
txtBox_B_small.place(x=50 + 15, y=115 + 20 + 40 + 30)

label = ttk.Label(tab_one, text="C = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 15, y=140 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="cm\u207B\u00B9", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 15, y=140 + 20 + 40 + 30)
txtBox_C_small = ttk.Entry(tab_one, width=15)
txtBox_C_small.place(x=50 + 15, y=140 + 20 + 40 + 30)

label = ttk.Label(tab_one, text="Molecular Mass [float]", font=("Helvetica", "10"), background="#CFDAED")
label.place(x= 5 + 15, y=175 + 7 + 50 + 30)
label = ttk.Label(tab_one, text="ex. H\u2082O → 18", font=("Helvetica", "9"), background="#CFDAED")
label.place(x= 20 + 15, y=200 + 5 + 50 + 30)
label = ttk.Label(tab_one, text="m = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 15, y=200 + 5 + 50 + 50)
label = ttk.Label(tab_one, text="Da", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 15, y=200 + 5 + 50 + 50)
txtBox_m_small = ttk.Entry(tab_one, width=15)
txtBox_m_small.place(x= 50 + 15, y=200 + 5 + 50 + 50)


label = ttk.Label(tab_one, text="Large Molecule", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5 + 300, y=65 + 30 + 30)
label = ttk.Label(tab_one, text="Rotational Constants [float]", font=("Helvetica", "10"), background="#CFDAED")
label.place(x= 5 + 300, y=65 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="B = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 300, y=90 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="cm\u207B\u00B9", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 300, y=90 + 20 + 40 + 30)
txtBox_B_large = ttk.Entry(tab_one, width=15)
txtBox_B_large.place(x=50 + 300, y=90 + 20 + 40 + 30)

label = ttk.Label(tab_one, text="C = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 300, y=115 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="cm\u207B\u00B9", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 300, y=115 + 20 + 40 + 30)
txtBox_C_large = ttk.Entry(tab_one, width=15)
txtBox_C_large.place(x=50 + 300, y=115 + 20 + 40 + 30)

label = ttk.Label(tab_one, text="Molecular Mass [float]", font=("Helvetica", "10"), background="#CFDAED")
label.place(x= 5 + 300, y=175 + 7 + 50 + 30)
label = ttk.Label(tab_one, text="ex. C\u2086H\u2086 → 78", font=("Helvetica", "9"), background="#CFDAED")
label.place(x= 20 + 300, y=200 + 5 + 50 + 30)
label = ttk.Label(tab_one, text="m = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 300, y=200 + 5 + 50 + 50)
label = ttk.Label(tab_one, text="Da", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 180 + 300, y=200 + 5 + 50 + 50)
txtBox_m_large = Entry(tab_one, width=15)
txtBox_m_large.place(x= 50 + 300, y=200 + 5 + 50 + 50)


label = ttk.Label(tab_one, text="Molecular Complex", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5 + 550, y=65 + 30 + 30)
label = ttk.Label(tab_one, text="Intermolecular Distance [float]", font=("Helvetica", "10"), background="#CFDAED")
label.place(x= 5 + 550, y=65 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="R\u2091 = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 20 + 550, y=90 + 20 + 40 + 30)
label = ttk.Label(tab_one, text="\u212B", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 190 + 550, y=90 + 20 + 40 + 30)
txtBox_Re = ttk.Entry(tab_one, width=15)
txtBox_Re.place(x=60 + 550, y=90 + 20 + 40 + 30)


#style = ttk.Style(tab_one)
#style.configure("Placeholder.TEntry", foreground="#d5d5d5", width=10)


# tab_twoに配置するウィジェットの作成
label = ttk.Label(tab_two, text="Matrix size and Potential parameters", font=("Helvetica", "16", "bold"), foreground = "#28487c", background="#CFDAED")
label.place(x= 5, y=5)

label = ttk.Label(tab_two, text="Matrix Size", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5, y=60 - 20)
label = ttk.Label(tab_two, text="[integer]", font=("Helvetica", "10", "normal"), background="#CFDAED")
label.place(x= 110, y=61 - 20)

label = ttk.Label(tab_two, text="n\u2080 = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 10, y=85 - 20)
txtBox_n0 = ttk.Entry(tab_two, width=15)
txtBox_n0.place(x=80, y=85 - 20)
label = ttk.Label(tab_two, text="n\u208A = n\u208B =  ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 10, y=110 - 20)
txtBox_nplsmns = ttk.Entry(tab_two, width=15)
txtBox_nplsmns.place(x=80, y=110 - 20)
label = ttk.Label(tab_two, text="j = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 10, y=135 - 20)
txtBox_j = ttk.Entry(tab_two, width=15)
txtBox_j.place(x=80, y=135 - 20)
label = ttk.Label(tab_two, text="m = ", font=("Times new roman", "10", "italic"), background="#CFDAED")
label.place(x= 10, y=160 - 20)
txtBox_m = ttk.Entry(tab_two, width=15)
txtBox_m.place(x=80, y=160 - 20)

label = ttk.Label(tab_two, text="Eigen Vector Output", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5, y=175)
label = ttk.Label(tab_two, text="[float]", font=("Helvetica", "10", "normal"), background="#CFDAED")
label.place(x= 195, y=176)
label = ttk.Label(tab_two, text="cutoff energy/cm\u207B\u00B9: ", font=("Helvetica", "10", "normal"), background="#CFDAED")
label.place(x= 10, y=200)
txtBox_cutoff_energy = PlaceholderEntry(tab_two, "default: 100", width=10, bg="white")
txtBox_cutoff_energy.place(x=225, y=200)
label = ttk.Label(tab_two, text="cutoff coefficient value: ", font=("Helvetica", "10", "normal"), background="#CFDAED")
label.place(x= 10, y=225)
txtBox_cutoff_coeff = PlaceholderEntry(tab_two, "default: -1", width=10, bg="white")
txtBox_cutoff_coeff.place(x=225, y=225)

label = ttk.Label(tab_two, text="Potential Expansion number", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 5, y=260 + 10)
label = ttk.Label(tab_two, text="LB, Internal rotation: ", font=("Helvetica", "8", "normal"), background="#CFDAED")
label.place(x= 10, y=285 + 10)
#combobox_max_LB = ttk.Combobox(tab_two, values="0  1  2  3  4  5", width = 10, state="readonly", style="office.TCombobox")
#combobox_max_LB.place(x=225, y=285 + 10)
label = ttk.Label(tab_two, text="m_cpl, Angular momentum coupling: ", font=("Helvetica", "8", "normal"), background="#CFDAED")
label.place(x= 10, y=310 + 10)
#combobox_max_mcpl = ttk.Combobox(tab_two, values="0  1  2  3", width = 10, state="readonly", style="office.TCombobox")
#combobox_max_mcpl.place(x=225, y=310 + 10)
label = ttk.Label(tab_two, text="R\u207F, R dependence of Angular term: ", font=("Helvetica", "8", "normal"), background="#CFDAED")
label.place(x= 10, y=335 + 10)
#combobox_max_n = ttk.Combobox(tab_two, values="0  6  8  10", width = 10, state="readonly", style="office.TCombobox")
#combobox_max_n.place(x=225, y=335 + 10)


label = ttk.Label(tab_two, text="Potential Parameter", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 315, y=5 + 35)
label = ttk.Label(tab_two, text="[float]", font=("Helvetica", "10", "normal"), background="#CFDAED")
label.place(x= 505, y=6 + 35)
label = ttk.Label(tab_two, text="Stretch-Bend Parameter", font=("Helvetica", "10", "underline"), background="#CFDAED")
label.place(x= 320, y=30 + 35)
label = ttk.Label(tab_two, text="kzz = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 320, y=50 + 35)
txtBox_kzz = ttk.Entry(tab_two, width=8)
txtBox_kzz.place(x=360, y=50 + 35)
label = ttk.Label(tab_two, text="a = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 430 + 20, y=50 + 35)
txtBox_az = ttk.Entry(tab_two, width=8)
txtBox_az.place(x=460 + 20, y=50 + 35)
label = ttk.Label(tab_two, text="kxx = ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 570, y=50 + 35)
txtBox_kxx = ttk.Entry(tab_two, width=8)
txtBox_kxx.place(x=615, y=50 + 35)
label = ttk.Label(tab_two, text="kxxz = ", font=("Times new roman", "10","normal", "italic"), background="#CFDAED")
label.place(x= 700, y=50 + 35)
txtBox_kxxz = ttk.Entry(tab_two, width=8)
txtBox_kxxz.place(x=750, y=50 + 35)

label = ttk.Label(tab_two, text="Interenal rotation Parameter", font=("Helvetica", "10", "underline"), background="#CFDAED")
label.place(x= 320, y=80 + 35)
label = ttk.Label(tab_two, text="LB ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 390, y=100 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 430, y=100 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 500, y=100 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 570, y=100 + 35)
label = ttk.Label(tab_two, text="3 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 640, y=100 + 35)
label = ttk.Label(tab_two, text="3 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 710, y=100 + 35)
label = ttk.Label(tab_two, text="3 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 780, y=100 + 35)
label = ttk.Label(tab_two, text="4 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 850, y=100 + 35)

label = ttk.Label(tab_two, text="k ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 390, y=125 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 430, y=125 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 500, y=125 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 570, y=125 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 640, y=125 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 710, y=125 + 35)
label = ttk.Label(tab_two, text="3 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 780, y=125 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 850, y=125 + 35)

label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 350, y=120 + 25 + 35)
label = ttk.Label(tab_two, text="R ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=145 + 25 + 35)
label = ttk.Label(tab_two, text="R\u00B2 ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=170 + 25 + 35)
label = ttk.Label(tab_two, text="\u03C1\u00B2 ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=195 + 25 + 35)

LB1 = 400
LB2 = 470
LB3 = 540
LB4 = 610
LB5 = 680
LB6 = 750
LB7 = 820
Rrho0 = 120 + 25 + 35
R1 = 145 + 25 + 35
R2 = 170 + 25 + 35
rho2 = 195 + 25 + 35

txtBox_V001 = PlaceholderEntry(tab_two, "V\u2080\u2080\u00B9", width=8, bg="white")
txtBox_V001.place(x=LB1, y=Rrho0)
txtBox_V002 = PlaceholderEntry(tab_two, "V\u2080\u2080\u00B2", width=8, bg="white")
txtBox_V002.place(x=LB2, y=Rrho0)
txtBox_V202 = PlaceholderEntry(tab_two, "V\u2080\u2082\u00B2", width=8, bg="white")
txtBox_V202.place(x=LB3, y=Rrho0)
txtBox_V003 = PlaceholderEntry(tab_two, "V\u2080\u2080\u00B3", width=8, bg="white")
txtBox_V003.place(x=LB4, y=Rrho0)
txtBox_V203 = PlaceholderEntry(tab_two, "V\u2080\u2082\u00B3", width=8, bg="white")
txtBox_V203.place(x=LB5, y=Rrho0)
txtBox_V303 = PlaceholderEntry(tab_two, "V\u2080\u2083\u00B3", width=8, bg="white")
txtBox_V303.place(x=LB6, y=Rrho0)
txtBox_V004 = PlaceholderEntry(tab_two, "V\u2080\u2080\u2074", width=8, bg="white")
txtBox_V004.place(x=LB7, y=Rrho0)
txtBox_R1V001 = PlaceholderEntry(tab_two, "dR V\u2080\u2080\u00B9", width=8, bg="white")
txtBox_R1V001.place(x=LB1, y=R1)
txtBox_R1V002 = PlaceholderEntry(tab_two, "dR V\u2080\u2080\u00B2", width=8, bg="white")
txtBox_R1V002.place(x=LB2, y=R1)
txtBox_R1V202 = PlaceholderEntry(tab_two, "dR V\u2080\u2082\u00B2", width=8, bg="white")
txtBox_R1V202.place(x=LB3, y=R1)
txtBox_R1V003 = PlaceholderEntry(tab_two, "dR V\u2080\u2080\u00B3", width=8, bg="white")
txtBox_R1V003.place(x=LB4, y=R1)
txtBox_R1V203 = PlaceholderEntry(tab_two, "dR V\u2080\u2082\u00B3", width=8, bg="white")
txtBox_R1V203.place(x=LB5, y=R1)
txtBox_R1V303 = PlaceholderEntry(tab_two, "dR V\u2080\u2083\u00B3", width=8, bg="white")
txtBox_R1V303.place(x=LB6, y=R1)
txtBox_R1V004 = PlaceholderEntry(tab_two, "dR V\u2080\u2080\u2074", width=8, bg="white")
txtBox_R1V004.place(x=LB7, y=R1)
txtBox_R2V001 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2080\u00B9", width=8, bg="white")
txtBox_R2V001.place(x=LB1, y=R2)
txtBox_R2V002 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2080\u00B2", width=8, bg="white")
txtBox_R2V002.place(x=LB2, y=R2)
txtBox_R2V202 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2082\u00B2", width=8, bg="white")
txtBox_R2V202.place(x=LB3, y=R2)
txtBox_R2V003 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2080\u00B3", width=8, bg="white")
txtBox_R2V003.place(x=LB4, y=R2)
txtBox_R2V203 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2082\u00B3", width=8, bg="white")
txtBox_R2V203.place(x=LB5, y=R2)
txtBox_R2V303 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2083\u00B3", width=8, bg="white")
txtBox_R2V303.place(x=LB6, y=R2)
txtBox_R2V004 = PlaceholderEntry(tab_two, "dR\u00B2 V\u2080\u2080\u2074", width=8, bg="white")
txtBox_R2V004.place(x=LB7, y=R2)
txtBox_rho2V001 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2080\u00B9", width=8, bg="white")
txtBox_rho2V001.place(x=LB1, y=rho2)
txtBox_rho2V002 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2080\u00B2", width=8, bg="white")
txtBox_rho2V002.place(x=LB2, y=rho2)
txtBox_rho2V202 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2082\u00B2", width=8, bg="white")
txtBox_rho2V202.place(x=LB3, y=rho2)
txtBox_rho2V003 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2080\u00B3", width=8, bg="white")
txtBox_rho2V003.place(x=LB4, y=rho2)
txtBox_rho2V203 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2082\u00B3", width=8, bg="white")
txtBox_rho2V203.place(x=LB5, y=rho2)
txtBox_rho2V303 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2083\u00B3", width=8, bg="white")
txtBox_rho2V303.place(x=LB6, y=rho2)
txtBox_rho2V004 = PlaceholderEntry(tab_two, "d\u03C1\u00B2 V\u2080\u2080\u2074", width=8, bg="white")
txtBox_rho2V004.place(x=LB7, y=rho2)


label = ttk.Label(tab_two, text="Angular momentum Parameter", font=("Helvetica", "10", "underline"), background="#CFDAED")
label.place(x= 320, y=220 + 30 + 35)
label = ttk.Label(tab_two, text="LB ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 380, y=240 + 30 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 430, y=240 + 30 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 535, y=240 + 30 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 675, y=240 + 30 + 35)
label = ttk.Label(tab_two, text="3 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 815, y=240 + 30 + 35)
label = ttk.Label(tab_two, text="k ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 380, y=240 + 55 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 430, y=240 + 55 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 535, y=240 + 55 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 675, y=240 + 55 + 35)
label = ttk.Label(tab_two, text="0 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 815, y=240 + 55 + 35)
label = ttk.Label(tab_two, text="m_cpl ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 380, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 430, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 500, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 570, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 640, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 710, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="1 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 780, y=260 + 55 + 35)
label = ttk.Label(tab_two, text="2 ", font=("Times new roman", "10", "normal"), background="#CFDAED")
label.place(x= 850, y=260 + 55 + 35)

label = ttk.Label(tab_two, text="R\u2070" , font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=280 + 55 + 35)
label = ttk.Label(tab_two, text="R\u207B\u2076 ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=305 + 55 + 35)
label = ttk.Label(tab_two, text="R\u207B\u2078 ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=330 + 55 + 35)
label = ttk.Label(tab_two, text="R\u207B\u2071\u2070 ", font=("Times new roman", "10", "normal", "italic"), background="#CFDAED")
label.place(x= 350, y=355 + 55 + 35)

LB1K0mcpl1 = 400
LB2K0mcpl1 = 470
LB2K0mcpl2 = 540
LB2K1mcpl1 = 610
LB2K1mcpl2 = 680
LB3K0mcpl1 = 750
LB3K0mcpl2 = 820
R0 = 280 + 55 + 35
R6 = 305 + 55 + 35
R8 = 330 + 55 + 35
R10 = 355 + 55 + 35

txtBox_V011_0 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B9", width=8, bg="white")
txtBox_V011_0.place(x=LB1K0mcpl1, y=R0)
txtBox_V012_0 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B2", width=8, bg="white")
txtBox_V012_0.place(x=LB2K0mcpl1, y=R0)
txtBox_V022_0 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B2", width=8, bg="white")
txtBox_V022_0.place(x=LB2K0mcpl2, y=R0)
txtBox_V212_0 = PlaceholderEntry(tab_two, "V\u2081\u2082\u00B2", width=8, bg="white")
txtBox_V212_0.place(x=LB2K1mcpl1, y=R0)
txtBox_V222_0 = PlaceholderEntry(tab_two, "V\u2082\u2082\u00B2", width=8, bg="white")
txtBox_V222_0.place(x=LB2K1mcpl2, y=R0)
txtBox_V013_0 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B3", width=8, bg="white")
txtBox_V013_0.place(x=LB3K0mcpl1, y=R0)
txtBox_V023_0 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B3", width=8, bg="white")
txtBox_V023_0.place(x=LB3K0mcpl2, y=R0)
txtBox_V011_6 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B9 R\u207B\u2076", width=8, bg="white")
txtBox_V011_6.place(x=LB1K0mcpl1, y=R6)
txtBox_V012_6 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B2 R\u207B\u2076", width=8, bg="white")
txtBox_V012_6.place(x=LB2K0mcpl1, y=R6)
txtBox_V022_6 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B2 R\u207B\u2076", width=8, bg="white")
txtBox_V022_6.place(x=LB2K0mcpl2, y=R6)
txtBox_V212_6 = PlaceholderEntry(tab_two, "V\u2081\u2082\u00B2 R\u207B\u2076", width=8, bg="white")
txtBox_V212_6.place(x=LB2K1mcpl1, y=R6)
txtBox_V222_6 = PlaceholderEntry(tab_two, "V\u2082\u2082\u00B2 R\u207B\u2076", width=8, bg="white")
txtBox_V222_6.place(x=LB2K1mcpl2, y=R6)
txtBox_V013_6 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B3 R\u207B\u2076", width=8, bg="white")
txtBox_V013_6.place(x=LB3K0mcpl1, y=R6)
txtBox_V023_6 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B3 R\u207B\u2076", width=8, bg="white")
txtBox_V023_6.place(x=LB3K0mcpl2, y=R6)
txtBox_V011_8 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B9 R\u207B\u2078", width=8, bg="white")
txtBox_V011_8.place(x=LB1K0mcpl1, y=R8)
txtBox_V012_8 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B2 R\u207B\u2078", width=8, bg="white")
txtBox_V012_8.place(x=LB2K0mcpl1, y=R8)
txtBox_V022_8 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B2 R\u207B\u2078", width=8, bg="white")
txtBox_V022_8.place(x=LB2K0mcpl2, y=R8)
txtBox_V212_8 = PlaceholderEntry(tab_two, "V\u2081\u2082\u00B2 R\u207B\u2078", width=8, bg="white")
txtBox_V212_8.place(x=LB2K1mcpl1, y=R8)
txtBox_V222_8 = PlaceholderEntry(tab_two, "V\u2082\u2082\u00B2 R\u207B\u2078", width=8, bg="white")
txtBox_V222_8.place(x=LB2K1mcpl2, y=R8)
txtBox_V013_8 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B3 R\u207B\u2078", width=8, bg="white")
txtBox_V013_8.place(x=LB3K0mcpl1, y=R8)
txtBox_V023_8 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B3 R\u207B\u2078", width=8, bg="white")
txtBox_V023_8.place(x=LB3K0mcpl2, y=R8)
txtBox_V011_10 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B9 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V011_10.place(x=LB1K0mcpl1, y=R10)
txtBox_V012_10 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B2 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V012_10.place(x=LB2K0mcpl1, y=R10)
txtBox_V022_10 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B2 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V022_10.place(x=LB2K0mcpl2, y=R10)
txtBox_V212_10 = PlaceholderEntry(tab_two, "V\u2081\u2082\u00B2 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V212_10.place(x=LB2K1mcpl1, y=R10)
txtBox_V222_10 = PlaceholderEntry(tab_two, "V\u2082\u2082\u00B2 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V222_10.place(x=LB2K1mcpl2, y=R10)
txtBox_V013_10 = PlaceholderEntry(tab_two, "V\u2081\u2080\u00B3 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V013_10.place(x=LB3K0mcpl1, y=R10)
txtBox_V023_10 = PlaceholderEntry(tab_two, "V\u2082\u2080\u00B3 R\u207B\u00B9\u2070", width=8, bg="white")
txtBox_V023_10.place(x=LB3K0mcpl2, y=R10)


#mcpl cover
label_cover_V101_0_mcpl = PlaceholderEntry(tab_two, "V_10^1", width=8, bg="gray", state="readonly")
label_cover_V102_0_mcpl = PlaceholderEntry(tab_two, "V_10^2", width=8, bg="gray", state="readonly")
label_cover_V202_0_mcpl = PlaceholderEntry(tab_two, "V_20^2", width=8, bg="gray", state="readonly")
label_cover_V112_0_mcpl = PlaceholderEntry(tab_two, "V_11^2", width=8, bg="gray", state="readonly")
label_cover_V212_0_mcpl = PlaceholderEntry(tab_two, "V_21^2", width=8, bg="gray", state="readonly")
label_cover_V103_0_mcpl = PlaceholderEntry(tab_two, "V_10^3", width=8, bg="gray", state="readonly")
label_cover_V203_0_mcpl = PlaceholderEntry(tab_two, "V_20^3", width=8, bg="gray", state="readonly")
label_cover_V101_6_mcpl = PlaceholderEntry(tab_two, "V_10^1_R6", width=8, bg="gray", state="readonly")
label_cover_V102_6_mcpl = PlaceholderEntry(tab_two, "V_10^2_R6", width=8, bg="gray", state="readonly")
label_cover_V202_6_mcpl = PlaceholderEntry(tab_two, "V_20^2_R6", width=8, bg="gray", state="readonly")
label_cover_V112_6_mcpl = PlaceholderEntry(tab_two, "V_11^2_R6", width=8, bg="gray", state="readonly")
label_cover_V212_6_mcpl = PlaceholderEntry(tab_two, "V_21^2_R6", width=8, bg="gray", state="readonly")
label_cover_V103_6_mcpl = PlaceholderEntry(tab_two, "V_10^3_R6", width=8, bg="gray", state="readonly")
label_cover_V203_6_mcpl = PlaceholderEntry(tab_two, "V_20^3_R6", width=8, bg="gray", state="readonly")
label_cover_V101_8_mcpl = PlaceholderEntry(tab_two, "V_10^1_R8", width=8, bg="gray", state="readonly")
label_cover_V102_8_mcpl = PlaceholderEntry(tab_two, "V_10^2_R8", width=8, bg="gray", state="readonly")
label_cover_V202_8_mcpl = PlaceholderEntry(tab_two, "V_20^2_R8", width=8, bg="gray", state="readonly")
label_cover_V112_8_mcpl = PlaceholderEntry(tab_two, "V_11^2_R8", width=8, bg="gray", state="readonly")
label_cover_V212_8_mcpl = PlaceholderEntry(tab_two, "V_21^2_R8", width=8, bg="gray", state="readonly")
label_cover_V103_8_mcpl = PlaceholderEntry(tab_two, "V_10^3_R8", width=8, bg="gray", state="readonly")
label_cover_V203_8_mcpl = PlaceholderEntry(tab_two, "V_20^3_R8", width=8, bg="gray", state="readonly")
label_cover_V101_10_mcpl = PlaceholderEntry(tab_two, "V_10^1_R10", width=8, bg="gray", state="readonly")
label_cover_V102_10_mcpl = PlaceholderEntry(tab_two, "V_10^2_R10", width=8, bg="gray", state="readonly")
label_cover_V202_10_mcpl = PlaceholderEntry(tab_two, "V_20^2_R10", width=8, bg="gray", state="readonly")
label_cover_V112_10_mcpl = PlaceholderEntry(tab_two, "V_11^2_R10", width=8, bg="gray", state="readonly")
label_cover_V212_10_mcpl = PlaceholderEntry(tab_two, "V_21^2_R10", width=8, bg="gray", state="readonly")
label_cover_V103_10_mcpl = PlaceholderEntry(tab_two, "V_10^3_R10", width=8, bg="gray", state="readonly")
label_cover_V203_10_mcpl = PlaceholderEntry(tab_two, "V_20^3_R10", width=8, bg="gray", state="readonly")
def feedback_mcpl(event):
    if combobox_max_mcpl.get() == "":
        return
    elif combobox_max_mcpl.get() == "0":
        label_cover_V101_0_mcpl.place(x=LB1K0mcpl1, y=R0)
        label_cover_V102_0_mcpl.place(x=LB2K0mcpl1, y=R0)
        label_cover_V202_0_mcpl.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_mcpl.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_mcpl.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_mcpl.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_mcpl.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_mcpl.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_mcpl.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_mcpl.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_mcpl.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_mcpl.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_mcpl.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_mcpl.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_mcpl.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_mcpl.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_mcpl.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_mcpl.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_mcpl.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_mcpl.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_mcpl.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_mcpl.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_mcpl.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_mcpl.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_mcpl.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_mcpl.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_mcpl.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_mcpl.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_mcpl.get() == "1":
        label_cover_V101_0_mcpl.place(x=10000, y=10000)
        label_cover_V102_0_mcpl.place(x=10000, y=10000)
        label_cover_V202_0_mcpl.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_mcpl.place(x=10000, y=10000)
        label_cover_V212_0_mcpl.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_mcpl.place(x=10000, y=10000)
        label_cover_V203_0_mcpl.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_mcpl.place(x=10000, y=10000)
        label_cover_V102_6_mcpl.place(x=10000, y=10000)
        label_cover_V202_6_mcpl.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_mcpl.place(x=10000, y=10000)
        label_cover_V212_6_mcpl.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_mcpl.place(x=10000, y=10000)
        label_cover_V203_6_mcpl.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_mcpl.place(x=10000, y=10000)
        label_cover_V102_8_mcpl.place(x=10000, y=10000)
        label_cover_V202_8_mcpl.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_mcpl.place(x=10000, y=10000)
        label_cover_V212_8_mcpl.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_mcpl.place(x=10000, y=10000)
        label_cover_V203_8_mcpl.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_mcpl.place(x=10000, y=10000)
        label_cover_V102_10_mcpl.place(x=10000, y=10000)
        label_cover_V202_10_mcpl.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_mcpl.place(x=10000, y=10000)
        label_cover_V212_10_mcpl.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_mcpl.place(x=10000, y=10000)
        label_cover_V203_10_mcpl.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_mcpl.get() == "2" or "3":
        label_cover_V101_0_mcpl.place(x=10000, y=10000)
        label_cover_V102_0_mcpl.place(x=10000, y=10000)
        label_cover_V202_0_mcpl.place(x=10000, y=10000)
        label_cover_V112_0_mcpl.place(x=10000, y=10000)
        label_cover_V212_0_mcpl.place(x=10000, y=10000)
        label_cover_V103_0_mcpl.place(x=10000, y=10000)
        label_cover_V203_0_mcpl.place(x=10000, y=10000)
        label_cover_V101_6_mcpl.place(x=10000, y=10000)
        label_cover_V102_6_mcpl.place(x=10000, y=10000)
        label_cover_V202_6_mcpl.place(x=10000, y=10000)
        label_cover_V112_6_mcpl.place(x=10000, y=10000)
        label_cover_V212_6_mcpl.place(x=10000, y=10000)
        label_cover_V103_6_mcpl.place(x=10000, y=10000)
        label_cover_V203_6_mcpl.place(x=10000, y=10000)
        label_cover_V101_8_mcpl.place(x=10000, y=10000)
        label_cover_V102_8_mcpl.place(x=10000, y=10000)
        label_cover_V202_8_mcpl.place(x=10000, y=10000)
        label_cover_V112_8_mcpl.place(x=10000, y=10000)
        label_cover_V212_8_mcpl.place(x=10000, y=10000)
        label_cover_V103_8_mcpl.place(x=10000, y=10000)
        label_cover_V203_8_mcpl.place(x=10000, y=10000)
        label_cover_V101_10_mcpl.place(x=10000, y=10000)
        label_cover_V102_10_mcpl.place(x=10000, y=10000)
        label_cover_V202_10_mcpl.place(x=10000, y=10000)
        label_cover_V112_10_mcpl.place(x=10000, y=10000)
        label_cover_V212_10_mcpl.place(x=10000, y=10000)
        label_cover_V103_10_mcpl.place(x=10000, y=10000)
        label_cover_V203_10_mcpl.place(x=10000, y=10000)



#n cover
label_cover_V101_0_n = PlaceholderEntry(tab_two, "V_10^1", width=8, bg="gray", state="readonly")
label_cover_V102_0_n = PlaceholderEntry(tab_two, "V_10^2", width=8, bg="gray", state="readonly")
label_cover_V202_0_n = PlaceholderEntry(tab_two, "V_20^2", width=8, bg="gray", state="readonly")
label_cover_V112_0_n = PlaceholderEntry(tab_two, "V_11^2", width=8, bg="gray", state="readonly")
label_cover_V212_0_n = PlaceholderEntry(tab_two, "V_21^2", width=8, bg="gray", state="readonly")
label_cover_V103_0_n = PlaceholderEntry(tab_two, "V_10^3", width=8, bg="gray", state="readonly")
label_cover_V203_0_n = PlaceholderEntry(tab_two, "V_20^3", width=8, bg="gray", state="readonly")
label_cover_V101_6_n = PlaceholderEntry(tab_two, "V_10^1_R6", width=8, bg="gray", state="readonly")
label_cover_V102_6_n = PlaceholderEntry(tab_two, "V_10^2_R6", width=8, bg="gray", state="readonly")
label_cover_V202_6_n = PlaceholderEntry(tab_two, "V_20^2_R6", width=8, bg="gray", state="readonly")
label_cover_V112_6_n = PlaceholderEntry(tab_two, "V_11^2_R6", width=8, bg="gray", state="readonly")
label_cover_V212_6_n = PlaceholderEntry(tab_two, "V_21^2_R6", width=8, bg="gray", state="readonly")
label_cover_V103_6_n = PlaceholderEntry(tab_two, "V_10^3_R6", width=8, bg="gray", state="readonly")
label_cover_V203_6_n = PlaceholderEntry(tab_two, "V_20^3_R6", width=8, bg="gray", state="readonly")
label_cover_V101_8_n = PlaceholderEntry(tab_two, "V_10^1_R8", width=8, bg="gray", state="readonly")
label_cover_V102_8_n = PlaceholderEntry(tab_two, "V_10^2_R8", width=8, bg="gray", state="readonly")
label_cover_V202_8_n = PlaceholderEntry(tab_two, "V_20^2_R8", width=8, bg="gray", state="readonly")
label_cover_V112_8_n = PlaceholderEntry(tab_two, "V_11^2_R8", width=8, bg="gray", state="readonly")
label_cover_V212_8_n = PlaceholderEntry(tab_two, "V_21^2_R8", width=8, bg="gray", state="readonly")
label_cover_V103_8_n = PlaceholderEntry(tab_two, "V_10^3_R8", width=8, bg="gray", state="readonly")
label_cover_V203_8_n = PlaceholderEntry(tab_two, "V_20^3_R8", width=8, bg="gray", state="readonly")
label_cover_V101_10_n = PlaceholderEntry(tab_two, "V_10^1_R10", width=8, bg="gray", state="readonly")
label_cover_V102_10_n = PlaceholderEntry(tab_two, "V_10^2_R10", width=8, bg="gray", state="readonly")
label_cover_V202_10_n = PlaceholderEntry(tab_two, "V_20^2_R10", width=8, bg="gray", state="readonly")
label_cover_V112_10_n = PlaceholderEntry(tab_two, "V_11^2_R10", width=8, bg="gray", state="readonly")
label_cover_V212_10_n = PlaceholderEntry(tab_two, "V_21^2_R10", width=8, bg="gray", state="readonly")
label_cover_V103_10_n = PlaceholderEntry(tab_two, "V_10^3_R10", width=8, bg="gray", state="readonly")
label_cover_V203_10_n = PlaceholderEntry(tab_two, "V_20^3_R10", width=8, bg="gray", state="readonly")
def feedback_n(event):
    if combobox_max_n.get() == "":
        return
    elif combobox_max_n.get() == "0":
        label_cover_V101_6_n.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_n.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_n.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_n.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_n.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_n.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_n.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_n.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_n.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_n.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_n.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_n.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_n.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_n.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_n.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_n.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_n.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_n.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_n.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_n.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_n.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_n.get() == "6":
        label_cover_V101_6_n.place(x=10000, y=10000)
        label_cover_V102_6_n.place(x=10000, y=10000)
        label_cover_V202_6_n.place(x=10000, y=10000)
        label_cover_V112_6_n.place(x=10000, y=10000)
        label_cover_V212_6_n.place(x=10000, y=10000)
        label_cover_V103_6_n.place(x=10000, y=10000)
        label_cover_V203_6_n.place(x=10000, y=10000)
        label_cover_V101_8_n.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_n.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_n.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_n.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_n.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_n.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_n.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_n.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_n.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_n.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_n.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_n.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_n.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_n.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_n.get() == "8":
        label_cover_V101_6_n.place(x=10000, y=10000)
        label_cover_V102_6_n.place(x=10000, y=10000)
        label_cover_V202_6_n.place(x=10000, y=10000)
        label_cover_V112_6_n.place(x=10000, y=10000)
        label_cover_V212_6_n.place(x=10000, y=10000)
        label_cover_V103_6_n.place(x=10000, y=10000)
        label_cover_V203_6_n.place(x=10000, y=10000)
        label_cover_V101_8_n.place(x=10000, y=10000)
        label_cover_V102_8_n.place(x=10000, y=10000)
        label_cover_V202_8_n.place(x=10000, y=10000)
        label_cover_V112_8_n.place(x=10000, y=10000)
        label_cover_V212_8_n.place(x=10000, y=10000)
        label_cover_V103_8_n.place(x=10000, y=10000)
        label_cover_V203_8_n.place(x=10000, y=10000)
        label_cover_V101_10_n.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_n.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_n.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_n.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_n.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_n.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_n.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_n.get() == "10":
        label_cover_V101_6_n.place(x=10000, y=10000)
        label_cover_V102_6_n.place(x=10000, y=10000)
        label_cover_V202_6_n.place(x=10000, y=10000)
        label_cover_V112_6_n.place(x=10000, y=10000)
        label_cover_V212_6_n.place(x=10000, y=10000)
        label_cover_V103_6_n.place(x=10000, y=10000)
        label_cover_V203_6_n.place(x=10000, y=10000)
        label_cover_V101_8_n.place(x=10000, y=10000)
        label_cover_V102_8_n.place(x=10000, y=10000)
        label_cover_V202_8_n.place(x=10000, y=10000)
        label_cover_V112_8_n.place(x=10000, y=10000)
        label_cover_V212_8_n.place(x=10000, y=10000)
        label_cover_V103_8_n.place(x=10000, y=10000)
        label_cover_V203_8_n.place(x=10000, y=10000)
        label_cover_V101_10_n.place(x=10000, y=10000)
        label_cover_V102_10_n.place(x=10000, y=10000)
        label_cover_V202_10_n.place(x=10000, y=10000)
        label_cover_V112_10_n.place(x=10000, y=10000)
        label_cover_V212_10_n.place(x=10000, y=10000)
        label_cover_V103_10_n.place(x=10000, y=10000)
        label_cover_V203_10_n.place(x=10000, y=10000)

#LB cover
label_cover_V001_LB = PlaceholderEntry(tab_two, "V_0^1", width=8, bg="gray", state="readonly")
label_cover_V002_LB = PlaceholderEntry(tab_two, "V_0^2", width=8, bg="gray", state="readonly")
label_cover_V022_LB = PlaceholderEntry(tab_two, "V_2^2", width=8, bg="gray", state="readonly")
label_cover_V003_LB = PlaceholderEntry(tab_two, "V_0^3", width=8, bg="gray", state="readonly")
label_cover_V023_LB = PlaceholderEntry(tab_two, "V_2^3", width=8, bg="gray", state="readonly")
label_cover_V033_LB = PlaceholderEntry(tab_two, "V_3^3", width=8, bg="gray", state="readonly")
label_cover_V004_LB = PlaceholderEntry(tab_two, "V_0^4", width=8, bg="gray", state="readonly")
label_cover_R1V001_LB = PlaceholderEntry(tab_two, "partial_R V_0^1", width=8, bg="gray", state="readonly")
label_cover_R1V002_LB = PlaceholderEntry(tab_two, "partial_R V_0^2", width=8, bg="gray", state="readonly")
label_cover_R1V022_LB = PlaceholderEntry(tab_two, "partial_R V_2^2", width=8, bg="gray", state="readonly")
label_cover_R1V003_LB = PlaceholderEntry(tab_two, "partial_R V_0^3", width=8, bg="gray", state="readonly")
label_cover_R1V023_LB = PlaceholderEntry(tab_two, "partial_R V_2^3", width=8, bg="gray", state="readonly")
label_cover_R1V033_LB = PlaceholderEntry(tab_two, "partial_R V_3^3", width=8, bg="gray", state="readonly")
label_cover_R1V004_LB = PlaceholderEntry(tab_two, "partial_R V_0^4", width=8, bg="gray", state="readonly")
label_cover_R2V001_LB = PlaceholderEntry(tab_two, "partial_R^2 V_0^1", width=8, bg="gray", state="readonly")
label_cover_R2V002_LB = PlaceholderEntry(tab_two, "partial_R^2 V_0^2", width=8, bg="gray", state="readonly")
label_cover_R2V022_LB = PlaceholderEntry(tab_two, "partial_R^2 V_2^2", width=8, bg="gray", state="readonly")
label_cover_R2V003_LB = PlaceholderEntry(tab_two, "partial_R^2 V_0^3", width=8, bg="gray", state="readonly")
label_cover_R2V023_LB = PlaceholderEntry(tab_two, "partial_R^2 V_2^3", width=8, bg="gray", state="readonly")
label_cover_R2V033_LB = PlaceholderEntry(tab_two, "partial_R^2 V_3^3", width=8, bg="gray", state="readonly")
label_cover_R2V004_LB = PlaceholderEntry(tab_two, "partial_R^2 V_0^4", width=8, bg="gray", state="readonly")
label_cover_rho2V001_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_0^1", width=8, bg="gray", state="readonly")
label_cover_rho2V002_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_0^2", width=8, bg="gray", state="readonly")
label_cover_rho2V022_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_2^2", width=8, bg="gray", state="readonly")
label_cover_rho2V003_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_0^3", width=8, bg="gray", state="readonly")
label_cover_rho2V023_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_2^3", width=8, bg="gray", state="readonly")
label_cover_rho2V033_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_3^3", width=8, bg="gray", state="readonly")
label_cover_rho2V004_LB = PlaceholderEntry(tab_two, "partial_rho^2 V_0^4", width=8, bg="gray", state="readonly")

label_cover_V101_0_LB = PlaceholderEntry(tab_two, "V_10^1", width=8, bg="gray", state="readonly")
label_cover_V102_0_LB = PlaceholderEntry(tab_two, "V_10^2", width=8, bg="gray", state="readonly")
label_cover_V202_0_LB = PlaceholderEntry(tab_two, "V_20^2", width=8, bg="gray", state="readonly")
label_cover_V112_0_LB = PlaceholderEntry(tab_two, "V_11^2", width=8, bg="gray", state="readonly")
label_cover_V212_0_LB = PlaceholderEntry(tab_two, "V_21^2", width=8, bg="gray", state="readonly")
label_cover_V103_0_LB = PlaceholderEntry(tab_two, "V_10^3", width=8, bg="gray", state="readonly")
label_cover_V203_0_LB = PlaceholderEntry(tab_two, "V_20^3", width=8, bg="gray", state="readonly")
label_cover_V101_6_LB = PlaceholderEntry(tab_two, "V_10^1_R6", width=8, bg="gray", state="readonly")
label_cover_V102_6_LB = PlaceholderEntry(tab_two, "V_10^2_R6", width=8, bg="gray", state="readonly")
label_cover_V202_6_LB = PlaceholderEntry(tab_two, "V_20^2_R6", width=8, bg="gray", state="readonly")
label_cover_V112_6_LB = PlaceholderEntry(tab_two, "V_11^2_R6", width=8, bg="gray", state="readonly")
label_cover_V212_6_LB = PlaceholderEntry(tab_two, "V_21^2_R6", width=8, bg="gray", state="readonly")
label_cover_V103_6_LB = PlaceholderEntry(tab_two, "V_10^3_R6", width=8, bg="gray", state="readonly")
label_cover_V203_6_LB = PlaceholderEntry(tab_two, "V_20^3_R6", width=8, bg="gray", state="readonly")
label_cover_V101_8_LB = PlaceholderEntry(tab_two, "V_10^1_R8", width=8, bg="gray", state="readonly")
label_cover_V102_8_LB = PlaceholderEntry(tab_two, "V_10^2_R8", width=8, bg="gray", state="readonly")
label_cover_V202_8_LB = PlaceholderEntry(tab_two, "V_20^2_R8", width=8, bg="gray", state="readonly")
label_cover_V112_8_LB = PlaceholderEntry(tab_two, "V_11^2_R8", width=8, bg="gray", state="readonly")
label_cover_V212_8_LB = PlaceholderEntry(tab_two, "V_21^2_R8", width=8, bg="gray", state="readonly")
label_cover_V103_8_LB = PlaceholderEntry(tab_two, "V_10^3_R8", width=8, bg="gray", state="readonly")
label_cover_V203_8_LB = PlaceholderEntry(tab_two, "V_20^3_R8", width=8, bg="gray", state="readonly")
label_cover_V101_10_LB = PlaceholderEntry(tab_two, "V_10^1_R10", width=8, bg="gray", state="readonly")
label_cover_V102_10_LB = PlaceholderEntry(tab_two, "V_10^2_R10", width=8, bg="gray", state="readonly")
label_cover_V202_10_LB = PlaceholderEntry(tab_two, "V_20^2_R10", width=8, bg="gray", state="readonly")
label_cover_V112_10_LB = PlaceholderEntry(tab_two, "V_11^2_R10", width=8, bg="gray", state="readonly")
label_cover_V212_10_LB = PlaceholderEntry(tab_two, "V_21^2_R10", width=8, bg="gray", state="readonly")
label_cover_V103_10_LB = PlaceholderEntry(tab_two, "V_10^3_R10", width=8, bg="gray", state="readonly")
label_cover_V203_10_LB = PlaceholderEntry(tab_two, "V_20^3_R10", width=8, bg="gray", state="readonly")
def feedback_LB(event): #symmetryの条件も入れるべき
    if combobox_max_LB.get() == "":
        return
    elif combobox_max_LB.get() == "0":
        label_cover_V001_LB.place(x=LB1, y=Rrho0)
        label_cover_V002_LB.place(x=LB2, y=Rrho0)
        label_cover_V022_LB.place(x=LB3, y=Rrho0)
        label_cover_V003_LB.place(x=LB4, y=Rrho0)
        label_cover_V023_LB.place(x=LB5, y=Rrho0)
        label_cover_V033_LB.place(x=LB6, y=Rrho0)
        label_cover_V004_LB.place(x=LB7, y=Rrho0)
        label_cover_R1V001_LB.place(x=LB1, y=R1)
        label_cover_R1V002_LB.place(x=LB2, y=R1)
        label_cover_R1V022_LB.place(x=LB3, y=R1)
        label_cover_R1V003_LB.place(x=LB4, y=R1)
        label_cover_R1V023_LB.place(x=LB5, y=R1)
        label_cover_R1V033_LB.place(x=LB6, y=R1)
        label_cover_R1V004_LB.place(x=LB7, y=R1)
        label_cover_R2V001_LB.place(x=LB1, y=R2)
        label_cover_R2V002_LB.place(x=LB2, y=R2)
        label_cover_R2V022_LB.place(x=LB3, y=R2)
        label_cover_R2V003_LB.place(x=LB4, y=R2)
        label_cover_R2V023_LB.place(x=LB5, y=R2)
        label_cover_R2V033_LB.place(x=LB6, y=R2)
        label_cover_R2V004_LB.place(x=LB7, y=R2)
        label_cover_rho2V001_LB.place(x=LB1, y=rho2)
        label_cover_rho2V002_LB.place(x=LB2, y=rho2)
        label_cover_rho2V022_LB.place(x=LB3, y=rho2)
        label_cover_rho2V003_LB.place(x=LB4, y=rho2)
        label_cover_rho2V023_LB.place(x=LB5, y=rho2)
        label_cover_rho2V033_LB.place(x=LB6, y=rho2)
        label_cover_rho2V004_LB.place(x=LB7, y=rho2)

        label_cover_V101_0_LB.place(x=LB1K0mcpl1, y=R0)
        label_cover_V102_0_LB.place(x=LB2K0mcpl1, y=R0)
        label_cover_V202_0_LB.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_LB.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_LB.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_LB.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_LB.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_LB.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_LB.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_LB.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_LB.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_LB.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_LB.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_LB.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_LB.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_LB.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_LB.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_LB.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_LB.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_LB.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_LB.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_LB.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_LB.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_LB.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_LB.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_LB.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_LB.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_LB.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_LB.get() == "1":
        label_cover_V001_LB.place(x=10000, y=10000)
        label_cover_V002_LB.place(x=LB2, y=Rrho0)
        label_cover_V022_LB.place(x=LB3, y=Rrho0)
        label_cover_V003_LB.place(x=LB4, y=Rrho0)
        label_cover_V023_LB.place(x=LB5, y=Rrho0)
        label_cover_V033_LB.place(x=LB6, y=Rrho0)
        label_cover_V004_LB.place(x=LB7, y=Rrho0)
        label_cover_R1V001_LB.place(x=10000, y=10000)
        label_cover_R1V002_LB.place(x=LB2, y=R1)
        label_cover_R1V022_LB.place(x=LB3, y=R1)
        label_cover_R1V003_LB.place(x=LB4, y=R1)
        label_cover_R1V023_LB.place(x=LB5, y=R1)
        label_cover_R1V033_LB.place(x=LB6, y=R1)
        label_cover_R1V004_LB.place(x=LB7, y=R1)
        label_cover_R2V001_LB.place(x=10000, y=10000)
        label_cover_R2V002_LB.place(x=LB2, y=R2)
        label_cover_R2V022_LB.place(x=LB3, y=R2)
        label_cover_R2V003_LB.place(x=LB4, y=R2)
        label_cover_R2V023_LB.place(x=LB5, y=R2)
        label_cover_R2V033_LB.place(x=LB6, y=R2)
        label_cover_R2V004_LB.place(x=LB7, y=R2)
        label_cover_rho2V001_LB.place(x=10000, y=10000)
        label_cover_rho2V002_LB.place(x=LB2, y=rho2)
        label_cover_rho2V022_LB.place(x=LB3, y=rho2)
        label_cover_rho2V003_LB.place(x=LB4, y=rho2)
        label_cover_rho2V023_LB.place(x=LB5, y=rho2)
        label_cover_rho2V033_LB.place(x=LB6, y=rho2)
        label_cover_rho2V004_LB.place(x=LB7, y=rho2)

        label_cover_V101_0_LB.place(x=10000, y=10000)
        label_cover_V102_0_LB.place(x=LB2K0mcpl1, y=R0)
        label_cover_V202_0_LB.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_LB.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_LB.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_LB.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_LB.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_LB.place(x=10000, y=10000)
        label_cover_V102_6_LB.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_LB.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_LB.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_LB.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_LB.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_LB.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_LB.place(x=10000, y=10000)
        label_cover_V102_8_LB.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_LB.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_LB.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_LB.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_LB.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_LB.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_LB.place(x=10000, y=10000)
        label_cover_V102_10_LB.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_LB.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_LB.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_LB.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_LB.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_LB.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_LB.get() == "2":
        label_cover_V001_LB.place(x=10000, y=10000)
        label_cover_V002_LB.place(x=10000, y=10000)
        label_cover_V022_LB.place(x=10000, y=10000)
        label_cover_V003_LB.place(x=LB4, y=Rrho0)
        label_cover_V023_LB.place(x=LB5, y=Rrho0)
        label_cover_V033_LB.place(x=LB6, y=Rrho0)
        label_cover_V004_LB.place(x=LB7, y=Rrho0)
        label_cover_R1V001_LB.place(x=10000, y=10000)
        label_cover_R1V002_LB.place(x=10000, y=10000)
        label_cover_R1V022_LB.place(x=10000, y=10000)
        label_cover_R1V003_LB.place(x=LB4, y=R1)
        label_cover_R1V023_LB.place(x=LB5, y=R1)
        label_cover_R1V033_LB.place(x=LB6, y=R1)
        label_cover_R1V004_LB.place(x=LB7, y=R1)
        label_cover_R2V001_LB.place(x=10000, y=10000)
        label_cover_R2V002_LB.place(x=10000, y=10000)
        label_cover_R2V022_LB.place(x=10000, y=10000)
        label_cover_R2V003_LB.place(x=LB4, y=R2)
        label_cover_R2V023_LB.place(x=LB5, y=R2)
        label_cover_R2V033_LB.place(x=LB6, y=R2)
        label_cover_R2V004_LB.place(x=LB7, y=R2)
        label_cover_rho2V001_LB.place(x=10000, y=10000)
        label_cover_rho2V002_LB.place(x=10000, y=10000)
        label_cover_rho2V022_LB.place(x=10000, y=10000)
        label_cover_rho2V003_LB.place(x=LB4, y=rho2)
        label_cover_rho2V023_LB.place(x=LB5, y=rho2)
        label_cover_rho2V033_LB.place(x=LB6, y=rho2)
        label_cover_rho2V004_LB.place(x=LB7, y=rho2)

        label_cover_V101_0_LB.place(x=10000, y=10000)
        label_cover_V102_0_LB.place(x=10000, y=10000)
        label_cover_V202_0_LB.place(x=10000, y=10000)
        label_cover_V112_0_LB.place(x=10000, y=10000)
        label_cover_V212_0_LB.place(x=10000, y=10000)
        label_cover_V103_0_LB.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_LB.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_LB.place(x=10000, y=10000)
        label_cover_V102_6_LB.place(x=10000, y=10000)
        label_cover_V202_6_LB.place(x=10000, y=10000)
        label_cover_V112_6_LB.place(x=10000, y=10000)
        label_cover_V212_6_LB.place(x=10000, y=10000)
        label_cover_V103_6_LB.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_LB.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_LB.place(x=10000, y=10000)
        label_cover_V102_8_LB.place(x=10000, y=10000)
        label_cover_V202_8_LB.place(x=10000, y=10000)
        label_cover_V112_8_LB.place(x=10000, y=10000)
        label_cover_V212_8_LB.place(x=10000, y=10000)
        label_cover_V103_8_LB.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_LB.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_LB.place(x=10000, y=10000)
        label_cover_V102_10_LB.place(x=10000, y=10000)
        label_cover_V202_10_LB.place(x=10000, y=10000)
        label_cover_V112_10_LB.place(x=10000, y=10000)
        label_cover_V212_10_LB.place(x=10000, y=10000)
        label_cover_V103_10_LB.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_LB.place(x=LB3K0mcpl2, y=R10)
    elif combobox_max_LB.get() == "3":
        label_cover_V001_LB.place(x=10000, y=10000)
        label_cover_V002_LB.place(x=10000, y=10000)
        label_cover_V022_LB.place(x=10000, y=10000)
        label_cover_V003_LB.place(x=10000, y=10000)
        label_cover_V023_LB.place(x=10000, y=10000)
        label_cover_V033_LB.place(x=10000, y=10000)
        label_cover_V004_LB.place(x=LB7, y=Rrho0)
        label_cover_R1V001_LB.place(x=10000, y=10000)
        label_cover_R1V002_LB.place(x=10000, y=10000)
        label_cover_R1V022_LB.place(x=10000, y=10000)
        label_cover_R1V003_LB.place(x=10000, y=10000)
        label_cover_R1V023_LB.place(x=10000, y=10000)
        label_cover_R1V033_LB.place(x=10000, y=10000)
        label_cover_R1V004_LB.place(x=LB7, y=R1)
        label_cover_R2V001_LB.place(x=10000, y=10000)
        label_cover_R2V002_LB.place(x=10000, y=10000)
        label_cover_R2V022_LB.place(x=10000, y=10000)
        label_cover_R2V003_LB.place(x=10000, y=10000)
        label_cover_R2V023_LB.place(x=10000, y=10000)
        label_cover_R2V033_LB.place(x=10000, y=10000)
        label_cover_R2V004_LB.place(x=LB7, y=R2)
        label_cover_rho2V001_LB.place(x=10000, y=10000)
        label_cover_rho2V002_LB.place(x=10000, y=10000)
        label_cover_rho2V022_LB.place(x=10000, y=10000)
        label_cover_rho2V003_LB.place(x=10000, y=10000)
        label_cover_rho2V023_LB.place(x=10000, y=10000)
        label_cover_rho2V033_LB.place(x=10000, y=10000)
        label_cover_rho2V004_LB.place(x=LB7, y=rho2)

        label_cover_V101_0_LB.place(x=10000, y=10000)
        label_cover_V102_0_LB.place(x=10000, y=10000)
        label_cover_V202_0_LB.place(x=10000, y=10000)
        label_cover_V112_0_LB.place(x=10000, y=10000)
        label_cover_V212_0_LB.place(x=10000, y=10000)
        label_cover_V103_0_LB.place(x=10000, y=10000)
        label_cover_V203_0_LB.place(x=10000, y=10000)
        label_cover_V101_6_LB.place(x=10000, y=10000)
        label_cover_V102_6_LB.place(x=10000, y=10000)
        label_cover_V202_6_LB.place(x=10000, y=10000)
        label_cover_V112_6_LB.place(x=10000, y=10000)
        label_cover_V212_6_LB.place(x=10000, y=10000)
        label_cover_V103_6_LB.place(x=10000, y=10000)
        label_cover_V203_6_LB.place(x=10000, y=10000)
        label_cover_V101_8_LB.place(x=10000, y=10000)
        label_cover_V102_8_LB.place(x=10000, y=10000)
        label_cover_V202_8_LB.place(x=10000, y=10000)
        label_cover_V112_8_LB.place(x=10000, y=10000)
        label_cover_V212_8_LB.place(x=10000, y=10000)
        label_cover_V103_8_LB.place(x=10000, y=10000)
        label_cover_V203_8_LB.place(x=10000, y=10000)
        label_cover_V101_10_LB.place(x=10000, y=10000)
        label_cover_V102_10_LB.place(x=10000, y=10000)
        label_cover_V202_10_LB.place(x=10000, y=10000)
        label_cover_V112_10_LB.place(x=10000, y=10000)
        label_cover_V212_10_LB.place(x=10000, y=10000)
        label_cover_V103_10_LB.place(x=10000, y=10000)
        label_cover_V203_10_LB.place(x=10000, y=10000)
    elif combobox_max_LB.get() == "4":
        label_cover_V001_LB.place(x=10000, y=10000)
        label_cover_V002_LB.place(x=10000, y=10000)
        label_cover_V022_LB.place(x=10000, y=10000)
        label_cover_V003_LB.place(x=10000, y=10000)
        label_cover_V023_LB.place(x=10000, y=10000)
        label_cover_V033_LB.place(x=10000, y=10000)
        label_cover_V004_LB.place(x=10000, y=10000)
        label_cover_R1V001_LB.place(x=10000, y=10000)
        label_cover_R1V002_LB.place(x=10000, y=10000)
        label_cover_R1V022_LB.place(x=10000, y=10000)
        label_cover_R1V003_LB.place(x=10000, y=10000)
        label_cover_R1V023_LB.place(x=10000, y=10000)
        label_cover_R1V033_LB.place(x=10000, y=10000)
        label_cover_R1V004_LB.place(x=10000, y=10000)
        label_cover_R2V001_LB.place(x=10000, y=10000)
        label_cover_R2V002_LB.place(x=10000, y=10000)
        label_cover_R2V022_LB.place(x=10000, y=10000)
        label_cover_R2V003_LB.place(x=10000, y=10000)
        label_cover_R2V023_LB.place(x=10000, y=10000)
        label_cover_R2V033_LB.place(x=10000, y=10000)
        label_cover_R2V004_LB.place(x=10000, y=10000)
        label_cover_rho2V001_LB.place(x=10000, y=10000)
        label_cover_rho2V002_LB.place(x=10000, y=10000)
        label_cover_rho2V022_LB.place(x=10000, y=10000)
        label_cover_rho2V003_LB.place(x=10000, y=10000)
        label_cover_rho2V023_LB.place(x=10000, y=10000)
        label_cover_rho2V033_LB.place(x=10000, y=10000)
        label_cover_rho2V004_LB.place(x=10000, y=10000)

        label_cover_V101_0_LB.place(x=10000, y=10000)
        label_cover_V102_0_LB.place(x=10000, y=10000)
        label_cover_V202_0_LB.place(x=10000, y=10000)
        label_cover_V112_0_LB.place(x=10000, y=10000)
        label_cover_V212_0_LB.place(x=10000, y=10000)
        label_cover_V103_0_LB.place(x=10000, y=10000)
        label_cover_V203_0_LB.place(x=10000, y=10000)
        label_cover_V101_6_LB.place(x=10000, y=10000)
        label_cover_V102_6_LB.place(x=10000, y=10000)
        label_cover_V202_6_LB.place(x=10000, y=10000)
        label_cover_V112_6_LB.place(x=10000, y=10000)
        label_cover_V212_6_LB.place(x=10000, y=10000)
        label_cover_V103_6_LB.place(x=10000, y=10000)
        label_cover_V203_6_LB.place(x=10000, y=10000)
        label_cover_V101_8_LB.place(x=10000, y=10000)
        label_cover_V102_8_LB.place(x=10000, y=10000)
        label_cover_V202_8_LB.place(x=10000, y=10000)
        label_cover_V112_8_LB.place(x=10000, y=10000)
        label_cover_V212_8_LB.place(x=10000, y=10000)
        label_cover_V103_8_LB.place(x=10000, y=10000)
        label_cover_V203_8_LB.place(x=10000, y=10000)
        label_cover_V101_10_LB.place(x=10000, y=10000)
        label_cover_V102_10_LB.place(x=10000, y=10000)
        label_cover_V202_10_LB.place(x=10000, y=10000)
        label_cover_V112_10_LB.place(x=10000, y=10000)
        label_cover_V212_10_LB.place(x=10000, y=10000)
        label_cover_V103_10_LB.place(x=10000, y=10000)
        label_cover_V203_10_LB.place(x=10000, y=10000)


#sym combobox
#参考：https://qiita.com/nanoru-namonai/items/224bb0219cf8d21436b6
#LB
dict_LB = {
    '':[0], #KeyErrorが出るので応急処置
    'K':[0],
    'D\u221Ed':[0, 2, 4],
    'C\u221Ev':[0, 1, 2, 3, 4],
    'C2v':[0, 1, 2, 3, 4],   #調べて更新する
    'C3v_prolate':[0, 1, 2, 3, 4],   #調べて更新する
    'C3v_oblate':[0, 1, 2, 3, 4],   #調べて更新する
    'Td':[0, 3, 4],
}
#m_cpl
dict_mcpl = {
    '':[0], #KeyErrorが出るので応急処置
    'K':[0],
    'D\u221Ed':[0, 1],
    'C\u221Ev':[0, 1],
    'C2v':[0, 1],
    'C3v_prolate':[0, 1],   #調べて更新する
    'C3v_oblate':[0, 1],   #調べて更新する
    'Td':[0, 1],
}
#n
dict_n = {
    '':[0], #KeyErrorが出るので応急処置
    'K':[0],
    'D\u221Ed':[0, 6, 8, 10],
    'C\u221Ev':[0, 6, 8, 10],
    'C2v':[0, 6, 8, 10],
    'C3v_prolate':[0, 6, 8, 10],  #調べて更新する
    'C3v_oblate':[0, 6, 8, 10],  #調べて更新する
    'Td':[0, 6, 8, 10],
}
var_material = StringVar()
combobox_sym = ttk.Combobox(tab_one, values=list(dict_LB.keys()) , textvariable=var_material, state="readonly", style="office.TCombobox")
#combobox_sym.bind('<<ComboboxSelected>>', lambda event: [combobox_max_mcpl.config(values=dict_mcpl[var_material.get()]), combobox_max_LB.config(values=dict_LB[var_material.get()]), combobox_max_n.config(values=dict_n[var_material.get()]), cb2.set(sym_[list(dict_LB.keys()).index(var_material.get())])])
combobox_sym.place(x= 20, y=50 + 30)

#sym cover
label_cover_V001_sym = PlaceholderEntry(tab_two, "V_0^1", width=8, bg="gray", state="readonly")
label_cover_V002_sym = PlaceholderEntry(tab_two, "V_0^2", width=8, bg="gray", state="readonly")
label_cover_V022_sym = PlaceholderEntry(tab_two, "V_2^2", width=8, bg="gray", state="readonly")
label_cover_V003_sym = PlaceholderEntry(tab_two, "V_0^3", width=8, bg="gray", state="readonly")
label_cover_V023_sym = PlaceholderEntry(tab_two, "V_2^3", width=8, bg="gray", state="readonly")
label_cover_V033_sym = PlaceholderEntry(tab_two, "V_3^3", width=8, bg="gray", state="readonly")
label_cover_V004_sym = PlaceholderEntry(tab_two, "V_0^4", width=8, bg="gray", state="readonly")
label_cover_R1V001_sym = PlaceholderEntry(tab_two, "partial_R V_0^1", width=8, bg="gray", state="readonly")
label_cover_R1V002_sym = PlaceholderEntry(tab_two, "partial_R V_0^2", width=8, bg="gray", state="readonly")
label_cover_R1V022_sym = PlaceholderEntry(tab_two, "partial_R V_2^2", width=8, bg="gray", state="readonly")
label_cover_R1V003_sym = PlaceholderEntry(tab_two, "partial_R V_0^3", width=8, bg="gray", state="readonly")
label_cover_R1V023_sym = PlaceholderEntry(tab_two, "partial_R V_2^3", width=8, bg="gray", state="readonly")
label_cover_R1V033_sym = PlaceholderEntry(tab_two, "partial_R V_3^3", width=8, bg="gray", state="readonly")
label_cover_R1V004_sym = PlaceholderEntry(tab_two, "partial_R V_0^4", width=8, bg="gray", state="readonly")
label_cover_R2V001_sym = PlaceholderEntry(tab_two, "partial_R^2 V_0^1", width=8, bg="gray", state="readonly")
label_cover_R2V002_sym = PlaceholderEntry(tab_two, "partial_R^2 V_0^2", width=8, bg="gray", state="readonly")
label_cover_R2V022_sym = PlaceholderEntry(tab_two, "partial_R^2 V_2^2", width=8, bg="gray", state="readonly")
label_cover_R2V003_sym = PlaceholderEntry(tab_two, "partial_R^2 V_0^3", width=8, bg="gray", state="readonly")
label_cover_R2V023_sym = PlaceholderEntry(tab_two, "partial_R^2 V_2^3", width=8, bg="gray", state="readonly")
label_cover_R2V033_sym = PlaceholderEntry(tab_two, "partial_R^2 V_3^3", width=8, bg="gray", state="readonly")
label_cover_R2V004_sym = PlaceholderEntry(tab_two, "partial_R^2 V_0^4", width=8, bg="gray", state="readonly")
label_cover_rho2V001_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_0^1", width=8, bg="gray", state="readonly")
label_cover_rho2V002_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_0^2", width=8, bg="gray", state="readonly")
label_cover_rho2V022_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_2^2", width=8, bg="gray", state="readonly")
label_cover_rho2V003_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_0^3", width=8, bg="gray", state="readonly")
label_cover_rho2V023_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_2^3", width=8, bg="gray", state="readonly")
label_cover_rho2V033_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_3^3", width=8, bg="gray", state="readonly")
label_cover_rho2V004_sym = PlaceholderEntry(tab_two, "partial_rho^2 V_0^4", width=8, bg="gray", state="readonly")

label_cover_V101_0_sym = PlaceholderEntry(tab_two, "V_10^1", width=8, bg="gray", state="readonly")
label_cover_V102_0_sym = PlaceholderEntry(tab_two, "V_10^2", width=8, bg="gray", state="readonly")
label_cover_V202_0_sym = PlaceholderEntry(tab_two, "V_20^2", width=8, bg="gray", state="readonly")
label_cover_V112_0_sym = PlaceholderEntry(tab_two, "V_11^2", width=8, bg="gray", state="readonly")
label_cover_V212_0_sym = PlaceholderEntry(tab_two, "V_21^2", width=8, bg="gray", state="readonly")
label_cover_V103_0_sym = PlaceholderEntry(tab_two, "V_10^3", width=8, bg="gray", state="readonly")
label_cover_V203_0_sym = PlaceholderEntry(tab_two, "V_20^3", width=8, bg="gray", state="readonly")
label_cover_V101_6_sym = PlaceholderEntry(tab_two, "V_10^1_R6", width=8, bg="gray", state="readonly")
label_cover_V102_6_sym = PlaceholderEntry(tab_two, "V_10^2_R6", width=8, bg="gray", state="readonly")
label_cover_V202_6_sym = PlaceholderEntry(tab_two, "V_20^2_R6", width=8, bg="gray", state="readonly")
label_cover_V112_6_sym = PlaceholderEntry(tab_two, "V_11^2_R6", width=8, bg="gray", state="readonly")
label_cover_V212_6_sym = PlaceholderEntry(tab_two, "V_21^2_R6", width=8, bg="gray", state="readonly")
label_cover_V103_6_sym = PlaceholderEntry(tab_two, "V_10^3_R6", width=8, bg="gray", state="readonly")
label_cover_V203_6_sym = PlaceholderEntry(tab_two, "V_20^3_R6", width=8, bg="gray", state="readonly")
label_cover_V101_8_sym = PlaceholderEntry(tab_two, "V_10^1_R8", width=8, bg="gray", state="readonly")
label_cover_V102_8_sym = PlaceholderEntry(tab_two, "V_10^2_R8", width=8, bg="gray", state="readonly")
label_cover_V202_8_sym = PlaceholderEntry(tab_two, "V_20^2_R8", width=8, bg="gray", state="readonly")
label_cover_V112_8_sym = PlaceholderEntry(tab_two, "V_11^2_R8", width=8, bg="gray", state="readonly")
label_cover_V212_8_sym = PlaceholderEntry(tab_two, "V_21^2_R8", width=8, bg="gray", state="readonly")
label_cover_V103_8_sym = PlaceholderEntry(tab_two, "V_10^3_R8", width=8, bg="gray", state="readonly")
label_cover_V203_8_sym = PlaceholderEntry(tab_two, "V_20^3_R8", width=8, bg="gray", state="readonly")
label_cover_V101_10_sym = PlaceholderEntry(tab_two, "V_10^1_R10", width=8, bg="gray", state="readonly")
label_cover_V102_10_sym = PlaceholderEntry(tab_two, "V_10^2_R10", width=8, bg="gray", state="readonly")
label_cover_V202_10_sym = PlaceholderEntry(tab_two, "V_20^2_R10", width=8, bg="gray", state="readonly")
label_cover_V112_10_sym = PlaceholderEntry(tab_two, "V_11^2_R10", width=8, bg="gray", state="readonly")
label_cover_V212_10_sym = PlaceholderEntry(tab_two, "V_21^2_R10", width=8, bg="gray", state="readonly")
label_cover_V103_10_sym = PlaceholderEntry(tab_two, "V_10^3_R10", width=8, bg="gray", state="readonly")
label_cover_V203_10_sym = PlaceholderEntry(tab_two, "V_20^3_R10", width=8, bg="gray", state="readonly")

label_cover_A = PlaceholderEntry(tab_one, "A", width=15, bg="gray", state="readonly")
label_cover_B = PlaceholderEntry(tab_one, "B", width=15, bg="gray", state="readonly")
label_cover_C = PlaceholderEntry(tab_one, "C", width=15, bg="gray", state="readonly")

def feedback_sym(event):
    if combobox_sym.get() == "":
        return
    
    elif combobox_sym.get() == "K":
        label_cover_A.place(x=65, y=180)
        label_cover_B.place(x=65, y=205)
        label_cover_C.place(x=65, y=230)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=LB1, y=Rrho0)
        label_cover_V002_sym.place(x=LB2, y=Rrho0)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=LB4, y=Rrho0)
        label_cover_V023_sym.place(x=LB5, y=Rrho0)
        label_cover_V033_sym.place(x=LB6, y=Rrho0)
        label_cover_V004_sym.place(x=LB7, y=Rrho0)
        label_cover_R1V001_sym.place(x=LB1, y=R1)
        label_cover_R1V002_sym.place(x=LB2, y=R1)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=LB4, y=R1)
        label_cover_R1V023_sym.place(x=LB5, y=R1)
        label_cover_R1V033_sym.place(x=LB6, y=R1)
        label_cover_R1V004_sym.place(x=LB7, y=R1)
        label_cover_R2V001_sym.place(x=LB1, y=R2)
        label_cover_R2V002_sym.place(x=LB2, y=R2)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=LB4, y=R2)
        label_cover_R2V023_sym.place(x=LB5, y=R2)
        label_cover_R2V033_sym.place(x=LB6, y=R2)
        label_cover_R2V004_sym.place(x=LB7, y=R2)
        label_cover_rho2V001_sym.place(x=LB1, y=rho2)
        label_cover_rho2V002_sym.place(x=LB2, y=rho2)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=LB4, y=rho2)
        label_cover_rho2V023_sym.place(x=LB5, y=rho2)
        label_cover_rho2V033_sym.place(x=LB6, y=rho2)
        label_cover_rho2V004_sym.place(x=LB7, y=rho2)

        label_cover_V101_0_sym.place(x=LB1K0mcpl1, y=R0)
        label_cover_V102_0_sym.place(x=LB2K0mcpl1, y=R0)
        label_cover_V202_0_sym.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_sym.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_sym.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_sym.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_sym.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_sym.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_sym.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_sym.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_sym.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_sym.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_sym.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_sym.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_sym.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_sym.place(x=LB3K0mcpl2, y=R10)

    elif combobox_sym.get() == "D\u221Ed":
        label_cover_A.place(x=65, y=180)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=65, y=230)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=LB1, y=Rrho0)
        label_cover_V002_sym.place(x=10000, y=10000)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=LB4, y=Rrho0)
        label_cover_V023_sym.place(x=LB5, y=Rrho0)
        label_cover_V033_sym.place(x=LB6, y=Rrho0)
        label_cover_V004_sym.place(x=10000, y=10000)
        label_cover_R1V001_sym.place(x=LB1, y=R1)
        label_cover_R1V002_sym.place(x=10000, y=10000)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=LB4, y=R1)
        label_cover_R1V023_sym.place(x=LB5, y=R1)
        label_cover_R1V033_sym.place(x=LB6, y=R1)
        label_cover_R1V004_sym.place(x=10000, y=10000)
        label_cover_R2V001_sym.place(x=LB1, y=R2)
        label_cover_R2V002_sym.place(x=10000, y=10000)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=LB4, y=R2)
        label_cover_R2V023_sym.place(x=LB5, y=R2)
        label_cover_R2V033_sym.place(x=LB6, y=R2)
        label_cover_R2V004_sym.place(x=10000, y=10000)
        label_cover_rho2V001_sym.place(x=LB1, y=rho2)
        label_cover_rho2V002_sym.place(x=10000, y=10000)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=LB4, y=rho2)
        label_cover_rho2V023_sym.place(x=LB5, y=rho2)
        label_cover_rho2V033_sym.place(x=LB6, y=rho2)
        label_cover_rho2V004_sym.place(x=10000, y=10000)

        label_cover_V101_0_sym.place(x=LB1K0mcpl1, y=R0)
        label_cover_V102_0_sym.place(x=10000, y=10000)
        label_cover_V202_0_sym.place(x=10000, y=10000)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=LB3K0mcpl1, y=R0)
        label_cover_V203_0_sym.place(x=LB3K0mcpl2, y=R0)
        label_cover_V101_6_sym.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_sym.place(x=10000, y=10000)
        label_cover_V202_6_sym.place(x=10000, y=10000)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=LB3K0mcpl1, y=R6)
        label_cover_V203_6_sym.place(x=LB3K0mcpl2, y=R6)
        label_cover_V101_8_sym.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_sym.place(x=10000, y=10000)
        label_cover_V202_8_sym.place(x=10000, y=10000)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=LB3K0mcpl1, y=R8)
        label_cover_V203_8_sym.place(x=LB3K0mcpl2, y=R8)
        label_cover_V101_10_sym.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_sym.place(x=10000, y=10000)
        label_cover_V202_10_sym.place(x=10000, y=10000)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=LB3K0mcpl1, y=R10)
        label_cover_V203_10_sym.place(x=LB3K0mcpl2, y=R10)

    elif combobox_sym.get() == "C\u221Ev":
        label_cover_A.place(x=65, y=180)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=65, y=230)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=10000, y=10000)
        label_cover_V002_sym.place(x=10000, y=10000)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=10000, y=10000)
        label_cover_V023_sym.place(x=LB5, y=Rrho0)
        label_cover_V033_sym.place(x=LB6, y=Rrho0)
        label_cover_V004_sym.place(x=10000, y=10000)
        label_cover_R1V001_sym.place(x=10000, y=10000)
        label_cover_R1V002_sym.place(x=10000, y=10000)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=10000, y=10000)
        label_cover_R1V023_sym.place(x=LB5, y=R1)
        label_cover_R1V033_sym.place(x=LB6, y=R1)
        label_cover_R1V004_sym.place(x=10000, y=10000)
        label_cover_R2V001_sym.place(x=10000, y=10000)
        label_cover_R2V002_sym.place(x=10000, y=10000)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=10000, y=10000)
        label_cover_R2V023_sym.place(x=LB5, y=R2)
        label_cover_R2V033_sym.place(x=LB6, y=R2)
        label_cover_R2V004_sym.place(x=10000, y=10000)
        label_cover_rho2V001_sym.place(x=10000, y=10000)
        label_cover_rho2V002_sym.place(x=10000, y=10000)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=10000, y=10000)
        label_cover_rho2V023_sym.place(x=LB5, y=rho2)
        label_cover_rho2V033_sym.place(x=LB6, y=rho2)
        label_cover_rho2V004_sym.place(x=10000, y=10000)

        label_cover_V101_0_sym.place(x=10000, y=10000)
        label_cover_V102_0_sym.place(x=10000, y=10000)
        label_cover_V202_0_sym.place(x=10000, y=10000)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=10000, y=10000)
        label_cover_V203_0_sym.place(x=10000, y=10000)
        label_cover_V101_6_sym.place(x=10000, y=10000)
        label_cover_V102_6_sym.place(x=10000, y=10000)
        label_cover_V202_6_sym.place(x=10000, y=10000)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=10000, y=10000)
        label_cover_V203_6_sym.place(x=10000, y=10000)
        label_cover_V101_8_sym.place(x=10000, y=10000)
        label_cover_V102_8_sym.place(x=10000, y=10000)
        label_cover_V202_8_sym.place(x=10000, y=10000)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=10000, y=10000)
        label_cover_V203_8_sym.place(x=10000, y=10000)
        label_cover_V101_10_sym.place(x=10000, y=10000)
        label_cover_V102_10_sym.place(x=10000, y=10000)
        label_cover_V202_10_sym.place(x=10000, y=10000)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=10000, y=10000)
        label_cover_V203_10_sym.place(x=10000, y=10000)

    elif combobox_sym.get() == "C2v":
        label_cover_A.place(x=10000, y=10000)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=10000, y=10000)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=10000, y=10000)
        label_cover_V002_sym.place(x=10000, y=10000)
        label_cover_V022_sym.place(x=10000, y=10000)
        label_cover_V003_sym.place(x=10000, y=10000)
        label_cover_V023_sym.place(x=10000, y=10000)
        label_cover_V033_sym.place(x=LB6, y=Rrho0)
        label_cover_V004_sym.place(x=LB7, y=Rrho0)
        label_cover_R1V001_sym.place(x=10000, y=10000)
        label_cover_R1V002_sym.place(x=10000, y=10000)
        label_cover_R1V022_sym.place(x=10000, y=10000)
        label_cover_R1V003_sym.place(x=10000, y=10000)
        label_cover_R1V023_sym.place(x=10000, y=10000)
        label_cover_R1V033_sym.place(x=LB6, y=R1)
        label_cover_R1V004_sym.place(x=LB7, y=R1)
        label_cover_R2V001_sym.place(x=10000, y=10000)
        label_cover_R2V002_sym.place(x=10000, y=10000)
        label_cover_R2V022_sym.place(x=10000, y=10000)
        label_cover_R2V003_sym.place(x=10000, y=10000)
        label_cover_R2V023_sym.place(x=10000, y=10000)
        label_cover_R2V033_sym.place(x=LB6, y=R2)
        label_cover_R2V004_sym.place(x=LB7, y=R2)
        label_cover_rho2V001_sym.place(x=10000, y=10000)
        label_cover_rho2V002_sym.place(x=10000, y=10000)
        label_cover_rho2V022_sym.place(x=10000, y=10000)
        label_cover_rho2V003_sym.place(x=10000, y=10000)
        label_cover_rho2V023_sym.place(x=10000, y=10000)
        label_cover_rho2V033_sym.place(x=LB6, y=rho2)
        label_cover_rho2V004_sym.place(x=LB7, y=rho2)

        label_cover_V101_0_sym.place(x=10000, y=10000)
        label_cover_V102_0_sym.place(x=10000, y=10000)
        label_cover_V202_0_sym.place(x=10000, y=10000)
        label_cover_V112_0_sym.place(x=10000, y=10000)
        label_cover_V212_0_sym.place(x=10000, y=10000)
        label_cover_V103_0_sym.place(x=10000, y=10000)
        label_cover_V203_0_sym.place(x=10000, y=10000)
        label_cover_V101_6_sym.place(x=10000, y=10000)
        label_cover_V102_6_sym.place(x=10000, y=10000)
        label_cover_V202_6_sym.place(x=10000, y=10000)
        label_cover_V112_6_sym.place(x=10000, y=10000)
        label_cover_V212_6_sym.place(x=10000, y=10000)
        label_cover_V103_6_sym.place(x=10000, y=10000)
        label_cover_V203_6_sym.place(x=10000, y=10000)
        label_cover_V101_8_sym.place(x=10000, y=10000)
        label_cover_V102_8_sym.place(x=10000, y=10000)
        label_cover_V202_8_sym.place(x=10000, y=10000)
        label_cover_V112_8_sym.place(x=10000, y=10000)
        label_cover_V212_8_sym.place(x=10000, y=10000)
        label_cover_V103_8_sym.place(x=10000, y=10000)
        label_cover_V203_8_sym.place(x=10000, y=10000)
        label_cover_V101_10_sym.place(x=10000, y=10000)
        label_cover_V102_10_sym.place(x=10000, y=10000)
        label_cover_V202_10_sym.place(x=10000, y=10000)
        label_cover_V112_10_sym.place(x=10000, y=10000)
        label_cover_V212_10_sym.place(x=10000, y=10000)
        label_cover_V103_10_sym.place(x=10000, y=10000)
        label_cover_V203_10_sym.place(x=10000, y=10000)
        
    elif combobox_sym.get() == "C3v_prolate":
        label_cover_A.place(x=10000, y=10000)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=65, y=230)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=10000, y=10000)
        label_cover_V002_sym.place(x=10000, y=10000)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=10000, y=10000)
        label_cover_V023_sym.place(x=LB5, y=Rrho0)
        label_cover_V033_sym.place(x=10000, y=10000)
        label_cover_V004_sym.place(x=LB7, y=Rrho0)
        label_cover_R1V001_sym.place(x=10000, y=10000)
        label_cover_R1V002_sym.place(x=10000, y=10000)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=10000, y=10000)
        label_cover_R1V023_sym.place(x=LB5, y=R1)
        label_cover_R1V033_sym.place(x=10000, y=10000)
        label_cover_R1V004_sym.place(x=LB7, y=R1)
        label_cover_R2V001_sym.place(x=10000, y=10000)
        label_cover_R2V002_sym.place(x=10000, y=10000)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=10000, y=10000)
        label_cover_R2V023_sym.place(x=LB5, y=R2)
        label_cover_R2V033_sym.place(x=10000, y=10000)
        label_cover_R2V004_sym.place(x=LB7, y=R2)
        label_cover_rho2V001_sym.place(x=10000, y=10000)
        label_cover_rho2V002_sym.place(x=10000, y=10000)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=10000, y=10000)
        label_cover_rho2V023_sym.place(x=LB5, y=rho2)
        label_cover_rho2V033_sym.place(x=10000, y=10000)
        label_cover_rho2V004_sym.place(x=LB7, y=rho2)

        label_cover_V101_0_sym.place(x=10000, y=10000)
        label_cover_V102_0_sym.place(x=10000, y=10000)
        label_cover_V202_0_sym.place(x=10000, y=10000)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=10000, y=10000)
        label_cover_V203_0_sym.place(x=10000, y=10000)
        label_cover_V101_6_sym.place(x=10000, y=10000)
        label_cover_V102_6_sym.place(x=10000, y=10000)
        label_cover_V202_6_sym.place(x=10000, y=10000)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=10000, y=10000)
        label_cover_V203_6_sym.place(x=10000, y=10000)
        label_cover_V101_8_sym.place(x=10000, y=10000)
        label_cover_V102_8_sym.place(x=10000, y=10000)
        label_cover_V202_8_sym.place(x=10000, y=10000)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=10000, y=10000)
        label_cover_V203_8_sym.place(x=10000, y=10000)
        label_cover_V101_10_sym.place(x=10000, y=10000)
        label_cover_V102_10_sym.place(x=10000, y=10000)
        label_cover_V202_10_sym.place(x=10000, y=10000)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=10000, y=10000)
        label_cover_V203_10_sym.place(x=10000, y=10000)
        
    elif combobox_sym.get() == "C3v_oblate":
        label_cover_A.place(x=65, y=180)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=10000, y=10000)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=10000, y=10000)
        label_cover_V002_sym.place(x=10000, y=10000)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=10000, y=10000)
        label_cover_V023_sym.place(x=LB5, y=Rrho0)
        label_cover_V033_sym.place(x=10000, y=10000)
        label_cover_V004_sym.place(x=LB7, y=Rrho0)
        label_cover_R1V001_sym.place(x=10000, y=10000)
        label_cover_R1V002_sym.place(x=10000, y=10000)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=10000, y=10000)
        label_cover_R1V023_sym.place(x=LB5, y=R1)
        label_cover_R1V033_sym.place(x=10000, y=10000)
        label_cover_R1V004_sym.place(x=LB7, y=R1)
        label_cover_R2V001_sym.place(x=10000, y=10000)
        label_cover_R2V002_sym.place(x=10000, y=10000)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=10000, y=10000)
        label_cover_R2V023_sym.place(x=LB5, y=R2)
        label_cover_R2V033_sym.place(x=10000, y=10000)
        label_cover_R2V004_sym.place(x=LB7, y=R2)
        label_cover_rho2V001_sym.place(x=10000, y=10000)
        label_cover_rho2V002_sym.place(x=10000, y=10000)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=10000, y=10000)
        label_cover_rho2V023_sym.place(x=LB5, y=rho2)
        label_cover_rho2V033_sym.place(x=10000, y=10000)
        label_cover_rho2V004_sym.place(x=LB7, y=rho2)

        label_cover_V101_0_sym.place(x=10000, y=10000)
        label_cover_V102_0_sym.place(x=10000, y=10000)
        label_cover_V202_0_sym.place(x=10000, y=10000)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=10000, y=10000)
        label_cover_V203_0_sym.place(x=10000, y=10000)
        label_cover_V101_6_sym.place(x=10000, y=10000)
        label_cover_V102_6_sym.place(x=10000, y=10000)
        label_cover_V202_6_sym.place(x=10000, y=10000)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=10000, y=10000)
        label_cover_V203_6_sym.place(x=10000, y=10000)
        label_cover_V101_8_sym.place(x=10000, y=10000)
        label_cover_V102_8_sym.place(x=10000, y=10000)
        label_cover_V202_8_sym.place(x=10000, y=10000)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=10000, y=10000)
        label_cover_V203_8_sym.place(x=10000, y=10000)
        label_cover_V101_10_sym.place(x=10000, y=10000)
        label_cover_V102_10_sym.place(x=10000, y=10000)
        label_cover_V202_10_sym.place(x=10000, y=10000)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=10000, y=10000)
        label_cover_V203_10_sym.place(x=10000, y=10000)

    elif combobox_sym.get() == "Td":
        label_cover_A.place(x=65, y=180)
        label_cover_B.place(x=10000, y=10000)
        label_cover_C.place(x=65, y=230)
        combobox_max_LB.config(values=dict_LB[var_material.get()])
        combobox_max_mcpl.config(values=dict_mcpl[var_material.get()])
        combobox_max_n.config(values=dict_n[var_material.get()])

        label_cover_V001_sym.place(x=LB1, y=Rrho0)
        label_cover_V002_sym.place(x=LB2, y=Rrho0)
        label_cover_V022_sym.place(x=LB3, y=Rrho0)
        label_cover_V003_sym.place(x=LB4, y=Rrho0)
        label_cover_V023_sym.place(x=10000, y=10000)
        label_cover_V033_sym.place(x=LB6, y=Rrho0)
        label_cover_V004_sym.place(x=10000, y=10000)
        label_cover_R1V001_sym.place(x=LB1, y=R1)
        label_cover_R1V002_sym.place(x=LB2, y=R1)
        label_cover_R1V022_sym.place(x=LB3, y=R1)
        label_cover_R1V003_sym.place(x=LB4, y=R1)
        label_cover_R1V023_sym.place(x=10000, y=10000)
        label_cover_R1V033_sym.place(x=LB6, y=R1)
        label_cover_R1V004_sym.place(x=10000, y=10000)
        label_cover_R2V001_sym.place(x=LB1, y=R2)
        label_cover_R2V002_sym.place(x=LB2, y=R2)
        label_cover_R2V022_sym.place(x=LB3, y=R2)
        label_cover_R2V003_sym.place(x=LB4, y=R2)
        label_cover_R2V023_sym.place(x=10000, y=10000)
        label_cover_R2V033_sym.place(x=LB6, y=R2)
        label_cover_R2V004_sym.place(x=10000, y=10000)
        label_cover_rho2V001_sym.place(x=LB1, y=rho2)
        label_cover_rho2V002_sym.place(x=LB2, y=rho2)
        label_cover_rho2V022_sym.place(x=LB3, y=rho2)
        label_cover_rho2V003_sym.place(x=LB4, y=rho2)
        label_cover_rho2V023_sym.place(x=10000, y=10000)
        label_cover_rho2V033_sym.place(x=LB6, y=rho2)
        label_cover_rho2V004_sym.place(x=10000, y=10000)

        label_cover_V101_0_sym.place(x=LB1K0mcpl1, y=R0)
        label_cover_V102_0_sym.place(x=LB2K0mcpl1, y=R0)
        label_cover_V202_0_sym.place(x=LB2K0mcpl2, y=R0)
        label_cover_V112_0_sym.place(x=LB2K1mcpl1, y=R0)
        label_cover_V212_0_sym.place(x=LB2K1mcpl2, y=R0)
        label_cover_V103_0_sym.place(x=10000, y=10000)
        label_cover_V203_0_sym.place(x=10000, y=10000)
        label_cover_V101_6_sym.place(x=LB1K0mcpl1, y=R6)
        label_cover_V102_6_sym.place(x=LB2K0mcpl1, y=R6)
        label_cover_V202_6_sym.place(x=LB2K0mcpl2, y=R6)
        label_cover_V112_6_sym.place(x=LB2K1mcpl1, y=R6)
        label_cover_V212_6_sym.place(x=LB2K1mcpl2, y=R6)
        label_cover_V103_6_sym.place(x=10000, y=10000)
        label_cover_V203_6_sym.place(x=10000, y=10000)
        label_cover_V101_8_sym.place(x=LB1K0mcpl1, y=R8)
        label_cover_V102_8_sym.place(x=LB2K0mcpl1, y=R8)
        label_cover_V202_8_sym.place(x=LB2K0mcpl2, y=R8)
        label_cover_V112_8_sym.place(x=LB2K1mcpl1, y=R8)
        label_cover_V212_8_sym.place(x=LB2K1mcpl2, y=R8)
        label_cover_V103_8_sym.place(x=10000, y=10000)
        label_cover_V203_8_sym.place(x=10000, y=10000)
        label_cover_V101_10_sym.place(x=LB1K0mcpl1, y=R10)
        label_cover_V102_10_sym.place(x=LB2K0mcpl1, y=R10)
        label_cover_V202_10_sym.place(x=LB2K0mcpl2, y=R10)
        label_cover_V112_10_sym.place(x=LB2K1mcpl1, y=R10)
        label_cover_V212_10_sym.place(x=LB2K1mcpl2, y=R10)
        label_cover_V103_10_sym.place(x=10000, y=10000)
        label_cover_V203_10_sym.place(x=10000, y=10000)

combobox_max_LB = ttk.Combobox(tab_two, values=list(dict_LB[var_material.get()]), width = 8, state="readonly", style="office.TCombobox")
combobox_max_LB.place(x=225, y=285 + 10)
combobox_max_mcpl = ttk.Combobox(tab_two, values=list(dict_mcpl[var_material.get()]), width = 8, state="readonly", style="office.TCombobox")
combobox_max_mcpl.place(x=225, y=310 + 10)
combobox_max_n = ttk.Combobox(tab_two, values=list(dict_mcpl[var_material.get()]), width = 8, state="readonly", style="office.TCombobox")
combobox_max_n.place(x=225, y=335 + 10)

combobox_max_mcpl.bind("<<ComboboxSelected>>", feedback_mcpl)
combobox_max_n.bind("<<ComboboxSelected>>", feedback_n)
combobox_max_LB.bind("<<ComboboxSelected>>", feedback_LB)
combobox_sym.bind("<<ComboboxSelected>>", feedback_sym)





# tab_thrに配置するウィジェットの作成
# Canvasの作成
canvas1 = tk.Canvas(tab_thr, bg = "#CFDAED")
# Canvasを配置
canvas1.pack(fill = tk.BOTH, expand = True)
# 線の描画
#canvas.create_line(20, 10, 280, 190, fill = "Blue", width = 5)

canvas1.create_rectangle(
    350, 10, # 四角の左上
    900, 440,  # 四角の右下
    outline = "gray",  # 枠の色
    width = 2,  # 枠の幅E
    fill = "#C0CEE8",  # 中身の色
)

timer = Timer(tab_thr)


label = ttk.Label(tab_thr, text="Results", font=("Helvetica", "16", "bold"), foreground = "#28487c", background="#CFDAED")
label.place(x= 5, y=5)

label = ttk.Label(tab_thr, text="Conceptual map of potential", font=("Helvetica", "16", "bold"), foreground = "#28487c", background="#C0CEE8")
label.place(x= 370, y=15)

#print("00")
#左側
def calc():
    p.start(5)          #プログレスバー開始
    sym = str(combobox_sym.get())
    #print("11")
    #Molecular Paramter
    mol_params= [txtBox_A_small.get(), txtBox_B_small.get(), txtBox_C_small.get(), txtBox_m_small.get(), txtBox_B_large.get(), txtBox_C_large.get(), txtBox_m_large.get(), txtBox_Re.get()]
    mol_params_error = ["rotational constant A should be float.", 
                       "rotational constant B should be float.", 
                       "rotational constant C should be float.", 
                       "molecular mass m should be float."
                       "rotational constant B should be float.", 
                       "rotational constant C should be float.", 
                       "molecular mass m should be float.", 
                       "intermolecular distance Re should be float."]
    #small Aは入れなくてもいい
    try:
        mol_params[0] = float(mol_params[0])
    except:
        mol_params[0] = 0
    #small Bは入れなくてもいい
    try:
        mol_params[1] = float(mol_params[1])
    except:
        mol_params[1] = 0
    #small Cは入れなくてもいい
    try:
        mol_params[2] = float(mol_params[2])
    except:
        mol_params[2] = 0
    for num in range (3, len(mol_params)):
        try:
            mol_params[num] = float(mol_params[num])
        except:
            messagebox.showerror("Error", mol_params_error[num] + ",\t" + mol_params[num])

    #Matrix Size
    mat_sizes = [txtBox_n0.get(), txtBox_nplsmns.get(), txtBox_j.get(), txtBox_m.get()]
    mol_sizes_error = ["matrix size n\u2080 should be integer", 
                       "matrix size n\u208A and nmns should be integer", 
                       "matrix size j should be integer", 
                       "quantum number m should be integer"]
    for num in range (0, len(mat_sizes)):
        try:
            mat_sizes[num] = int(mat_sizes[num])
        except:
            messagebox.showerror("Error", mol_sizes_error[num] + ",\t" + mat_sizes[num])

    #Cut Off Paramter
    cutoffs = [txtBox_cutoff_energy.get(), txtBox_cutoff_coeff.get()]
    try:
        cutoffs[0] = float(cutoffs[0])
    except:
        cutoffs[0] = 100
    try:
        cutoffs[1] = float(cutoffs[1])
    except:
        cutoffs[1] = -1

    #うまいこと例外処理をする．
    max_LB = int(combobox_max_LB.get())
    max_mcpl = int(combobox_max_mcpl.get())
    max_n = int(combobox_max_n.get())
    pot_exps = [max_LB, max_mcpl, max_n]
    #print("22")
    #Potential Paramter
    pot_params = [txtBox_kzz.get(), txtBox_az.get(), txtBox_kxx.get(), txtBox_kxxz.get(), 
                  txtBox_V001.get(), txtBox_V002.get(), txtBox_V202.get(), txtBox_V003.get(), txtBox_V203.get(), txtBox_V303.get(), txtBox_V004.get(), 
                  txtBox_R1V001.get(), txtBox_R1V002.get(), txtBox_R1V202.get(), txtBox_R1V003.get(), txtBox_R1V203.get(), txtBox_R1V303.get(), txtBox_R1V004.get(), 
                  txtBox_R2V001.get(), txtBox_R2V002.get(), txtBox_R2V202.get(), txtBox_R2V003.get(), txtBox_R2V203.get(), txtBox_R2V303.get(), txtBox_R2V004.get(), 
                  txtBox_rho2V001.get(), txtBox_rho2V002.get(), txtBox_rho2V202.get(), txtBox_rho2V003.get(), txtBox_rho2V203.get(), txtBox_rho2V303.get(), txtBox_rho2V004.get(), 
                  txtBox_V011_0.get(), txtBox_V012_0.get(), txtBox_V022_0.get(), txtBox_V212_0.get(), txtBox_V222_0.get(), txtBox_V013_0.get(), txtBox_V023_0.get(), 
                  txtBox_V011_6.get(), txtBox_V012_6.get(), txtBox_V022_6.get(), txtBox_V212_6.get(), txtBox_V222_6.get(), txtBox_V013_6.get(), txtBox_V023_6.get(), 
                  txtBox_V011_8.get(), txtBox_V012_8.get(), txtBox_V022_8.get(), txtBox_V212_8.get(), txtBox_V222_8.get(), txtBox_V013_8.get(), txtBox_V023_8.get(), 
                  txtBox_V011_10.get(), txtBox_V012_10.get(), txtBox_V022_10.get(), txtBox_V212_10.get(), txtBox_V222_10.get(), txtBox_V013_10.get(), txtBox_V023_10.get()]
    for num in range (0, len(pot_params)):
        try:
            pot_params[num] = float(pot_params[num])
        except:
            pot_params[num] = float(0)
    Parameters = [sym, mol_params, mat_sizes, cutoffs, pot_exps, pot_params]

    CSBICalculation_Module.calculation(Parameters)
    label1 = ttk.Label(tab_thr, text="completed       ", font=("Helvetica", "12", "normal"), background="#CFDAED")
    label1.place(x= 20, y=120) 

    p.stop()            #プログレスバー停止
    return

def info():
    sym = str(combobox_sym.get())
    #Molecular Paramter
    mol_params= [txtBox_A_small.get(), txtBox_B_small.get(), txtBox_C_small.get(), txtBox_m_small.get(), txtBox_B_large.get(), txtBox_C_large.get(), txtBox_m_large.get(), txtBox_Re.get()]
    mol_params_error = ["rotational constant A should be float.", 
                       "rotational constant B should be float.", 
                       "rotational constant C should be float.", 
                       "molecular mass m should be float."
                       "rotational constant B should be float.", 
                       "rotational constant C should be float.", 
                       "molecular mass m should be float.", 
                       "intermolecular distance Re should be float."]
    #small Aは入れなくてもいい
    try:
        mol_params[0] = float(mol_params[0])
    except:
        mol_params[0] = 0
    #small Bは入れなくてもいい
    try:
        mol_params[1] = float(mol_params[1])
    except:
        mol_params[1] = 0
    #small Cは入れなくてもいい
    try:
        mol_params[2] = float(mol_params[2])
    except:
        mol_params[2] = 0
    for num in range (3, len(mol_params)):
        try:
            mol_params[num] = float(mol_params[num])
        except:
            messagebox.showerror("Error", mol_params_error[num] + ",\t" + mol_params[num])

    #Matrix Size
    mat_sizes = [txtBox_n0.get(), txtBox_nplsmns.get(), txtBox_j.get(), txtBox_m.get()]
    mol_sizes_error = ["matrix size n\u2080 should be integer", 
                       "matrix size n\u208A and nmns should be integer", 
                       "matrix size j should be integer", 
                       "quantum number m should be integer"]
    for num in range (0, len(mat_sizes)):
        try:
            mat_sizes[num] = int(mat_sizes[num])
        except:
            messagebox.showerror("Error", mol_sizes_error[num] + ",\t" + mat_sizes[num])

    #Cut Off Paramter
    cutoffs = [txtBox_cutoff_energy.get(), txtBox_cutoff_coeff.get()]
    cutoffs_error = ["energy cut off parameter should be float", 
                       "coefficient cut off parameter should be float"]
    try:
        cutoffs[0] = float(cutoffs[0])
    except:
        cutoffs[0] = 100
    try:
        cutoffs[1] = float(cutoffs[1])
    except:
        cutoffs[1] = -1

    #うまいこと例外処理をする．
    max_LB = int(combobox_max_LB.get())
    max_mcpl = int(combobox_max_mcpl.get())
    max_n = int(combobox_max_n.get())
    pot_exps = [max_LB, max_mcpl, max_n]
    #print("22")
    #Potential Paramter
    pot_params = [txtBox_kzz.get(), txtBox_az.get(), txtBox_kxx.get(), txtBox_kxxz.get(), 
                  txtBox_V001.get(), txtBox_V002.get(), txtBox_V202.get(), txtBox_V003.get(), txtBox_V203.get(), txtBox_V303.get(), txtBox_V004.get(), 
                  txtBox_R1V001.get(), txtBox_R1V002.get(), txtBox_R1V202.get(), txtBox_R1V003.get(), txtBox_R1V203.get(), txtBox_R1V303.get(), txtBox_R1V004.get(), 
                  txtBox_R2V001.get(), txtBox_R2V002.get(), txtBox_R2V202.get(), txtBox_R2V003.get(), txtBox_R2V203.get(), txtBox_R2V303.get(), txtBox_R2V004.get(), 
                  txtBox_rho2V001.get(), txtBox_rho2V002.get(), txtBox_rho2V202.get(), txtBox_rho2V003.get(), txtBox_rho2V203.get(), txtBox_rho2V303.get(), txtBox_rho2V004.get(), 
                  txtBox_V011_0.get(), txtBox_V012_0.get(), txtBox_V022_0.get(), txtBox_V212_0.get(), txtBox_V222_0.get(), txtBox_V013_0.get(), txtBox_V023_0.get(), 
                  txtBox_V011_6.get(), txtBox_V012_6.get(), txtBox_V022_6.get(), txtBox_V212_6.get(), txtBox_V222_6.get(), txtBox_V013_6.get(), txtBox_V023_6.get(), 
                  txtBox_V011_8.get(), txtBox_V012_8.get(), txtBox_V022_8.get(), txtBox_V212_8.get(), txtBox_V222_8.get(), txtBox_V013_8.get(), txtBox_V023_8.get(), 
                  txtBox_V011_10.get(), txtBox_V012_10.get(), txtBox_V022_10.get(), txtBox_V212_10.get(), txtBox_V222_10.get(), txtBox_V013_10.get(), txtBox_V023_10.get()]
    for num in range (0, len(pot_params)):
        try:
            pot_params[num] = float(pot_params[num])
        except:
            pot_params[num] = float(0)
    Parameters = [sym, mol_params, mat_sizes, cutoffs, pot_exps, pot_params]
    label = ttk.Label(tab_thr, text="n\u2080 = " + txtBox_n0.get() + ", n\u208A = " + txtBox_nplsmns.get() + ", j = " + txtBox_j.get() + ", m = " + txtBox_m.get(), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=200)
    label = ttk.Label(tab_thr, text="A_small = " + str(mol_params[0]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=230)
    label = ttk.Label(tab_thr, text="B_small = " + str(mol_params[1]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=250)
    label = ttk.Label(tab_thr, text="C_small = " + str(mol_params[2]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=270)
    label = ttk.Label(tab_thr, text="B_large = " + str(mol_params[4]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=290)
    label = ttk.Label(tab_thr, text="C_large = " + str(mol_params[5]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=310)
    label = ttk.Label(tab_thr, text="R\u2091 = " + str(mol_params[7]), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=330)
    label = ttk.Label(tab_thr, text="dimension: " + str(dimension(int(txtBox_n0.get()), int(txtBox_nplsmns.get()), int(txtBox_nplsmns.get()), int(txtBox_j.get()), int(txtBox_m.get()))), font=("Helvetica", "10", "normal"), background="#CFDAED")
    label.place(x= 20, y=360)

    c = 2.99792458*10**(8)
    hbar = 1.054571817*10**(-34)
    kzz = pot_params[0]
    az = pot_params[1]
    kxx = pot_params[2]
    kxxz = pot_params[3]
    mu = mol_params[3]*mol_params[6]/(mol_params[3] + mol_params[6])/(6.02*10**23)/(10**3)
    B_large = mol_params[4]
    Re = mol_params[7]
    barrier = max(np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[4]), 
                  np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[5]), 
                  np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[6]), 
                  np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[7]), 
                  np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[8]), 
                  np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[9]), 
                  np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[10]))

    Ix = hbar*hbar/(2*B_large)*5.03412*pow(10, 22)
    Re2Ix = (Re*pow(10, -10))*(Re*pow(10, -10))/Ix
    omegas = np.sqrt(2*kzz*az*az*1.98645*10**(-23)*10**(20)/mu)
    omegab = np.sqrt(2*kxx*1.98645*pow(10, -23)*pow(10, 20)*(1/mu + Re2Ix))
    shbaromega = 1/(2*np.pi)*omegas/c/100
    shbaromega_chi = az**2*hbar**2/(2*mu)*5.03312*10**(22)*10**(20)
    bhbaromega = 1/(2*np.pi)*omegab/c/100
    omegasb = np.sqrt(2*abs(kxxz)*1.98645*pow(10, -23)*pow(10, 20)*(1/mu + Re2Ix))
    sbhbaromega = 1/(2*np.pi)*omegasb/c/100
    FWHM_s = 2*np.sqrt(2*np.log(2))*np.sqrt(hbar/(mu*omegas))*10**10
    FWHM_b = 2*np.sqrt(2*np.log(2))*np.sqrt(hbar/((1/mu + Re2Ix)*omegab))*10**10
    SIcpl = max(np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[11])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[12])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[13])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[14])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[15])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[16])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[17])*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[18])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[19])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[20])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[21])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[22])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[23])*FWHM_s*FWHM_s, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[24])*FWHM_s*FWHM_s, 
                )
    BIcpl = max(np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[25])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[26])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[27])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[28])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[29])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[30])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[31])*FWHM_b*FWHM_b, 
                np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[32]), 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[33]), 
                np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[34]), 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[35]), 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[36]), 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[37]), 
                np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[38]),)
    SBIcpl = max(np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[39])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[40])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[41])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[42])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[43])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[44])/Re**6, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[45])/Re**6,
                 np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[46])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[47])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[48])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[49])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[50])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[51])/Re**8, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[52])/Re**8,
                 np.sqrt(1/(4*np.pi)*(2*1 + 1))*abs(pot_params[53])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[54])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*2 + 1))*abs(pot_params[55])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[56])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[57])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[58])/Re**10, 
                 np.sqrt(1/(4*np.pi)*(2*3 + 1))*abs(pot_params[59])/Re**10)
    
    x1 = np.linspace(-2.0, 2.0, 100)
    y1 = float(kzz)*(1 - np.exp(-float(az)*(x1) ))**2
    x2 = np.linspace(-2.0, 2.0, 100)
    y2 = float(barrier)*(np.cos(x2*np.pi) + 1)
    x3 = np.linspace(-2.0, 2.0, 100)
    y3 = float(kxx)*(x3)**2
    
    
    # Figure instance
    fig = plt.figure(dpi=45, figsize=(4,3), facecolor="#C0CEE8")
    # ax1
    ax1 = fig.add_subplot(111)
    ax1.plot(x1, y1)
    ax1.set_title('Stretch space', fontsize = "24")
    plt.hlines(shbaromega*(0 + 1/2) - shbaromega_chi*(0 + 1/2)**2, -1, 1, color="#5881C1")
    plt.hlines(shbaromega*(1 + 1/2) - shbaromega_chi*(1 + 1/2)**2, -1, 1, color="#5881C1")
    plt.hlines(shbaromega*(2 + 1/2) - shbaromega_chi*(2 + 1/2)**2, -1, 1, color="#5881C1")
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-2, 2)
    plt.ylim(-10, 500)
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.set_facecolor("#C0CEE8")
    canvas = FigureCanvasTkAgg(fig, tab_thr)  # Generate canvas instance, Embedding fig in root
    canvas.draw()
    canvas.get_tk_widget().place(x= 540, y=40)
    label = ttk.Label(tab_thr, text="strtch frequency: " + str(np.round(shbaromega, 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 550, y=170) 
    
    # Figure instance
    fig2 = plt.figure(dpi=45, figsize=(4,3), facecolor="#C0CEE8")
    # ax2
    ax2 = fig2.add_subplot(111)
    ax2.plot(x2, y2)
    ax2.set_title('Internal Rotation space', fontsize = "24")
    plt.hlines(0, -2, 2, color="#5881C1")
    plt.hlines(2*mol_params[1], -2, 2, color="#5881C1") 
    plt.hlines(6*mol_params[1], -2, 2, color="#5881C1") 
    plt.hlines(12*mol_params[1], -2, 2, color="#5881C1") 
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-2, 2)
    plt.ylim(-10, 500)
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    ax2.set_facecolor("#C0CEE8")
    canvas = FigureCanvasTkAgg(fig2, tab_thr)  # Generate canvas instance, Embedding fig in root
    canvas.draw()
    canvas.get_tk_widget().place(x= 370, y=250)
    label = ttk.Label(tab_thr, text="internal rotational barrier: " + str(np.round(2*barrier, 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 360, y=380) 
    
    # Figure instance
    fig3 = plt.figure(dpi=45, figsize=(4,3), facecolor="#C0CEE8")
    # ax1
    ax3 = fig3.add_subplot(111)
    ax3.plot(x3, y3)
    ax3.set_title('Bend space', fontsize = "24")
    plt.hlines(bhbaromega/2, -1, 1, color="#5881C1")
    plt.hlines(bhbaromega*(3/2), -1, 1, color="#5881C1") 
    plt.hlines(bhbaromega*(5/2), -1, 1, color="#5881C1")
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-2, 2)
    plt.ylim(-10, 500)
    ax3.set_xlabel('')
    ax3.set_ylabel('')
    ax3.set_facecolor("#C0CEE8")
    canvas = FigureCanvasTkAgg(fig3, tab_thr)  # Generate canvas instance, Embedding fig in root
    canvas.draw()
    canvas.get_tk_widget().place(x= 700, y=250)
    label = ttk.Label(tab_thr, text="bend frequency: " + str(np.round(bhbaromega, 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 710, y=380) 
    
    canvas1.create_line(
        630, 100, # 四角の左上
        450, 350,  # 四角の右下
        width = 2,  # 枠の幅E
    )
    canvas1.create_line(
        820, 350, # 四角の左上
        450, 350,  # 四角の右下
        width = 2,  # 枠の幅E
    )
    canvas1.create_line(
        820, 350, # 四角の左上
        630, 100,  # 四角の右下
        width = 2,  # 枠の幅E
    )
    label = ttk.Label(tab_thr, text="S-B cpl.: " + str(round(abs(sbhbaromega), 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 750, y=200) 
    label = ttk.Label(tab_thr, text="S-I cpl.: " + str(round(abs(SIcpl), 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 380, y=200) 
    label = ttk.Label(tab_thr, text="B-I cpl.: " + str(round(abs(BIcpl), 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 570, y=320) 
    label = ttk.Label(tab_thr, text="S-B-I cpl.: " + str(round(abs(SBIcpl), 0)) + " cm\u207B\u00B9", font=("Helvetica", "10", "normal"), background="#C0CEE8")
    label.place(x= 570, y=230) 

    #timer = Timer(tab_thr)
    time = estimated_time(dimension(int(txtBox_n0.get()), int(txtBox_nplsmns.get()), int(txtBox_nplsmns.get()), int(txtBox_j.get()), int(txtBox_m.get())))
    
    timer.hours = time//3600
    timer.minutes = round(time%3600//60)
    timer.seconds = round(time%3600%60)
    #timer.timer_running = True
    #thread1 = threading.Thread(target=timer.countdown())    #この状態だと計算が終わったあとにカウントダウンが始まる．
    #thread1.start()
    #thread1.join()
    label1 = ttk.Label(tab_thr, text="calculating" + "......", font=("Helvetica", "12", "normal"), background="#CFDAED")
    label1.place(x= 20, y=120) 

    return

# StringVarのインスタンスを格納する変数textの設定
text_start1 = tk.StringVar(tab_thr)
text_start1.set("1. Estimate time")
text_start2 = tk.StringVar(tab_thr)
text_start2.set(" 2. Start ")
button1 = tk.Button(tab_thr, textvariable=text_start1, command=lambda: [info(), timer.start_stop_timer()], font=("Helvetica", "16", "normal"), fg="black" , activeforeground="#006ab6", background="#A3B8DD")
button1.place(x=10, y=50)
button2 = tk.Button(tab_thr, textvariable=text_start2, command=calc, font=("Helvetica", "16", "normal"), fg="black" , activeforeground="#006ab6", background="#A3B8DD")
button2.place(x=215, y=50)

label = ttk.Label(tab_thr, text="State", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 20, y=100) 
label = ttk.Label(tab_thr, text="Calculation Data", font=("Helvetica", "12", "bold"), background="#CFDAED")
label.place(x= 20, y=180)

#プログレスバー
p = ttk.Progressbar(
    tab_thr,
    mode="indeterminate",   #非確定的
    )
p.place(x= 20, y=150) 


#右側
def show_eigen_value():
    text_value.set("Result_value.txt ↓")
    return
# StringVarのインスタンスを格納する変数textの設定
text_value = tk.StringVar(tab_thr)
text_value.set("show eigen value chart data")
button_val = tk.Button(tab_thr, textvariable=text_value, command=show_eigen_value, font=("Helvetica", "10", "normal"), fg="black" , activeforeground="#006ab6", background="#A3B8DD")
button_val.place(x=390, y=400)

def show_eigen_vector():
    text_vector.set("Result_vector.txt ↓")
    return
# StringVarのインスタンスを格納する変数textの設定
text_vector = tk.StringVar(tab_thr)
text_vector.set("show eigen vector chart data")
button_vec = tk.Button(tab_thr, textvariable=text_vector, command=show_eigen_vector, font=("Helvetica", "10", "normal"), fg="black" , activeforeground="#006ab6", background="#A3B8DD")
button_vec.place(x=620, y=400)





baseGround.protocol("WM_DELETE_WINDOW", lambda :quit_me(baseGround))

# ウィジェットの配置
notebook.pack(expand=True, fill='both', padx=10, pady=10)


baseGround.mainloop()