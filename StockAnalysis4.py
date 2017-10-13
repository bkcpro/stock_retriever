'''
Python Final Project:
Listed Company Financial Retriver
Team 6

UI Group:
Fang Wang
Nija Binoy
Bhargava Kunchanapalli
'''


import tkinter as tk	
# import dictionaryEvents as de
from io import BytesIO
import os
import urllib
import urllib.request
import base64
from PIL import Image, ImageTk
from Scraper import Crawler
import webbrowser
from urllib import parse
from tkinter import messagebox as tkMessageBox

stockCrawler= None
linkDict=dict()
#inheriting Tk
class MainPanel(tk.Tk):
	def __init__(self, name):
		super(MainPanel, self).__init__()
		self.geometry("700x550+51+51") #### is not 700*550 better????
		self.title(name)
		self.initMainPanel()
		self.initMenuBar()

	def initMainPanel(self):
		self.searchText = None
		self.descLabel = None

		### inner frame ####
		label1=tk.Label(text ="Please input company name to search financial info: ",font="calibri 15 bold",width=1200,fg='White',bg='steel blue',height=2)
		label1.pack(fill=tk.X,side=tk.TOP)
		label2=tk.Label(width=3,bg='steel blue',height=800,pady=5)
		label2.pack(fill=tk.Y,side=tk.LEFT)
		label3=tk.Label(width=3,bg='steel blue',height=800,pady=5)
		label3.pack(fill=tk.Y,side=tk.RIGHT)
		label4=tk.Label(width=1200,text =" All copy right reserved by Python Team 6",
		fg='Black',bg='steel blue',height=2,pady=5)
		label4.pack(fill=tk.X,side=tk.BOTTOM)


	####### outer frame ##############
	def initMenuBar(self):
		menubar = tk.Menu(self,fg = "white",font="Calibri 12 bold",bg='steel blue')

                ### [About]###
		editmenu = tk.Menu(menubar, tearoff=0)
		editmenu.configure(fg= "white",font="Calibri 12 bold",bg='steel blue')
		editmenu.add_command(label="Google Finance", command=self.AboutGoogleFinance)
		
		editmenu.add_separator()
		editmenu.add_command(label="International Technological University", command=self.AboutITU)
		editmenu.add_separator()
		editmenu.add_command(label="Development Team", command=self.AboutDevelopTeam)
		
		
		menubar.add_cascade(label="About", menu=editmenu)
		self.config(menu=menubar)
		
		### [User Manual]####
		helpmenu=tk.Menu(menubar,tearoff=0)
		helpmenu.configure(fg= "white",font="Calibri 12 bold",bg='steel blue')
		helpmenu.add_command(label="User Manual",command=self.userManual)
		menubar.add_cascade(label="User Manual",menu=helpmenu)
		self.config(menu=menubar)

	def run(self):
		print("this text is going to get overided")
	def userManual(self):
		self.counter += 1
		file_name=r'F:\ITU course\Python\Final project\0815\UserManual.txt'
		manualWindow=tk.Toplevel(self)
		manualWindow.title('User Manual')
		file=open(file_name,'r')
		data=file.read()
		file.close()
		Results=tk.Label(manualWindow,text=data,justify="left",wraplength="500",relief="raised",font="calibri 12")
		Results.pack(side="top",fill="both",expand=True,padx=10,pady=10)

	def AboutGoogleFinance(self):
		self.counter += 1
		file_name=r'F:\ITU course\Python\Final project\0815\GoogleFinance.txt'
		manualWindow=tk.Toplevel(self)
		manualWindow.title('About Google Finance')
		file=open(file_name,'r')
		data=file.read()
		file.close()
		Results=tk.Label(manualWindow,text=data,justify="left",wraplength="500",relief="raised")
		Results.pack(side="top",fill="both",expand=True,padx=10,pady=10)
	def AboutITU(self):
		self.counter += 1
		file_name=r'F:\ITU course\Python\Final project\0815\ITU.txt'
		manualWindow=tk.Toplevel(self)
		manualWindow.title('About ITU')
		file=open(file_name,'r')
		data=file.read()
		file.close()
		Results=tk.Label(manualWindow,text=data,justify="left",wraplength="500",relief="raised")
		Results.pack(side="top",fill="both",expand=True,padx=10,pady=10)
	def AboutDevelopTeam(self):
		self.counter += 1
		file_name=r'F:\ITU course\Python\Final project\0815\PythonTeam6.txt'
		manualWindow=tk.Toplevel(self)
		manualWindow.title('About The Development Team')
		file=open(file_name,'r')
		data=file.read()
		file.close()
		Results=tk.Label(manualWindow,text=data,justify="left",wraplength="500",relief="raised")
		Results.pack(side="top",fill="both",expand=True,padx=10,pady=10)
		


