"""
writer to csv file
"""

import csv
import trackers
import settings

def create_excel():
    if (trackers.measStack):
        with open(settings.excelFileName, "w", newline='') as csv_output:
            csv_output = csv.writer(csv_output)
            # Insert Metadata/ Constants:
            csv_output.writerow(['Start Date','%s' % settings.startDate])
            csv_output.writerow(['Start Time','%s' % settings.startTime])
            csv_output.writerow(['printerNumber','%s' % settings.printerNumber])
            csv_output.writerow(['designName','%s' % settings.designName])
            csv_output.writerow(['printParameters','%s' % settings.printParameters])
            # Insert Header:
            csv_output.writerow(['localID','Measurement','Seconds from reference','Time'])
            # Insert data:
            csv_output.writerows(trackers.measStack)
