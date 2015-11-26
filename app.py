import sys
import requests
import os

def getArg(arg):
    args = sys.argv
    for a in args:
        # Check if it even contains it
        if a.startswith(arg):
            # Check if the argument is the word provided
            # Matches "app.py foo = bar" and "app.py foo bar" for arg = foo
            if a == arg:
                # Check if the argument is followed by an =
                # Matches "app.py foo = bar"
                if (args.index(a)) + 1 < len(args) and args[args.index(a) + 1] == "=":
                        if (args.index(a) + 2) <= len(args):
                            return args[args.index(a) + 2]
                # Matches "app.py foo bar" (assumes no "=" means a boolean flag)
                else:
                    return True
            # Check if argument includes "="
            # Matches "app.py foo=bar"
            elif a.startswith(arg + "="):
                l = len(arg + "=")
                return a[l:]
    return False

def printIfVerbose(msg):
    if getArg("verbose") or getArg("v"):
        print(msg)

def getRemoteHosts():
    return ["https://adaway.org/hosts.txt",
			"http://winhelp2002.mvps.org/hosts.txt",
			"http://hosts-file.net/.%5Cad_servers.txt",
			"http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",
			"https://cdn.mnbryant.com/hosts.txt",
            "https://cdn.mnbryant.com/hosts_pron_strict.txt"]

def getHostsFileLocation():
    if sys.platform.startswith("linux"):
        return "/etc/hosts"
    elif sys.platform == "windows":
        # Needs check with environment variable to get correct location
        return os.path.join(os.getenv("SystemRoot"), "System32", "drivers", "etc", "hosts")

def getHostsFromFiles():
    urlList = getRemoteHosts()
    hostsList = ["127.0.0.1 localhost localhost.localdomain"]
    for url in urlList:
        printIfVerbose("Downloading from " + url)
        r = requests.get(url)
        hListStr = r.text
        hList = hListStr.splitlines()
        hostsList = hostsList + hList
    printIfVerbose("Downloads complete")
    return hostsList

def getOutputFileName():
    # Will have logic to use custom name from cl args
    out = getArg("out")
    if out == False:
        printIfVerbose("Using default hosts file location")
        return getHostsFileLocation()
    else:
        return out

def writeHostsFile():
    hostsList = getHostsFromFiles()
    outFile = getOutputFileName()
    bakFile = outFile + ".bak"
    if os.path.isfile(outFile):
        printIfVerbose("File exists and will be backed up before continuing")
        if os.path.isfile(bakFile):
            printIfVerbose("Backup exists and will be overwritten")
            os.remove(bakFile)
        printIfVerbose("Backing up")
        os.rename(outFile, bakFile)
    hosts = open(outFile, "a")
    printIfVerbose("Writing to file")
    for entry in hostsList:
        entry += "\n"
        hosts.write(entry)
    hosts.close()
    printIfVerbose("Finished writing to file")

def run():
    writeHostsFile()

run()
