import sys
import cv2
umbral_minimo = 100
umbral_maximo = 200

def procesado(imagen):
	#Pasamos la imagen a grises
	img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
	cv2.imshow('Imagen en Gris',img_gris)
	##Realizamos un filtro gausiano para poder eliminar el posible ruido de la imagen
	#Lo anteriormencionado con un kernel de 5x5
	gaussiana = cv2.GaussianBlur(img_gris, (5, 5), 0)
	cv2.imshow('Filtro Gausiano - Suavizado - Filtro de Paso Bajo',gaussiana)
	##Ahora realizaremos un procesado para detectar bordes Canny
	#Sobel - Tecnica del calculo con derivadas
	#Filtrado de Bordes por supresion non-maximun - permite adelgazar bordes basandose en el gradiante
	#Umbral por histeresis - un umbral maximo y un minimo
	canny = cv2.Canny(gaussiana, umbral_minimo, umbral_maximo)
	cv2.imshow('Canny',canny)
	##Con esto vamos a obtener los contornos para la imagen: cv2.findContours(imagenbinarizada, modo_contorno, metodo_aproximacion)
	(imagen2, contornos, jerarquia) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	#Mostramos el numero de monedas por consola
	print("He encontrado {} objetos".format(len(contornos)))
	cv2.drawContours(imagen,contornos,-1,(0,0,255), 2)
	cv2.imshow("Contornos", imagen)

if __name__=='__main__':
	img = cv2.imread("Imagenes/sevecreible.JPG",1)
	procesado(img)

cv2.imshow('Imagen Original',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

