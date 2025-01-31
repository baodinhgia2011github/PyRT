import calendar
import time
import os
def clearConsole():
    os.system("CLS" if os.name=="nt" else "clear")
def getYearFromFile(inputFile):
    attempts=5
    while attempts>0:
        if os.path.exists(inputFile) and os.path.getsize(inputFile)>0:
            with open(inputFile,"r") as f:
                try:
                    year=int(f.readline().strip())
                    if 1<=year<2**1024:
                        return year
                    else:
                        print(f"ERROR: Invalid year in '{inputFile}'.\nPlease enter a valid year between 1 and 1^1024.")
                        return None
                except ValueError:
                    print(f"ERROR: The file '{inputFile}' does not contain a valid integer year.")
                    return None
        print(f"Waiting for input file '{inputFile}'... ({attempts} attempt(s) left)")
        time.sleep(1)
        attempts-=1
    print(f"ERROR: Unable to open input file '{inputFile}'.\nPlease ensure the file exist.")
    return None
def generateCalendar(year,outputFile):
    with open(outputFile,"w") as f:
        f.write(f"Calendar for {year}\n\n")
        for month in range(1,13):
            f.write(calendar.month(year,month))
            f.write("\n")
def main():
    inputFile,outputFile="calendar.inp","calendar.out"
    print(f"Please create and open the input file: '{inputFile}' and enter the year you want to create calendar for.")
    year=getYearFromFile(inputFile)
    if year is None:
        return
    clearConsole()
    generateCalendar(year,outputFile)
    print(f"Calendar generated successfully in '{outputFile}'.","Please re-enter the year in the input file if you want to generate another calendar.",sep="\n")
if __name__=="__main__":
    main()