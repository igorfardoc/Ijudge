import sys
import os
from time import sleep


solution_id = int(sys.argv[1])
now = int(sys.argv[2])
time_limit = int(sys.argv[3])
file_out = sys.argv[4]
cur = os.getcwd() + '\\testing' + str(solution_id) + '-' + str(now)
cmd = 'cd ' + cur + ' & '
cmd += 'start /b ' + cur + '\\' + str(solution_id) + '-' + str(now) + '.exe & '
cmd += 'ping 127.0.0.1 -n ' + str(time_limit) + ' & '
cmd += 'taskkill /im ' + str(solution_id) + '-' + str(now) + '.exe /f'
os.system(cmd)
sleep(1)
f = open(cur + '\\config_res.txt', 'w')
try:
    f2 = open(cur + '\\' + file_out)
    text = f2.read().strip()
    f2.close()
    f1 = open(cur + '\\ans.txt')
    text1 = f1.read().strip()
    f1.close()
    if text != text1:
        f.write('Wrong answer')
    else:
        f.write('OK')
except:
    f.write('Format error')
f.close()
sleep(1)