#Class StockPanel is Inherited from MainPanel
class StockPanel(MainPanel):
	counter=0
	def __init__(self, name):
		super(StockPanel,self).__init__(name)
		
		self.initStockPanel()
		self.configure(background = 'steel blue')
	
	def run(self):
		self.mainloop()

	def initStockPanel(self):		
		# the area where we will enter text
		m1 = tk.PanedWindow(width=100)
		m1.pack(fill=tk.X,side=tk.TOP)

		m3 = tk.PanedWindow(m1, orient=tk.VERTICAL)
		
		m4 = tk.PanedWindow(m3)
		m3.add(m4)
		self.searchText = tk.Text(width=25, height=1,bg='white',font="calibri 12 bold")
		searchBtn = tk.Button(text ="  Search..  ",command = self.searchClick);
		searchBtn.config(fg = "white",font="calibri 14 bold",bg='midnight blue',relief=tk.RAISED)
		m4.add(self.searchText)
		m4.add(searchBtn)
#label for logo ********************
		# logoLabel = tk.Label(width=30)
		# logoLabel.place(x=5, y=160)  
		# image=img,
		
		m1.add(m3)
		self.infoPanel = tk.PanedWindow(m1, orient=tk.VERTICAL)
		m3.add(self.infoPanel)

		#m1.add(m3)


#****************************************************************

		m2 = tk.PanedWindow(m1, orient=tk.VERTICAL)
		m1.add(m2)

		addBtn = tk.Button(text ="Stock Price",font="calibri 14 bold",width=20,fg='white',bg='steel blue',command = self.stockPriceClick)
		m2.add(addBtn)

		f = tk.Frame(height=5, width=32,pady=20)
		#f.pack_propagate(0) # don't shrink
		f.pack(fill=tk.X,side=tk.TOP)

		updateBtn = tk.Button(f ,text ="Company History",font="calibri 14 bold",fg='white',bg='steel blue' ,command = self.compHistory)
		updateBtn.pack(fill=tk.X, side=tk.TOP)
		m2.add(f)

		fDel = tk.Frame(height=5, width=32,pady=20)
		#f.pack_propagate(0) # don't shrink
		fDel.pack(fill=tk.X,side=tk.TOP)

		deleteButton = tk.Button(fDel ,text ="Relevant Analysis",font="calibri 14 bold",fg='white',bg='steel blue',
		command = self.relAnalysis);
		deleteButton.pack(fill=tk.X, side=tk.TOP)
		m2.add(fDel)

#newly added buttons******************************************
		news=tk.Frame(height=5,width=32,pady=20)
		news.pack(fill=tk.X,side=tk.BOTTOM)
		

		newsButton= tk.Button(news ,text ="Latest News",font="calibri 14 bold",fg='white',bg='steel blue',
		command = self.lateNews);
		newsButton.pack(fill=tk.X,side=tk.BOTTOM)
		m2.add(news)

		trend=tk.Frame(height=5,width=32,pady=20)
		trend.pack(fill=tk.X,side=tk.BOTTOM)

		trendButton= tk.Button(trend ,text ="Industry Trend",font="calibri 14 bold",fg='white',bg='steel blue',
		command = self.indusTrend);
		trendButton.pack(fill=tk.X,side=tk.BOTTOM)
		m2.add(trend)

		saveInfo= tk.Frame(height=5, width=32,pady=20)
		saveInfo.pack(fill=tk.X,side=tk.BOTTOM)

		saveButton = tk.Button(saveInfo ,text ="Save Search Result", font="calibri 14 bold",fg="white",bg="midnight blue",
		command=self.saveRes);
		saveButton.pack(side=tk.BOTTOM)
		m2.add(saveInfo)

 




