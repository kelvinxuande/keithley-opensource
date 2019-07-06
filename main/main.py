"""
main script of keithley_openSource
Primarily handles GUI windows, user inputs, function threads and expected exceptions for various 'script exits'
"""

# IMPORTING STANDARD MODULES:
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import threading
import os
import visa
from time import sleep

# IMPORTING CUSTOM MODULES:
import settings
import trackers
import calculations
import backend
import miscFunctions

def thread_exception():
    trackers.inDialog = True
    if (settings.measMode[0] == 1):
        triggerWindow.wm_attributes("-disabled", True)
    else:
        pollWindow.wm_attributes("-disabled", True)
    MsgBox = messagebox.showinfo ('Connection(s) Lost!','Program will now quit.\nExcel has been written.',icon = 'warning')
    miscFunctions.create_excel()
    os._exit(0)

def ExitApplication():
    trackers.inDialog = True
    if (settings.measMode[0] == 1):
        triggerWindow.wm_attributes("-disabled", True)
    else:
        pollWindow.wm_attributes("-disabled", True)
    
    MsgBox = messagebox.askquestion ('Exit Application','Exit the application?',icon = 'warning')
    if MsgBox == 'no':
        trackers.inDialog = False
        if (settings.measMode[0] == 1):
            triggerWindow.wm_attributes("-disabled", False)
        else:
            pollWindow.wm_attributes("-disabled", False)
    else:
        miscFunctions.create_excel()
        os._exit(0)

def view_command(delete):   
# receives either 1 or 0 from calling function to determine whether to add or delete entries
    if (settings.measMode == [1,0]):
        if (delete==0):
            trigger_listbox.insert(END, trackers.measStack[(trackers.index)-1])    
            trigger_listbox.see("end")
        else:
            trigger_listbox.delete(trackers.index)
            trigger_listbox.see("end")
    else:
        if (delete==0):
            poll_listbox.insert(END, trackers.measStack[(trackers.index)-1])    
            poll_listbox.see("end")
        else:
            poll_listbox.delete(trackers.index)

def delete_command():   
# only available for trigger mode
    if (trackers.inDialog == False) and (trackers.trigger_paused==0):
        trackers.measStack.pop()
        print(*trackers.measStack, sep = "\n")
        # backend.delete(trackers.index)
        backend.delete()
        trackers.index = trackers.index - 1
        view_command(1)
        
def polling_thread():
    while 1:
        if (trackers.poll_paused==0):
            try:
                if (trackers.index<settings.numberOftimes):
                    trackers.index = trackers.index + 1
                    # value = settings.scope.query('READ?')
                    # value = value.strip('\n')
                    value = 0.1
                                    
                    timeDiff = calculations.timeDifference(1)
                    timeNow = calculations.timeDifference(0)
                    Date = datetime.now().strftime('%d/%m/%Y')
                    
                    print('New Measurement: = %s' % value)
                    trackers.measStack.append([trackers.index, value, timeDiff, timeNow])
                    print(*trackers.measStack, sep = "\n")

                    clean_value = 0.1            
                    backend.insert(Date, timeNow, trackers.index, clean_value, timeDiff, 
                    settings.printerNumber, settings.designName, settings.printParameters)
                    
                    view_command(0)
                    sleep(settings.period-0.2)  # Offset sleep
                else:
                    # print("Finished Polling! Exiting System")
                    poll_progressBar.stop()
                    poll_quitButton.config(state="normal")
                    poll_pauseButton.config(state="disabled")
                    # ExitApplication()
            except:
                thread_exception()
        else:
            # print("Polling paused")
            pass
        sleep(0.2)  # High CPU usage occurs when it is an infinite loop with no sleep

            
def triggering_thread():
    while 1:
        try:
            data = settings.arduinoUSB.readline()[:-2]
            if (data) and (trackers.inDialog == False) and (trackers.trigger_paused==0):
                trackers.index = trackers.index + 1
                # value = settings.scope.query('READ?')
                # value = value.strip('\n')
                value = 0.1
                
                timeDiff = "NA"
                timeNow = calculations.timeDifference(0)
                Date = datetime.now().strftime('%d/%m/%Y')
                
                print('New Measurement: = %s' % value)
                trackers.measStack.append([trackers.index, value, timeDiff, timeNow])
                print(*trackers.measStack, sep = "\n")
  
                # settings.updated_dict['%d' % settings.index] = ['%s' % value]        
                # buffer = (settings.updated_dict['%d' % settings.index])
                # clean_value = buffer[0]
                clean_value = 0.1            
                backend.insert(Date, timeNow, trackers.index, clean_value, timeDiff, 
                settings.printerNumber, settings.designName, settings.printParameters)                   

                view_command(0)
        except:
            thread_exception()
        sleep(0.2)
            
