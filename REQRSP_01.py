import pyautogui
import os
import logging
import time
import subprocess
import threading
from PIL import Image
from PIL import ImageDraw


AUTOMATIC_RESPONSE = True
AUTOMATIC_RESPONSE_RATE_SECONDS = 10


REQUEST_FILE_NAME = "REQ.txt"
PRIME_REQUEST_FILE_NAME = "RQ.txt"
RESPONSE_FILE_SUB_DIR = "RSP\\"
RESPONSE_FILE_NAME = RESPONSE_FILE_SUB_DIR + "RSP.png"


EXCEPTION_RETRIES = 22
EXCEPTION_RETRY_DELAY = 0.5


# DON'T THROW EXCEPTION ON MOVETO(0,0)
pyautogui.FAILSAFE = False


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


HELP_TEXT = """
------------------------------------------------------------------------------
REQRSP v1 [POOR MAN'S PORTLESS/CLIENTLESS VNC SERVER FOR DROPBOX FOR WINDOWS]:
------------------------------------------------------------------------------

1.  PRIME REQUEST FILE AUTOMATICALLY GENERATED 	=  .\\""" + PRIME_REQUEST_FILE_NAME + """
2.  INSERT COMMANDS INTO PRIME REQUEST FILE  	=  .\\""" + PRIME_REQUEST_FILE_NAME + """
3.  TO SEND REQUEST COMMANDS, SAVE FILE AS 	=  .\\""" + REQUEST_FILE_NAME + """ 
4.  SERVER WILL PROCESS REQUEST FILE  		=  .\\""" + REQUEST_FILE_NAME + """
5.  SERVER WILL SEND RESPONSE SCREENSHOT  	=  .\\""" + RESPONSE_FILE_NAME + """
6.  WATCH RESPONSES PROPAGATE WITH IRFANVIEW WATCH HOTFOLDER FUNCTION
7.  CLICK MOUSE ON RESPONSE SCREENSHOT IN IRFANVIEW TO OBTAIN SCREEN COORDINATES 

---------------------
REQRSP COMMANDS LIST:
---------------------

?					=  display help text with notepad
/					=  close help text with key sequence = [Alt]+[F4], [N]
E {start} <cmdString>			=  execute windows command
M <x> <y>					=  move mouse to screen coordinates
L {<x> <y>}				=  leftclick here {or at screen coordinates}
D {<x> <y>}				=  left doubleclick here {or at screen coordinates}
R {<x> <y>}				=  rightclick here {or at screen coordinates}
G {<fromX> <toX>} <toX> <toY>		=  drag mouse {from coordinates} to coordinates
S [<distanceUp> | <-distanceDown>]	=  scroll [distance up | -distance down]
T <text>				=  typewrite text
N {<text>}				=  press enter {or typewrite text then insert newline}
K <key1> {<key2> <key...>}		=  press key {or press hotkey sequence}
A					=  select all: 	[Ctrl]+[A]
X					=  cut: 	[Ctrl]+[X]
C					=  copy: 	[Ctrl]+[C]
V					=  paste: 	[Ctrl]+[V]
Z					=  undo: 	[Ctrl]+[Z]
Y					=  redo: 	[Ctrl]+[Y]
AUTO [ON | OFF] {<seconds>}		=  set automatic response mode [on | off] {set rate}
DEBUG [ON | OFF]			=  set debug messages [off | on]
"""


