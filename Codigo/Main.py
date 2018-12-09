import sys
import cv2
import numpy as np
import copy
umbral_minimo = 100
umbral_maximo = 200
ancho=600
alto=600
areaMin=400
areaMax=1000
#Con esto vamos a manejar los valores de la imagen, lo que vamos a detectar
#H_MIN_VALUE,H_MAX_VALUE,S_MIN_VALUE,S_MAX_VALUE,V_MIN_VALUE,V_MAX_VALUE
MiArray = [255,255,255,255,255,255]

cv2.namedWindow('Calibrador')
fill_val = np.array([255, 255, 255], np.uint8)

##Con esta funcion vamos a controlar los valores dados por la interfaz
def trackbar_callback(idx, value): 
	MiArray[idx]=value

def procesado(imagen):
	#Pasamos la imagen a grises
	img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
	cv2.imshow('Imagen en Gris',img_gris)
	##Realizamos un filtro gausiano para poder eliminar el posible ruido de la imagen
	#Lo anteriormencionado con un kernel de 5x5
	##gaussiana = cv2.GaussianBlur(img_gris, (5, 5), 0)
	##cv2.imshow('Filtro Gausiano - Suavizado - Filtro de Paso Bajo',gaussiana)
	##Ahora realizaremos un procesado para detectar bordes Canny
	#Sobel - Tecnica del calculo con derivadas
	#Filtrado de Bordes por supresion non-maximun - permite adelgazar bordes basandose en el gradiante
	#Umbral por histeresis - un umbral maximo y un minimo
	##canny = cv2.Canny(gaussiana, umbral_minimo, umbral_maximo)
	##cv2.imshow('Canny',canny)
	##Con esto vamos a obtener los contornos para la imagen: cv2.findContours(imagenbinarizada, modo_contorno, metodo_aproximacion)
	##(imagen2, contornos, jerarquia) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	#Mostramos el numero de monedas por consola
	##print("He encontrado {} objetos".format(len(contornos)))
	##cv2.drawContours(imagen,contornos,-1,(0,0,255), 2)
	##cv2.imshow("Contornos", imagen)
	
	
