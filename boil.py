#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from prettytable import PrettyTable


class Log(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, rowspan=5, sticky=tk.N+tk.S)
        self.log = tk.StringVar()
        self.logListBox = tk.Listbox(self, yscrollcommand=self.yScroll.set, listvariable=self.log, font=("Courier", 10))
        self.logListBox.grid(row=0, column=0, rowspan=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.logListBox.yview
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.tasks = []

    def insertText(self, text, index=tk.END):
        self.logListBox.insert(index, text)
        self.logListBox.yview(tk.END)

    def pushArray(self, array):
        for line in array:
            self.logListBox.insert(tk.END, line)
        self.logListBox.yview(tk.END)

    def curSelection(self):
        return self.logListBox.curselection()

    def clear(self):
        self.log.set('')


class Table(tk.Frame):
    def __init__(self, *args, rows=4, columns=4, stretch=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.entries = {}
        self.entryWidth = 10
        for i in range(rows):
            for j in range(columns):
                self.entries[(i, j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
        if stretch:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
            for j in range(columns):
                self.columnconfigure(j, weight=1)

    def __getitem__(self, index):
        return self.entries[index].get()

    def __setitem__(self, index, value):
        self.entries[index].set(value)

    def findMinValue(self):
        minV = self[(0, 0)]
        minI = (0, 0)
        for i in range(self.rows):
            for j in range(self.columns):
                if self[(i, j)] < minV:
                    minV = self[(i, j)]
                    minI = (i, j)
        return (minI, minV)

    def getCellValue(self, row, column):
        return self.entries[(row, column)].get()

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
                rows[i] += self.entries[(i, j)].get()
        return rows

    def getColumnsSum(self):
        columns = [0 for i in range(self.columns)]
        for i in range(self.rows):
            for j in range(self.columns):
                columns[j] += self.entries[(i, j)].get()
        return columns

    def getCellsSum(self):
        sum = 0
        for i in range(self.rows):
            for j in range(self.columns):
                sum += self.entries[(i, j)].get()
        return sum

    def addRows(self, rowNum):
        prevRowNum = self.rows
        self.rows += rowNum
        for i in range(prevRowNum, self.rows):
            for j in range(self.columns):
                self.entries[(i, j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i, j)].set(0)

    def addColumns(self, columnNum):
        prevColumnNum = self.columns
        self.columns += columnNum
        for i in range(self.rows):
            for j in range(prevColumnNum, self.columns):
                self.entries[(i, j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i, j)].set(0)

    def updateTableSize(self, rows, columns, stretch=False):
        oldEntries = self.entries
        for child in self.winfo_children():
            child.destroy()
        self.entries = {}
        self.rows = rows
        self.columns = columns
        for i in range(rows):
            for j in range(columns):
                if (i, j) in oldEntries:
                    self.entries[(i, j)] = oldEntries[(i, j)]
                else:
                    self.entries[(i, j)] = tk.IntVar()
                    self.entries[(i, j)].set(0)
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
        if stretch:
            for i in range(rows):
                self.rowconfigure(i, weight=1)
            for j in range(columns):
                self.columnconfigure(j, weight=1)


class MenuButtons(tk.Frame):
    def __init__(self, *args, table, suppliers, receivers, log, **kwargs):
        super().__init__(*args, **kwargs)
        self.supplierNumber = tk.IntVar()
        self.receiverNumber = tk.IntVar()
        self.supplierNumberEntry = tk.Entry(self, textvariable=self.supplierNumber, width=5)
        self.supplierNumberEntry.grid(row=0, column=1)
        self.supplierNumberLabel = tk.Label(self, text='Supplier number:')
        self.supplierNumberLabel.grid(row=0, column=0)
        self.receiverNumberEntry = tk.Entry(self, textvariable=self.receiverNumber, width=5)
        self.receiverNumberEntry.grid(row=1, column=1)
        self.receiverNumberLabel = tk.Label(self, text='Receiver number:')
        self.receiverNumberLabel.grid(row=1, column=0)
        self.updateTableBtn = tk.Button(self, text='Update Table')
        self.updateTableBtn.grid(row=2, column=0, columnspan=2)
        self.updateTableBtn.bind('<Button-1>', self.updateTableBtnAction)
        self.calculateBtn = tk.Button(self, text='Calculate')
        self.calculateBtn.grid(row=3, column=0, columnspan=2)
        self.calculateBtn.bind('<Button-1>', self.calculateBtnAction)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.supplierNumber.set(suppliers.getRows())
        self.receiverNumber.set(receivers.getColumns())
        self.table = table
        self.suppliers = suppliers
        self.receivers = receivers
        self.log = log
        self.stepTable = None

    def updateTableBtnAction(self, event):
        rowNumber = self.supplierNumber.get()
        columnNumber = self.receiverNumber.get()
        self.table.updateTableSize(rowNumber, columnNumber)
        self.suppliers.updateTableSize(rowNumber, 1)
        self.receivers.updateTableSize(1, columnNumber)

    def printArray(self, array=None):
        x = PrettyTable()
        if not array:
            array = [[self.table[(i, j)] for j in range(self.table.getColumns())] for i in range(self.table.getRows())]
        x.field_names = [' '] + ['O{}'.format(i) for i in range(self.table.getColumns())]
        for i, row in enumerate(array):
            x.add_row(['D{}'.format(i)] + row)
        for line in str(x).split('\n'):
            self.log.insertText('{}'.format(line))

    def calculateInitValues(self):
        supplierSum = self.suppliers.getCellsSum()
        receiverSum = self.receivers.getCellsSum()
        self.log.insertText('suppliers sum: {}'.format(supplierSum))
        self.log.insertText('receivers sum: {}'.format(receiverSum))
        if supplierSum > receiverSum:
            self.log.insertText('suppliers > receivers - adding fictional receiver')
            self.table.addColumns(1)
            self.receivers.addColumns(1)
            self.receivers[(0, self.receivers.getColumns()-1)] = supplierSum - receiverSum
        elif receiverSum > supplierSum:
            self.log.insertText('receivers > suppliers - adding fictional supplier')
            self.table.addRows(1)
            self.suppliers.addRows(1)
            self.suppliers[(self.suppliers.getRows()-1, 0)] = receiverSum - supplierSum

        suppliers = self.suppliers.getRowsSum()
        receivers = self.receivers.getColumnsSum()

        self.log.insertText('suppliers: {}'.format(suppliers))
        self.log.insertText('receivers: {}'.format(receivers))

        array = [[0 for j in range(self.table.getColumns())] for i in range(self.table.getRows())]
        minI, minV = self.table.findMinValue()

        self.printArray()
        self.printArray(array)


    def calculateStep(self):
        pass

    def calculateBtnAction(self, event):
        self.log.clear()
        self.calculateInitValues()


if __name__ == '__main__':
    root = tk.Tk()
    log = Log(root)
    initTable = Table(root, stretch=True)
    initLabel = tk.Label(root, text='Dos\\Odb', height=1)
    suppliers = Table(root, rows=4, columns=1, stretch=True)
    receivers = Table(root, rows=1, columns=4, stretch=True)
    buttons = MenuButtons(root, table=initTable, suppliers=suppliers, receivers=receivers, log=log)
    initLabel.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
    suppliers.grid(row=1, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
    receivers.grid(row=0, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    initTable.grid(row=1, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    log.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.W+tk.S+tk.E)
    buttons.grid(row=0, column=2, rowspan=3, sticky=tk.N+tk.W+tk.S+tk.E)

    root.grid_columnconfigure(1, weight=1)

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.mainloop()
