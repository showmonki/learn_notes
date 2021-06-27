import yagmail


def set_auth():
	import getpass
	auth_code = getpass.getpass("provide auth code to send email: ")
	return auth_code


def send_email(auth_code, email_attachments=None):
	# 发送对象列表
	#    Warning: QtConsole does not support password mode, the text you type will be visible.
	yag_server = yagmail.SMTP(user='xxx@163.com', password=auth_code, host='smtp.163.com')
	email_to = ['xxxx@hotmail.com']
	email_subject = 'Automatically notification'
	email_content = 'Task completed. Please check service and close it'
	# 附件列表
	# email_attachments = [ ./attachments/report.png , ]

	# 发送邮件
	yag_server.send(email_to, email_subject, email_content, attachments=email_attachments)
	# 邮件发送完毕之后，关闭连接即可

	# 关闭连接
	yag_server.close()


if __name__ == '__main__':
	auth_code = set_auth()
	send_email(auth_code)
