import sys
import os
import ast
from datetime import datetime

#idk how to do checklists and such, if it encounters one it might crash - needs testing
#if you really need this please open a github issue of pull request
#Another notes app is referred to as notes for brevity

def main():
	'''
	export your google keep notes with takeout
	unzip the downloaded archive
	cd to the Keep folder
	download this python script to the folder you are in
	from this folder run
	python3 GKeepToNotes.py *.json
	import ./res/notes_converted.json in notes and hope it works
	'''
	files = sys.argv[1:]
	respath='./res/'
	if not os.path.exists(respath):
		os.makedirs(respath)
	id=1
	#notes has all notes in one json file. GKeep has one json file per note.
	filename_all= ''.join((respath,'notes_converted.json'))
	file_all= open(filename_all,'a')
	readout=open(filename_all,'r')
	#notes header
	file_all.write('{"version":4,"notes":{')
	for filename in files:
		print("Converting " + filename)
		filein=open(filename,'r')
		line = filein.readlines()
		line = line[0].replace("\":false,", "\":False,").replace("\":true,", "\":True,").replace("\\/", "/") #change list to python format

		if line[len(line)-1:] == "\\":
			line=line[:-1]
		parsed_data = ast.literal_eval(line)

		if parsed_data['isTrashed']:
			notestatus=2
		elif parsed_data['isArchived']:
			notestatus=1
		else:
			notestatus=0

		if parsed_data['isPinned']:
			notepinned=2
		else:
			notepinned=1

		note_line = ''.join(["\"",str(id),"\":{\"type\":0,\"title\":\"", parsed_data['title'].replace("\n", "\\n").replace("\"", "\\\""), "\",\"content\":\"", parsed_data['textContent'].replace("\n", "\\n").replace("\"", "\\\""), "\",\"metadata\":\"{\\\"type\\\":\\\"blank\\\"}\", \"added\":\"", datetime.utcfromtimestamp(parsed_data['createdTimestampUsec']/1000000).strftime('%Y-%m-%dT%H:%M:%S.000Z'), "\",\"modified\":\"", datetime.utcfromtimestamp(parsed_data['userEditedTimestampUsec']/1000000).strftime('%Y-%m-%dT%H:%M:%S.000Z'),"\",\"status\":", str(notestatus), ",\"pinned\":", str(notepinned), "}"]) #to anyone modifying this: good luck!
#structure is "id": {"type": 0,"title": "Title","content": "insert note here","metadata": "{\"type\":\"blank\"}","added": "2024-08-23T07:29:59.161Z","modified": "2024-08-23T07:30:17.821Z","status": 0,"pinned": 1}
#					checklist or not																				dateTtime.000Z														1-archived 2-trash   2-pinned
		if id==1:
			pass
			file_all.writelines(note_line)
		else:
			pass
			file_all.writelines(',')
			file_all.writelines(note_line)
		readout.readlines()
		filein.close()
		id=id+1
	file_all.write('}}')
	file_all.close()
if __name__ == '__main__':
	main()
