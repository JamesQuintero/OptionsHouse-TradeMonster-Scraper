##### Scrapes price data from optionshouse/trademonster #####

import urllib.request           #script for URL request handling
import urllib.parse             #script for URL handling
import time                     #scripting timing handling
import datetime                 #data and time handling
from datetime import date


class OptionsHouse:


	def __init__(self):
		pass

	#retrieves num_days' worth of 1min data for stock_symbol
	def download1MinIntradayHistory(self, stock_symbol, num_days):

		# POST https://www.trademonster.com:443/services/chartsData HTTP/1.1
		# Host: www.trademonster.com
		# User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
		# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
		# Accept-Language: en-US,en;q=0.5
		# Accept-Encoding: gzip, deflate
		# Connection: keep-alive
		# Content-type: application/xml
		# Content-length: 530

		# <getDataForChartsAndVolatility>
		# 	<userId>xxxxxxxxxxxxxx</userId>
		# 	<studiesMaxPeriod>0</studiesMaxPeriod>
		# 	<frequency>1</frequency>
		# 	<range>480</range>
		# 	<retrieveVolatility>false</retrieveVolatility>
		# 	<includeExtendedHours>false</includeExtendedHours>
		# 	<instrumentId>xxxxxxxxxxxxxxx</instrumentId>
		# 	<delayed>false</delayed>
		# 	<instrumentType>Equity</instrumentType>
		# 	<symbols>
		# 		<symbol>AAPL</symbol>
		# 		<coefficient>1</coefficient>
		# 		<instrumentType>Equity</instrumentType>
		# 	</symbols>
		# </getDataForChartsAndVolatility>

		#user_id can be any 13 digit number
		user_id=1000000000013
		#might not be important
		studiesMaxPeriod=0
		#1 = 1 min data
		frequency=1

		#gets 1 month worth of 1min data
		if num_days>1:
			range_var=480

		#gets about the last day's worth
		if num_days==1:
			range_var=45

		#probably to identity what part of site data was retrieved
		instrumentId=1000000000450


		post_data="""<getDataForChartsAndVolatility>
									<userId>"""+str(user_id)+"""</userId>
									<studiesMaxPeriod>"""+str(studiesMaxPeriod)+"""</studiesMaxPeriod>
									<frequency>"""+str(frequency)+"""</frequency>
									<range>"""+str(range_var)+"""</range>
									<retrieveVolatility>false</retrieveVolatility>
									<includeExtendedHours>false</includeExtendedHours>
									<instrumentId>"""+str(instrumentId)+"""</instrumentId>
									<delayed>false</delayed>
									<instrumentType>Equity</instrumentType>
									<symbols>
										<symbol>"""+str(stock_symbol)+"""</symbol>
										<coefficient>1</coefficient>
										<instrumentType>Equity</instrumentType>
										</symbols>
									</getDataForChartsAndVolatility>"""
		post_data=post_data.encode('UTF-8')
		r = urllib.request.Request("https://www.trademonster.com:443/services/chartsData", data=post_data, headers={'Content-Type': 'application/xml'})
		u = urllib.request.urlopen(r)
		response = u.read()

		response=str(response.decode("utf-8"))



		to_return=[]
		while True or len(to_return):
			try:
				close=float(self.stringBetween(response, "<close>", "</close>"))
				response=response[response.find("</close>")+8:]

				high=float(self.stringBetween(response, "<high>", "</high>"))
				response=response[response.find("</high>")+7:]

				low=float(self.stringBetween(response, "<low>", "</low>"))
				response=response[response.find("</low>")+6:]

				open_price=float(self.stringBetween(response, "<open>", "</open>"))
				#has +90 because ~90 characters after are junk, and this makes the program faster
				response=response[response.find("</open>")+90:]

				temp_list={}
				temp_list['date']=""
				temp_list['open']=open_price
				temp_list['high']=high
				temp_list['low']=low
				temp_list['close']=close
				#never coded it to retrieve volume for some reason
				temp_list['volume']=0
				to_return.append(temp_list)
			except Exception as error:
				break

		#if wanting only today's data
		if num_days==1:
			cur_time=self.currentTime()

			#don't want to get extra data if past 4PM EST
			if cur_time['hour']<16:
				num_minutes=cur_time['hour']*60 + cur_time['minute']
			else:
				num_minutes=16*60

			old_minutes=9*60 + 30
			num_minutes=num_minutes-old_minutes

		else:
			num_minutes=num_days*6.5*60


		while len(to_return)>num_minutes and len(to_return)>0:
			to_return.pop(0)


		return to_return

	#retrieves stock_symbol's current price by looking at the current 1min data's closing price
	def currentPrice(self, stock_symbol):

		#user_id can be any 13 digit number
		user_id=1000000000003
		#might not be important
		studiesMaxPeriod=0
		#1 = 1 min data
		frequency=1
		#1 = 1 day of frequency data
		range_var=1
		#probably to identity what part of site data was retrieved
		instrumentId=1000000000450

		post_data="<getDataForChartsAndVolatility><userId>"+str(user_id)+"</userId><studiesMaxPeriod>"+str(studiesMaxPeriod)+"</studiesMaxPeriod><frequency>"+str(frequency)+"</frequency><range>"+str(range_var)+"</range><retrieveVolatility>false</retrieveVolatility><includeExtendedHours>false</includeExtendedHours><instrumentId>"+str(instrumentId)+"</instrumentId><delayed>false</delayed><instrumentType>Equity</instrumentType><symbols><symbol>"+str(stock_symbol)+"</symbol><coefficient>1</coefficient><instrumentType>Equity</instrumentType></symbols></getDataForChartsAndVolatility>"
		post_data=post_data.encode('UTF-8')
		try:
			r = urllib.request.Request("https://www.trademonster.com:443/services/chartsData", data=post_data, headers={'Content-Type': 'application/xml'})
			u = urllib.request.urlopen(r)
			response = u.read()

			response=str(response.decode("utf-8"))
		except Exception as error:
			print("Error trying to get current price, waiting 30 seconds to retry...")
			time.sleep(30)
			return currentPrice(stock_symbol)



		to_return=[]
		while len(to_return)==0:
			try:
				close=float(self.stringBetween(response, "<close>", "</close>"))
				response=response[response.find("</close>")+8:]

				high=float(self.stringBetween(response, "<high>", "</high>"))
				response=response[response.find("</high>")+7:]

				low=float(self.stringBetween(response, "<low>", "</low>"))
				response=response[response.find("</low>")+6:]

				open_price=float(self.stringBetween(response, "<open>", "</open>"))
				#has +90 because ~90 characters after are junk, and this makes the program faster
				response=response[response.find("</open>")+90:]

				temp_list={}
				temp_list['close']=close
				to_return.append(temp_list)
			except Exception as error:
				temp_list={}
				temp_list['close']=0
				to_return.append(temp_list)
				break

		return float(to_return[-1]['close'])

	#returns whatever part string is between "start" string and "end" string
	def stringBetween(self, string, start, end):

		if start in string and end in string:
			return string[string.find(start)+len(start):string.find(end)]

		return ""

	#returns current time in format: {"hour": 17, "minute": 3, "second": 49}
	def currentTime(self):
		#2013-12-15 17:45:35.177000
		curDate=str(datetime.datetime.utcnow() + datetime.timedelta(hours=-7))
		time=curDate.split(' ')
		time=time[1]
		time=time.split(':')

		to_return={}
		to_return['hour']=int(time[0])
		to_return['minute']=int(time[1])
		to_return['second']=int(float(time[2]))
		print(to_return)
		return to_return



if __name__=="__main__":
	optionshouse=OptionsHouse()

	symbols=["AAPL", "FB", "AAL", "BABA", "TWTR", "YHOO", "MSFT", "AMZN", "F"]
	for x in range(0, len(symbols)):
		print(symbols[x]+": "+str(optionshouse.currentPrice(symbols[x])))

	# data=optionshouse.download_1min_intraday_history(stock_symbol, 1)

	# with open("./optionshouse_"+str(stock_symbol)+".csv", 'w', newline='') as file:
	# 	contents = csv.writer(file)
	# 	contents.writerows(data)