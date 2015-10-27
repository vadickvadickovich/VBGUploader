import re
import sys
import os
import subprocess
import getpass

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

	def getPictureList(self):
		"""Return list of pictutes and tags."""
		return self.picturesInfo

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

class VBSUploader:
	"""VBSUploader main class.

	Init Parameters:
        siteName (Type STR):
            The site name.

        siteUrl (Type STR):
            URL of VladBidloSite.

        username (Type STR):
            Your username of the site.

        password (Type STR):
            Your user password in plain text.

        scriptDir (Type STR):
        	Script folder for temp files like cookies
	"""
	def __init__(self, siteName, siteURL, username="", password="", scriptDir=".VBSUploader"):
		self.siteName = siteName
		self.siteURL = siteURL

		if username == "":
			username = raw_input("Username for " + self.siteName + ": ")

		if password == "":
			password = getpass.getpass("Password for " + self.siteName + ": ")

		if not self.checkURL(self.siteURL):
			print "Invalid URL"
			sys.exit()

		self.createScriptDir(scriptDir)
		self.login(username, password)

	def createScriptDir(self, scriptDir):
		"""Script folder creator. This folder contains files like cookies and logs

        Parameters:
            scriptDir (Type STR):
                Name of Script Folder
        """
		if not os.path.exists(scriptDir):
			os.makedirs(scriptDir)

		self.scriptDir = scriptDir

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

	def login(self, username, password):
		"""Login method to get cookies

        Parameters:
            username (Type STR):
                yep, it's username

            password (Type STR):
                and it's passowrd, how genius
        """
		self.cookies = self.scriptDir + "/" + self.siteName + ".cookies"
		subprocess.call(["curl", "-s", "-b", self.cookies, "-c", self.cookies, "-d", "user[name]=" + username + "&user[password]=" + password, self.siteURL + "/user/authenticate.xml"])

	def postCreate(self, fileName, tags):
		"""Post Creator and file uploader

        Parameters:
            fileName (Type STR):
                Picture filename

            tags (Type STR):
                Tags for post
        """
		subprocess.call(["curl", "-s", "-b", self.cookies, "-c", self.cookies, "-F", "post[tags]=" + tags, "-F", "post[file]=@" + fileName, self.siteURL + "/post/create.xml"])

	def massUpload(self, folderPath, infoFileName):
		"""Mass upload from folder with file contains list of pictures and tags

        Parameters:
            folderPath (Type STR):
                Path to folder with pictures and info file

            infoFileName (Type STR):
            	Name of file contains list of pictures and tags
        """
		if not os.path.exists(folderPath):
			print folderPath + " not exists"
			sys.exit()

		parser = VBSParser(folderPath + "/" + infoFileName)
		picturesList = parser.getPictureList()

		for picture in picturesList:
			fileName = folderPath + "/" + picture.fileName
			tags = picture.tags
			self.postCreate(fileName, tags)

def main():
	vbsuploader = VBSUploader("VladBidloGallery", "http://bidlogallery.vadickproduction.com")
	#vbsuploader.postCreate("test.jpg", "all_male archer emiya_shirou fate/stay_night male scrap_iron sword weapon")
	vbsuploader.massUpload("archer", "files.bbs")

	print

if __name__ == '__main__':
	main()
