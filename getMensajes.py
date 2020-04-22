import datetime as dt
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PIL import Image
from selenium import webdriver
from splinter import Browser


class Datos: 
    def __init__(self, sender, pw_mail, reciever, legajo, pw_utn, servicio):
        self.sender = sender
        self.pw_mail = pw_mail
        self.reciever = reciever
        self.legajo = legajo
        self.pw_utn = pw_utn
        self.servicio = servicio

    def getSender(self):
        return self.sender

    def getPw_mail(self):
        return self.pw_mail
    
    def getReciever(self):
        return self.reciever

    def getLegajo(self):
        return self.legajo
    
    def getPw_utn(self):
        return self.pw_utn
    
    def getServicio(self):
        return self.servicio
    



def leerDatos():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname,'datos')

    f = open(filename, 'r')

    sender = f.readline().split(None, 1)[0]
    pw_mail = f.readline().split(None, 1)[0]
    reciever = f.readline().split(None, 1)[0]
    legajo = f.readline().split(None, 1)[0]
    pw_utn = f.readline().split(None, 1)[0]
    servicio = f.readline().split(None, 1)[0]

    dato = Datos(sender,pw_mail,reciever,legajo,pw_utn,servicio)

    return dato


 ## LEO LOS DATOS CARGADOS EN EL ARCHIVO 'datos.txt'   

dato = leerDatos()

## ENTRAR A LA PAGINA DE LA FACULTAD Y OBTENER UNA SCREENSHOT DE LOS MENSAJES
executable_path = {'executable_path':r'/home/tomas/PycharmProjects/getMSG/driver/chromedriver'}
options = webdriver.ChromeOptions()
options.add_argument("--start-minimized")
options.add_argument("--disable-notifications")
browser = Browser('chrome', **executable_path, headless=False, options=options, incognito=True)
browser.visit("http://frc.utn.edu.ar")
browser.find_by_text("Facultad").click()
browser.find_by_id("B").click()
browser.find_by_id('txtUsuario').first.fill(dato.getLegajo())
browser.find_by_id('pwdClave').first.fill(dato.getPw_utn())
browser.find_by_xpath('//select[@id="txtDominios"]//option[@value="'+dato.getServicio()+'"]').first.click()
browser.find_by_id("btnEnviar").click()
time.sleep(10)
screenshot_path = "/home/tomas/Documents/ProyectosVC/getMensajesFacultad/last_sc.png"
screenshot =  browser.screenshot(screenshot_path, full=False)
browser.quit()

## DIRECCIONES Y CONTRA
sender_address = dato.getSender()
sender_pass = dato.getPw_mail()
receiver_address = dato.getReciever()

## OBTENER MES, DIA, HORA Y MINUTOS
current_time = dt.datetime.now()
dia = current_time.day
mes = current_time.month
hora = current_time.hour
minuto = current_time.minute

## MIME SETUP
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'Screenshot '+str(dia)+'/'+str(mes)+'  '+str(hora)+':'+str(minuto)

## OBTENGO LA SC QUE ACABO DE CREAR
sc_path = "/home/tomas/Documents/ProyectosVC/getMensajesFacultad/"
attach_file_name = os.listdir(sc_path)
full_sc_path = "" + sc_path + attach_file_name[0]
attach_file = Image.open(full_sc_path) 

## ABRO LA IMAGEN
img_data = open(full_sc_path, 'rb').read()

## CREO EL MENSAJE
text = MIMEText("test")
message.attach(text)
image = MIMEImage(img_data, name=os.path.basename(full_sc_path))
message.attach(image)

## ME CONECTO AL SERVICIO DE GMAIL Y ENVIO EL MAIL
s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(sender_address,sender_pass)
s.sendmail(sender_address,receiver_address, message.as_string())
s.quit()

