import imaplib
import re

def encontrar_index(texto, x):
	posiciones = []
	index = 0
	
	while index != -1:
		index = texto.find(x,index)
		if index != -1:
			posiciones.append(index)
			index += 1

	return posiciones


#Generando txt para cada parametro
archivo_ReceivedFirst= open("ReceivedFirst_gog.txt", "w")
archivo_ReceivedLast= open("ReceivedPreLast_gog.txt", "w")
archivo_UTC= open("UTC_gog.txt", "w")
archivo_MsgID= open("MsgID_gog.txt", "w")


#datos
host = 'imap.gmail.com'
imap = imaplib.IMAP4_SSL(host)

imap.login('andresaros433@gmail.com', 'rlildkfqjrlwdrcu')
imap.select('Inbox')
typ, data = imap.search(None,'FROM', 'newsletter@email.gog.com')
contador=0


for num in data[0].split():
    #corta en 40 correos
    if(contador>40):
         break
    #busca los Received
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Received)])')
    datito= data[0][1].decode()
    aux=encontrar_index(datito,'Received')
    #selecciona el primero(Firts) y el penultimo(last)
    lista_ReceivedFirst=datito[aux[2]:len(datito)-2]
    lista_ReceivedLast=datito[aux[1]:aux[2]-1]
    #busca los utc dentro del primer received
    aux1=encontrar_index(lista_ReceivedFirst,'+')
    aux2=encontrar_index(lista_ReceivedFirst,')')
    lista_UTC=lista_ReceivedFirst[aux1[0]:aux2[2]+1]
    #escribe en los archivos
    archivo_ReceivedFirst.write(lista_ReceivedFirst)
    archivo_ReceivedLast.write(lista_ReceivedLast)
    archivo_UTC.write(lista_UTC+'\n')
    #busca el MessageId
    typ, data = imap.fetch(num, '(BODY[HEADER.FIELDS (Message-ID)])')
    datito= data[0][1].decode()
    datito=datito.replace("Message-ID:", "")
    datito=datito.replace(">", "")
    datito=datito.replace("<", "")
    datito=datito.replace("Message-Id:", "")
    datito=datito.strip()
    #escribe messageid
    archivo_MsgID.write(datito+'\n')
    
    
     

    contador=contador+1

print(contador) 
imap.close()

archivo_ReceivedFirst.close()
archivo_ReceivedLast.close()
archivo_UTC.close()

