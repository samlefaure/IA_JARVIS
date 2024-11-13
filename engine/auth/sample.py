# import cv2

# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #create a video capture object which is helpful to capture videos through webcam
# cam.set(3, 640) # set video FrameWidth
# cam.set(4, 480) # set video FrameHeight


# detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')
# #Haar Cascade classifier is an effective object detection approach

# face_id = input("Enter a Numeric user ID  here:  ")
# #Use integer ID for every new face (0,1,2,3,4,5,6,7,8,9........)

# print("Taking samples, look at camera ....... ")
# count = 0 # Initializing sampling face count

# while True:

#     ret, img = cam.read() #read the frames using the above created object
#     converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #The function converts an input image from one color space to another
#     faces = detector.detectMultiScale(converted_image, 1.3, 5)

#     for (x,y,w,h) in faces:

#         cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) #used to draw a rectangle on any image
#         count += 1

        
#         cv2.imwrite("engine\\auth\\samples\\face." + str(face_id) + '.' + str(count) + ".jpg", converted_image[y:y+h,x:x+w])
#         # To capture & Save images into the datasets folder

#         cv2.imshow('image', img) #Used to display an image in a window

#     k = cv2.waitKey(100) & 0xff # Waits for a pressed key
#     if k == 27: # Press 'ESC' to stop
#         break
#     elif count >= 100: # Take 50 sample (More sample --> More accuracy)
#          break

# print("Samples taken now closing the program....")
# cam.release()
# cv2.destroyAllWindows()

import cv2

# Créer un objet de capture vidéo pour capturer les vidéos à partir de la webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Définir la largeur du cadre vidéo
cam.set(4, 480)  # Définir la hauteur du cadre vidéo

# Utiliser un classificateur en cascade Haar pour la détection de visages
detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')

# Demander un ID utilisateur numérique
face_id = input("Enter a Numeric user ID here: ")

print("Taking samples, look at the camera ....... ")
count = 0  # Initialiser le compteur d'échantillons de visage

while True:
    ret, img = cam.read()  # Lire les frames avec l'objet cam
    img = cv2.resize(img, (320, 240))  # Réduire la taille de l'image pour accélérer le traitement
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convertir en niveaux de gris
    faces = detector.detectMultiScale(converted_image, scaleFactor=1.1, minNeighbors=4)  # Optimiser les paramètres

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dessiner un rectangle autour du visage
        count += 1

        # Capturer et enregistrer les images dans le dossier des datasets
        cv2.imwrite(f"engine\\auth\\samples\\face.{face_id}.{count}.jpg", converted_image[y:y + h, x:x + w])

    # Augmenter légèrement le délai pour éviter un traitement trop rapide
    k = cv2.waitKey(200) & 0xff
    if k == 27:  # Appuyer sur 'ESC' pour arrêter
        break
    elif count >= 100:  # Prendre 100 échantillons
        break

print("Samples taken, now closing the program....")
cam.release()  # Libérer la webcam
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
