# -*- coding: utf-8 -*-
import socket
import os


def get_response(request):

	directory_start = request.find(' ')
	directory_cut = request[directory_start + 1: ]
	directory_end = directory_cut.find(' ')
	directory = directory_cut[: directory_end]

	directory_media = "/home/mikhail/technotrackWEB/technotrack-web1-autumn-2017/httpserver/files"
	media_list = os.listdir(directory_media)
	media_list_str = '\n'.join(media_list)

	if directory[0 : 7] != "/media/":
		no_file_flag = 2
	else:
		no_file_flag = 1
		for i in media_list:
			if directory[7 :] == i:
				no_file_flag = 0
				directory_media_file = i
				break

	if directory == "/":
		user_agent_start = request.find('User-Agent: ')
		user_agent_cut = request[user_agent_start + len('User-Agent: ') :]
		user_agent_end = user_agent_cut.find('\n')
		user_agent = user_agent_cut[: user_agent_end]
		return 'HTTP/1.1 200 OK\n\n' + 'Hello mister!\nYou are: ' + user_agent + "\n"
	elif directory == "/test/":
		return 'HTTP/1.1 200 OK\n\n' + request + "\n"
	elif directory == "/media/":
		return 'HTTP/1.1 200 OK\n\n' + media_list_str + "\n"
	elif no_file_flag == 0 and directory == "/media/" + directory_media_file:
		file = open(directory_media + "/" + directory_media_file, "r")
		file_content = file.read()
		file.close
		return 'HTTP/1.1 200 OK\n\n' + file_content + "\n"
	#elif directory == "/media/" + "test2.txt":
	#	file = open(directory_media + "/test2.txt", "r")
	#	file_content = file.read()
	#	file.close
	#	return 'HTTP/1.1 200 OK\n\n' + file_content + "\n"
	elif no_file_flag == 1:
		return 'HTTP/1.1 404 Not found\n\n' + 'File not found' + "\n"
	else:
		return 'HTTP/1.1 404 Not found\n\n' + 'Page not found' + "\n"

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
        client_socket.close()
    except KeyboardInterrupt:  # при нажатии сочетания клавиш Ctrl+C переходит в блок закрытия сокета
        print 'Stopped'
        server_socket.close()  # закрытие соединения
        exit()
