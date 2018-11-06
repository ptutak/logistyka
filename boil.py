#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from prettytable import PrettyTable
from prettytable import ALL
import numpy as np
import scipy.linalg as lg
from time import sleep

# Dummy value, real values used cannot be greater than this one
MAXIMAL_COST = 10000000000

# Must be LESS than MAXIMAL_COST - leave as is
DUMMY_COST = MAXIMAL_COST - 1

class Log(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, rowspan=5, sticky=tk.N+tk.S)
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=6, column=0, columnspan=1, sticky=tk.W+tk.E)
        self.log = tk.StringVar()
        self.logListBox = tk.Listbox(self,
                                     yscrollcommand=self.yScroll.set,
                                     xscrollcommand=self.xScroll.set,
                                     listvariable=self.log,
                                     font=("Courier", 10))
        self.logListBox.grid(row=0, column=0, rowspan=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.yScroll['command'] = self.logListBox.yview
        self.xScroll['command'] = self.logListBox.xview
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.tasks = []

    def print(self, text, index=tk.END):
        self.logListBox.insert(index, str(text))
        self.logListBox.yview(tk.END)
        self.update_idletasks()

    def printArray(self, array, index=tk.END):
        x = PrettyTable()
        x.header = False
        x.hrules = ALL
        for row in array:
            x.add_row(row)
        for line in str(x).split('\n'):
            self.logListBox.insert(index, line)
        self.logListBox.yview(tk.END)
        self.update_idletasks()

    def pushArray(self, array):
        for line in array:
            self.logListBox.insert(tk.END, line)
        self.logListBox.yview(tk.END)
        self.update_idletasks()

    def curSelection(self):
        return self.logListBox.curselection()

    def clear(self):
        self.log.set('')


class Table(tk.Frame):
    def __init__(self, *args, rows=3, columns=3, stretch=False, **kwargs):
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

    def getArray(self):
        return [[self[(i, j)] for j in range(self.columns)] for i in range(self.rows)]

    def setArray(self, array):
        for i in range(self.rows):
            for j in range(self.columns):
                self[(i, j)] = array[i][j]

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

    def addRows(self, rowNum, value=0):
        prevRowNum = self.rows
        self.rows += rowNum
        for i in range(prevRowNum, self.rows):
            for j in range(self.columns):
                self.entries[(i, j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i, j)].set(value)

    def addColumns(self, columnNum, value=0):
        prevColumnNum = self.columns
        self.columns += columnNum
        for i in range(self.rows):
            for j in range(prevColumnNum, self.columns):
                self.entries[(i, j)] = tk.IntVar()
                entry = tk.Entry(self, textvariable=self.entries[(i, j)], width=self.entryWidth)
                entry.grid(row=i, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                self.entries[(i, j)].set(value)

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
        self.costTable = table
        self.suppliers = suppliers
        self.receivers = receivers
        self.quantArray = None
        self.log = log

    def updateTableBtnAction(self, event):
        rowNumber = self.supplierNumber.get()
        columnNumber = self.receiverNumber.get()
        self.costTable.updateTableSize(rowNumber, columnNumber)
        self.suppliers.updateTableSize(rowNumber, 1)
        self.receivers.updateTableSize(1, columnNumber)

    def wrapArray(self, array):
        if not array:
            return array
        fieldNames = [' '] + ['O{}'.format(i) for i in range(len(array[0]))]
        newArr = [fieldNames]
        for i, row in enumerate(array):
            newArr.append(['D{}'.format(i)] + row)
        return newArr

    def getMinValueArray(self, array=None):
        if not array:
            array = self.costTable.getArray()
        minV = array[0][0]
        minI = (0, 0)
        for i in range(len(array)):
            for j in range(len(array[0])):
                if array[i][j] < minV:
                    minV = array[i][j]
                    minI = (i, j)
        return (minI, minV)

    def updateQuantArray(self, costArray):
        recSumAct = np.sum(np.array(self.quantArray), axis=0)
        supSumAct = np.sum(np.array(self.quantArray), axis=1)
        recSum = np.array(self.receivers.getColumnsSum())
        supSum = np.array(self.suppliers.getRowsSum())
        diffSup = supSum - supSumAct
        diffRec = recSum - recSumAct
        if any(diffSup):
            minI, minV = self.getMinValueArray(costArray)
            if diffSup[minI[0]] > diffRec[minI[1]]:
                self.quantArray[minI[0]][minI[1]] += diffRec[minI[1]]
                for i in range(len(supSum)):
                    costArray[i][minI[1]] = MAXIMAL_COST
            else:
                self.quantArray[minI[0]][minI[1]] += diffSup[minI[0]]
                for i in range(len(recSum)):
                    costArray[minI[0]][i] = MAXIMAL_COST
        return costArray

    def calculateInitValues(self):
        self.quantArray = None
        supplierSum = self.suppliers.getCellsSum()
        receiverSum = self.receivers.getCellsSum()
        self.log.print('suppliers sum: {}'.format(supplierSum))
        self.log.print('receivers sum: {}'.format(receiverSum))
        if supplierSum > receiverSum:
            self.log.print('suppliers > receivers - adding fictional receiver')
            self.costTable.addColumns(1, DUMMY_COST)
            self.receivers.addColumns(1)
            self.receivers[(0, self.receivers.getColumns()-1)] = supplierSum - receiverSum
        elif receiverSum > supplierSum:
            self.log.print('receivers > suppliers - adding fictional supplier')
            self.costTable.addRows(1, DUMMY_COST)
            self.suppliers.addRows(1)
            self.suppliers[(self.suppliers.getRows()-1, 0)] = receiverSum - supplierSum

        suppliers = self.suppliers.getRowsSum()
        receivers = self.receivers.getColumnsSum()

        self.log.print('suppliers: {}'.format(suppliers))
        self.log.print('receivers: {}'.format(receivers))

        costArray = self.costTable.getArray()

        self.quantArray = [[0 for j in range(self.costTable.getColumns())] for i in range(self.costTable.getRows())]
        while not np.array_equal(np.sum(np.array(self.quantArray), axis=0), np.array(self.receivers.getColumnsSum())):
            costArray = self.updateQuantArray(costArray)

        costArray = self.costTable.getArray()
        for i in range(len(costArray)):
            for j in range(len(costArray[i])):
                if costArray[i][j] == DUMMY_COST:
                    costArray[i][j] = 0
        self.costTable.setArray(costArray)

    def calculateDualVariables(self):
        costArray = self.costTable.getArray()
        quantArray = self.quantArray
        rows = len(quantArray)
        columns = len(quantArray[0])
        A = []
        B = []
        for i in range(rows):
            aRow = [0 for _ in range(rows+columns)]
            for j in range(columns):
                if quantArray[i][j]:
                    aRow[i] = 1
                    aRow[rows+j] = 1
                    B.append(-costArray[i][j])
                    A.append(aRow)
                    aRow = [0 for _ in range(rows+columns)]
        for i, x in enumerate(quantArray):
            if any(x):
                if len(B) < rows+columns:
                    tmp = [0 for _ in range(rows+columns)]
                    tmp[i] = 1
                    A.append(tmp)
                    B.append(0)
                else:
                    break
        A = np.array(A)
        B = np.array(B)
        return lg.solve(A, B)

    def calculateStepMatrix(self, dualVariables):
        matrix = []
        quantArray = np.array(self.quantArray)
        costArray = np.array(self.costTable.getArray())
        rows = self.costTable.getRows()
        columns = self.costTable.getColumns()
        for i in range(rows):
            matrix.append([])
            for j in range(columns):
                if quantArray[i, j]:
                    matrix[i].append('x')
                else:
                    matrix[i].append(dualVariables[i]+dualVariables[rows+j]+costArray[i, j])
        return matrix

    def searchNextStep(self, path, matrix):
        rows = len(matrix)
        columns = len(matrix[0])
        rowNexts = []
        odd = False
        results = []
        i = path[-1][0]
        j = path[-1][1]
        if matrix[i][j] == 'x':
            odd = True
        for k in range(rows):
            if k == j:
                continue
            if not odd and matrix[i][k] == 'x':
                rowNexts.append((i, k))
            elif matrix[i][k] != 'x':
                rowNexts.append((i, k))
        for row in rowNexts:
            if row not in path:
                results.append(row)

        columnNexts = []
        for k in range(columns):
            if k == i:
                continue
            if not odd and matrix[k][j] == 'x':
                columnNexts.append((k, j))
            elif matrix[k][j] != 'x':
                columnNexts.append((k, j))

        for col in columnNexts:
            if col not in path:
                results.append(col)

        return results

    def generatePaths(self, matrix):
        rows = len(matrix)
        columns = len(matrix[0])
        for i in range(rows):
            for j in range(columns):
                if matrix[i][j] != 'x':
                    minimal = matrix[i][j]
                    minIndeces = (i, j)
                    break
        for i in range(rows):
            for j in range(columns):
                if matrix[i][j] < minimal:
                    minimal = matrix[i][j]
                    minIndeces = (i, j)
        start = minIndeces
        path = (start,)
        nextSteps = self.searchNextStep(path, matrix)
        oldPaths = []
        for step in nextSteps:
            oldPaths.append(path + (step,))
        finished = False
        while not finished:
            newPaths = []
            finished = True
            for path in oldPaths:
                if path[-1] != start:
                    nextSteps = self.searchNextStep(path, matrix)
                    for step in nextSteps:
                        if step != start:
                            finished = False
                        newPaths.append(path + (step,))
            oldPaths = newPaths
        return oldPaths


    def calculateBtnAction(self, event):
        self.log.clear()
        self.calculateInitValues()
        self.log.print('Cost table:')
        self.log.printArray(self.wrapArray(self.costTable.getArray()))
        self.log.print('Actual transport:')
        self.log.printArray(self.wrapArray(self.quantArray))
        res = self.calculateDualVariables()
        self.log.print('Dual variables:')
        self.log.printArray([res])
        matrix = self.calculateStepMatrix(res)
        self.log.print('Matrix:')
        self.log.printArray(matrix)
        paths = self.generatePaths(matrix)
        for path in paths:
            self.log.printArray(path)

if __name__ == '__main__':
    root = tk.Tk()
    log = Log(root)
    initLabel = tk.Label(root, text='Dos\\Odb', height=1)
    suppliers = Table(root, rows=3, columns=1, stretch=True)
    receivers = Table(root, rows=1, columns=3, stretch=True)
    initTable = Table(root, stretch=True)
    buttons = MenuButtons(root, table=initTable, suppliers=suppliers, receivers=receivers, log=log)
    initLabel.grid(row=0, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
    suppliers.grid(row=1, column=0, sticky=tk.N+tk.W+tk.S+tk.E)
    receivers.grid(row=0, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    initTable.grid(row=1, column=1, sticky=tk.N+tk.W+tk.S+tk.E)
    log.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.W+tk.S+tk.E)
    buttons.grid(row=0, column=2, rowspan=3, sticky=tk.N+tk.W+tk.S+tk.E)

    root.grid_columnconfigure(1, weight=1)

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(2, weight=0)
    root.mainloop()
