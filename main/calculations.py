"""
Generate estimated time based on start time, poll period and number of polls
Designed for use-cases shorter than 24 hours
"""
from datetime import datetime

def updateEst(numberOftimes, period):
    totalSeconds = (numberOftimes*period)
    clockedHours = int(totalSeconds/3600)
    secondsLeft = totalSeconds - (clockedHours*3600)
    clockedMins = int(secondsLeft/60)
    # clockedSeconds = secondsLeft - (clockedMins*60)
    time_h = datetime.now().strftime('%H')
    time_m = datetime.now().strftime('%M')
    time_hours = int(time_h)
    time_minutes = int(time_m)
    time_hours = time_hours + clockedHours
    time_minutes = time_minutes + clockedMins
    zero = "0"
    if (time_minutes>60):
        time_minutes = time_minutes - 60
        time_hours = time_hours + 1
    if (time_hours>24):
        time_hours = time_hours - 24
    if (time_minutes<10):
        time_minutes = str(time_minutes)
        time_minutes = zero + time_minutes
    if (time_hours<10):
        time_hours = str(time_hours)
        time_hours = zero + time_hours
    if (clockedHours==0 and clockedMins==0):
        runTime = ("Less than one minute")
    else:
        runTime = ("%d Hrs %d Mins" %(clockedHours, clockedMins))
    startTime = datetime.now().strftime('%H:%M')
    endTime = ("%s:%s" %(time_hours, time_minutes))
    return runTime, startTime, endTime

hours_runStartTime = 99
runStartTime = 0

def set_runStartTime():
    global hours_runStartTime
    global runStartTime
    mins = int(datetime.now().strftime('%M'))
    secs = int(datetime.now().strftime('%S'))
    hours_runStartTime = int(datetime.now().strftime('%H'))
    runStartTime = (hours_runStartTime*3600)+(mins*60)+secs
    
def timeDifference(option):
    global hours_runStartTime
    global runStartTime
    # 0 to just get currentTime, 1 to get time difference in seconds between poll start time and current time
    if (option == 1):
        # time = datetime.now().strftime('%H:%M:%S.%f')
        hours = int(datetime.now().strftime('%H'))
        mins = int(datetime.now().strftime('%M'))
        secs = int(datetime.now().strftime('%S'))        
        if hours_runStartTime > hours:
            hours = hours + 24
        currentTime_inSecs = (hours*3600)+(mins*60)+secs
        timeDifference = currentTime_inSecs - runStartTime
        return timeDifference
    else:   # if option == 0:
        currentTime = datetime.now().strftime('%H:%M:%S')
        return currentTime