def filtrado(Mverde,Mcafe,original,otros):
	originalclone = copy.copy(original)
	mascaraDeOtros = copy.copy(otros)
	src = copy.copy(original)
	##Se obtiene el treshold de la mascara de pasto cafe
	t, dst = cv2.threshold(Mcafe, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
	#Se obtiene para el pasto verde
	t2, dst2 = cv2.threshold(Mverde, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
	# obtener los contornos de los pastos verde , cafes y objetos desconocidos
	a, contours,c = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	a2, contours2,c2 = cv2.findContours(dst2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# dibujar los contornos (todos sin importar el tamano)
	#cv2.drawContours(src, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
	

	#Aqui se hace el proceso de dibujar los contornos de pasto verde
	for c2 in contours2:
	    area = cv2.contourArea(c2)
	    if area > areaMin:
	        cv2.drawContours(src, [c2], -1, (0, 255, 0),3, cv2.LINE_AA)
	    if area > areaMax+10000 :
	    	(x, y, w, h) = cv2.boundingRect(c2)
	        cv2.putText(src, "SEGURO", (x + (w/3), y + (h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0.5, 2);
	#Se eliminan los contornos indeseados, estas son areas que no son
	#lo suficientemente grandes como para causar un incendio
	for c in contours:
	    area = cv2.contourArea(c)
	    if area > areaMin:
	        cv2.drawContours(src, [c], 0, (0, 0, 255), 2, cv2.LINE_AA)
	#Se encierran en un rectangulo las areas mas grandes con riesgo a incendio
	X=0
	Y=0
	for c in contours:
	    area = cv2.contourArea(c)
	    if area > areaMax:
	        (x, y, w, h) = cv2.boundingRect(c)
	        Y=y
	        X=x
	        cv2.putText(src, "RIESGO", (x + (w/3), y + (h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0.5, 2);
	        cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1, cv2.LINE_AA)

	#Mverde = cv2.GaussianBlur(Mverde, (7,7), 0)
	white = [255,255,255]
	black = [0,0,0]
	rojo =[9,10,229]
	verde = [15,176,9]
	#Aqui se filtra la imagen original y la mascara para poder dibujar en rojo areas de peligro
	#y en verde areas seguras (pasto verde sin riesgo a incendio)
	for x in xrange(0,ancho):
		pass
		for y in xrange(0,alto):
			pass
			verde_xy =Mverde[x,y]
			cafe_xy =Mcafe[x,y]
			otro_xy=mascaraDeOtros[x,y]
			#Checamos los pixeles de la mascara de otros y si detecta negro lo pasa a blanco
			#si detecta blanco lo pasa a negro
			if all(otro_xy==white):
				pass
				mascaraDeOtros[x,y]=0
			if all(otro_xy==black):
				pass
				mascaraDeOtros[x,y]=255
			#Checamos pixeles para dibujarlos verde en base a la mascara verde
			if all(verde_xy==white):
				pass
				original[x,y]=verde
				#originalclone[x,y]=verde
			elif all(verde_xy==black):
				original[x,y]=black
				originalclone[x,y]=black
			#Checamos pixeles para dibujarlos rojos en base a la mascara cafe
			if all(cafe_xy==white):
				pass
				original[x,y]=rojo
				#originalclone[x,y]=rojo


	#Se obtienen para otros objetos
	t3, dst3 = cv2.threshold(mascaraDeOtros, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
	#Se obtienen los contornos de otros
	a3, contours3,c3 = cv2.findContours(dst3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#Aqui se hace el proceso de dibujar los contornos de otros objetos
	for c3 in contours3:
	    area = cv2.contourArea(c3)
	    if area > areaMin:
	    	(x, y, w, h) = cv2.boundingRect(c3)
	    	cv2.putText(src, "OTRO", (x + (w/3), y + (h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0.5, 2);
	        cv2.drawContours(src, [c3], -1, (153, 0, 0),2, cv2.LINE_AA)

	#Se imprimen las imagenes
	cv2.imshow('SRC',src)
	cv2.imshow('Resultado', original)
	cv2.imshow('Original', originalclone) 			
	cv2.waitKey(0)

def obtenerImagen(hsv,original):
	print MiArray
	hsv = cv2.GaussianBlur(hsv, (7,7), 3)
	image = np.full((100, 600, 3), fill_val) 
	cv2.imshow('Calibrador', image)
	verde_bajos = np.array([25,55,0])
	verde_altos = np.array([118, 255, 255])
	cafe_bajo = np.array([9,50,50])
	cafe_alto = np.array([24,158,255])

	mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
	mascara_cafe = cv2.inRange(hsv, cafe_bajo, cafe_alto)
	##mask = cv2.add(mascara_verde, mascara_verde)
	##mask = cv2.add(mask, mascara_cafe)
	#ascara_verde2=cv2.GaussianBlur(mascara_verde, (3,3), 0)
	#mascara_cafe2=cv2.GaussianBlur(mascara_cafe, (3,3), 0)
	##cv2.GaussianBlur(original, (1,1), 0)
	##Un filtro gaussiano no nos sirve, procedemos a realizar una erosion
	kernel = np.ones((3,3),np.uint8)
	#Se aplica la transformacion: Erode
	transformacion1 = cv2.dilate(mascara_verde,kernel,iterations = 1)
	transformacion2 = cv2.dilate(mascara_cafe,kernel,iterations = 1)
	##Se aplica el efecto dilatacion
	transformacion3 = cv2.erode(transformacion1,kernel,iterations = 1)
	transformacion4 = cv2.erode(transformacion2,kernel,iterations = 1)
	###Mostramos las imagenes
	transformacion5 = cv2.morphologyEx(transformacion3,cv2.MORPH_OPEN,kernel)
	transformacion6= cv2.morphologyEx(transformacion4,cv2.MORPH_OPEN,kernel)
	transformacion7 = cv2.morphologyEx(transformacion5,cv2.MORPH_CLOSE,kernel)
 	transformacion8 = cv2.morphologyEx(transformacion6,cv2.MORPH_CLOSE,kernel)
 	mascaraDeOtros = cv2.add(mascara_verde, mascara_verde)
 	mascaraDeOtros = cv2.add(mascaraDeOtros, mascara_cafe)
 	cv2.imshow('ptr', mascaraDeOtros)
	cv2.imshow('Verde', transformacion7)
	cv2.imshow('Cafe', transformacion8) 
	filtrado(transformacion7,transformacion8,original,mascaraDeOtros)

def calibrar(hsv):
	hsv = cv2.GaussianBlur(hsv, (7,7), 3)
	while True: 
		print MiArray
		image = np.full((100, 600, 3), fill_val) 
		cv2.imshow('Calibrador', image)

		verde_bajos = np.array([MiArray[0],MiArray[2],MiArray[4]])
		verde_altos = np.array([MiArray[1],MiArray[3],MiArray[5]])
		mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
		cv2.imshow('HSV', hsv) 
		cv2.imshow('CALIBRANDO...', mascara_verde) 
		
		key = cv2.waitKey(3) 
		if key == 27: 
			break 


if __name__=='__main__':
	cv2.createTrackbar('H_MIN_VALUE', 'Calibrador', 49, 255, lambda v: trackbar_callback(0, v)) 
	cv2.createTrackbar('H_MAX_VALUE', 'Calibrador', 107, 255, lambda v: trackbar_callback(1, v)) 
	cv2.createTrackbar('S_MIN_VALUE', 'Calibrador', 50, 255, lambda v: trackbar_callback(2, v))
	cv2.createTrackbar('S_MAX_VALUE', 'Calibrador', 255, 255, lambda v: trackbar_callback(3, v)) 
	cv2.createTrackbar('V_MIN_VALUE', 'Calibrador', 50, 255, lambda v: trackbar_callback(4, v)) 
	cv2.createTrackbar('V_MAX_VALUE', 'Calibrador', 255, 255, lambda v: trackbar_callback(5, v))
	##img = cv2.imread("Imagenes/opencv_logo.png",1)
	img = cv2.imread("Imagenes/1041.jpg",1)
	resized_image = cv2.resize(img, (ancho, alto))
	hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
	cv2.imshow('Original', resized_image)
	##procesado(resized_image)
	###solo tener una de las siguientes funciones des-comentada
	##calibrar(hsv)
	obtenerImagen(hsv,resized_image)
	cv2.destroyAllWindows() 

#Estos son los valores aproximados para detectar el verde
#verde_bajos = np.array([49,50,50]) //
#verde_altos = np.array([107, 255, 255])