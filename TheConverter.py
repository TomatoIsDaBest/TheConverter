from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from ScrollableNotebook import *
import requests
import win32api
import threading
import webbrowser

__author__ = 'Phúc Bảo'
__credits__ = ['Phúc Bảo']
__version__ = '1.0'
__maintainer__ = 'Phúc Bảo'
__email__ = 'phucbaonn@gmail.com'
__status__ = 'Beta'

_AppName_ = 'The Converter'


######==============================https://convertlive.com/

window = Tk()
window.resizable(0,0)
window.title("The Converter 1.0")
window.geometry("600x300")
window.iconbitmap("logo.ico")


notebook = ScrollableNotebook(window, wheelscroll = True, tabmenu = True)
frame1=Frame(notebook)
frame2=Frame(notebook)
frame3=Frame(notebook)
frame4=Frame(notebook)
frame5 = Frame(notebook)
frame6 = Frame(notebook)
frame7 = Frame(notebook)
notebook.add(frame1,text="Money Converter")
notebook.add(frame2,text="Temperature Converter")
notebook.add(frame3,text="Length Converter")
notebook.add(frame4,text="Data size Converter")
notebook.add(frame5,text="Weight Converter")
notebook.add(frame6, text = "BMI Caculate")
notebook.add(frame7,text="About this software")
notebook.pack(fill = BOTH, expand = True)

class UpdateApp:
    def check_update():
        try:
            response = requests.get("ttps://github.com/TomatoIsDaBest/TheConverter")
            data = response.text

            if float(data) > float(__version__):
                messagebox.showinfo("Software Update", "Update Available!")
                mb1 = messagebox.askyesno("Update!", f{_AppName_} {__version__} "needs to update to version" {data})

#==========================================================================BMI====================================================

class BMI:   
    def bmi_caculate(self): 
        kg = int(self.weight_textbox.get())
        met = int(self.height_textbox.get()) / 100
        chi_so_bmi = kg/(met*met)
        chi_so_bmi = round(chi_so_bmi, 3)
        self.bmi_result(chi_so_bmi)
        
    def bmi_result(self, chi_so_bmi):
        if chi_so_bmi < 18.5:
            self.result_label.config(text = str(chi_so_bmi) + " " + " is underweight")
        elif chi_so_bmi >= 18.6 and chi_so_bmi < 24.9:
            self.result_label.config(text = str(chi_so_bmi) + " " + " is normal")
        elif chi_so_bmi >= 25 and chi_so_bmi <= 29.9:
            self.result_label.config(text = str(chi_so_bmi) + " " + " is overweight")
        elif chi_so_bmi >= 30 and chi_so_bmi <= 34.9:
            self.result_label.config(text = str(chi_so_bmi) + " " + " is obese")
        elif chi_so_bmi >= 35:
            self.result_label.config(text = str(chi_so_bmi) + " " + " is extremely obese")

    def reset(self):
        self.weight_textbox.delete(0, END)
        self.height_textbox.delete(0, END)

    def what_is_bmi(self):
        messagebox.showinfo("What's BMI?", "Body mass index, also known as body mass index.\nCommonly known as BMI by the English name\nbody mass index, is a way of determining whether a person's\nbody is thin or fat by an index. This index was\nproposed by Belgian scientist Adolphe Quetelet in 1832.")

    def __init__(self, master):
        self.master = LabelFrame(master, text = "BMI Caculate", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = True)
       
        self.label_height = Label(self.master, text = "Enter height (cm) ")
        self.label_height.place(x = 20, y = 10)
        self.height_textbox = Entry(self.master, width = 60)
        self.height_textbox.place(x = 170, y = 10)

        self.result_label = Label(self.master, text = "Result", font = (14))
        self.result_label.place(x = 230, y = 130)

        self.label_weight = Label(self.master, text = "Enter weight (kg) ")
        self.label_weight.place(x = 20, y = 40)
        self.weight_textbox = Entry(self.master, width = 60)
        self.weight_textbox.place(x = 170, y = 40)       

        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Caculate", command = self.bmi_caculate, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)
   