def window_controller():
    mode_selected = option.get()
    settings.printerNumber = pn.get()
    settings.designName = dn.get()
    settings.printParameters = pp.get()
    if (mode_selected=="Push Button"):
        settings.measMode = [1,0]                
        print(settings.measMode)
        rootWindow.destroy()
        pollWindow.destroy()
        triggerWindow.deiconify()
        child_thread = threading.Thread(target=triggering_thread)
        child_thread.start()
    else:
        settings.measMode = [0,1]                
        print(settings.measMode)
        rootWindow.destroy()
        triggerWindow.destroy()
        pollWindow.deiconify()
        child_thread = threading.Thread(target=polling_thread)
        child_thread.start()

def calculateFeedback():
    settings.numberOftimes = int(poll_entryNum.get())
    settings.period = int(poll_entryPeriod.get())
    runTime, startTime, endTime = calculations.updateEst(settings.numberOftimes, settings.period)
    est_RT.set(runTime)
    est_ST.set(startTime)
    est_ET.set(endTime)

def start_poll():
    poll_pauseButton.config(state="normal")
    calculate_button.config(state="disabled")
    poll_entryNum.config(state="disabled")
    poll_entryPeriod.config(state="disabled")
    poll_startButton.config(state="disabled")
    
    calculateFeedback()
    calculations.set_runStartTime()
    poll_paused()

def trigger_paused():
    if (trackers.trigger_paused==1):
        trackers.trigger_paused = 0
        pause_trigger.set("PAUSE")
    else:
        trackers.trigger_paused = 1
        pause_trigger.set("RESUME")

def poll_paused():
    if (trackers.poll_paused==1):
        trackers.poll_paused = 0
        poll_progressBar.start()
        pause_textVariable.set("PAUSE")
        poll_quitButton.config(state="disabled")
    else:
        trackers.poll_paused = 1
        poll_progressBar.stop()
        pause_textVariable.set("RESUME")
        poll_quitButton.config(state="normal")



# FIRST WINDOW:
root = Tk()
root.withdraw()
rootWindow = Toplevel(root)
rootWindow.title("semiAuto v2.0 Setup")
rootWindow.iconbitmap(r'stacked-files.ico')
# rootWindow.attributes("-topmost", True)
rootWindow.resizable(0,0)
rootWindow.protocol("WM_DELETE_WINDOW", ExitApplication)
statusFrame = Frame(rootWindow)
statusFrame.pack()
statusLabelFrame = LabelFrame(statusFrame, text='HARDWARE STATUS', font="Helvetica 8 bold")
statusLabelFrame.pack(fill="both", expand="yes", padx="7", pady=(7,0))
labelFrame = Frame(rootWindow)
labelFrame.pack()
labelLabelFrame = LabelFrame(statusFrame, text='LABELLING', font="Helvetica 8 bold")
labelLabelFrame.pack(fill="both", expand="yes", padx="7")
methodLabelFrame = LabelFrame(statusFrame, text='MEASUREMENT MODE', font="Helvetica 8 bold")
methodLabelFrame.pack(fill="both", expand="yes", padx="7")
firstButtonFrame = Frame(rootWindow)
firstButtonFrame.pack()
if 0 in settings.hardware_status:
    statusbarPrompt = Label(statusLabelFrame, text="One or more components\nshown below are not connected,\nplease exit program and try again", width=40, font="Helvetica 8", fg="RED")
    statusbarPrompt.pack()
statusbar = Label(statusLabelFrame, text="ARDUINO:", width=40, font="Helvetica 8 bold")
statusbar.pack()
if (settings.hardware_status[0]==0):
    statusbar = Label(statusLabelFrame, text="NOT CONNECTED", width=40, font="Helvetica 8", fg="RED")
    statusbar.pack()
else:
    statusbar = Label(statusLabelFrame, text="CONNECTED", width=40, font="Helvetica 8", fg="GREEN")
    statusbar.pack()
statusbar = Label(statusLabelFrame, text="DIGITAL MULTIMETER:", width=40, font="Helvetica 8 bold")
statusbar.pack()
statusbar = Label(statusLabelFrame, text="USB0::0x05E6::0x6500::04391587::INSTR", width=40, font="Helvetica 8")
statusbar.pack()
if (settings.hardware_status[1]==0):
    statusbar = Label(statusLabelFrame, text="NOT CONNECTED", width=40, font="Helvetica 8", fg="RED")
    statusbar.pack(pady=(0,7))
else:
    statusbar = Label(statusLabelFrame, text="CONNECTED", width=40, font="Helvetica 8", fg="GREEN")
    statusbar.pack(pady=(0,7))
