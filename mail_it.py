# utilize email.mime to impliment message attachments and pictures etc.
# based on a sample library to handle attachments.

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# populate some defaults for a mail handler.
def send_mail(send_from, send_to, subject, text, files = None, server = "smtp.mailgun.org"):
	assert isinstance(send_to, list) # force the send_to object to be a list.
	
	# looks like applying each of these as attributes to the msg instance of MIMEMultipart()
	# it probably is possible to initialize those in the class constructor, but I don't know for sure, may test it at a later date.
	msg = MIMEMultipart() # utilizing an instance of the class MIMEMultipart (seems to be the multimedia SMTP handler.)
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to)
	msg['Date'] = formatdate(localtime=True) # this is an easier way to format the date than how I was doing it.
	msg['Subject'] = subject
	
	
	msg.attach(MIMEText(text))
	
	for f in files or []:
		with open(f,'rb') as fin:
			part = MIMEApplication(
				fin.read(),
				Name=basename(f)
			)
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
			msg.attach(part)
			
	smtp = smtplib.SMTP(server, 587)
	smtp.login('lol@mg.deeppatel.me', 'havefunscrapingthisinvalidpassword')
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.close()
	
if __name__ == "__main__":
	from sys import argv
	if len(argv) < 2:
		cont = input("Continue? (Y/N) ")
		if not cont.upper() == "N":
			argv.append(input("From Address: "))
			argv.append(input("To Address: ").split(';'))
			argv.append(input("Subject: "))
			argv.append(input("Message: "))
			attach = input("Add attachment? (Y/N) ")
			if attach.upper() == 'Y':
				attlist = input(" Type the list of file paths to attach, seperated by semicolons. ")
				attlist = attlist.split(';')
				assert isinstance(attlist, list)
				argv.append(attlist)
			else:
				argv.append([])
		else:
			quit()
	else:
		while len(argv) < 6:
			argv.append('')
	send_mail(argv[1],argv[2],argv[3],argv[4],argv[5])
