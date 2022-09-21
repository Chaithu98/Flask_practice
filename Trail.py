import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("krishnakanha324@gmail.com", "lwwkgnghvuhjaegs")
query="hello"
message = "-------------Welcome to Coffe on clouds-----------\n"
print(message)
for item in query:
    val =" Item :"+item['Item']
try:
        #s.sendmail("krishnakanha324@gmail.com", val, message)
    print('notification sent')
except:
    print('error sending notification')
    s.quit()