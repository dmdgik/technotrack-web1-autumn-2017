# -*- coding: utf-8 -*-
import socket


def get_response(request):

	directory_start = request.find('GET ')
	directory_cut = request[directory_start + 4: ]
	directory_end = directory_cut.find(' ')

	directory = directory_cut[: directory_end]

	if directory == "/":
		user_agent_start = request.find('User-Agent: ')
		user_agent_cut = request[user_agent_start + len('User-Agent: ') :]
		user_agent_end = user_agent_cut.find('\n')
		user_agent = user_agent_cut[: user_agent_end]
		return 'Hello mister!\nYou are: ' + user_agent + '\nYour directory: ' + directory
	else:
		return 'Not found' + directory

def send_response(): 
	pass


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto = 0)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # привязка сокета к хосту и порту
server_socket.listen(1)  # запуск режима прослушивания сокета с максимальным количеством подключений 0

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # при подключении к серверу выводить сообщение
        request_string = client_socket.recv(2048)  # принятия данных от пользователя порциями по 2048 байт
        client_socket.send(get_response(request_string))  # вывод информации из функции get_response
        client_socket.send('\n\n\n' + request_string)
        client_socket.close()
    except KeyboardInterrupt:  # при нажатии сочетания клавиш Ctrl+C переходит в блок закрытия сокета
        print 'Stopped'
        server_socket.close()  # закрытие соединения
        exit()
