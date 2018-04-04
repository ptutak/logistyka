#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:30:14 2018

@author: ptutak
"""
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
frame = tk.Frame(root)
labelText=tk.StringVar()

label=tk.Label(frame,textvariable=labelText)

button=tk.Button(frame, text="Click Me")

labelText.set("I am a label")

label.pack()
button.pack()
frame.pack()

root.mainloop()