class ReqRsp:

	requestFileName = REQUEST_FILE_NAME
	primeRequestFileName = PRIME_REQUEST_FILE_NAME
	responseFileSubDir = RESPONSE_FILE_SUB_DIR
	responseFileName = RESPONSE_FILE_NAME

	automaticResponse = AUTOMATIC_RESPONSE
	automaticResponseRate = AUTOMATIC_RESPONSE_RATE_SECONDS
	
	helpText = HELP_TEXT

	exceptionRetries = EXCEPTION_RETRIES
	exceptionRetryDelay = EXCEPTION_RETRY_DELAY


	def __init__(self):
		self.allRequests = []

		self.exceptionRetryFail = False

		if not os.path.exists(os.getcwd() + "\\" + ReqRsp.responseFileSubDir): 
			os.makedirs(os.getcwd() + "\\" + ReqRsp.responseFileSubDir)

		self.do_screenshotResponse()
		self.create_primeRequestFile()

		if ReqRsp.automaticResponse:
			self.threadAutoResponse = threading.Thread(target=self.automatic_screenshotResponse)
			self.threadAutoResponse.start()

		self.currentWD = os.getcwd()
		self.requestFilePath = os.path.join(self.currentWD, ReqRsp.requestFileName)
		logger.info("REQUEST FILE PATH = " + self.requestFilePath)


	def create_primeRequestFile(self):

		tryAgain = ReqRsp.exceptionRetries
		while tryAgain > 0:
			try:
				logger.debug("CREATING PRIMEREQUESTFILE")
				primeRequestFile = open(ReqRsp.primeRequestFileName, 'w')
				primeRequestFile.close()
				tryAgain = 0
			except:
				logger.debug("TRYING CREATE_PRIMEREQUESTFILE AGAIN")
				tryAgain -= 1
				time.sleep(ReqRsp.exceptionRetryDelay)
				if tryAgain == 0:
					req.exceptionRetryFail = True
					logger.error("EXCEPTION IN CREATE_PRIMEREQUESTFILE")


	def read_requestFile(self):

		tryAgain = ReqRsp.exceptionRetries
		while tryAgain > 0:
			try:
				requestFile = open(ReqRsp.requestFileName, 'r')
				self.allRequests = requestFile.readlines()
				requestFile.close()
				tryAgain = 0
			except:
				logger.debug("TRYING READ_REQUESTFILE #1 AGAIN")
				tryAgain -= 1
				time.sleep(ReqRsp.exceptionRetryDelay)
				if tryAgain == 0:
					req.exceptionRetryFail = True
					logger.error("EXCEPTION #1 IN READ_REQUESTFILE")


		logger.debug("READ REQUESTFILE LINES = " + str(len(self.allRequests)))
		logger.debug(self.allRequests)


		self.create_primeRequestFile()
		time.sleep(1)


		tryAgain = ReqRsp.exceptionRetries
		while tryAgain > 0 and not req.exceptionRetryFail:
			try:
				logger.debug("DELETING REQUESTFILE")
				os.remove(ReqRsp.requestFileName)
				tryAgain = 0
			except:
				logger.debug("TRYING READ_REQUESTFILE #2 AGAIN")
				tryAgain -= 1
				time.sleep(ReqRsp.exceptionRetryDelay)
				if tryAgain == 0:
					req.exceptionRetryFail = True
					logger.error("EXCEPTION #2 IN READ_REQUESTFILE")			
		

	def automatic_screenshotResponse(self):
		logger.info("AUTOMATIC RESPONSE RATE = " + str(ReqRsp.automaticResponseRate) + " SECONDS")
		logger.info("TO TERMINATE PROGRAM PRESS = [Ctrl]+[Break]") 
		while True:
			if ReqRsp.automaticResponse:
				self.do_screenshotResponse()
			time.sleep(ReqRsp.automaticResponseRate)


	def do_screenshotResponse(self):
		logger.debug("RESPONSE")
		screenshot = pyautogui.screenshot()

		xSize, ySize = pyautogui.size()
		xPos, yPos = pyautogui.position()
		
		screenshotWithCursor = ImageDraw.Draw(screenshot)

#		ImageDraw.line([(x1, y1), (x2, y2)], width=pixels, fill='color')
# 		ImageDraw.rectangle((left, top, right, bottom), outline='color', fill='color')
#		ImageDraw.point((x, y), fill='color')

#		DRAW XHAIRS
		screenshotWithCursor.line([(xPos - 11, yPos), (xPos + 11, yPos)], width=3, fill='red')
		screenshotWithCursor.line([(xPos, yPos - 11), (xPos, yPos + 11)], width=3, fill='red')
		screenshotWithCursor.line([(xPos - 4, yPos), (xPos + 4, yPos)], width=3, fill='#00ffff')
		screenshotWithCursor.line([(xPos, yPos - 4), (xPos, yPos + 4)], width=3, fill='#00ffff')

#		DRAW CONCENTRICS
		screenshotWithCursor.rectangle((xPos - 50, yPos - 50, xPos + 50, yPos + 50), outline='#00ffff')
		screenshotWithCursor.rectangle((xPos - 100, yPos - 100, xPos + 100, yPos + 100), outline='red')

