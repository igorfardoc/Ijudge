from time import sleep
import sys
import os


solution_id = int(sys.argv[1])
problem_id = int(sys.argv[2])
file_in = sys.argv[3]
file_out = sys.argv[4]
time_limit = int(sys.argv[5])
tests = open(os.getcwd() + '\\problems\\' + str(problem_id) + '\\tests_file.txt').read()
mass = tests.split('\n\n')
path_ans = os.getcwd() + '\\problems\\' + str(problem_id) + '\\answers_file.txt'
answers = open(path_ans).read()
mass1 = answers.split('\n\n')
now = 0
path1 = os.getcwd() + '\\solutions\\solution' + str(solution_id) + '.cpp'
os.system('g++ ' + path1 + ' -o ' + os.getcwd() + '\\' + str(solution_id) + '.exe')
ok = True
result = 'Error'
try:
    f = open(os.getcwd() + '\\' + str(solution_id) + '.exe')
    f.close()
except Exception:
    ok = False
if ok:
    for i in mass:
        path = os.getcwd() + '\\testing' + str(solution_id) + '-' + str(now)
        os.makedirs(path)
        open(path + '\\' + file_in, 'w').write(i)
        os.system('copy ' + os.getcwd() + '\\test.py ' + path + '\\test.py')
        new_name = str(solution_id) + '-' + str(now) + '.exe'
        os.system('copy ' + os.getcwd() + '\\' + str(solution_id) + '.exe ' + path + '\\' + new_name)
        open(path + '\\ans.txt', 'w').write(mass1[now])
        cmd = 'start /b python ' + path + '\\test.py ' + str(solution_id) + ' ' + str(now) + ' '
        cmd += str(time_limit) + ' ' + file_out
        os.system(cmd)
        now += 1
    sleep(time_limit + 5)
    os.system('del ' + os.getcwd() + '\\' + str(solution_id) + '.exe')
    now = 0
    ok = True
    result = 'OK'
    for i in mass:
        path = os.getcwd() + '\\testing' + str(solution_id) + '-' + str(now)
        if ok:
            f = open(path + '\\config_res.txt')
            res = f.read()
            f.close()
            if res != 'OK':
                result = res + ', test ' + str(now + 1)
                ok = False
        os.system('rd /s /q ' + path)
        now += 1
else:
    result = 'Compilation error'
open('test' + str(solution_id) + '.txt', 'w').write(result)