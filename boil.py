#!/bin/python3

import tkinter as tk
from tkinter import ttk


class Log(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, rowspan=5, sticky=tk.N+tk.S)
        self.taskList = tk.StringVar()
        self.taskListBox = tk.Listbox(self, yscrollcommand=self.yScroll.set, listvariable=self.taskList)
        self.taskListBox.grid(row=0, column=0, rowspan=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.taskListBox.yview
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tasks = []

    def insertText(self, text, index=tk.END):
        self.taskListBox.insert(index, text)

    def insertTask(self, index, task):
        if index=='end':
            self.tasks.append(task)
        else:
            self.tasks.insert(index, task)
        self.taskListBox.insert(index, task)

    def putTasks(self, tasks):
        self.tasks=tasks
        for task in tasks:
            self.taskListBox.insert(tk.END,tuple(task))

    def curSelection(self):
        return self.taskListBox.curselection()

    def getTasks(self):
        return self.tasks

    def clearTasks(self):
        self.tasks=[]
        self.taskList.set('')


class Table(tk.Frame):
    def __init__(self, *args, rows, columns, strech=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.entries = {}
        for i in range(rows):
            for j in range(columns):
                self.entries[(i,j)] = tk.StringVar()
                entry = Entry(self, textvariable=self.entries[(i,j)])
                entry.grid(row=i, column=j)
        if strech:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
            for j in range(columns):
                self.columnconfigure(j, weight=1)

    def getCellValue(self, row, column):
        return self.entries[(row, column)]

    def setCellValue(self, row, column, value):
        self.entries[(row, column)].set(value)


class MenuButtons(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.supplierNumber = tk.IntVar()
        self.receiverNumber = tk.IntVar()
        self.supplierNumberEntry = tk.Entry(self, textvariable=self.supplierNumber)
        self.supplierNumberEntry.grid(row=0, column=0)
        self.receiverNumberEntry = tk.Entry(self, textvariable=self.receiverNumber)
        self.receiverNumberEntry.grid(row=0, column=1)
        self.updateTableBtn = tk.Button(self, text='Update Table')
        self.updateTableBtn.grid(row=1, column=0, columnspan=2)
        self.updateTableBtn.bind('<Button-1>', self.updateTableBtnAction)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.supplierNumber.set('Suppliers Number')
        self.receiverNumber.set('Receiver Number')
    
    def updateTableBtnAction(self, event):
        rowNumber = self.supplierNumber.get()
        columnNumber = self.receiverNumber.get()





if __name__=='__main__':
    root = tk.Tk()
    log=Log(root)
    log.grid(row=1,column=0,sticky=tk.N+tk.W+tk.S+tk.E)
    
    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=1)
    root.grid_rowconfigure(1,weight=1)
    root.mainloop()