################ Search Implementation#############################	
	def searchClick(self):
		self.srchTxt = self.searchText.get(1.0,tk.END).replace('\n', '')
		#print("Tx:" + self.srchTxt.strip())
		if(self.srchTxt.strip()==''):
		 	tkMessageBox.showwarning("Error message!",'Enter name of the Company! ')
		 	return
		else:
			global stockCrawler
			stockCrawler=Crawler(self.srchTxt)
			self.createInfoPanel()
		#if(stockCrawler!= None):
		# 		# desc = dc.userView(srchTxt)
		# if(desc == None):
		# 	self.myPanel.setDesc("")
		# 	tkMessageBox.showwarning("Entry Not Found","No Entry Found for given Keyword " + srchTxt)
		# else:
		# 	self.myPanel.setDesc(desc)
################ [Stock Price] button opens a new window ########################
	def stockPriceClick(self):
		self.counter += 1
		t = tk.Toplevel(self,background='steel blue')
		t.title("STOCK PRICE DETAILS AND CHART")
		mainWin= tk.PanedWindow(t,orient=tk.VERTICAL,bg='midnight blue',relief=tk.RAISED)
		mainWin.pack(expand=1)
#finance chart representing 5-day stock price
		textLabel1= tk.Label(mainWin,text="5-day Stock Price Performance",justify="left",bg='steel blue')
		textLabel1.config(bd=6,fg = "white",font="calibri 14 bold")
		textLabel1.pack(side="top",padx=10,pady=10)
		mainWin.add(textLabel1)
		secWin= tk.PanedWindow(mainWin)
		mainWin.add(secWin)
		labelWin = tk.PanedWindow(secWin, orient=tk.VERTICAL,background='steel blue',relief=tk.RAISED)
		secWin.add(labelWin)


#Company name******************		
		cmpnyName,b=stockCrawler.get_name()
		# cmpnyName=''.join(cmpnyName)
		cmpnyLabel=tk.Label(labelWin,text=cmpnyName,justify="left",bg='steel blue')
		cmpnyLabel.config(fg = "black",font="calibri 14 bold")
		cmpnyLabel.pack(side="top",padx=10,pady=10)
		labelWin.add(cmpnyLabel)
#  company stock price********************
		stockPrice=stockCrawler.price
		stkPriceLabel=tk.Label(labelWin,text='Current Price: $'+stockPrice,justify="left",bg='steel blue')
		stkPriceLabel.config(fg = "black",font="calibri 14 bold")
		stkPriceLabel.pack(side="top",padx=10,pady=10)
		labelWin.add(stkPriceLabel)
#The value of price Change Percent********************
		percntgChange=stockCrawler.price_change_rate
		moreInfo=stockCrawler.information
		newMoreInfo=""
		i=1
		InfoDict={1:'Range ',2:'52 week ',3:'Open',4:'Vol/Avg',5:'Mkt cap',6:'P/E',7:'Div/yield',8:'EPS',9:'Shares',10:'Beta',11:'Inst.own'}
		for item in moreInfo:
			title=InfoDict.get(i)
			fullValue=title+":"+item+" "
			newMoreInfo+=fullValue
			i=i+1

		priceChangeLabel=tk.Label(labelWin,text='Price Change {0} :'.format(percntgChange)+"\n"+newMoreInfo,justify="left",bg='steel blue')
		priceChangeLabel.config(fg = "black",font="calibri 14 bold")
		priceChangeLabel.pack(side="top",padx=10,pady=10)
		labelWin.add(priceChangeLabel)

		secWin.add(labelWin)

#### stock price chart (5days) #################

		url = stockCrawler.chart
		with urllib.request.urlopen(url) as u:
			raw_data = u.read()
		im = Image.open(BytesIO(raw_data))
		img=ImageTk.PhotoImage(im)
		imgLabel1 = tk.Label(secWin,image = img,bg='midnight blue',relief=tk.RAISED)
		imgLabel1.image=img

		imgLabel1.pack(side="bottom",padx=10,pady=10)
		secWin.add(imgLabel1)

