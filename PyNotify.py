#! /usr/bin/python
import subprocess
import time

class Setup:
	success_message = "Success!!! The job has been submitted successfully!"

	def __init__(self):
		self.askMessage()
		self.askTime()
		self.confirmExecution()

	def askMessage(self):
		self.message = raw_input("What would you like your message to be? ")

	def askTime(self):
		self.time = raw_input("When should this be displayed? ").lower()
		if ' ' in self.time:
			self.time_split = self.time.split(' ')
			self.time_value = int(self.time_split[0])
			self.time_unit = self.time_split[1]

	def confirmExecution(self):
		if ':' in self.time:
			self.confirm = raw_input('Just to verify, you would like to display the message, "' + self.message + '," at ' + self.time + ', right? (yes/no) ').lower()
		else:
			self.confirm = raw_input('Just to verify, you would like to display the message, "' + self.message + '," ' + self.time + ', right? (yes/no) ').lower()
			# self.confirm = subprocess.call('zenity --title="Confirm" --text="Just to verify, you would like to display the message, \"' + self.message + '\", at ' + self.time + ', right?" --question', shell=True);

		if self.confirm == "y" or self.confirm == "yes":
			self.execute()
		elif self.confirm == "":
			print "\nI'm sorry, I didn't quite get that..."
			self.confirmExecution()
		else:
			self.tryAgain()

	def execute(self):
		if 'second' in self.time:
			time.sleep(self.time_value) # this sort of works...
			self.shell_command = "echo 'notify-send \"%s\"' | at now" % self.message #...but not how you'd think...(no notification)
			#The actual bash command would look like: sleep %r; echo 'notify-send "%s"' | at now
		elif "from now" in self.time:
			try: #If the time isn't an integer, then an exception is thrown
				self.shell_command = "echo 'notify-send \"%s\"' | at now + %r %s" % (self.message, int(self.time_value), self.time_unit)
			except ValueError:
				print "\nI'm sorry, but it seems that a non-number was entered for the length of time. Please try again..."
				self.askTime()
				self.confirmExecution()
				self.execute()
			subprocess.call(self.shell_command, shell=True)
			print self.success_message
			exit()
		elif 'now' in self.time:
			self.shell_command = "echo 'notify-send \"%s\"' | at now" % (self.message)
			subprocess.call(self.shell_command, shell=True)
			print self.success_message
		elif ':' in self.time:
			self.shell_command = "echo 'notify-send \"%s\"' | at %r" % (self.message, self.time)
			subprocess.call(self.shell_command, shell=True)
			print self.success_message
			exit()
		else:
			print """I am not 100% certain regarding how to process your request...\nPlease enter it manually instead:\n\n\techo 'notify-send \"%s\"' | at [time]\n\t\tor\n\techo 'notify-send \"%s\"' | at now + [time]"""
			exit()


	def tryAgain(self):
		self.try_again = raw_input("\nOh, I see. Let's try that again, then, shall we? (yes/no) ").lower()
		if self.try_again == "y" or self.try_again == "yes":
			print "\n"
			Setup()
		elif self.try_again == "n" or self.try_again == "no":
			exit()
		else:
			self.tryAgain()

Setup()