#		DRAW CENTER
		screenshotWithCursor.rectangle((xPos - 1, yPos - 1, xPos + 1, yPos + 1), outline='red', fill='red')

		screenshot.save(ReqRsp.responseFileName)

	
	def set_automaticResponse(self, request):
		if request[1].upper() == "OFF":
			if len(request) == 2:
				logger.info("AUTOMATIC RESPONSE MODE OFF")
				ReqRsp.automaticResponse = False
			elif len(request) == 3:
				if request[2].isdecimal():
					logger.info("AUTOMATIC RESPONSE RATE = " + str(request[2]))
					ReqRsp.automaticResponseRate = int(request[2])
					logger.info("AUTOMATIC RESPONSE MODE OFF")
					ReqRsp.automaticResponse = False
		elif request[1].upper() == "ON":
			if len(request) == 2:
				logger.info("AUTOMATIC RESPONSE MODE ON")
				ReqRsp.automaticResponse = True
			elif len(request) == 3:
				if request[2].isdecimal():
					logger.info("AUTOMATIC RESPONSE RATE = " + str(request[2]))
					ReqRsp.automaticResponseRate = int(request[2])
					logger.info("AUTOMATIC RESPONSE MODE ON")
					ReqRsp.automaticResponse = True


	def set_debugMessages(self, request):
		if len(request) == 2:
			if request[1].upper() == "OFF":
				logger.info("DEBUG MESSAGES OFF")
				logger.setLevel(logging.INFO)
			elif request[1].upper() == "ON":
				logger.info("DEBUG MESSAGES ON")
				logger.setLevel(logging.DEBUG)


	def do_openHelp(self, request):
		if len(request) == 1:
			logger.info(["DO_OPENHELP"])
			subprocess.Popen(['start', 'notepad'], shell=True)
