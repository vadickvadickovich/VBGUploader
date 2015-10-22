fileName = "files.bbs"

filesbbs = open("files.bbs", "r")
fileContent = filesbbs.readlines()
filesbbs.close()

for line in fileContent:
	picFileName, tags = line.split(" - ")
	print "File: " + picFileName + " Tags: " + tags