#===========================================MONEY CONVERTER=======================================================

class RealTimeCurrencyConverter:
    def __init__(self, url):       
        self.data = requests.get(url).json()
        self.currencies = self.data["rates"]        

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 

        if from_currency != 'USD': 
            amount = amount / self.currencies[from_currency] 
    
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)

class MoneyConvert: 

    def reset(self):
        self.dollar_textbox.delete(0, END)

    def perform(self):
        amount = float(self.dollar_textbox.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()
 
        converted_amount= self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 5)
     
        self.converted_amount_field_label.config(text = str(converted_amount) + " " + self.chon_don_vi2.get())        

    def __init__(self, master):   
        self.master = master
        
        self.currency_converter = converter

        self.master = LabelFrame(self.master, text = "Money Converter", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = YES)

        self.from_currency_variable = StringVar()
        self.from_currency_variable.set("USD")
        self.to_currency_variable = StringVar()
        self.to_currency_variable.set("EUR")   

        
        self.chon_don_vi1 = Combobox(self.master, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), state = 'readonly', width = 20, justify = CENTER)
        
        self.chon_don_vi1.place(x = 420, y = 10)

        self.chon_don_vi2 = Combobox(self.master, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), state = 'readonly', width = 20, justify = CENTER)
        
        self.chon_don_vi2.place(x = 420, y = 40)
        
        self.date_label = Label(self.master, text = f"Date : {self.currency_converter.data['date']}", bd = 5)
        self.date_label.place(x = 480, y = 230)
        self.converted_amount_field_label = Label(self.master, text = 'Result', fg = 'black', relief = FLAT, justify = CENTER, bd = 0, font = (14))
        self.converted_amount_field_label.place(x = 230, y = 130)
        self.label_dollar = Label(self.master, text = "Convert")
        self.label_dollar.place(x = 20, y = 10)
        self.label_choose_unit = Label(self.master, text = "To")
        self.label_choose_unit.place(x = 20, y = 40)        

        self.dollar_textbox = Entry(self.master, width = 50)
        self.dollar_textbox.place(x = 100, y = 10)        
        
        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Convert", command = self.perform, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)


#==========================================CONVERT TEMPERATURE==============================================

class ConvertTemp:
    def convert(self):
        temp = float(self.temp_textbox.get())
        self.don_vi_de_tinh1 = str(self.chon_don_vi_can_chuyen_doi.get())
        self.don_vi_de_tinh2 = str(self.chon_don_vi_bi_chuyen_doi.get())
        # độ c sang độ f
        if self.don_vi_de_tinh1 == "C" and self.don_vi_de_tinh2 == "F":
            kq = temp * 1.8 + 32
            kq = round(kq, 4)
            self.result(kq)
        # độ f sang độ c
        elif self.don_vi_de_tinh1.strip() == "F" and self.don_vi_de_tinh2 == "C":
            kq = (temp - 32) / 1.8
            kq = round(kq, 4)
            self.result(kq)

        # độ c sang độ k
        elif self.don_vi_de_tinh1.strip() == "C" and self.don_vi_de_tinh2 == "K":
            kq = temp + 273.15
            kq = round(kq, 4)
            self.result(kq)
        # độ k sang độ c
        elif self.don_vi_de_tinh1.strip() == "K" and self.don_vi_de_tinh2 == "C":
            kq = temp - 273.15
            kq = round(kq, 4)
            self.result(kq)

        # độ f sang độ k
        elif self.don_vi_de_tinh1.strip() == "F" and self.don_vi_de_tinh2 == "K":
            kq = ((temp - 32) / 1.8) + 273.15 
            kq = round(kq, 4)
            self.result(kq)
        # độ k sang độ f
        elif self.don_vi_de_tinh1.strip() == "K" and self.don_vi_de_tinh2 == "F":
            kq = ((temp - 273.15) * 1.8) + 32
            kq = round(kq, 4)
            self.result(kq)


    def result(self, kq):
        self.result_label.config(text = str(kq) + " " + self.chon_don_vi_bi_chuyen_doi.get())

    def reset(self):
        self.temp_textbox.delete(0, END)

    def __init__(self, master):
        self.master = LabelFrame(master, text = "Temperature Converter", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = YES)
        

        self.don_vi = StringVar()
        self.chon_don_vi_can_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_can_chuyen_doi["values"] = ("C", "F", "K")
        self.chon_don_vi_can_chuyen_doi.current(0)
        self.chon_don_vi_can_chuyen_doi.place(x = 420, y = 10)

        self.chon_don_vi_bi_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_bi_chuyen_doi["values"] = ("C", "F", "K")
        self.chon_don_vi_bi_chuyen_doi.current(1)
        self.chon_don_vi_bi_chuyen_doi.place(x = 420, y = 40)        

        self.label_temp = Label(self.master, text = "Convert")
        self.label_temp.place(x = 20, y = 10)
        self.label_choose_unit = Label(self.master, text = "To")
        self.label_choose_unit.place(x = 20, y = 40)
        self.result_label = Label(self.master, text = "Result", font = (14))
        self.result_label.place(x = 230, y = 130)

        self.temp_textbox = Entry(self.master, width = 50)
        self.temp_textbox.place(x = 100, y = 10)

        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Convert", command = self.convert, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)

