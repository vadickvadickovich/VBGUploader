import re
import sys
import os

class pictureInfo:
	def __init__(self, fileName, tags):
		self.fileName = fileName
		self.tags = tags

class VBSParser:
	"""Class to parse file with fileNames and tags.

    Init Parameters:
        fileName (Type STR):
            Path and fileName to file.
    """
	def __init__(self, fileName):
		self.fileName = fileName
		self.picturesInfo = []

		if not self.checkFile(self.fileName):
			print "File Not Exists"
			sys.exit()

		self.loadContent()
		self.parseContent()

	def checkFile(self, fileName):
		"""Check if file exists.

	    Parameters:
	        fileName (Type STR):
	            Path and fileName to file.
	    """
		if os.path.isfile(fileName):
			return True
		else:
			return False

	def loadContent(self):
		"""Load content from file and return it."""
		tagsFile = open(self.fileName, "r")
		self.content = tagsFile.readlines()
		tagsFile.close()

	def parseContent(self):
		"""Parse loaded content and save it to picturesInfo as structure: (fileName, tags)"""
		for line in self.content:
			fileName, tags = line.split(" - ")
			self.picturesInfo.append(pictureInfo(fileName, tags))

	def debugPrint(self):
		writeFile = open("output.out", "w")
		for picture in self.picturesInfo:
			outputString = "File: " + picture.fileName + " Tags: " + picture.tags
			print outputString
			writeFile.write(outputString + "\n")
		writeFile.close()


class VBSUploader:
	"""VBSUploader main class.

	Init Parameters:
        siteName (Type STR):
            The site name.

        siteUrl (Type STR):
            URL of VladBidloSite.

        hashString (Type STR):
            String that is hashed (required to login).

        username (Type STR):
            Your username of the site.

        password (Type STR):
            Your user password in plain text.
	"""

	def __init__(self, siteName, siteURL, username, password, hashString):
		self.siteName = siteName
		self.siteURL = siteURL
		self.username = username
		self.password = password
		self.hashString = hashString

		if not self.checkURL(self.siteURL):
			print "Invalid URL"
			sys.exit()

	def checkURL(self, url):
		"""URL validator for siteUrl parameter of VBSUploader.

        Parameters:
            url (Type STR):
                The URL to validate.
        """
		regex = re.compile(
			r'^(?:http|https)://'
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?| \
			[A-Z0-9-]{2,}(?<!-)\.?)|'
			r'localhost|' 
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' 
			r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
			r'(?::\d+)?'
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)

		if re.search(regex, url):
			return True
		else:
			return False

	def postCreate(self):
		pass

	def upload(self):
		pass

	def uploadFromFolder(self):
		pass

def main():
	parser = VBSParser('files.bbs')
	parser.debugPrint()

if __name__ == '__main__':
	main()