customBar = Label(labelLabelFrame, text="Printer Number:", width=20, font="Helvetica 8 bold")
customBar.pack()
pn = Entry(labelLabelFrame, width=20, justify=CENTER)
pn.pack()
customBar = Label(labelLabelFrame, text="Design Name:", width=20, font="Helvetica 8 bold")
customBar.pack(pady=(7,0))
dn = Entry(labelLabelFrame, width=20, justify=CENTER)
dn.pack()
customBar = Label(labelLabelFrame, text="Print Parameters:", width=20, font="Helvetica 8 bold")
customBar.pack(pady=(7,0))
pp = Entry(labelLabelFrame, width=20, justify=CENTER)
pp.pack(pady=(0,10))
option = ttk.Combobox(methodLabelFrame, values=["Push Button", "Polling [BETA]"], width=17)
option.set('Push Button')
option.pack(pady=10)
zeroBar = Label(firstButtonFrame, text="Please zero DMM before starting!", width=40, font="Helvetica 8", fg="RED")
zeroBar.pack()
if 0 in settings.hardware_status:
    b1=ttk.Button(firstButtonFrame, text="START SESSION", width=15, state="disabled")
    b1.pack(pady=(10,0))
else:
    b1=ttk.Button(firstButtonFrame, text="START SESSION", width=15, command=window_controller)
    b1.pack(pady=(10,0))
b2=ttk.Button(firstButtonFrame, text="QUIT", width=15, command=ExitApplication)
b2.pack(pady=10)

# TRIGGERING WINDOW:
triggerWindow = Toplevel(root)
triggerWindow.withdraw()
triggerWindow.title("semiAuto v2.0 > Trigger Mode")
triggerWindow.iconbitmap(r'stacked-files.ico')
triggerWindow.resizable(0,0)
triggerWindow.protocol("WM_DELETE_WINDOW", ExitApplication)
pause_trigger = StringVar()
pause_trigger.set("PAUSE")
trigger_middleFrame = Frame(triggerWindow)
trigger_middleFrame.pack()
trigger_buttonFrame = Frame(triggerWindow)
trigger_buttonFrame.pack(side=RIGHT)
trigger_bottomFrame = Frame(triggerWindow)
trigger_bottomFrame.pack(side=LEFT)
trigger_toplabel = Label(trigger_middleFrame, text="Reading Table", width=40, font="Helvetica 10 bold")
trigger_toplabel.pack(pady=(7,0))
trigger_statusbar = Label(trigger_middleFrame, text="[Index / Measurement / Secs from Reference / Time]")
trigger_statusbar.pack()
trigger_scrollbar = ttk.Scrollbar(trigger_middleFrame)
trigger_scrollbar.pack(side=LEFT, fill=Y, padx=10)
trigger_listbox = Listbox(trigger_middleFrame, height=15, width=47, borderwidth=1, relief="solid", font="Helvetica 10")
trigger_listbox.pack(padx=(0,10))
trigger_scrollbar.configure(command=trigger_listbox.yview)
trigger_listbox.configure(yscrollcommand=trigger_scrollbar.set)
poll_pauseButton = ttk.Button(trigger_buttonFrame, textvariable=pause_trigger, width=10, command=trigger_paused)
poll_pauseButton.pack(side=RIGHT, padx=(0,10), pady=12)
trigger_delButton = ttk.Button(trigger_buttonFrame, text="DELETE LAST", width=12, command=delete_command)
trigger_delButton.pack(side=RIGHT, pady=10)
trigger_quitButton = ttk.Button(trigger_buttonFrame, text="SAVE AND QUIT", width=18, command=ExitApplication)
trigger_quitButton.pack(side=RIGHT, padx=(0,63), pady=10)