class LengthConvert:
    def convert(self):
        lenght = float(self.lenght_textbox.get())
        self.don_vi_de_tinh1 = str(self.chon_don_vi_can_chuyen_doi.get())
        self.don_vi_de_tinh2 = str(self.chon_don_vi_bi_chuyen_doi.get())
        #cm sang in
        if self.don_vi_de_tinh1.strip() == "CM" and self.don_vi_de_tinh2 == "IN":
            kq = lenght / 2.54
            kq = round(kq, 4)
            self.result(kq)
        #cm sang ft
        elif self.don_vi_de_tinh1.strip() == "CM" and self.don_vi_de_tinh2 == "FT":
            kq = lenght / 30.48
            kq = round(kq, 4)
            self.result(kq)
        # cm sang m
        elif self.don_vi_de_tinh1.strip() == "CM" and self.don_vi_de_tinh2 == "M":
            kq = lenght / 100
            kq = round(kq, 4)
            self.result(kq)
        #cm sang km
        elif self.don_vi_de_tinh1.strip()  == "CM" and self.don_vi_de_tinh2 == "KM":
            kq = lenght / 1000000
            kq = round(kq, 4)
            self.result(kq)
        #in sang cm
        elif self.don_vi_de_tinh1.strip() == "IN" and self.don_vi_de_tinh2 == "CM":
            kq = lenght * 2.54
            kq = round(kq, 4)
            self.result(kq)
        #in sang ft
        elif self.don_vi_de_tinh1.strip() == "IN" and self.don_vi_de_tinh2 == "FT":
            kq = lenght / 12
            kq = round(kq, 4)
            self.result(kq)
        #in sang m
        elif self.don_vi_de_tinh1.strip() == "IN" and self.don_vi_de_tinh2 == "M":
            kq = lenght / 39.37
            kq = round(kq, 4)
            self.result(kq)
        #in sang km
        elif self.don_vi_de_tinh1.strip() == "IN" and self.don_vi_de_tinh2 == "KM":
            kq = lenght / 39370.0787
            kq = round(kq, 4)
            self.result(kq)
        #ft sang cm
        elif self.don_vi_de_tinh1.strip() == "FT" and self.don_vi_de_tinh2 == "CM":
            kq = lenght * 30.48
            kq = round(kq, 4)
            self.result(kq)
        #ft sang in
        elif self.don_vi_de_tinh1.strip() == "FT" and self.don_vi_de_tinh2 == "IN":
            kq = lenght * 12
            kq = round(kq, 4)
            self.result(kq)
        #ft sang m
        elif self.don_vi_de_tinh1.strip() == "FT" and self.don_vi_de_tinh2 == "M":
            kq = lenght / 3.2808
            kq = round(kq, 4)
            self.result(kq)
        #ft sang km
        elif self.don_vi_de_tinh1.strip() == "FT" and self.don_vi_de_tinh2 == "KM":
            kq = lenght / 3280.8399
            kq = round(kq, 4)
            self.result(kq)
        #m sang cm
        elif self.don_vi_de_tinh1.strip() == "M" and self.don_vi_de_tinh2 == "CM":
            kq = lenght * 100
            kq = round(kq, 4)
            self.result(kq)
        #m sang in
        elif self.don_vi_de_tinh1.strip() == "M" and self.don_vi_de_tinh2 == "IN":
            kq = lenght * 39.37
            kq = round(kq, 4)
            self.result(kq)
        #m sang ft
        elif self.don_vi_de_tinh1.strip() == "M" and self.don_vi_de_tinh2 == "FT":
            kq = lenght * 3.2808
            kq = round(kq, 4)
            self.result(kq)
        #m sang km
        elif self.don_vi_de_tinh1.strip() == "M" and self.don_vi_de_tinh2 == "KM":
            kq = lenght / 1000
            kq = round(kq, 4)
            self.result(kq)        
        #km sang cm
        elif self.don_vi_de_tinh1.strip() == "KM" and self.don_vi_de_tinh2 == "CM":
            kq = lenght * 1000000
            kq = round(kq, 4)
            self.result(kq)
        #km sang in        
        elif self.don_vi_de_tinh1.strip() == "KM" and self.don_vi_de_tinh2 == "IN":
            kq = lenght * 39370.0787
            kq = round(kq, 4)
            self.result(kq)
        #km sang ft
        elif self.don_vi_de_tinh1.strip() == "KM" and self.don_vi_de_tinh2 == "FT":
            kq = lenght * 3280.8399
            kq = round(kq, 4)
            self.result(kq)
        #km sang m
        elif self.don_vi_de_tinh1.strip() == "KM" and self.don_vi_de_tinh2 == "M":
            kq = lenght * 1000
            kq = round(kq, 4)
            self.result(kq)

    def result(self, kq):       
        self.result_label.config(text = str(kq) + " " + self.don_vi_de_tinh2)
        
    def reset(self):
        self.lenght_textbox.delete(0, END)

    def __init__(self, master):
        self.master = master        

        self.master = LabelFrame(master, text = "Length Converter", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = YES)

        self.don_vi = StringVar()
        self.chon_don_vi_can_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_can_chuyen_doi["values"] = ("CM", "IN", "FT", "M", "KM")
        self.chon_don_vi_can_chuyen_doi.current(0)
        self.chon_don_vi_can_chuyen_doi.place(x = 420, y = 10)

        self.chon_don_vi_bi_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_bi_chuyen_doi["values"] = ("CM", "IN", "FT", "M", "KM")
        self.chon_don_vi_bi_chuyen_doi.current(1)
        self.chon_don_vi_bi_chuyen_doi.place(x = 420, y = 40)      

        self.label = Label(self.master, text = "Convert")
        self.label.place(x = 20, y = 10)
        self.label_choose_unit = Label(self.master, text = "To")
        self.label_choose_unit.place(x = 20, y = 40)
        self.result_label = Label(self.master, text = "Result", font = (14), bd = 0)
        self.result_label.place(x = 230, y = 130)

        self.lenght_textbox = Entry(self.master, width = 50)
        self.lenght_textbox.place(x = 100, y = 10)

        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Convert", command = self.convert, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)

