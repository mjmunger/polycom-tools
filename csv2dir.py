#!/usr/bin/python
import csv
with open('/tmp/CompanyDirectory.csv','rb') as csvfile:
	myreader = csv.reader(csvfile,delimiter=',',quotechar='"')
	for row in myreader:
		print row