# POLLING WINDOW:
pollWindow = Toplevel(root)
pollWindow.title("semiAuto v2.0 > Polling Mode [Beta]")
pollWindow.iconbitmap(r'stacked-files.ico')
pollWindow.resizable(0,0)
est_RT = IntVar()
est_ST = IntVar()
est_ET = IntVar()
numDefault = IntVar()
periodDefault = IntVar()
numDefault.set(1000)
periodDefault.set(1)
pause_textVariable = StringVar()
pause_textVariable.set("PAUSE")
pollWindow.protocol("WM_DELETE_WINDOW", ExitApplication)
poll_frameLeft = Frame(pollWindow)
poll_frameLeft.pack(side=LEFT)
poll_labelFrame = LabelFrame(poll_frameLeft, text='CONFIGURATION', font="Helvetica 10 bold")
poll_labelFrame.pack(padx=(12,0), pady=(7,0))
poll_inputPrompt = Label(poll_frameLeft, text="Only integer values are accepted", fg="RED", justify=CENTER)
poll_inputPrompt.pack(padx=(12,0), pady=(0))
calculate_button = ttk.Button(poll_frameLeft, text="CALCULATE ESTIMATE", width=24, command=calculateFeedback)
calculate_button.pack(padx=(12,0), pady=(6,10))
poll_labelFrame1 = LabelFrame(poll_frameLeft, text='ESTIMATION', font="Helvetica 10 bold")
poll_labelFrame1.pack(padx=(12,0), pady=(10,0))
poll_innerFrame = Frame(poll_labelFrame)
poll_innerFrame.pack(side=LEFT)
poll_innerFrame1 = Frame(poll_labelFrame)
poll_innerFrame1.pack(side=LEFT)
poll_innerFrame2 = Frame(poll_labelFrame1)
poll_innerFrame2.pack(side=LEFT)
poll_innerFrame3 = Frame(poll_labelFrame1)
poll_innerFrame3.pack(side=LEFT)
poll_innerFrame4 = Frame(poll_labelFrame1)
poll_innerFrame4.pack(side=LEFT)
poll_frameRight = Frame(pollWindow)
poll_frameRight.pack(side=LEFT)
poll_buttonFrame = Frame(poll_frameRight)
poll_buttonFrame.pack(side=BOTTOM, fill='x')
poll_labelText = Label(poll_innerFrame, text="Number of Times")
poll_labelText.pack(padx="20", pady=(7,0))
poll_labelText1 = Label(poll_innerFrame1, text="Period [secs]")
poll_labelText1.pack(padx="20", pady=(7,0))
poll_entryNum = Entry(poll_innerFrame, width=20, textvariable = numDefault, justify=CENTER)
poll_entryNum.pack(padx=(10,5), pady="7")
poll_entryPeriod = Entry(poll_innerFrame1, width=20, textvariable = periodDefault, justify=CENTER)
poll_entryPeriod.pack(padx=(5,10), pady="7")
poll_labelText2 = Label(poll_innerFrame2, text="Run Time")
poll_labelText2.pack(padx=(10,5), pady=(7,0))
poll_labelText3 = Label(poll_innerFrame3, text="Start Time")
poll_labelText3.pack(pady=(7,0))
poll_labelText4 = Label(poll_innerFrame4, text="End Time")
poll_labelText4.pack(padx=(5,10), pady=(7,0))
poll_calText = Label(poll_innerFrame2, width=20, justify=CENTER, textvariable=est_RT, relief=RIDGE)
poll_calText.pack(padx=(10,5), pady="7")
poll_calText1 = Label(poll_innerFrame3, width=20, justify=CENTER, textvariable=est_ST, relief=RIDGE)
poll_calText1.pack(padx=(5,5), pady="7")
poll_calText2 = Label(poll_innerFrame4, width=20, justify=CENTER, textvariable=est_ET, relief=RIDGE)
poll_calText2.pack(padx=(5,10), pady="7")
poll_prompt = Label(poll_frameLeft, text="Please make sure that probes\nare secured in the right positions", fg="RED", justify=CENTER)
poll_prompt.pack(padx=(0), pady=(0))
poll_startButton = ttk.Button(poll_frameLeft, text="START POLLING", width=18, command=start_poll)
poll_startButton.pack(padx=(10,0), pady=(6,0))
poll_refBar = Label(poll_frameRight, text="[Index / Measurement / Secs from Reference / Time]")
poll_refBar.pack(pady=(7,0), padx=(29,0))
poll_scrollbar = ttk.Scrollbar(poll_frameRight)
poll_scrollbar.pack(side=LEFT, fill=Y, padx=10)
poll_listbox = Listbox(poll_frameRight, height=15, width=47, borderwidth=1, relief="solid", font="Helvetica 10")
poll_listbox.pack(padx=(0,10))
poll_scrollbar.configure(command=poll_listbox.yview)
poll_listbox.configure(yscrollcommand=poll_scrollbar.set)
poll_quitButton = ttk.Button(poll_buttonFrame, text="SAVE AND QUIT", state=DISABLED, width=16, command=ExitApplication)
poll_quitButton.pack(side=RIGHT, padx=(0,10), pady=12)
poll_pauseButton = ttk.Button(poll_buttonFrame, textvariable=pause_textVariable, state=DISABLED, width=16, command=poll_paused)
poll_pauseButton.pack(side=RIGHT, padx=(0,10), pady=12)
poll_progressBar = ttk.Progressbar(poll_buttonFrame,orient=HORIZONTAL,length=100, maximum="20", mode='indeterminate')   # Maximum is the total ammount of intervals in progessbar
poll_progressBar.pack(side=RIGHT, padx=(0,10), pady=12)
pollWindow.withdraw()

root.mainloop()