#
# Project:     Twitter Followers Keeper
# Project URL: http://github.com/sch3m4/tfk
#
# Author:      Chema Garcia (aka sch3m4)
# Contact:     @sch3m4
#              chema@safetybits.net
#              http://safetybits.net
#
# Date:        9/2012
# 
#

import sys
import time
import pynotify
import threading

from tfkui import Ui_MainWindow,Ui_frmAbout,Ui_frmLog
from followers import Followers

from PyQt4 import QtCore,QtGui,QtSql
from matplotlib import pyplot
from datetime import datetime


class TFK(QtGui.QMainWindow):
	"""
	The main class of the application
	"""

	# main window
	ui = None
	# database
	DBFILE = 'tfk.db'
	ACCOUNTS_TABLE = 'accounts'
	FOLLOWERS_TABLE = 'followers'
	LOG_TABLE = 'log'
	db = None
	query = None
	# followers class to get the followers for a given account
	followers = None
	# system tray class instance
	systray = None
	# time values
	timevals = None
	# thread to check the followers
	threadck = None
	threadfinish = None  # event to stop checking
	# logs dialog
	logs = None
	# about dialog
	about = None


	class SystemTray(QtGui.QSystemTrayIcon):
		sysTray = None
		parent = None
		hidden = False
		
		def setParent(self,parent):
			self.parent = parent

		def activated(self,reason):
			if reason == QtGui.QSystemTrayIcon.DoubleClick:
				if self.hidden == False:
					self.parent.hide()
					self.hidden = True
				else:
					self.parent.show()
					self.hidden = False


		def create(self):
			self.sysTray = QtGui.QSystemTrayIcon(self)
			trayicon = QtGui.QIcon()
			trayicon.addPixmap(QtGui.QPixmap(QtCore.QString.fromUtf8(":/imagenes/icono")))
			self.sysTray.setIcon(trayicon)
			self.connect(self.sysTray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.activated)
			self.sysTray.setVisible(True)
			
			
		def showMessage(self,title="[ TFKeeper ]",message=None,icon="dialog-information",urgency=pynotify.URGENCY_NORMAL,timeout=2000):
			n = pynotify.Notification(title,message,icon)
			n.set_urgency(urgency)
			n.set_timeout(timeout)
			n.show()


		def destroy(self):
			self.sysTray.setVisible(False)

	# [  TIME VALUES MODIFICATIONS  ]
	# -------------------------------
	class TimeValues():
		# check interval
		CHECK_INTERVAL = 30 * 60
		# superclass
		parent = None

		def setParent(self,parent):
			self.parent = parent


		# check interval
		def modifiedInterval(self,val):
			"""
			Function to update the check interval
			"""
			self.CHECK_INTERVAL = val * 60
			
			
		def getInterval(self):
			return self.CHECK_INTERVAL


		# connection timeout
		def modifiedTimeout(self,val):
			"""
			Function to update the connection timeout
			"""
			try:
				timeout = int(val)
				self.parent.followers.setTimes(timeout=timeout)
				if timeout == 0:
					raise Exception('Connection timeout cannot be zero')
			except Exception,e:
				QtGui.QMessageBox.critical(None, "Incorrect connection timeout value", str(e))
				self.parent.ui.spbTimeout.setValue(Followers.TIMEOUT)


		# connection retries
		def modifiedRetries(self,val):
			"""
			Function to update the connection retries
			"""
			try:
				retries = int(val)
				self.parent.followers.setTimes(retries=retries)
			except Exception,e:
				QtGui.QMessageBox.critical(self, "Incorrect connection retries value", str(e))
				self.parent.ui.spbRetries.setValue(Followers.RETRIES)

			
		# connection retries delay on error (min)
		def modifiedMinDelay(self,val):
			"""
			Function to update the connection retries delay on error (min)
			"""
			try:
				delay = int(val)
				if delay > self.parent.followers.MAX_DELAY:
					raise Exception('Min. delay must by lower than max. delay')
				self.parent.followers.setTimes(mindelay=delay)
			except Exception,e:
				QtGui.QMessageBox.critical(None, "Incorrect value for connection retries (min.)" , str(e))
				self.parent.ui.spbMinDelay.setValue(Followers.MIN_DELAY)
			
			
		# connection retries delay on error (max)
		def modifiedMaxDelay(self,val):
			"""
			Function to update the connection retries delay on error (max)
			"""
			try:
				delay = int(val)
				if delay < self.followers.MIN_DELAY:
					raise Exception('Max. delay must be bigger than min. delay')
				self.followers.setTimes(maxdelay=delay)
			except Exception,e:
				QtGui.QMessageBox.critical(self, "Incorrect value for connection retries (max.)" , str(e))
				self.ui.spbMaxDelay.setValue(Followers.MAX_DELAY)


	def __init__(self):

		# initializes the GUI
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		# about dialog
		self.about = QtGui.QDialog()
		self.about.ui = Ui_frmAbout()
		self.about.ui.setupUi(self.about)
		self.about.setAttribute(QtCore.Qt.WA_DeleteOnClose)		
		
		# store some needed objects
		self.followers = Followers()
		self.systray = self.SystemTray()
		self.systray.setParent(self)
		self.timevals = self.TimeValues()
		self.timevals.setParent(self)

		self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
		self.db.setDatabaseName(self.DBFILE)
		# cannot open database
		if not self.db.open():
			QtGui.QMessageBox.critical(self, "Cannot open database file", "The database file cannot be opened")
			sys.exit(-1)  # fix this

		# display on LCD the slider interval value
		self.ui.sldInterval.valueChanged.connect(self.ui.lcdInterval.display)
		# update the check interval
		self.ui.sldInterval.valueChanged.connect(self.timevals.modifiedInterval)
		# update the timeout
		self.ui.spbTimeout.valueChanged.connect(self.timevals.modifiedTimeout)
		# update connection retries
		self.ui.spbRetries.valueChanged.connect(self.timevals.modifiedRetries)
		# update min. delay
		self.ui.spbMinDelay.valueChanged.connect(self.timevals.modifiedMinDelay)
		# update max. delay
		self.ui.spbMaxDelay.valueChanged.connect(self.timevals.modifiedMaxDelay)

		# buttons events
		QtCore.QObject.connect(self.ui.btnStart, QtCore.SIGNAL("clicked()"), self.event_watching)
		# show about window
		QtCore.QObject.connect(self.ui.btnAbout, QtCore.SIGNAL("clicked()"), self.about.exec_)
		QtCore.QObject.connect(self.ui.btnViewLog, QtCore.SIGNAL("clicked()"), self.showLogWindow)
		# save chart
		QtCore.QObject.connect(self.ui.btnSaveChart, QtCore.SIGNAL("clicked()"), self.showSaveChart)
		# when changes the account name, display his followers
		#QtCore.QObject.connect(self.ui.cboAccount, QtCore.SIGNAL("currentIndexChanged(string)"), self.displayStoredFollowers)
		self.ui.cboAccount.activated.connect(self.displayStoredFollowers)

		# set the account combobox editable
		self.ui.cboAccount.setEditable(True)

		self.query = QtSql.QSqlQuery()
		# enables foreign keys
		self.query.exec_("PRAGMA foreign_keys = ON")
		# create the log table
		self.query.exec_("CREATE TABLE %s( id INTEGER PRIMARY KEY , date DATE , message TEXT )" % self.LOG_TABLE )
		# after insert, autoadd the 'date' datetime
		self.query.exec_("CREATE TRIGGER autoadded_log AFTER INSERT ON %s BEGIN UPDATE %s SET date = DATETIME('NOW') WHERE rowid = new.rowid; END;" % (self.LOG_TABLE, self.LOG_TABLE))
		# create the accounts table
		self.query.exec_("CREATE TABLE %s( id INTEGER PRIMARY KEY , name TEXT UNIQUE , added DATE , lastchecked DATE )" % self.ACCOUNTS_TABLE )
		# after insert, autoadd the 'added' datetime
		self.query.exec_("CREATE TRIGGER autoadded_account AFTER INSERT ON %s BEGIN UPDATE %s SET added = DATETIME('NOW') WHERE rowid = new.rowid; END;" % (self.ACCOUNTS_TABLE, self.ACCOUNTS_TABLE))
		# create the followers table
		self.query.exec_("CREATE TABLE %s( accountid INTEGER , follower TEXT, started DATE , stopped DATE , FOREIGN KEY (accountid) REFERENCES accounts(id))" % self.FOLLOWERS_TABLE )
		# after insert, autoadd the 'started' datetime
		self.query.exec_("CREATE TRIGGER autoadded_follower AFTER INSERT ON %s BEGIN UPDATE %s SET started = DATETIME('NOW') WHERE rowid = new.rowid; END;" % (self.FOLLOWERS_TABLE, self.FOLLOWERS_TABLE))


		self.displayStoredAccounts()
		self.displayStoredFollowers()

		# set the tray icon
		self.systray.create()
		

	def displayStoredFollowers(self,account=None):
		
		# set the followers of the current account
		if account is None or type(account) == int:
			account = self.ui.cboAccount.currentText()
		
		if len(account) > 0:
			self.query.prepare("SELECT COUNT(follower) FROM %s WHERE accountid = (SELECT id FROM %s WHERE name = :account) AND stopped IS NULL" % (self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE) )
			self.query.bindValue(':account', account)
			self.query.exec_()
			self.query.next()
			val = str(self.query.value(0).toPyObject())
			self.ui.lcdFollowers.display(val)
			
	
	def displayStoredAccounts(self):
		# retrieves the stored accounts
		self.query.exec_("SELECT name FROM %s" % self.ACCOUNTS_TABLE)
		while self.query.next():
			item = self.query.value(0).toString()
			if self.ui.cboAccount.findText(item) < 0:
				self.ui.cboAccount.addItem(item)
			
			
	def addLog(self,message,icon='dialog-information',timeout=2000,todb = False):
		"""
		Function to add an entry to Log table
		"""
		if todb is True:
			self.query.prepare("INSERT INTO %s (message) VALUES (:message)" % self.LOG_TABLE)
			self.query.bindValue(":message", message )
			self.query.exec_()
			
		self.systray.showMessage(message=message,icon=icon,timeout=timeout)
	
	def addAccount(self,account):
		"""
		Function to add an account to the database
		"""
		self.query.prepare("INSERT INTO %s (name) VALUES (:name)" % self.ACCOUNTS_TABLE)
		self.query.bindValue(":name" , account)
		self.query.exec_()
	
	
	def updateAccountChecked(self,account):
		self.query.prepare("UPDATE %s SET lastchecked = DATETIME('NOW') WHERE name = :account" % self.ACCOUNTS_TABLE)
		self.query.bindValue(':account', account)
		self.query.exec_()
	
	
	def addFollower(self,account,follower):
		self.query.prepare("INSERT INTO %s (accountid,follower) VALUES((SELECT id FROM %s WHERE name = :account),:follower)" % (self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE) )
		self.query.bindValue(":account",account)
		self.query.bindValue(":follower",follower)
		self.query.exec_()
	
	
	def rmFollower(self,account,follower):
		self.query.prepare("UPDATE %s SET stopped = DATETIME('NOW') WHERE follower = :follower AND accountid = (SELECT id FROM %s WHERE name = :account)" % (self.FOLLOWERS_TABLE,self.ACCOUNTS_TABLE))
		self.query.bindValue(":account",account)
		self.query.bindValue(":follower",follower)
		self.query.exec_()
		
		
	def closeEvent(self, event):
		"""
		We're about to finish
		"""
		
		if self.threadfinish is not None:  # there is a thread running
			self.threadfinish.set()
			self.threadck.join(0)

		# close the database
		self.db.close()
		# remove systray
		self.systray.destroy()
		# accept the event (close the application)		
		event.accept()
	
	
	def removeLogs(self):
		reply = QtGui.QMessageBox.question(self, 'Are you sure?', "You are about to remove %d log entry/entries, are you sure?" % (len(self.logs.ui.tblLog.selectedIndexes()) / 3), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply != QtGui.QMessageBox.Yes:
			return
		
		for idx in self.logs.ui.tblLog.selectedIndexes():
			iid = self.logs.ui.tblLog.item(idx.row(),0).text()
			self.query.prepare("DELETE FROM %s WHERE id = :id" % self.LOG_TABLE)
			self.query.bindValue(':id',iid)
			self.query.exec_()
		
		self.showLogWindow(True)

	
	def showLogWindow(self, logreload = False ):
		if logreload is False:
			# Log's dialog
			self.logs = QtGui.QDialog()
			self.logs.ui = Ui_frmLog()
			self.logs.ui.setupUi(self.logs)
			self.logs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
			QtCore.QObject.connect(self.logs.ui.btnRemoveLog, QtCore.SIGNAL("clicked()"), self.removeLogs)
		
		# get the log history
		self.query.exec_("SELECT * FROM %s ORDER BY date DESC" % self.LOG_TABLE)
		items = []
		while self.query.next():
			iid = str(self.query.value(0).toPyObject())
			date = str(self.query.value(1).toPyObject())
			msg = str(self.query.value(2).toPyObject())
			items.append([iid,date,msg])
			
		self.logs.ui.tblLog.setRowCount(len(items))
		self.logs.ui.tblLog.setColumnCount(3)
		
		row = 0
		for item in items:
			col = 0
			for part in item:
				newItem = QtGui.QTableWidgetItem(part)
				self.logs.ui.tblLog.setItem(row, col, newItem)
				col += 1
			row += 1
		
		self.logs.ui.tblLog.resizeColumnsToContents()
		
		if logreload is False:
			self.logs.exec_()
		
	def showSaveChart(self):
		width = 30  # bar width
		
		filename = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save followers chart..." , "", "*.png" )
		filename = str(filename[0])
		account = self.ui.cboAccount.currentText()
		
		#plt.figure
		self.query.prepare("SELECT follower,started,stopped FROM %s WHERE stopped IS NOT null AND accountid = (SELECT accountid FROM %s WHERE name = :account) ORDER BY started ASC" % (self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE))
		self.query.bindValue(":account",account)
		self.query.exec_()
		
		followers = []
		dates = []
		while self.query.next():
			fw = str(self.query.value(0).toPyObject())
			started = str(self.query.value(1).toPyObject())
			stopped = str(self.query.value(2).toPyObject())
			followers.append(fw)
			dates.append([started,stopped])

		if len(dates) == 0:
			QtGui.QMessageBox.critical(self, "Not enough data", "This account has no unfollowers yet")
			return
		
		# x axis item width
		xval = [ (width * i) + (i-1) * 10 for i in range(1,len(followers) + 1)]
		yval = [ (datetime.strptime(c[1],"%Y-%m-%d %H:%M:%S") - datetime.strptime(c[0],"%Y-%m-%d %H:%M:%S")).total_seconds() for c in dates ]
		
		ax = pyplot.subplot(111)
		ax.yaxis_date()		
		
		ax.bar(xval, yval, width=width, align="center")
		
		# add the followed period of time
		for i in followers:
			index = followers.index(i)
			diff = datetime.strptime(dates[index][1],"%Y-%m-%d %H:%M:%S") - datetime.strptime(dates[index][0],"%Y-%m-%d %H:%M:%S")
			followers[index] = i + "\n(%s)" % diff
			
		pyplot.xticks(xval,followers )
		pyplot.yticks(yval,[str(c[1]) for c in dates])
		
		#add in labels and title
		pyplot.title("TFK / %s Unfollowers" % account)
		pyplot.tight_layout()
		pyplot.grid(True)
		
		#save figure to file
		pyplot.savefig(filename,dpi=100,aspect='auto')
		

	def checkFollowers(self, account):
		"""
		Function to check the followers
		"""
		
		self.addAccount(account)
		self.displayStoredAccounts()

		while not self.threadfinish.isSet():
			# update the log
			self.addLog("Checking %s followers" % account)
			
			# retrieves the followers
			followers,err = self.followers.getFollowers(account)
			
			if err is not None:  # error?
				self.addLog("Failed: %s" % err , 'dialog-warning' , todb = True)
			else:

				# get the amount of followers
				self.query.prepare("SELECT COUNT(follower) FROM %s JOIN %s ON %s.accountid = %s.id WHERE %s.name = :account" % (self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE, self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE, self.ACCOUNTS_TABLE ) )
				self.query.bindValue(":account",account)
				self.query.exec_()
				self.query.next()
				storedfw = self.query.value(0).toInt()[0]
				unfw = 0
				
				if storedfw == 0:  # has no followers stored yet
					for fw in followers[1]:
						self.addFollower(account, fw)
				else:  # has followers

					# get the stored followers
					self.query.prepare("SELECT follower,stopped FROM %s JOIN %s ON %s.accountid = %s.id WHERE %s.name = :account AND stopped IS NULL" % (self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE, self.FOLLOWERS_TABLE, self.ACCOUNTS_TABLE, self.ACCOUNTS_TABLE ) )
					self.query.bindValue(":account",account)
					self.query.exec_()
				
					fwlist = [[],[]]
					while self.query.next():
						fw = str(self.query.value(0).toPyObject())
						st = str(self.query.value(1).toPyObject())
						fwlist[0].append(fw)
						fwlist[1].append(st)
						
					# unfollowers
					for fw in fwlist[0]:
						if not fw in followers[1]:
							self.rmFollower(account, fw)
							self.addLog("%s has unfollowed %s" % (fw, account), "dialog-warning" , timeout=pynotify.EXPIRES_NEVER , todb = True)
							unfw += 1

					# new followers
					for fw in followers[1]:
						if not fw in fwlist[0] or len(fwlist[1][fwlist[0].index(fw)]) > 0:
							self.addFollower(account, fw)
							self.addLog("%s has started following %s" % (fw,account)  , timeout=pynotify.EXPIRES_NEVER , todb = True)
							
			# updates the 'lastchecked' date
			self.updateAccountChecked(account)
			self.displayStoredFollowers(account)
			
			self.addLog("%s has %d follower(s) and %d unfollower(s)" % (account, followers[0], unfw))
			
			# wait for the check interval to finish (fix it, it is VERY DIRTY....)
			for i in range(0, self.timevals.getInterval()):
				time.sleep(1)
				if self.threadfinish.isSet():
					return


	# [   APPLICATION ITSELF   ]
	# --------------------------
	def event_watching ( self ):
		account = self.ui.cboAccount.currentText()
		if len(account) == 0:
			QtGui.QMessageBox.critical(self, "Empty account", "You need to specify an account")
			return

		# start/stop the thread to check the followers
		if self.threadfinish is None:
			self.threadfinish = threading.Event()

		if self.ui.btnStart.text() == "STOP!":
			self.threadfinish.set()  # set the flag to true
			self.threadck.join()
			self.addLog("You are not keeping followers!")
			self.ui.btnStart.setText("Start Keeping!")
		else:
			self.threadfinish.clear()  # set the flag to false
			self.threadck = threading.Thread(target=self.checkFollowers, args=(account,))
			self.threadck.start()  # the thread starts
			self.ui.btnStart.setText("STOP!")
	
		return


if __name__ == "__main__":

	pynotify.init("Twitter Followers Keeper")
	
	# create Qt application
	app = QtGui.QApplication(sys.argv)
	# create main window
	window = TFK()
	# connect signal for app finish
	QtCore.QObject.connect(app,QtCore.SIGNAL("lastWindowClosed()"),app,QtCore.SLOT("quit()"))
	# start the app up
	window.show()
	sys.exit(app.exec_())

