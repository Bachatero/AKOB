# no explicit close() is needed when "with as" is used
with open("text.txt", "w") as textfile:
	textfile.write("Success!")
