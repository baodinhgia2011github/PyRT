import os
import platform
import time
import ctypes
import datetime
from time import sleep
if not platform.system()=="Windows":
    import psutil
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
        ctypes.windll.kernel32.SetConsoleTextAttribute(
            ctypes.windll.kernel32.GetStdHandle(-11),color
        )
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
    DayOfWeek=currentTime.strftime("%A")
    MonthOfYear=currentTime.strftime("%B")
    date=currentTime.day
    year=currentTime.year
    hour=currentTime.hour
    minute=currentTime.minute
    second=currentTime.second
    suffix=["th","st","nd","rd"]+["th"]*16+["st","nd","rd"]+["th"]*7
    setConsoleColor(FOREGROUND_RED)
    print(f"Current time: {hour:02}:{minute:02}:{second:02}")
    setConsoleColor(FOREGROUND_GREEN)
    print(f"Current date: {DayOfWeek}, {MonthOfYear} {date:02}{suffix[date%10]},{year}")
    setConsoleColor(FOREGROUND_WHITE)
    print("\n")
def displayBatteryStatus():
    print("\033[1mBattery Status:\033[0m")
    if platform.system()=="Windows":
        powerStatus=SystemPowerStatus()
        result=ctypes.windll.kernel32.GetSystemPowerStatus(
            ctypes.pointer(powerStatus)
            )
        if result:
            ACLine="Connected" if powerStatus.ACLineStatus else "Not connected"
            print(f"AC line: ",end="")
            setConsoleColor(FOREGROUND_GREEN if ACLine=="Connected" else FOREGROUND_RED)
            print(f"{ACLine}")
            batteryPercentage=powerStatus.BatteryLifePercent
            if batteryPercentage>=40:
                setConsoleColor(FOREGROUND_GREEN)
            elif batteryPercentage>15:
                setConsoleColor(FOREGROUND_YELLOW)
            else:
                setConsoleColor(FOREGROUND_RED)
            print(f"Battery percentage: {batteryPercentage}%")
            setConsoleColor(FOREGROUND_WHITE)
            batteryLifeTime=powerStatus.BatteryLifeTime
            if batteryLifeTime!=0xFFFFFFFF:
                hours=batteryLifeTime//3600
                minutes=(batteryLifeTime%3600)//60
                print(f"Remaining battery life: {hours} hour(s) {minutes} minute(s)")
            else:
                print("Remaining battery life: ",end="")
                setConsoleColor(FOREGROUND_YELLOW)
                print("Unknown (Unable to calculate or AC connected)")
        else:
            setConsoleColor(FOREGROUND_RED)
            print("ERROR: Failed to retrieve power status.")
    elif platform.system() in ["Linux","Darwin"]:
        battery=psutil.sensors_battery()
        if battery:
            ACLine="Connected" if battery.power_plugged else "Not connected"
            print(f"AC line: ",end="")
            setConsoleColor(FOREGROUND_GREEN if battery.power_plugged else FOREGROUND_RED)
            print(f"{ACLine}")
            batteryPercentage=battery.percent
            if batteryPercentage>=40:
                setConsoleColor(FOREGROUND_GREEN)
            elif batteryPercentage>15:
                setConsoleColor(FOREGROUND_YELLOW)
            else:
                setConsoleColor(FOREGROUND_RED)
            print(f"Battery percentage: {batteryPercentage}%")
            setConsoleColor(FOREGROUND_WHITE)
            if not battery.power_plugged:
                hours,minutes=divmod(battery.secsleft//60,60)
                print(f"Remaining battery life: {hours} hour(s) {minutes} minute(s)")
            else:
                print("Battery is charging or fully charged.")
        else:
            print("Battery information not available.")
    else:
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
        print("This program is optimized for Windows, Linux, and MacOS.","Some features may not work",sep="\n")
    print("Thank you for using RTC_File3")
    sleep(2)
def recommendation():
    clearConsole()
    print("Recommended using this program with")
    print("Visual Studio Code installed with Python 3.13 or higher version")
    sleep(1)
def preparation():
    print("Starting project",end="")
    for _ in range(3):
        print('.',end='')
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
            print("\nTo exit program, please press Ctrl+C to terminate")
        previousSecond=second
        sleep(0.5)
if __name__=="__main__":
    main()

'''
Program information:
Program name: RTC (Real-Time Clock)
Lines: 153
Program is optimized for:
- Windows
- Linux
- MacOS
(Programmed with the help of AI)
'''