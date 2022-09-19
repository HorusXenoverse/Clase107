from turtle import distance
import cv2
import time
import math

#Almacena las posiciones fijas de la canasta
p1 = 530
p2 = 300

#Matrices para guardar posiciones de trayectoria
xS = []
yS = []

video = cv2.VideoCapture("bb3.mp4")

# Cargar rastreador 
tracker = cv2.TrackerCSRT_create()

# Leer el primer cuadro del video
returned, img = video.read()

# Seleccionar el cuadro delimitador en la imagen
bbox = cv2.selectROI("Rastreando", img, False)

# Inicializar el rastreador en la imagen y el cuadro delimitador
tracker.init(img, bbox)

print(bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])

    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

    cv2.putText(img,"Rastreando",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

#Funcion para marcar los puntos medios, marcar la trayectoria y calcular la distancia
def goal_track(img, bbox):
    #Almacena posicion x, y, w, h del objeto marcado
    x, y, w, h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])

    #Calculamos el punto medio del cuadro del objeto
    c1 = x + int(w/2)
    c2 = y + int(w/2)

    #Dibujamos circulo a objeto y canasta
    cv2.circle(img, (c1,c2), 2, (0, 255, 0), 3)
    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)

    #Calculamos la distancia y mediante el if mostramos si se logró una canasta
    distancia = math.sqrt(  ((c1-p1)**2) + ((c2-p2)**2)  )
    if distancia <= 20:
        cv2.putText(img, "Canasta", (300,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
     
    #Metimos en las matrices vacias las posiciones X y Y del objeto
    xS.append(c1)
    yS.append(c2)

    #Recorrimos con el ciclo for la posicion para dibujar un circulo en cada una mostrando su trayectoria
    for circulo in range(len(xS) -1):
        cv2.circle(img, (xS[circulo], yS[circulo]), 2, (0, 0, 255), 1)    
 


while True:
    
    check, img = video.read()   

    # Actualizar el rastreador en la imagen y el cuadro delimitador
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img,"Perdido",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    #Se mando a llamar la funcion
    goal_track(img, bbox)

    cv2.imshow("Resultado", img)
            
    key = cv2.waitKey(25)
    if key == 32:
        print("Detenido")
        break

video.release()
cv2.destroyALLwindows()