################ [Company History] button opens a new window ########################
	def compHistory(self):
		self.counter += 1
		t = tk.Toplevel(self,background='steel blue')
		t.title("COMPANY DETAILS")
		mainWin2= tk.PanedWindow(t,orient=tk.VERTICAL,bg='midnight blue',relief=tk.RAISED)
		mainWin2.pack(expand=1)

		cmpnyName,b=stockCrawler.get_name()
		# cmpnyName=''.join(cmpnyName)
		textLabel2= tk.Label(mainWin2,text=cmpnyName+' Description from Google Finance:',justify="left",bg='steel blue')
		textLabel2.config(bd=6,fg = "white",font="calibri 14 bold",underline=1)
		textLabel2.pack(side="top",padx=10,pady=10)
		mainWin2.add(textLabel2)
		secWin2= tk.PanedWindow(mainWin2)
		mainWin2.add(secWin2)
		labelWin2 = tk.PanedWindow(secWin2, orient=tk.VERTICAL,background='steel blue',relief=tk.RAISED)
		secWin2.add(labelWin2)

		a,b=stockCrawler.get_related_companies()

		cmpnyLabel2=tk.Label(labelWin2,text=a,padx=3,pady=3,justify="left",wraplength="600",relief="raised",bg='steel blue')
		cmpnyLabel2.config(fg = "black",font="calibri 13")
		cmpnyLabel2.pack(side="top",padx=10,pady=200)
		labelWin2.add(cmpnyLabel2)

		secWin2.add(labelWin2)

################ [Relevant Analysis] button opens a new window ########################
	def relAnalysis(self):
		self.counter += 1
		t = tk.Toplevel(self,background='steel blue')
		t.title("RELEVANT ANALSIS (Income Statement Details)")
		mainWin3= tk.PanedWindow(t,orient=tk.VERTICAL,bg='midnight blue',relief=tk.RAISED)
		mainWin3.pack(expand=1)

		
		textLabel3= tk.Label(mainWin3,text="Revenue,Net income,Profit margin (15M)",justify="left",bg='steel blue')
		textLabel3.config(bd=6,fg = "white",font="calibri 14 bold")
		textLabel3.pack(side="top",padx=10,pady=10)
		mainWin3.add(textLabel3)
		secWin3= tk.PanedWindow(mainWin3)
		mainWin3.add(secWin3)
		labelWin3 = tk.PanedWindow(secWin3, orient=tk.VERTICAL,background='steel blue',relief=tk.RAISED)
		secWin3.add(labelWin3)
#*************** newly added test*******************
		chart1,chart2=stockCrawler.get_quarterly_chart()
		
		url = "http://"+chart1
	
		with urllib.request.urlopen(url) as u:
			raw_data = u.read()
		im = Image.open(BytesIO(raw_data))
		img=ImageTk.PhotoImage(im)
#**************************************

		chart1Label=tk.Label(labelWin3,image = img,bg='midnight blue',relief=tk.RAISED)
		chart1Label.image=img
		chart1Label.pack(side="top",padx=10,pady=10)
		labelWin3.add(chart1Label)

		secWin3.add(labelWin3)

#**************************************newly added********************
		url = "http://"+chart2
		with urllib.request.urlopen(url) as u:
			raw_data = u.read()
		im = Image.open(BytesIO(raw_data))
		img=ImageTk.PhotoImage(im)
		textLabel3= tk.Label(mainWin3,text="Revenue,Operating income,Operating margin(%) (15M) ",justify="left",bg='steel blue')
		textLabel3.config(bd=6,fg = "white",font="calibri 14 bold")
		textLabel3.pack(side="top",padx=10,pady=10)
		mainWin3.add(textLabel3)

		chart2Win= tk.PanedWindow(mainWin3)
		chart2Label=tk.Label(chart2Win,image = img,bg='midnight blue',relief=tk.RAISED)
		chart2Label.image=img
		chart2Label.pack(side="bottom",padx=10,pady=10)
		chart2Win.add(chart2Label)

		mainWin3.add(chart2Win)

#**********************************************************

		# url = stockCrawler.chart
		# with urllib.request.urlopen(url) as u:
		# 	raw_data = u.read()
		# im = Image.open(BytesIO(raw_data))
		# img=ImageTk.PhotoImage(im)
		# imgLabel1 = tk.Label(secWin,image = img,bg='midnight blue',relief=tk.RAISED)
		# imgLabel1.image=img

		# imgLabel1.pack(side="bottom",padx=10,pady=10)
		# secWin.add(imgLabel1)

