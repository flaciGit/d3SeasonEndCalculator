#DESC:
#
#	Diablo 3 season length analysis with data from https://diablo.fandom.com/wiki/Season
#
#
#	python3
#	data fetch from html
#	data conversion to date type
#	command line arguments
#	season end date calculations with average, median and addition

import argparse
from lxml import html
# pip install --upgrade lxml
import requests
# pip install requests
import statistics
# pip install statistics 
from datetime import datetime, timedelta

#command line argument parsing
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description='In depth analysis.')
parser.add_argument("-i", type=str2bool, nargs='?', const=True, default=False, help="Activate in depth mode.")

#calculating dates
def d3SeasonEndCalculator(inDepth):

	#fetch data
	page = requests.get('https://diablo.fandom.com/wiki/Season')
	tree = html.fromstring(page.content)
	
	seasonDates = tree.xpath('//table[@class="article-table"]/tr//td/text()')
	
	#extract dates from data
	i = 1
	data = []
	while(i < len(seasonDates)):
		
		if(seasonDates[i].strip()):
			data.append(seasonDates[i].strip())
		if(i%3 == 0):
			i+=4
		else:
			i+=1
	
	if(inDepth):
		print("\nDATES:\n")
		print(data)
	
	#calculate season lengths
	i = 0
	seasonLengths = []
	
	while(i < len(data)-1):
		seasonLength = datetime.strptime(data[i+1], '%d %b %Y') - datetime.strptime(data[i], '%d %b %Y')
		seasonLengths.append(seasonLength.days)
		if(i%2==0):
			i+=2
		else:
			i+=1
	
	if(inDepth):
		print("\nSEASON LENGTHS: (days)\n")
		print(seasonLengths)
	
	
	print("\nESTIMATED SEASON LENGTHS:")
	
	#Average season length
	sum = 0
	print("\n\tAverage season length:")
	for x in seasonLengths:
		sum += x
		
	print("\t",sum // len(seasonLengths),"days")
	
	if(inDepth):
		#Average season length without the longest season
		print("\n\tAverage season length without the longest:")
		print("\t",(sum - max(seasonLengths)) // (len(seasonLengths)-1),"days")
		
		#Average season length without the shortest season
		print("\n\tAverage season length without the shortest:")
		print("\t",(sum - min(seasonLengths)) // (len(seasonLengths)-1),"days")
		
		#Average season length without the longest and shortest season
		print("\n\tAverage season length without the longest and shortest season:")
		print("\t",(sum - max(seasonLengths) - min(seasonLengths)) // (len(seasonLengths)-2),"days")
		
		#median
		print("\n\tMedian of the season lengths:")
		print("\t",statistics.median(seasonLengths),"days")

	#estimated season end date
	print("\n\tAverage season end date:")
	print("\t", datetime.strptime(data[len(data)-1], '%d %b %Y').date() + timedelta(days=(sum // len(seasonLengths))))
	

	if(inDepth):
		#Average season end date without the longest season
		print("\n\tAverage season end date without the longest:")
		print("\t",datetime.strptime(data[len(data)-1], '%d %b %Y').date() +  timedelta((sum - max(seasonLengths)) // (len(seasonLengths)-1)))
		
		#Average season end date without the shortest season
		print("\n\tAverage season end date without the shortest:")
		print("\t",datetime.strptime(data[len(data)-1], '%d %b %Y').date() +  timedelta((sum - min(seasonLengths)) // (len(seasonLengths)-1)))
		
		
		#Average season end date without the longest and shortest season
		print("\n\tAverage season end date without the longest and shortest season:")
		print("\t",datetime.strptime(data[len(data)-1], '%d %b %Y').date() +
			timedelta((sum - max(seasonLengths) - min(seasonLengths)) // (len(seasonLengths)-2)))
		
		#Season end date with the median
		print("\n\tSeason end date with the median of the season lengths:")
		print("\t",datetime.strptime(data[len(data)-1], '%d %b %Y').date() + timedelta(statistics.median(seasonLengths)))
		
		
	#season end with the simple addition of 90 days to the start date
	print("\n\tSeason end date with the addition of 90 days:")
	print("\t",datetime.strptime(data[len(data)-1], '%d %b %Y').date() + timedelta(90))
		
		
		
		
if __name__ == '__main__':
	args = parser.parse_args()
	d3SeasonEndCalculator(args.i**1)