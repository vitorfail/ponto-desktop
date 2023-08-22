import cv2
import keyboard
import os
from pathlib import Path

def CadastroRosto(id, nome):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    font = cv2.FONT_HERSHEY_SIMPLEX



    # Initialize individual sampling face count
    count = 0
    appdata_path = os.getenv('APPDATA')
    file_path = os.path.join(appdata_path, "PontoLog\\dataset")
    user = id+"_"+nome
    caminho_appdata = Path.home() / "AppData\Roaming\PontoLog\dataset"

	# Caminho completo para a pasta "AppData" do usuário (Unix-like)
	# Caminho completo da pasta que você deseja criar
    caminho_completo = caminho_appdata / user
    caminho_completo.mkdir()

    laco = True
    space = True
    while laco:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
                    # Save the captured image into the datasets folder
            cv2.putText(
                        img, 
                        "Deixe o rosto enquadrado", 
                        (x-100,y-40), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                    )
            cv2.putText(
                        img, 
                        "Aperte espaco e espere 7 segundos.", 
                        (x-150,y-5), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                    )
            if count==20:
                laco= False
            if space == False:                
                cv2.imwrite(file_path+"\\"+user+"\\"+str(id) + '.' + str(count)+".jpg", gray[y:y+h+100,x:x+w+100])
                count= count+1
     

        cv2.imshow('Cadastrar Rosto',img)
        k = cv2.waitKey(1)
        if keyboard.is_pressed('space'):
            space = False # press 'ESC' to quit

    cap.release()
    cv2.destroyAllWindows()