################ [Latest News] button opens a new window ########################
	def lateNews(self):
		self.counter += 1
		t = tk.Toplevel(self,background='steel blue')
		t.title("RELATED NEWS")
		mainWin4= tk.PanedWindow(t,orient=tk.VERTICAL,bg='midnight blue',relief=tk.RAISED)
		mainWin4.pack(expand=1)

		titles,links=stockCrawler.get_news()
		
		
		textLabel4= tk.Label(mainWin4,text="The latest news are:",justify="left",bg='steel blue')
		textLabel4.config(bd=6,fg = "white",font="calibri 14 bold")
		textLabel4.pack(side="top",padx=10,pady=10)
		mainWin4.add(textLabel4)

		secWin4= tk.PanedWindow(mainWin4,orient=tk.VERTICAL)
		mainWin4.add(secWin4)

		
		

		i=1
		for item in titles:
			if i==16:
				break
			newItem=str(i)+')'+item
			linkDict[newItem]=links[i]
			labelWin4 = tk.Label(secWin4,text=newItem, fg="black", anchor=tk.W,cursor="hand2",justify=tk.RIGHT,relief=tk.RAISED)
			labelWin4.config(font="calibri 12 bold",padx=10,pady=10)
			labelWin4.pack()
			labelWin4.bind("<Button-1>",self.callback)
			secWin4.add(labelWin4)
			i+=1

	def callback(self,event):

		    linkToOpen=linkDict.get(event.widget.cget("text"))
		    
		    webbrowser.open_new(linkToOpen)	

################ [Industry Trend] button opens a new window ########################
	def indusTrend(self):
		self.counter += 1
		t = tk.Toplevel(None,background='steel blue')
		t.title("INDUSTRY TREND")
		mainWin5= tk.PanedWindow(t,orient=tk.VERTICAL,bg='midnight blue',relief=tk.RAISED)
		mainWin5.pack(expand=1)
		a,b=stockCrawler.get_related_companies()
		cmpnyName="<Name>"
		textLabel5= tk.Label(mainWin5,text="Other Companies Within The Industry Are:",justify="left",bg='steel blue')
		textLabel5.config(bd=6,fg = "white",font="calibri 14 bold")
		textLabel5.pack(side="top",padx=10,pady=10)
		mainWin5.add(textLabel5)
		secWin5= tk.PanedWindow(mainWin5,orient=tk.VERTICAL)
		mainWin5.add(secWin5)
		labelWin5 = tk.PanedWindow(secWin5, orient=tk.HORIZONTAL,background='steel blue',relief=tk.RAISED)
		# secWin5.add(labelWin5)

		# cmpnyLabel5=tk.Label(labelWin5,text=b,justify="left",bg='steel blue',wraplength=600)
		# cmpnyLabel5.config(fg = "white",font="calibri 14 bold")
		# cmpnyLabel5.pack(side="top",padx=10,pady=10)
		# labelWin5.add(cmpnyLabel5)

		# secWin5.add(labelWin5)
		titleDict={1:'STOCK',2:'COMPANYNAME',3:'PRICE',4:'CHANGE',5:'CHG%',6:'MKTCAP'}
		

		for key in titleDict:
			cmpnyLabel5 = tk.Label(labelWin5,text=titleDict[key], fg="red")
			if(key == 2):
				cmpnyLabel5.config(font="calibri 15 bold",padx=2,pady=2,anchor=tk.W,width=30,relief=tk.RAISED)
			else:
				cmpnyLabel5.config(font="calibri 15 bold",padx=2,pady=2,anchor=tk.W,width=10)
			cmpnyLabel5.pack()
			labelWin5.add(cmpnyLabel5)
		secWin5.add(labelWin5)
		labelWin5 = tk.PanedWindow(secWin5, orient=tk.HORIZONTAL,background='steel blue',relief=tk.RAISED)



		for row in b:
			rowCnt = 1
			for item in row:
				cmpnyLabel5 = tk.Label(labelWin5,text=item.replace("\"","").replace("[",""), fg="black")
				if(rowCnt == 2):
					cmpnyLabel5.config(font="calibri 14 bold",padx=2,pady=2,anchor=tk.W,width=30)
				else:
					cmpnyLabel5.config(font="calibri 14 bold",padx=2,pady=2,anchor=tk.W,width=10)
				cmpnyLabel5.pack()
				labelWin5.add(cmpnyLabel5)
				rowCnt+=1
			secWin5.add(labelWin5)
			labelWin5 = tk.PanedWindow(secWin5, orient=tk.HORIZONTAL,background='steel blue',relief=tk.RAISED)

