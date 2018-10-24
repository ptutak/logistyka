#!/usr/bin/python3

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
    def __init__(self, *args, rows=4, columns=4, strech=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.entries = {}
        for i in range(rows):
            for j in range(columns):
                self.entries[(i,j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i,j)])
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
        if strech:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
            for j in range(columns):
                self.columnconfigure(j, weight=1)

    def getCellValue(self, row, column):
        return self.entries[(row, column)]

    def setCellValue(self, row, column, value):
        self.entries[(row, column)].set(value)
    
    def getRows(self):
        return self.rows

    def getColumns(self):
        return self.columns
    
    def getRowsSum(self):
        rows = [0 for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                rows[i]+=self.entries[(i,j)].get()
        return rows
    
    def getColumnsSum(self):
        columns = [0 for i in range(self.columns)]
        for i in range(self.rows):
            for j in range(self.columns):
                columns[j]+=self.entries[(i,j)].get()
        return columns

    def getCellsSum(self):
        sum = 0
        for i in range(self.rows):
            for j in range(self.columns):
                sum += self.entries[(i,j)].get()
        return sum

    def addRow(self):
        entryVals = {}
        for k,v in self.entries.items():
            entryVals[k] = v
        self.rows += 1
        for i in range(self.rows):
            for j in range(self.columns):
                self.entries[(i,j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i,j)])
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i,j)].set(0)

    def updateTableSize(self, rows, columns, stretch=False):
        for child in self.winfo_children():
            child.destroy()
        self.entries = {}
        self.rows = rows
        self.columns = columns
        for i in range(rows):
            for j in range(columns):
                self.entries[(i,j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i,j)])
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i,j)].set(0)

        if stretch:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
            for j in range(columns):
                self.columnconfigure(j, weight=1)


class MenuButtons(tk.Frame):
    def __init__(self, *args, table, suppliers, receivers, log, **kwargs):
        super().__init__(*args,**kwargs)
        self.supplierNumber = tk.IntVar()
        self.receiverNumber = tk.IntVar()
        self.supplierNumberEntry = tk.Entry(self, textvariable=self.supplierNumber)
        self.supplierNumberEntry.grid(row=0, column=1)
        self.supplierNumberLabel = tk.Label(self, text='Supplier number:')
        self.receiverNumberEntry = tk.Entry(self, textvariable=self.receiverNumber)
        self.receiverNumberEntry.grid(row=1, column=1)
        self.updateTableBtn = tk.Button(self, text='Update Table')
        self.updateTableBtn.grid(row=2, column=0, columnspan=2)
        self.updateTableBtn.bind('<Button-1>', self.updateTableBtnAction)
        self.calculateBtn = tk.Button(self, text='Calculate')
        self.calculateBtn.grid(row=3, column=0, columnspan=2)
        self.calculateBtn.bind('<Button-1>', self.calculateBtnAction)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.supplierNumber.set(suppliers.getRows())
        self.receiverNumber.set(receivers.getColumns())
        self.table = table
        self.suppliers = suppliers
        self.receivers = receivers
        self.log = log
    def updateTableBtnAction(self, event):
        rowNumber = self.supplierNumber.get()
        columnNumber = self.receiverNumber.get()
        self.table.updateTableSize(rowNumber, columnNumber)
        self.suppliers.updateTableSize(rowNumber,1)
        self.receivers.updateTableSize(1,columnNumber)
    def calculateInitValues(self):
        supplierSum = self.suppliers.getCellsSum()
        receiversSum = self.receivers.getCellsSum()
        self.log.insertText('suppliers: {}'.format(supplierSum))
        self.log.insertText('receivers: {}'.format(receiversSum))
    def calculateBtnAction(self, event):
        self.calculateInitValues()





if __name__=='__main__':
    root = tk.Tk()
    log = Log(root)
    initTable = Table(root)
    initLabel = tk.Label(root, text='Dos\\Odb')
    suppliers = Table(root, rows=4, columns=1)
    receivers = Table(root, rows=1, columns=4)
    buttons = MenuButtons(root, table=initTable, suppliers=suppliers, receivers=receivers, log=log)
    initLabel.grid(row=0, column=0)
    suppliers.grid(row=1, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
    receivers.grid(row=0, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    initTable.grid(row=1, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    log.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.W+tk.S+tk.E)
    buttons.grid(row=0, column=2, rowspan=1, sticky=tk.N+tk.W+tk.S+tk.E)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.mainloop()
