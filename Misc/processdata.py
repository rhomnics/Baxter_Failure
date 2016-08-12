import csv
with open('results-survey791575.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['             Thank you for watching.     STOP!      Intervene                      [][VidNum]'])