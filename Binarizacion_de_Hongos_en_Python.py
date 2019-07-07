import cv2
import numpy as np
import pandas as pd

######################################################################################################

def area_del_cultivo_de_bacterias(nombre,Binar = 125,dim_del_kernel = 5, iteraciones = 4):
	
	gray = cv2.imread(nombre,0)				# Lee la imagen en escala de grises
	gray = cv2.resize(gray, (400,400))		# redimensiona la imagen 

	Rango_bajo = Binar						# Rango de Binarización
	Rango_alto = 255						# Tono de la Binarización

	# Binarización
	ret,Mascara = cv2.threshold(gray,Rango_bajo,Rango_alto,cv2.THRESH_BINARY_INV)

	# Filtros

	# Definimos el Kernel
	kernel = np.ones((dim_del_kernel,dim_del_kernel),np.uint8)

	# Erosión
	MascaraEND = cv2.erode(Mascara,kernel,iterations = iteraciones)

	# Opening
	MascaraEND = cv2.morphologyEx(MascaraEND, cv2.MORPH_OPEN,kernel)

	# Dilatación
	MascaraEND = cv2.dilate(MascaraEND,kernel,iterations = iteraciones)

	# Momentos
	moments = cv2.moments(MascaraEND)
	area = int(moments['m00'])
	print("El tamaño del cultivo es de "+str(area) +" pixeles")

	cv2.imshow('Escala de grises',gray)
	cv2.imshow('Binarizada',Mascara)
	cv2.imshow('Filtrada',MascaraEND)

	cv2.waitKey(0) 			# Presione una tecla para pasar a la siguiente imagen
	return(area)

#####################################################################################################

formato = ".jpg"			# Formato de las imagenes
Ndata = 4					# Número de imagenes
Datos_de_Areas = []			# Lista de almacenamiento de datos para las areas
Fechas = []					# Fechas en la que se tomo las imagenes

for cond_i in range (0,Ndata):
	nombre = str(cond_i+1)+formato 							# Nombre de la imagen actual
	area = area_del_cultivo_de_bacterias(nombre)			# Area optenida del cultivo
	Datos_de_Areas.append(area)								# Agrega el dato a una lista
	Fechas.append((cond_i+25))							# Agrega el dato a una lista

	# Se organiza la Data 
	data = {'Fecha (Junio)': Fechas,'Area del cultivo (En pixeles)': Datos_de_Areas}
	df = pd.DataFrame(data, columns = ['Fecha (Junio)','Area del cultivo (En pixeles)'])

# Se guarda la data en un archivo excel
df.to_excel('Data.xlsx', sheet_name='Data')

#######################################################################################################
