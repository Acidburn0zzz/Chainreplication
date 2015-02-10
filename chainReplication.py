import da
import sys
sys.path.insert(0, './src/client')
sys.path.insert(0, './src/master')
sys.path.insert(0, './src/server')
import da
import master
import server
import client

def main():
    fileName = sys.argv[1]
    mrm = master.main(fileName)
    server.main(mrm, fileName)
    client.main(mrm, fileName)
