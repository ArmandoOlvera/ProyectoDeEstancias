import sys
import cv2
import numpy as np

umbral_minimo = 100
umbral_maximo = 200
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
	
	
def filtrado(mascara_verde,original):
	white = [255,255,255]
	black = [0,0,0]
	for x in xrange(0,600):
		pass
		for y in xrange(0,600):
			pass
			channels_xy = mascara_verde[x,y]
			if all(channels_xy==white):
				pass
			elif all(channels_xy==black):
				original[x,y]=black
	cv2.imshow('Resultado', original) 			
	cv2.waitKey(0)

def obtenerImagen(hsv,original):
	print MiArray
	image = np.full((100, 600, 3), fill_val) 
	cv2.imshow('Calibrador', image)
	verde_bajos = np.array([49,50,50])
	verde_altos = np.array([107, 255, 255])
	mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
	cv2.imshow('Finale', mascara_verde) 
	filtrado(mascara_verde,original)

def calibrar(hsv):
	while True: 
		print MiArray
		image = np.full((100, 600, 3), fill_val) 
		cv2.imshow('Calibrador', image)
		verde_bajos = np.array([MiArray[0],MiArray[2],MiArray[4]])
		verde_altos = np.array([MiArray[1],MiArray[3],MiArray[5]])
		mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
		##cv2.imshow('HSV', hsv) 
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
	resized_image = cv2.resize(img, (600, 600))
	hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
	cv2.imshow('Original', resized_image)
	##procesado(resized_image)
	###solo tener una de las siguientes funciones des-comentada
	calibrar(hsv)
	##obtenerImagen(hsv,resized_image)
	cv2.destroyAllWindows() 

#Estos son los valores aproximados para detectar el verde
#verde_bajos = np.array([49,50,50]) //
#verde_altos = np.array([107, 255, 255])