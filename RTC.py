import os
import platform
import time
import ctypes
import datetime
import calendar
from time import sleep
if platform.system() is not "Windows":
    try:
        import psutil
    except ImportError:
        print("ERROR: psutil library is not detected.\nPlease check your Python version or install 'psutil' library using 'pip install psutil' and try again.")
        exit()
if platform.system() is "Windows":
    FOREGROUND_GREEN=0x0A
    FOREGROUND_RED=0x0C
    FOREGROUND_YELLOW=0x0E
    FOREGROUND_WHITE=0x07
class SystemPowerStatus(ctypes.Structure):
    _fields_=[
        ("ACLineStatus",ctypes.c_byte),
        ("BatteryFlag",ctypes.c_byte),
        ("BatteryLifePercent",ctypes.c_byte),
        ("Reversed1",ctypes.c_byte),
        ("BatteryLifeTime",ctypes.c_ulong),
        ("BatteryFullLifeTime",ctypes.c_ulong)
    ]
def setConsoleColor(color):
    if platform.system()=="Windows":
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11),color)
    else:
        colors={
            FOREGROUND_GREEN:"\033[32m",
            FOREGROUND_RED:"\033[31m",
            FOREGROUND_YELLOW:"\033[33m",
            FOREGROUND_WHITE:"\033[37m"
        }
        print(colors.get(color,""),end="")
def clearConsole():
    os.system("CLS" if platform.system()=="Windows" else "clear")
def displayTimeAndDate():
    currentTime=datetime.datetime.now()
    dayOfWeek=currentTime.strftime("%A")
    monthOfYear=currentTime.strftime("%B")
    date=currentTime.day
    year=currentTime.year
    hour=currentTime.hour
    minute=currentTime.minute
    second=currentTime.second
    suffix=[None]+["th"]*31
    for i in [1,21,31]:
        suffix[i]="st"
    for i in [2,22]:
        suffix[i]="nd"
    for i in [3,23]:
        suffix[i]="rd"
    setConsoleColor(FOREGROUND_RED)
    print(f"Current time: {hour:02}:{minute:02}:{second:02}")
    setConsoleColor(FOREGROUND_GREEN)
    print(f"Current date: {dayOfWeek}, {monthOfYear} {date}{suffix[date]}, {year}")
    setConsoleColor(FOREGROUND_WHITE)
    print("\n")
def displayCurrentMonthCalendar():
    currentTime=datetime.datetime.now()
    monthOfYear=currentTime.strftime("%B")
    month=currentTime.month
    year=currentTime.year
    print(calendar.month(year,month))
def displayBatteryStatus():
    print("\033[1mBattery status:\033[0m")
    if platform.system() is "Windows":
        powerStatus=SystemPowerStatus()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.pointer(powerStatus)):
            setConsoleColor(FOREGROUND_RED)
            print("ERROR: Failed to retrieve power status.")
            setConsoleColor(FOREGROUND_WHITE)
            return
        ACLine=("Connected" if powerStatus.ACLineStatus else 
                "Not connected" if not powerStatus.ACLineStatus else 
                "Unknown"
        )
        print("AC Line: ",end="")
        setConsoleColor(FOREGROUND_GREEN if ACLine=="Connected" else 
                        FOREGROUND_YELLOW if ACLine=="Not connected" else 
                        FOREGROUND_RED
        )
        print(f"{ACLine}")
        batteryPercentage=powerStatus.BatteryLifePercent
        setConsoleColor(FOREGROUND_GREEN if batteryPercentage>=40 else 
                        FOREGROUND_YELLOW if batteryPercentage>15 else 
                        FOREGROUND_RED
        )
        print(f"Battery Percentage: {batteryPercentage}%")
        setConsoleColor(FOREGROUND_WHITE)
        if not powerStatus.BatteryLifeTime==0xFFFFFFFF:
            hours,minutes=divmod(powerStatus.BatteryLifeTime//60,60)
        else:
            print("Remaining Battery Life: ",end='')
            setConsoleColor(FOREGROUND_YELLOW)
            print("Unknown (Unable to connected or AC connected).")
    elif platform.system() is "Linux" or "Darwin":
        battery=psutil.sensors_battery()
        if battery:
            print("AC Line: ",end="")
            setConsoleColor(FOREGROUND_GREEN if battery.power_plugged else
                            FOREGROUND_RED
            )
            print("Connected" if battery.power_plugged else
                  "Not connected"
            )
            setConsoleColor(
                FOREGROUND_GREEN if battery.percent>=40 else
                FOREGROUND_YELLOW if battery.percent>15 else
                FOREGROUND_RED
            )
            print(f"Battery Precentage: {battery.percent}%")
            setConsoleColor(FOREGROUND_WHITE)
            if battery.secsleft==psutil.POWER_TIME_UNLIMITED:
                print("Remaining Battery Life: Unlimited (AC connected)")
            else:
                hours,minutes=divmod(battery.secsleft//60,60)
                print(f"Remaining Battery Life: {hours} hour(s) {minutes} minute(s)")
        else:
            setConsoleColor(FOREGROUND_RED)
            print("Battery information not available.")
    else:
        setConsoleColor(FOREGROUND_RED)
        print("Battery status not supported on this OS.")
    setConsoleColor(FOREGROUND_WHITE)
    print("\n")
def displayDeviceInformation():
    print("Device information:")
    print(f"Device generation: {platform.system()} {platform.release()}")
    print(f"Device version: {platform.version()}")
    print(f"Device platform: {platform.platform()}")
    print(f"CPU: {platform.processor()}")
    print("\n")
def warning():
    if platform.system() not in ["Windows","Linux","Darwin"]:
        print("This program is optimized for Windows, Linux and MacOS.","Some featues may not work",sep="\n")
    print("Thank you for using RTC.")
    sleep(2)
def recommendation():
    clearConsole()
    print("Recommended using this program with Visual Studio or\nVisual Studio Code with Python 3.13 or higher version that has been installed.")
    sleep(1)
def preparation():
    print("Starting project",end="")
    for _ in range(3):
        print('.',end="")
        sleep(1)
    clearConsole()
def main():
    recommendation()
    warning()
    preparation()
    previousSecond=-1
    while True:
        currentTime=datetime.datetime.now()
        second=currentTime.second
        if second!=previousSecond:
            clearConsole()
            displayTimeAndDate()
            displayBatteryStatus()
            displayDeviceInformation()
            displayCurrentMonthCalendar()
            print("\nTo exit program, press Ctrl+C to terminate")
        previousSecond=second
        sleep(0.5)
if __name__=="__main__":
    main()
