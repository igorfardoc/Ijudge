# Ijudge - тестирующая система

Идеей проекта было создать свою тестирующую систему для проверки программ пользователей, написанных под определенные задачи.

Программа состоит из трех основных модулей. Два из них, test и testing, отвечают за тестирование программ пользователей и один, main, за взаимодействие с сайтом.
Безусловно, есть еще несколько модулей, четыре из них – классы для хранения в базе данных: User, Problem, Contest, Solution.
Также стоит заменить, что тестирование не останавливает работу основной программы и сайт не виснет. Это достигается благодаря тому, что модуль тестирования запускается отдельным процессом.
Библиотеки, необходимые для работы программы:
1)	Flask – для создания сайта и взаимодействий с пользователями и администратором
2)	Sqlalchemy – для работы с базой данных
3)	Os – для выполнения команд в командной строке
4)	Sys – для передачи аргументов через командную строку
5)	Datetime – для отслеживания времени
6)	Werkzeug – для хеширования паролей
7)	Time – для задержки работы программы
