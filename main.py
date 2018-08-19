#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2016  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import signal
import json
import sys
import multiprocessing
import time
import os
import datetime
import ntplib
from datetime import date
import pygtk
pygtk.require('2.0')
import gtk
import cups
from xhtml2pdf import pisa
from firebase import firebase
from basecalc import runCharge

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }
firebase = firebase.FirebaseApplication('https://zacatecas47-bfa49.firebaseio.com', None)

def scanner(proc):
		
		shift = False
		ss = ""
		done = False
		print "On Scanner"
		fp0 = open('/dev/hidraw0', 'rb')
		fp1 = open('/dev/hidraw1', 'rb')
		fp2 = open('/dev/hidraw2', 'rb')
		
		while not done:
			buffer = fp2.read(8)
			if buffer:
				for c in buffer:
					if ord(c) > 0:
						if int(ord(c)) == 40:
							done = True
							break;
						if shift: 
							if int(ord(c)) == 2 :
								shift = True
							else:
								ss += hid2[ int(ord(c)) ]
								shift = False
						else:
							if int(ord(c)) == 2 :
								shift = True
							else:
								ss += hid[ int(ord(c)) ]
		
		proc.exitCode = ss
		print 'exit: ' + proc.exitCode


def getCorretcTime():
	try:
		client = ntplib.NTPClient()
		response = client.request('europe.pool.ntp.org')
		os.system('date' + time.strftime('%m%d%H%M%Y.%S', time.localtime(response.tx_time)))
	except:
		print 'Could not sinc with time server'
	print 'gotDatetime'
	
def getHour():
	return datetime.datetime.now().strftime('%H:%M')
	
def getDay():
	return datetime.datetime.now().strftime('%d,%m,%Y')
	
def getDayCode():
	toRet = datetime.datetime.now().strftime('%Y%m%d%H%M')
	toRet = toRet[3:]
	return  toRet

