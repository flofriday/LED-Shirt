deploy: *.py
	rshell "cp *.py /pyboard/"

run:
	rshell "cp *.py /pyboard/"
	rshell "repl pyboard 'import main'"

list:
	rshell "ls /pyboard/"

remove:
	rshell "rm /pyboard/*"