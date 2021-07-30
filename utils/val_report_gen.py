#!/usr/bin/python3

import time
import os
import sys
import subprocess
from prettytable import PrettyTable

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

sdo_dir=sys.argv[1];
if len(sys.argv) == 4:
	print ("\n\n\t/path/to/val_report_gen.py "+sys.argv[1]+" da="+sys.argv[2]+" aes_mode="+sys.argv[3])
else:
	print("Pass the arguments correctly........")
	print("Usage: /path/to/val_report_gen.py (absolute path of sdo) (da) (aes_mode)")
	exit(0)

os.system("cd "+sdo_dir+" && make pristine >> /tmp/csdk_unittest_log.txt 2>&1 && cmake -Dunit-test=true -DHTTPPROXY=true -DBUILD=release -DAES_MODE="+sys.argv[3]+" -DDA="+sys.argv[2]+" >> /tmp/csdk_unittest_log.txt 2>&1 && make -j4 >> /tmp/csdk_unittest_log.txt 2>&1")

list1=os.listdir(sdo_dir+"/build/")
list2=[]; list3=[]; list4=[]

for data in list1[:]:
    if (not data.startswith("test")) or (data.endswith("_runner.c")):
        list1.remove(data)

for i in range(0, len(list1)):
	if list1[i] in list1:
		valid=0
		log = subprocess.Popen(["valgrind","--leak-check=full","./build/"+list1[i]], cwd=sdo_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = log.communicate()
		for data in err.decode("utf-8").splitlines(err.decode("utf-8").count("\n")):
			if data.count("  total heap usage:"):
				list3.append(data.split("==   ")[1])
			if data.count("All heap blocks were freed") and data.count("no leaks are possible"):
				list2.append(data.split("== ")[1]); valid=1; list4.append(bcolors.OKGREEN+"PASS"+bcolors.ENDC);
		if valid==0:
			print(out.decode("utf-8"))
			print(err.decode("utf-8"))
			list2.append("Some heap blocks were not freed. Please check it..."); list4.append(bcolors.FAIL+"FAIL"+bcolors.ENDC);

table = PrettyTable(['Ser.No', 'TestCase', 'Heap Summary', 'Memory freed status', 'Results'])
for i in range(0, len(list1)):
	table.add_row([i+1, list1[i], list2[i], list3[i], list4[i]])
print(table)
