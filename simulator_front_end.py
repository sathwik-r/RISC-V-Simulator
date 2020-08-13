from tkinter import *
from tkinter import messagebox, scrolledtext
from tkinter.ttk import Combobox, Notebook

from converttomachinecode1 import *
from driver_step import myFunc
from error_handling import *
from predictor import pipeline_predictor_func
from stall_no_dataforwarding import stall_no_dataforwarding_func
from stalling_dataforwarding import stalling_dataforwarding_func
from unpipelined import unpipelined_func

registers = {}  # register dictionary
memory = {}  # memory
step_count = 0
blocks = []
run_var = 0
if __name__ == '__main__':
    for i in range(32):
        registers[i] = 0

    window = Tk()
    window.title('RISC-V Simulator')
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    var1 = StringVar()
    l = Label(window, bg='green', fg='yellow', font=('Arial', 20), width=20, text="RISC-V Editor & Simulator").grid(
        row=0,
        columnspan=17,
        pady=7)

    index = 1


    def popupmsg():
        popup = Tk()
        popup.wm_title("Statistics")
        txt = scrolledtext.ScrolledText(popup)
        txt.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.pack()
        file = open("Stats.txt", 'r')
        if file is not None:
            contents = file.read().splitlines()
            for line in contents:
                txt.insert(END, line + '\n')
        file.close()

        popup.mainloop()


    def updateRunOption(event):
        global run_var
        if runCombo.current() == 0:
            run_var = 0
        if runCombo.current() == 1:
            run_var = 1
        if runCombo.current() == 2:
            run_var = 2
        if runCombo.current() == 3:
            run_var = 3


    def step():
        global step_count
        # print(PC_Seq)
        lb.selection_clear(0, END)
        lb.selection_set(int(globalss.PC_Seq[step_count % len(PC_Seq)] / 4))
        lb.event_generate("<<ListboxSelect>>")

        for i in range(32):
            field[i].delete(0, END)
            field[i].insert(0, str(reg_step[step_count % len(PC_Seq)][i]))
        for i in range(64):
            field2[i].delete(0, END)
            field2[i].insert(0, str(memory_step[step_count % len(PC_Seq)][i]))

        step_count += 1


    def previous():
        global step_count
        step_count -= 1
        # print(PC_Seq)
        lb.selection_clear(0, END)
        lb.selection_set(int(globalss.PC_Seq[step_count % len(PC_Seq)] / 4))
        lb.event_generate("<<ListboxSelect>>")

        for i in range(32):
            field[i].delete(0, END)
            field[i].insert(0, str(reg_step[step_count % len(PC_Seq)][i]))
        for i in range(64):
            field2[i].delete(0, END)
            field2[i].insert(0, str(memory_step[step_count % len(PC_Seq)][i]))


    def run():
        #myFunc()
        if run_var == 0:
            unpipelined_func()
        elif run_var == 1:
            stall_no_dataforwarding_func()
        elif run_var == 2:
            stalling_dataforwarding_func()
        elif run_var == 3:
            pipeline_predictor_func()

        for i in range(32):
            registers[i] = globalss.register[i]
            print(registers[i])
            field[i].delete(0, END)
            field[i].insert(0, str(registers[i]))
        for i in range(64):
            field2[i].delete(0, END)
            field2[i].insert(0, str(globalss.memory_array[i]))

        messagebox.showinfo("Success",
                            "Code compilation successful. Machine code has been saved in machinecode.txt. Use the "
                            "editor to open it.")
        F.delete("1.0", END)
        D.delete("1.0", END)
        E.delete("1.0", END)
        W.delete("1.0", END)
        M.delete("1.0", END)
        file1 = open("Details.txt", 'r')
        if file1 is not NONE:
            contents1 = file1.read().splitlines()
            for line in contents1:
                parts = line.split()
                if (parts[0] == 'F'):
                    F.insert(END, line + "\n")
                if (parts[0] == 'D'):
                    D.insert(END, line + "\n")
                if (parts[0] == 'E'):
                    E.insert(END, line + "\n")
                if (parts[0] == 'W'):
                    W.insert(END, line + "\n")
                if (parts[0] == 'M'):
                    M.insert(END, line + "\n")
        file1.close()
        if run_var!= 0:
            popupmsg()


    def dump():
        file = open("store.txt", 'w')
        file.write("Register Values:\n")
        for i in range(32):
            str1 = "x" + str(i) + ": " + str(registers[i]) + "\n"
            file.write(str1)
        file.write("Stack Values Values:\n")
        for i in range(1000):
            str1 = str(1000 - i) + ": " + str(globalss.stack_array[i]) + "\n"
            file.write(str1)
        for i in range(1000):
            str1 = str(hex(268435456 + i)) + ": " + str(globalss.memory_array[i]) + "\n"
            file.write(str1)
        file.close()
        messagebox.showinfo("Success",
                            "Execution terminated, all reg, stack and memory values stored in store.txt")
        window.after(3500, lambda: window.destroy())


    def openfile():
        # file = filedialog.askopenfile(parent=window, title="Select a file",
        #     filetypes=(("ASM file", "*.asm"), ("All Files", "*.*")))
        file = open('assembly.txt', 'w')
        data = textArea.get('1.0', 'end' + '-1c')
        file.write(data)
        file.close()
        file = open('assembly.txt', 'r')
        if file is not None:
            contents = file.read().splitlines()
            addLine = FALSE
            for line in contents:
                if ".text" in line and addLine == FALSE:
                    addLine = TRUE
                    continue
                elif addLine == FALSE:
                    continue
                lb.insert('end', line)

            file.close()
            run()


    def repSelect(event):
        if w.current() == 0:
            for i in range(32):
                field[i].delete(0, END)
                field[i].insert(0, str(registers[i]))
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(globalss.memory_array[i]))

        if w.current() == 1:
            for i in range(32):
                field[i].delete(0, END)
                field[i].insert(0, str(chr(registers[i])))
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(chr(globalss.memory_array[i])))

        if w.current() == 2:
            for i in range(32):
                field[i].delete(0, END)
                field[i].insert(0, str(bin(registers[i])))
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(bin(globalss.memory_array[i])))

        if w.current() == 3:
            for i in range(32):
                field[i].delete(0, END)
                field[i].insert(0, str(hex(registers[i])))
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(hex(globalss.memory_array[i])))


    def jumpSelect(event):
        if z.current() == 0:
            for i in range(16):
                # label2[i] = Label(window, text=str(hex(268435456 + i * 4)))
                label2[i].config(text=str(hex(268435456 + i * 4)))
                # label2[i].grid(row=4 + i, column=2+6, padx=1, pady=0, sticky=E)
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(globalss.memory_array[i]))

        if z.current() == 1:
            for i in range(16):
                # label2[i] = Label(window, text=str(1000 - i * 4))
                # label2[i].grid(row=4 + i, column=2+6, padx=1, pady=0, sticky=E)
                label2[i].config(text=str(1000 - i * 4))
            for i in range(64):
                field2[i].delete(0, END)
                field2[i].insert(0, str(globalss.stack_array[1000 - i]))


    b1 = Button(window, text='Step', width=10, height=2, command=step)
    b1.grid(row=1, column=2, padx=2, pady=7)
    b2 = Button(window, text="Run", width=10, height=2, command=run)
    b2.grid(row=1, column=4, padx=2, pady=7)
    b3 = Button(window, text="Dump", width=10, height=2, command=dump)
    b3.grid(row=1, column=5, padx=2, pady=7)
    b4 = Button(window, text="Simulate", width=10, height=2, command=openfile)
    b4.grid(row=1, column=0, padx=2, pady=7)
    run_options = ['Unpipelined', 'Stall with No Data Forwarding', 'Stalling with Data Forwarding',
                   'Pipelined Predictor']
    var1 = StringVar(window)
    var1.set('Unpipelined')

    runCombo = Combobox(window, values=run_options, state="readonly")
    runCombo.grid(row=1, column=1)
    runCombo.current(0)
    runCombo.bind("<<ComboboxSelected>>", updateRunOption)
    b5 = Button(window, text="Previous", width=10, height=2, command=previous)
    b5.grid(row=1, column=3, pady=7)
    var2 = StringVar()
    var2.set((1, 2, 3, 4))

    textArea = scrolledtext.ScrolledText(window, height=40, width=30, padx=2)
    textArea.grid(row=2, column=0, rowspan=20, columnspan=2)
    scrollbar = Scrollbar(window)
    lb = Listbox(window, height=40, width=30)
    lb.grid(row=2, column=2 + 0, rowspan=20, columnspan=2, padx=5, pady=10)
    lb.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lb.yview)
    n = Notebook(window)
    n.grid(row=2, column=4, rowspan=10, columnspan=7)
    f1 = Frame(n, highlightbackground="red")  # first page, which would get widgets gridded into it
    f2 = Frame(n, highlightbackground="red")  # second page
    n.add(f1, text='Register')
    n.add(f2, text='Memory')
    # lb.pack()
    label = [Label()] * 32
    field = [Entry()] * 32
    l2 = Label(f1, text="Register Values")
    l2.grid(row=2, column=2 + 2, columnspan=2, sticky=W + E, padx=10)
    l3 = Label(f2, text="Memory Values")
    l3.grid(row=2, column=2 + 6, columnspan=2, padx=10)
    for i in range(32):
        if i < 16:
            label[i] = Label(f1, text="x" + str(i), width=5)
            label[i].grid(row=4 + i, column=2 + 2, padx=1, pady=3, sticky=E)
            field[i] = Entry(f1)
            field[i].grid(row=4 + i, column=2 + 3, padx=1, pady=3)
        else:
            label[i] = Label(f1, text="x" + str(i), width=5)
            label[i].grid(row=4 + i - 16, column=2 + 4, padx=1, pady=3, sticky=E)
            field[i] = Entry(f1)
            field[i].grid(row=4 + i - 16, column=2 + 5, padx=10, pady=3)
        # label[i].pack()
        # field[i].pack()
        label2 = [Label()] * 16
        field2 = [Entry()] * 64
        memlab0 = Label(f2, text="0")
        memlab0.grid(row=3, column=2 + 7)
        memlab1 = Label(f2, text="1")
        memlab1.grid(row=3, column=2 + 8)
        memlab2 = Label(f2, text="2")
        memlab2.grid(row=3, column=2 + 9)
        memlab3 = Label(f2, text="3")
        memlab3.grid(row=3, column=2 + 10)
    for i in range(16):
        label2[i] = Label(f2, text=str(hex(268435456 + i * 4)))
        label2[i].grid(row=4 + i, column=2 + 6, padx=1, pady=3, sticky=E)
        field2[4 * i] = Entry(f2)
        field2[4 * i].grid(row=4 + i, column=2 + 7, padx=2, pady=3)
        field2[4 * i + 1] = Entry(f2)
        field2[4 * i + 1].grid(row=4 + i, column=2 + 8, padx=2, pady=3)
        field2[4 * i + 2] = Entry(f2)
        field2[4 * i + 2].grid(row=4 + i, column=2 + 9, padx=2, pady=3)
        field2[4 * i + 3] = Entry(f2)
        field2[4 * i + 3].grid(row=4 + i, column=2 + 10, padx=2, pady=3)

    choices = ['Decimal', 'ASCII', 'Binary', 'Hexadecimal']
    variable = StringVar(window)
    variable.set('Decimal')

    w = Combobox(window, values=choices, state="readonly")
    w.grid(row=20, column=2 + 3)
    w.current(0)
    w.bind("<<ComboboxSelected>>", repSelect)
    repChoiceLabel = Label(window, text="Choose base:").grid(row=20, column=2 + 2)
    stackMemChoicLabel = Label(window, text="Jump To:").grid(row=20, column=2 + 6)
    z = Combobox(window, values=["memory", "stack"], state="readonly")
    z.grid(row=20, column=2 + 7)
    z.current(0)
    z.bind("<<ComboboxSelected>>", jumpSelect)

    FLab = Label(window, bg='red', text="Fetch", width=10)
    FLab.grid(row=3, column=11, columnspan=2)
    F = scrolledtext.ScrolledText(window, width=50, height=5)
    F.grid(row=3, column=13, rowspan=2)
    DLab = Label(window, bg='blue', text="Decode", width=10)
    DLab.grid(row=5, column=11, columnspan=2)
    D = scrolledtext.ScrolledText(window, width=50, height=5)
    D.grid(row=5, column=13, rowspan=2)
    ELab = Label(window, bg='green', text="Execute", width=10)
    ELab.grid(row=7, column=11, columnspan=2)
    E = scrolledtext.ScrolledText(window, width=50, height=5)
    E.grid(row=7, column=13, rowspan=2)
    MLab = Label(window, bg='yellow', text="Write", width=10)
    MLab.grid(row=9, column=11, columnspan=2)
    M = scrolledtext.ScrolledText(window, width=50, height=5)
    M.grid(row=9, column=13, rowspan=2)
    WLab = Label(window, bg='orange', text="Modify", width=10)
    WLab.grid(row=11, column=11, columnspan=2)
    W = scrolledtext.ScrolledText(window, width=50, height=5)
    W.grid(row=11, column=13, rowspan=2)
    window.mainloop()