class Base:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(800,600)
		self.window.set_title('Zacatecas 47')
		self.window.connect('destroy',self.close_window)
		
		#Add objects to window
		#self.mFixed = gtk.Fixed()
		self.titleBox = gtk.VBox()
		self.placasBox = gtk.VBox()
		self.entriesBox = gtk.HBox()
		self.buttonsBox = gtk.HBox()
		self.lostBox = gtk.HBox()
		self.generalBox = gtk.VBox()
		self.mLabel = gtk.Label('Estacionamiento Publico Zacatecas 47')
		self.placasLabel = gtk.Label('Indique las placas')
		self.uploadBtn = gtk.Button('Salida')
		self.uploadBtn.connect('clicked', self.exitClicked)
		self.printBtn = gtk.Button('Registrar')
		self.printBtn.connect('clicked', self.regClicked)
		self.lostTicket = gtk.Button('Boleto Perdido')
		self.lostTicket.connect('clicked', self.lostTicketClick)
		self.placasText = gtk.Entry()
		self.titleBox.pack_start(self.mLabel,False,True,20)
		self.placasBox.pack_start(self.placasLabel,False,True,5)
		self.placasBox.pack_start(self.placasText,False,True,5)
		self.buttonsBox.pack_start(self.printBtn,True,False,5)
		self.buttonsBox.pack_start(self.uploadBtn,True,False,5)
		self.lostBox.pack_start(self.lostTicket,True,False,5)
		self.entriesBox.pack_start(self.placasBox,True,True,15)
		self.generalBox.pack_start(self.titleBox,False,True,25)
		self.generalBox.pack_start(self.entriesBox,False,True,25)
		self.generalBox.pack_start(self.buttonsBox,False,True,25)
		self.generalBox.pack_start(self.lostBox,False,True,25)
		self.window.add(self.generalBox)
		
		#Show the window
		self.window.show_all()
		
	def handler(self,signum,frame):
		if self.p.is_alive():
			raise Exception('end od time')
		
	def lostTicketClick(self, button):
		dialog = gtk.Dialog('Registrar Salida',self.window,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		label = gtk.Label('ingrese las placas del auto')
		dialog.vbox.add(label)
		label.show()
		entry = gtk.Entry()
		dialog.vbox.add(entry)
		entry.show()
		res = dialog.run()
		if res == gtk.RESPONSE_ACCEPT:
			plates = entry.get_text().upper()
			carData = firebase.get('/Autos',None)
			data = json.dumps(carData)
			aData = json.loads(data)
			if aData is not None:
				for (i,car) in aData.items():
					acheck = car['Placa']
					if acheck == plates and car['HoraSalida'] == '':
						self.lostExit(car,i)
						dialog.destroy()
						return
		dialog3 = gtk.MessageDialog(self.window,0,gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE,'Campo Invalido')
		dialog3.format_secondary_text('Auto no en la base de datos')
		dialog3.run()
		dialog3.destroy()
		dialog.destroy()
	
	def exitClicked(self, button):
		self.exitCode = ''
		dialog = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_OK,'Salida')
		dialog.format_secondary_text("Da click en el botón de OK para comenzar el scanner, una vez iniciado contarás con 15 segundos para escanear el boleto, de lo contrario la ventana se cerrará automáticamente.")
		signal.signal(signal.SIGALRM, self.handler)
		self.p = None
		try:
			dialog.run()
			signal.alarm(15)
			self.p= multiprocessing.Process(target=scanner(self))
			self.p.start()
		except Exception, exc:
			dialog.destroy()
		#
		#
		#p.join(1)
		#print 'pAlive? ', p.is_alive()
		#p.terminate()
		#p.join()
		dialog.destroy()
		

		
		if self.exitCode != '':
			self.carExit(False)
			
	def lostExit(self,isLost,localCode):
		toCharge = firebase.get('/Cargos',None)
		chargeData = json.dumps(toCharge)
		cData = json.loads(chargeData)
		#ntC = int(toCharge)
		if isLost['HoraSalida'] != '':
			dialog3 = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,'Salida Invalida')
			dialog3.format_secondary_text('Auto ya cuenta con salida')
			dialog3.run()
			dialog3.destroy()
			return
		dialog = gtk.Dialog('Registrar Salida',self.window,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		label2 = gtk.Label(isLost['Placa'])
		dialog.vbox.add(label2)
		label2.show()
		label3 = gtk.Label('Fecha Entrada: ' + isLost['DiaEntrada'])
		dialog.vbox.add(label3)
		label3.show()
		label4 = gtk.Label('Hora Entrada: ' + isLost['HoraEntrada'])
		dialog.vbox.add(label4)
		label4.show()
		eTime = getHour()
		label5 = gtk.Label('Hora Salida: ' + eTime)
		dialog.vbox.add(label5)
		label5.show()
		totalCharge = runCharge(cData['Hora'],cData['Cuarto'],isLost['DiaEntrada'],isLost['HoraEntrada'],getDay(),eTime,cData['Lost'])
		label6 = gtk.Label('Total a Cobrar: $' + str(totalCharge))
		dialog.vbox.add(label6)
		label6.show()
		res = dialog.run()
		if res == gtk.RESPONSE_ACCEPT:
			data = { 'DiaEntrada' : isLost['DiaEntrada'],
			'DiaSalida' : getDay(),
			'HoraEntrada' : isLost['HoraEntrada'],
			'HoraSalida' : eTime,
			'Placa' : isLost['Placa'],
			'TotalCobrado' : totalCharge}
			result = firebase.put('/Autos',localCode,data)
			if result != '':
				dialog2 = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,'Salida')
				dialog2.format_secondary_text('Salida Registrada Exitosamente')
				dialog2.run()
				dialog2.destroy()
		else:
			dialog.destroy()
		dialog.destroy()
	
	def carExit(self,isLost):
		localCode = self.exitCode
		localCode = localCode[:-1]
		self.exitCode = ''
		toCharge = firebase.get('/Cargos',None)
		chargeData = json.dumps(toCharge)
		cData = json.loads(chargeData)
		#ntC = int(toCharge)
		dataUrl = '/Autos/' + localCode
		carData = firebase.get(dataUrl,None)
		data = json.dumps(carData)
		aData = json.loads(data)
		if aData['HoraSalida'] != '':
			dialog3 = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,'Salida Invalida')
			dialog3.format_secondary_text('Auto ya cuenta con salida')
			dialog3.run()
			dialog3.destroy()
			return
		dialog = gtk.Dialog('Registrar Salida',self.window,gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT,gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		label2 = gtk.Label(aData['Placa'])
		dialog.vbox.add(label2)
		label2.show()
		label3 = gtk.Label('Fecha Entrada: ' + aData['DiaEntrada'])
		dialog.vbox.add(label3)
		label3.show()
		label4 = gtk.Label('Hora Entrada: ' + aData['HoraEntrada'])
		dialog.vbox.add(label4)
		label4.show()
		eTime = getHour()
		label5 = gtk.Label('Hora Salida: ' + eTime)
		dialog.vbox.add(label5)
		label5.show()
		totalCharge = runCharge(cData['Hora'],cData['Cuarto'],aData['DiaEntrada'],aData['HoraEntrada'],getDay(),eTime,0)
		label6 = gtk.Label('Total a Cobrar: $' + str(totalCharge))
		dialog.vbox.add(label6)
		label6.show()
		res = dialog.run()
		if res == gtk.RESPONSE_ACCEPT:
			data = { 'DiaEntrada' : aData['DiaEntrada'],
			'DiaSalida' : getDay(),
			'HoraEntrada' : aData['HoraEntrada'],
			'HoraSalida' : eTime,
			'Placa' : aData['Placa'],
			'TotalCobrado' : totalCharge}
			result = firebase.put('/Autos',localCode,data)
			if result != '':
				dialog2 = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,'Salida')
				dialog2.format_secondary_text('Salida Registrada Exitosamente')
				dialog2.run()
				dialog2.destroy()
		
		dialog.destroy()
		
		
		
	def regClicked(self, button):
		toprint = self.placasText.get_text().upper()
		carData = firebase.get('/Autos',None)
		data = json.dumps(carData)
		aData = json.loads(data)
		shoudlAdd = False
		if aData is not None:
			for (i,car) in aData.items():
				acheck = car['Placa']
				if acheck == toprint and car['HoraSalida'] == '':
					dialog = gtk.MessageDialog(self.window,0,gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE,'Campo Invalido')
					dialog.format_secondary_text('Auto ya ingresado sin hora de salida')
					dialog.run()
					dialog.destroy()
					return
					
		if toprint != '':
			print 'REG Car: ' + toprint
			getCorretcTime()
			entryHour = getHour()
			codedDate = getDayCode() + toprint
			data = { 'DiaEntrada' : getDay(),
			'DiaSalida' : '',
			'HoraEntrada' : entryHour,
			'HoraSalida' : '',
			'Placa' : toprint,
			'TotalCobrado' : ''}
			result = firebase.put('/Autos',codedDate,data)
			if result != '':
				self.placasText.set_text('')
				self.printT(toprint,codedDate,entryHour,getDay())
				dialog = gtk.MessageDialog(self.window,0,gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE,'Ingreso Exitoso')
				dialog.format_secondary_text('Entrada Registrada Exitosamente')
				dialog.run()
				dialog.destroy()
			
			
		else:
			dialog = gtk.MessageDialog(self.window,0,gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE,'Campo Invalido')
			dialog.format_secondary_text("Es necesario llenar las placas y Color/Marca del auto para continuar")
			dialog.run()
			dialog.destroy()
		
		
		
	def printT(self,plates,aTag,inHour):
	
		filename = 'print.pdf'
		xhtml = '<html>\n<head>\n'
		xhtml += '<style>\n@page {\nsize: 2.4in 3.4in;\nmargin: 2mm 2mm 2mm 2mm;\n}\n</style>\n'
		xhtml += '</head>\n'
		xhtml += '<body>\n'
		xhtml += '<h1 style=\'text-align:center;\'>Estacionamiento Publico </br> Zacatecas 47 </br> <img src=\'https://cdn4.iconfinder.com/data/icons/car-silhouettes/1000/beetle-512.png\' style=\'width:50px;height:50px;\'> </h1>\n'
		xhtml += '<h2 style=\'text-align:center;\'>' + plates + '</h2>\n'
		xhtml += '<p style=\'text-align:center;\'>' + +'</h2>\n'
		xhtml += '<p style=\'text-align:center;\'> <b> Hora de entrada:</b> '+ inHour +'</p>\n'
		xhtml += '<p style=\'text-align:center;\'><pdf:barcode value='+ aTag +'/></p>\n'
		xhtml += '<p style=\'text-align:center; font-size: 45%\'>*CONSULTE NUESTRAS CLAUSULAS EN HTTP://paranoidinteractive.com/zacatecas</br>*LA RECEPCION DE ESTE BOLETO IMPLICA LA ACEPTACION DE LAS CLAUSULAS DEL ESTACIONAMIENTO </br>*NO SE RECIBEN AUTOMOVILES CON PERSONAS O MASCOTAS EN EL INTERIOR</p>\n'
		xhtml += '<p style=\'text-align:center; font-size: 75%\'>HORARIO DE LUN a VIER DE 8:30AM a 9:00PM </br> HORARIO SABADOS DE 8:00AM a 3:00PM</p>\n'
		xhtml += '</body>\n'
		xhtml += '</html>\n'
		pdf = pisa.CreatePDF(xhtml, file(filename, 'w'))
		if not pdf.err:
			pdf.dest.close()
		
			conn = cups.Connection()
			printers = conn.getPrinters()
			for printer in printers:
				print printer,printers[printer]['device-uri']
				printer_name = printers.keys()[0]
				conn.printFile(printer_name, filename,'Python_Status_print',{'CutMedia':'1'})
		else:
			print 'unable to create pdf'
		
	def main(self):
		gtk.main()
		
	def close_window(self,widget,data = None):
		gtk.main_quit()

if (__name__ == '__main__'):
	base = Base()
	base.main()
