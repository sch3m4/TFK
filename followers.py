import urllib2
import random
import time


class Followers():
	"""
	Class to get the followers for a given account
	"""

	TIMEOUT = 30
	MIN_DELAY = 1
	MAX_DELAY = 4
	RETRIES = 5

	def __init__(self):
		pass


	def setTimes(self,timeout=TIMEOUT,mindelay=MIN_DELAY,maxdelay=MAX_DELAY,retries=RETRIES):
		"""
		Set the default times values
		"""
		self.TIMEOUT = timeout
		self.MIN_DELAY = mindelay
		self.MAX_DELAY = maxdelay
		self.RETRIES = retries

	
	def waitDelay(self):
		# wait a random period of time
		delay = random.uniform(self.MIN_DELAY,self.MAX_DELAY)
		time.sleep(delay)


	def getFollowers(self,account=None):

		followers = [0,[]]
		lasterr = None

		if account is None:
			return (followers,'Invalid account')

		random.seed()

		# do the response
		cursor = None
		cont = 0
		while cont < self.RETRIES:
			try:
				"""
				Followers are given in modulus 100, so if the account has 300 followers, you will have to do
				3 requests in which the server will reply with 100 followers on each request
				"""
				if cursor is None: # the first one
					url = 'http://twitter.com/%s/followers/users' % account
				else: # the following ones
					url = 'http://twitter.com/%s/followers/users?cursor=%s' % (account, cursor)					

				req = urllib2.Request(url)
				req.add_header("Referer", "http://twitter.com/%s/followers/" % account)
				response = urllib2.urlopen(req,timeout=self.TIMEOUT)
				code = response.code
				body = response.read()
				response.close()
			except Exception,e:
				lasterr = e
				cont += 1
				self.waitDelay()
				continue

			# bad return code
			if code != 200:
				lasterr = 'Got HTTP response code: %d' % code
				break

			# get followers account name
			for fw in body.split('data-screen-name=\\\"')[1:]:
				name = fw[0:fw.index('\\')]
				if name in followers[1]:
					continue
				followers[1].append(name)

			# has more followers?
			if '"has_more_items":false' in body:
				break

			if not '"has_more_items":true' in body:
				continue

			# get the cursor value to get the next 100 followers
			more = '"has_more_items":true,"cursor":"'
			try:
				cursor = body[body.index(more) + len(more):]
			except Exception,e:
				cont += 1
				continue
			cursor = cursor[0:cursor.index('"')]

		if cont >= self.RETRIES:
			lasterr = 'Max. retries value has been reached!'

		# set the amount of followers
		followers[0] = len(followers[1])
		return (followers,lasterr)	