#			logger.debug("WAITING 3 SECONDS")
			time.sleep(1)
			pyautogui.typewrite(ReqRsp.helpText)
			pyautogui.keyDown('alt')
			pyautogui.press('space')
			pyautogui.keyUp('alt')
			pyautogui.press('x')
			time.sleep(1)
		
	
	def do_closeHelp(self, request):
		if len(request) == 1:
			logger.info(["DO_CLOSEHELP"])
			pyautogui.keyDown('alt')
			pyautogui.press('f4')
			pyautogui.keyUp('alt')
			pyautogui.press('n')
			
		
	def do_executeCmd(self, request):
		if len(request) > 1:
			logger.info(["DO_EXECUTE"] + request[1:])
			subprocess.Popen(request[1:], shell=True)
			logger.debug("WAITING 5 SECONDS")
			time.sleep(5)
			
		
	def do_leftClick(self, request):
		if len(request) == 1:
			here = list(pyautogui.position())
			logger.info(["DO_LEFTCLICK ="] + here)
			pyautogui.click(here)
		elif len(request) == 3 and request[1].isdecimal() and request[2].isdecimal():
			logger.info(["DO_LEFTCLICK ="] + request[1:])
			pyautogui.click(int(request[1]), int(request[2]))

	def do_doubleClick(self, request):
		if len(request) == 1:
			here = list(pyautogui.position())
			logger.info(["DO_DOUBLECLICK ="] + here)
			pyautogui.doubleClick(here)
		elif len(request) == 3 and request[1].isdecimal() and request[2].isdecimal():
			logger.info(["DO_DOUBLECLICK ="] + request[1:])
			pyautogui.doubleClick(int(request[1]), int(request[2]))
	
	def do_rightClick(self, request):
		if len(request) == 1:
			here = list(pyautogui.position())
			logger.info(["DO_RIGHTCLICK ="] + here)
			pyautogui.rightClick(here)
		elif len(request) == 3 and request[1].isdecimal() and request[2].isdecimal():
			logger.info(["DO_RIGHTCLICK ="] + request[1:])
			pyautogui.rightClick(int(request[1]), int(request[2]))

	def do_moveTo(self, request):
		if len(request) == 3 and request[1].isdecimal() and request[2].isdecimal():
			logger.info(["DO_MOVETO ="] + request[1:])
			pyautogui.moveTo(int(request[1]), int(request[2]), duration=0.1)

	def do_dragTo(self, request):
		if len(request) == 3 and request[1].isdecimal() and request[2].isdecimal():
			here = list(pyautogui.position())
			logger.info(["DO_DRAGTO ="] + here + request[1:])
			pyautogui.dragTo(int(request[1]), int(request[2]), duration=0.1)
		elif len(request) == 5 and request[1].isdecimal() and request[2].isdecimal() \
							and request[3].isdecimal() and request[4].isdecimal():
			logger.info(["DO_DRAGTO ="] + request[1:])
			pyautogui.moveTo(int(request[1]), int(request[2]), duration=0.1)
			pyautogui.dragTo(int(request[3]), int(request[4]), duration=0.1)

	def do_scrollUp(self, request):
		if len(request) == 2 and (request[1].isdecimal() or \
							(request[1][0] == '-' and request[1][1:].isdecimal())):
			logger.info(["DO_SCROLLUP ="] + request[1:])
			pyautogui.scroll(int(request[1]))


	def do_typewrite(self, line):
		if len(line) > 2:
			logger.info("['DO_TYPEWRITE =', '" + line[2:-1] + "']")
			pyautogui.typewrite(line[2:-1])

	def do_typewriteNewline(self, line):
		if len(line.split()) == 1:
			logger.info("['DO_TYPEWRITENEWLINE']")
			pyautogui.press('enter')
		elif len(line) > 1:
			logger.info("['DO_TYPEWRITENEWLINE =', '" + line[2:-1] + "']")
			pyautogui.typewrite(line[2:])

	def do_hotkeyPress(self, request):
		if len(request) == 2:
			logger.info(["DO_HOTKEY ="] + request[1:])
			pyautogui.press(request[1])
		elif len(request) > 2:
			logger.info(["DO_HOTKEY ="] + request[1:])
			for index in range(1,len(request)):
				pyautogui.keyDown(request[index])
			for index in range(1,len(request)):
				pyautogui.keyUp(request[index])


	def do_cut(self, request):
		if len(request) == 1:
			logger.info(["DO_CUT"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('x')
			pyautogui.keyUp('ctrl')

	def do_copy(self, request):
		if len(request) == 1:
			logger.info(["DO_COPY"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('c')
			pyautogui.keyUp('ctrl')

	def do_paste(self, request):
		if len(request) == 1:
			logger.info(["DO_PASTE"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('v')
			pyautogui.keyUp('ctrl')

	def do_selectAll(self, request):
		if len(request) == 1:
			logger.info(["DO_SELECTALL"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('a')
			pyautogui.keyUp('ctrl')

	def do_undo(self, request):
		if len(request) == 1:
			logger.info(["DO_UNDO"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('z')
			pyautogui.keyUp('ctrl')

	def do_redo(self, request):
		if len(request) == 1:
			logger.info(["DO_REDO"])
			pyautogui.keyDown('ctrl')
			pyautogui.press('y')
			pyautogui.keyUp('ctrl')


	def parse_allRequests(self):
		for index in range(len(self.allRequests)):
			line = self.allRequests[index]
			if index == (len(self.allRequests) - 1):
				line += '\n'
			logger.debug("PARSING LINE = " + str(index) + " OF LENGTH " + str(len(line)))
			request = line.split()
			logger.debug(request)
			if len(request) > 0:
				if request[0].upper() == 'E': self.do_executeCmd(request)
				if request[0].upper() == 'L': self.do_leftClick(request)
				if request[0].upper() == 'D': self.do_doubleClick(request)
				if request[0].upper() == 'R': self.do_rightClick(request)
				if request[0].upper() == 'M': self.do_moveTo(request)
				if request[0].upper() == 'G': self.do_dragTo(request)				
				if request[0].upper() == 'T': self.do_typewrite(line)
				if request[0].upper() == 'N': self.do_typewriteNewline(line)
				if request[0].upper() == 'K': self.do_hotkeyPress(request)
				if request[0].upper() == 'S': self.do_scrollUp(request)
				if request[0].upper() == 'X': self.do_cut(request)
				if request[0].upper() == 'C': self.do_copy(request)
				if request[0].upper() == 'V': self.do_paste(request)
				if request[0].upper() == 'A': self.do_selectAll(request)
				if request[0].upper() == 'Z': self.do_undo(request)
				if request[0].upper() == 'Y': self.do_redo(request)
				if request[0].upper() == '?': self.do_openHelp(request)
				if request[0].upper() == '/': self.do_closeHelp(request)
				if request[0].upper() == 'AUTO': self.set_automaticResponse(request)
				if request[0].upper() == 'DEBUG': self.set_debugMessages(request)
			time.sleep(1)
		logger.debug("FINISHED PARSING ALL REQUESTS")


if __name__ == "__main__":

	req = ReqRsp()

	while True:

		req.exceptionRetryFail = False
		
#		if True == True:
		try:
				
			if os.path.exists(req.requestFilePath):
			
				logger.debug("REQUESTFILE EXISTS AT: " + req.requestFilePath)

				req.read_requestFile()
				req.parse_allRequests()

				req.do_screenshotResponse()		
				time.sleep(1)

		except:
			logger.error("EXCEPTION IN MAIN")
			