################ [Save Search Result] Saves results into a file ########################
	def saveRes(self):

		x, y = stockCrawler.get_name()
		str1 = "CompanyInfo_"+"".join(x.split())+".txt"
		str2 = "PriceChart_"+"".join(x.split())+".jpg"
		str3 = "RelevantAnalysis1_"+"".join(x.split())+".jpg"
		str4 = "RelevantAnalysis2_"+"".join(x.split())+".jpg"

		filp = open(str1,"w")

		filp.write("Company Name: {!s}, Nasdaq Name: {!s}".format(x, y))

		a, b = stockCrawler.get_related_companies()
		filp.write("\n\nCompany description: %s" % a)

		filp.write("\n\nStock Price: %s"%stockCrawler.price)

		filp.write("\n\nCompany Related Information: %s" % stockCrawler.information)

		filp.write("\n\nPrice Change Rate: %s"%stockCrawler.price_change_rate)

		urllib.request.urlretrieve(stockCrawler.chart, str2) #StockChart information

		chart1, chart2 = stockCrawler.get_quarterly_chart()  #Relevant Analysis
		url_relevant1 = "http://" + chart1
		url_relevant2 = "http://" + chart2
		urllib.request.urlretrieve(url_relevant1, str3)
		urllib.request.urlretrieve(url_relevant2, str4)

		filp.close()


################ InfoPanel ########################
	def createInfoPanel(self):
		for child in self.infoPanel.winfo_children():
				print(type(child))
				child.destroy()
		logoUrl=stockCrawler.get_logo(self.srchTxt)
		if(logoUrl==None):
			defaultImg=Image.open('defaultImg.jpg')
			im=defaultImg.resize((150, 150), Image.ANTIALIAS) 
		else:
			logoUrl="http://"+ logoUrl
			with urllib.request.urlopen(logoUrl) as u:
				raw_data = u.read()
			im = Image.open(BytesIO(raw_data))
 
		img=ImageTk.PhotoImage(im)
		logoLabel = tk.Label(self.infoPanel,image=img,width=150,anchor=tk.S,justify=tk.LEFT,height=150)
		logoLabel.image=img
		self.infoPanel.add(logoLabel)
		print(self.infoPanel)

# Company name******************		
		companyName,b=stockCrawler.get_name()
		# companyName=''.join(companyName)
		stockPrice=stockCrawler.price
		fullValue="Company Name:"+'\n'+companyName
		cmpnyLabel=tk.Label(self.infoPanel,text=fullValue)
		cmpnyLabel.config(fg = "black",font="calibri 14 bold",wraplength=500,height=5)
		#cmpnyLabel.pack()
		self.infoPanel.add(cmpnyLabel)
		#m1.add(m3)
#  company stock price********************
		stockPrice=stockCrawler.price
		stkPriceLabel=tk.Label(self.infoPanel,text='Current Stock price:'+'\n'+'$'+stockPrice)
		stkPriceLabel.config(fg = "black",font="calibri 14 bold",pady=-50,height=0)
		#stkPriceLabel.pack()
		self.infoPanel.add(stkPriceLabel)
# 		#m1.add(m3)
# # The value of price Change Percent********************
# 		percntgChange=stockCrawler.price_change
# 		priceChangeLabel=tk.Label(self.infoPanel,text='Price Change value:'+percntgChange,justify="left")
# 		priceChangeLabel.config(fg = "midnight blue",font="calibri 14 bold")
# 		priceChangeLabel.pack(side="top",padx=10,pady=10)
# 		self.infoPanel.add(priceChangeLabel)

#################  Search frame ###############################		
 
#Build my Panel		
myPanel= StockPanel("LISTED COMPANY FINANCIAL INFO RETRIEVER")
myPanel.run()

