# Introduction
This is a simple tool for web scan, required by redrock team.
So it is just a homework.
# Function
- Subdomain scan
- Port scan
- Alive detect
- Waf detect (through wafw00f and linux only)
- Sql inject detect (through sqlmap)
# Usage
use `scanner.py -h` to see help
```
usage: scanner.py [-h] [-b] [-p] [-i] [-a] [-d DOMAIN] [-m MODE]
                  [-n THREAD_NUM] [-c DIC] [-w URL] [-s SQL_URL]

optional arguments:
  -h, --help     show this help message and exit
  -b             Booming subdomains
  -p             Port scan mode
  -i             Detect information disclosure
  -a             Alive detection
  -d DOMAIN      Select the domain or ip
  -m MODE        Select the port_scan mode (0, 50, 100, 1000)
  -n THREAD_NUM  Select the thread num
  -c DIC         Select the dictionary
  -w URL         Test for waf (linux only)
  -s SQL_URL     Test for sql inject (you need sqlmap)
```
# Example
Subdomain scan
`scanner.py -bd cqupt.edu.cn -c small.txt`
Port scan
`scanner.py -pd 202.202.32.60`
Alive detect
`scanner.py -ad 202.202.32.60`
Waf detect (through wafw00f and linux only)
`scanner.py -w www.cqupt.edu.cn`
Sql inject detect (through sqlmap)
`scanner.py -s http://43.247.91.228:84/Less-1/?id=1`