class DataConvert:    
    def convert(self):
        data = float(self.data_textbox.get())
        self.don_vi_de_tinh1 = str(self.chon_don_vi_can_chuyen_doi.get())
        self.don_vi_de_tinh2 = str(self.chon_don_vi_bi_chuyen_doi.get())
        #byte sang bit
        if self.don_vi_de_tinh1.strip() == "BYTE" and self.don_vi_de_tinh2 == "BIT":
            kq = data * 8
            kq = round(kq, 4)
            self.result(kq)
        #byte sang kb
        elif self.don_vi_de_tinh1.strip() == "BYTE" and self.don_vi_de_tinh2 == "KB":
            kq = data / 1024
            kq = round(kq, 4)
            self.result(kq)
        #byte sang mb
        elif self.don_vi_de_tinh1.strip() == "BYTE" and self.don_vi_de_tinh2 == "MB":
            kq = data / 1048576
            kq = round(kq, 4)
            self.result(kq)
        #byte sang gb
        elif self.don_vi_de_tinh1.strip() == "BYTE" and self.don_vi_de_tinh2 == "GB":
            kq = data / 1073741824
            kq = round(kq, 4)
            self.result(kq)
        #byte sang tb
        elif self.don_vi_de_tinh1.strip() == "BYTE" and self.don_vi_de_tinh2 == "TB":
            kq = data / 1099511627776
            kq = round(kq, 4)
            self.result(kq)
        
        #kb sang byte
        elif self.don_vi_de_tinh1.strip() == "KB" and self.don_vi_de_tinh2 == "BYTE":
            kq = data * 1024
            kq = round(kq, 4)
            self.result(kq)
        #kb sang mb
        elif self.don_vi_de_tinh1.strip() == "KB" and self.don_vi_de_tinh2 == "MB":
            kq = data / 1024
            kq = round(kq, 4)
            self.result(kq)
        #kb sang gb
        elif self.don_vi_de_tinh1.strip() == "KB" and self.don_vi_de_tinh2 == "GB":
            kq = data / 1048576
            kq = round(kq, 4)
            self.result(kq)
        #kb sang tb
        elif self.don_vi_de_tinh1.strip() == "KB" and self.don_vi_de_tinh2 == "TB":
            kq = data / 1073741824
            kq = round(kq, 4)
            self.result(kq)
       
        #mb sang byte
        elif self.don_vi_de_tinh1.strip() == "MB" and self.don_vi_de_tinh2 == "BYTE":
            kq = data * 1048576
            kq = round(kq, 4)
            self.result(kq)
        #mb sang kb
        elif self.don_vi_de_tinh1.strip() == "MB" and self.don_vi_de_tinh2 == "KB":
            kq = data * 1024
            kq = round(kq, 4)
            self.result(kq)
        #mb sang gb
        elif self.don_vi_de_tinh1.strip() == "MB" and self.don_vi_de_tinh2 == "GB":
            kq = data / 1024
            kq = round(kq, 4)
            self.result(kq)
        #mb sang tb
        elif self.don_vi_de_tinh1.strip() == "MB" and self.don_vi_de_tinh2 == "TB":
            kq = data / 1048576
            kq = round(kq, 4)
            self.result(kq)
        
        #gb sang byte
        elif self.don_vi_de_tinh1.strip() == "GB" and self.don_vi_de_tinh2 == "BYTE":
            kq = data * 1073741824
            kq = round(kq, 4)
            self.result(kq)
        #gb sang kb
        elif self.don_vi_de_tinh1.strip() == "GB" and self.don_vi_de_tinh2 == "BB":
            kq = data * 1048576
            kq = round(kq, 4)
            self.result(kq)
        #gb sang mb
        elif self.don_vi_de_tinh1.strip() == "GB" and self.don_vi_de_tinh2 == "MB":
            kq = data * 1024
            kq = round(kq, 4)
            self.result(kq)
        #gb sang tb
        elif self.don_vi_de_tinh1.strip() == "GB" and self.don_vi_de_tinh2 == "TB":
            kq = data / 1024
            kq = round(kq, 4)
            self.result(kq)
        #tb sang byte
        elif self.don_vi_de_tinh1.strip() == "TB" and self.don_vi_de_tinh2 == "BYTE":
            kq = data * 1099511627776
            kq = round(kq, 4)
            self.result(kq)
        #tb sang kb
        elif self.don_vi_de_tinh1.strip() == "TB" and self.don_vi_de_tinh2 == "KB":
            kq = data * 1073741824
            kq = round(kq, 4)
            self.result(kq)
        #tb sang mb
        elif self.don_vi_de_tinh1.strip() == "TB" and self.don_vi_de_tinh2 == "MB":
            kq = data * 1048576
            kq = round(kq, 4)
            self.result(kq)
        #tb sang gb
        elif self.don_vi_de_tinh1.strip() == "TB" and self.don_vi_de_tinh2 == "GB":
            kq = data * 1024
            kq = round(kq, 4)
            self.result(kq)

    def result(self, kq):
        self.result_label.config(text = str(kq) + " " + self.chon_don_vi_bi_chuyen_doi.get())

    def reset(self):
        self.data_textbox.delete(0, END)

    def __init__(self, master):
        self.master = master

        self.master = LabelFrame(master, text = "Data Size Converter", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = YES)

        self.don_vi = StringVar()
        self.chon_don_vi_can_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_can_chuyen_doi["values"] = ("Byte", "Bit", "KB", "MB", "GB", "TB")
        self.chon_don_vi_can_chuyen_doi.current(0)
        self.chon_don_vi_can_chuyen_doi.place(x = 420, y = 10)

        self.chon_don_vi_bi_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_bi_chuyen_doi["values"] = ("Byte", "Bit", "KB", "MB", "GB", "TB")
        self.chon_don_vi_bi_chuyen_doi.current(1)
        self.chon_don_vi_bi_chuyen_doi.place(x = 420, y = 40)        

        self.label = Label(self.master, text = "Convert")
        self.label.place(x = 20, y = 10)
        self.label_choose_unit = Label(self.master, text = "To")
        self.label_choose_unit.place(x = 20, y = 40)
        self.result_label = Label(self.master, text = "Result", font = (14))
        self.result_label.place(x = 230, y = 130)

        self.data_textbox = Entry(self.master, width = 50)        
        self.data_textbox.place(x = 100, y = 10)

        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Convert", command = self.convert, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)

