import io
import os
import re
import subprocess
from settings import *

currentDir = os.path.dirname(os.path.abspath(__file__))

def writeConfigFile(filename):

    writePath = currentDir+"/"+filename.strip(DBFileExtension)

    if not os.path.exists(writePath):
        os.makedirs(writePath)

    writePath = writePath + "/" + generatedConfigFileName

    print "creating path", writePath
    mode = 'w'

    f = open(writePath, mode)
    f.write("")

    # Read the lines from the template, substitute the values, and write to the new config file
    for line in io.open(configTemplate, 'r'):

        line = line.replace('database_name_here', filename.strip(DBFileExtension))
        line = line.replace('username_here', username)
        line = line.replace('password_here', password)
        line = line.replace('whereDBLives_here', whereDBLives)

        f.write(line)

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def createDB(filename):
    
    mySQLLogin = mySQLPath + " --host="+ whereDBLives +" -u" + username +" -p"+ password + " "

    createTheDatabase = (mySQLLogin+"-e '" + "CREATE DATABASE " + filename.strip(DBFileExtension)+"'")
    fillDataBase = (mySQLLogin + " " +filename.strip(DBFileExtension)+"< "+filename)

    subprocess_cmd(createTheDatabase)
    subprocess_cmd(fillDataBase)

for filename in os.listdir(currentDir):
    if filename.endswith(DBFileExtension):
        os.rename(filename, re.sub('[\(\)\{\}\-<>]', '', filename))

for filename in os.listdir(currentDir):
    if filename.endswith(DBFileExtension):
        print "detected ",filename
        createDB(filename)
        writeConfigFile(filename)