from tkinter import *
from tkinter import messagebox as mb


def check1():
    global s
    s = entry.get()
    if s.isdigit() == False:
        mb.showerror("Ошибка", "Должно быть введено число")
    else:
        entry.delete(0, END)
        label['text'] = s
        frame2.destroy()



def Enter_Digit():
    global entry
    global label
    global frame2

    frame2 = Tk()
    frame2.geometry("150x150")
    frame2.title('Enter')
    entry = Entry(frame2)
    Label_left = Label(frame2, text='Сколько мест выделяем?')
    Label_left.pack(side="top")
    entry.pack(pady=10)
    Button(frame2, text='Ввод', command=check1).pack()
    label = Label(frame2, height=5, width=30)
    label.pack()
    frame2.mainloop(1)

    return s