class WeightConverter:
    def convert(self):
        weight = float(self.weight_textbox.get())
        self.don_vi_de_tinh1 = str(self.chon_don_vi_can_chuyen_doi.get())
        self.don_vi_de_tinh2 = str(self.chon_don_vi_bi_chuyen_doi.get())
        #mg sang g
        if self.don_vi_de_tinh1.strip() == "MG" and self.don_vi_de_tinh2 == "G":
            kq = weight / 1000
            kq = round(kq, 4)
            self.result(kq)
        #mg sang kg
        elif self.don_vi_de_tinh1.strip() == "MG" and self.don_vi_de_tinh2 == "KG":
            kq = weight / 1000000
            kq = round(kq, 4)
            self.result(kq)
        #mg sang t
        elif self.don_vi_de_tinh1.strip() == "MG" and self.don_vi_de_tinh2 == "T":
            kq = weight / 1000000000
            kq = round(kq, 4)
            self.result(kq)
        #g sang mg
        elif self.don_vi_de_tinh1.strip() == "G" and self.don_vi_de_tinh2 == "MG":
            kq = weight * 1000
            kq = round(kq, 4)
            self.result(kq)
        #g sang kg
        elif self.don_vi_de_tinh1.strip() == "G" and self.don_vi_de_tinh2 == "KG":
            kq = weight / 1000
            kq = round(kq, 4)
            self.result(kq)
        #g sang t
        elif self.don_vi_de_tinh1.strip() == "G" and self.don_vi_de_tinh2 == "T":
            kq = weight / 1000000
            kq = round(kq, 4)
            self.result(kq)
        #kg sang mg
        elif self.don_vi_de_tinh1.strip() == "KG" and self.don_vi_de_tinh2 == "MG":
            kq = weight * 1000000
            kq = round(kq, 4)
            self.result(kq)
        #kg sang g
        elif self.don_vi_de_tinh1.strip() == "KG" and self.don_vi_de_tinh2 == "G":
            kq = weight * 1000
            kq = round(kq, 4)
            self.result(kq)
        #kg sang t
        elif self.don_vi_de_tinh1.strip() == "KG" and self.don_vi_de_tinh2 == "T":
            kq = weight / 1000
            kq = round(kq, 4)
            self.result(kq)
        #t sang mg
        elif self.don_vi_de_tinh1.strip() == "T" and self.don_vi_de_tinh2 == "MG":
            kq = weight * 1000000000
            kq = round(kq, 4)
            self.result(kq)
        #t sang g
        elif self.don_vi_de_tinh1.strip() == "T" and self.don_vi_de_tinh2 == "G":
            kq = weight * 1000000
            kq = round(kq, 4)
            self.result(kq)
        #t sang kg
        elif self.don_vi_de_tinh1.strip() == "T" and self.don_vi_de_tinh2 == "KG":
            kq = weight * 1000
            kq = round(kq, 4)
            self.result(kq)


    def result(self, kq):
        self.result_label.config(text = str(kq) + " " + self.don_vi_de_tinh2)

    def reset(self):
        self.weight_textbox.delete(0, END)

    def __init__(self, master):
        self.master = master
        
        self.master = LabelFrame(master, text = "Weight Converter", font = (16))
        self.master.config(relief = FLAT)
        self.master.pack(fill = BOTH, expand = YES)

        self.don_vi = StringVar()
        self.chon_don_vi_can_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_can_chuyen_doi["values"] = ("MG", "G", "KG", "T")
        self.chon_don_vi_can_chuyen_doi.current(0)
        self.chon_don_vi_can_chuyen_doi.place(x = 420, y = 10)
        
        self.chon_don_vi_bi_chuyen_doi = Combobox(self.master, width = 20, justify = CENTER, state = "readonly")
        self.chon_don_vi_bi_chuyen_doi["values"] = ("MG", "G", "KG", "T")
        self.chon_don_vi_bi_chuyen_doi.current(1)
        self.chon_don_vi_bi_chuyen_doi.place(x = 420, y = 40)      

        self.label = Label(self.master, text = "Convert")
        self.label.place(x = 20, y = 10)
        self.label_choose_unit = Label(self.master, text = "To")
        self.label_choose_unit.place(x = 20, y = 40)
        self.result_label = Label(self.master, text = "Result", font = (14))
        self.result_label.place(x = 230, y = 130)

        self.weight_textbox = Entry(self.master, width = 50)        
        self.weight_textbox.place(x = 100, y = 10)

        self.reset_button = Button(self.master, text = "Clear", command = self.reset, width = 12)
        self.reset_button.place(x = 5, y = 225)
        self.convert_button = Button(self.master, text = "Convert", command = self.convert, width = 23)
        self.convert_button.place(x = 180, y = 80)
        self.exit_button = Button(self.master, text = "Exit", command = window.destroy)
        self.exit_button.place(x = 120, y = 225)

def AboutSoftware():
    messagebox.showinfo("About this software", "I started to make this software on 22th January.\nI think I just make a BMI Converter but I have so much ideas so I made this software")
def AboutMe():
    messagebox.showinfo("About me", "I'm from VietNam\nI am currently studying at Nui Sap town secondary school.")

money_convert = MoneyConvert(frame1) 

convert_temp = ConvertTemp(frame2) 

lenght_convert = LengthConvert(frame3)

data_convert = DataConvert(frame4)

weight_convert = WeightConverter(frame5)

bmi = BMI(frame6)

thanks_for_using_label = Label(frame7, text = "Thank you for using my software! :)\nDev by Phúc Bảo 12 years old.", font = (10))
thanks_for_using_label.pack(expand = True)

email_label = Entry(frame7, width = 31, bd = 0)

email_label.insert(0, "My Gmail phucbaonn@gmail.com")
email_label.config(state = "readonly")
email_label.pack(expand = True)

about_software = Button(frame7, text = "About this\nsoftware", command = AboutSoftware)
about_software.place(x = 2, y = 233)

about_me = Button(frame7, text = "About me", command = AboutMe)
about_me.place(x = 530, y = 248)


window.mainloop()