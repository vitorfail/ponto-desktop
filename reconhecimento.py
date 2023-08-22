import cv2
import os 
import keyboard
import tkinter.messagebox as tkmb


def Reconhecimento(id_, nome, appdata_path):
    file_path = os.path.join(appdata_path, "PontoLog\\dataFace\\")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(file_path+"\\"+str(id_)+"_"+nome+".yml")
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Marcelo', 'Paula', 'Ilza', 'Z', 'W'] 
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    v = True
    while v:
        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less them 100 ==> "0" : perfect match 
            if (confidence < 60 and confidence> 40 and confidence>0):
                id = nome.upper()
                confidence = "  {0}%".format(round(confidence))
                v= False
            else:
                id = "Reconhecendo...."
                confidence = "  {0}%".format(round(confidence))
            
            cv2.putText(
                        img, 
                        str(id), 
                        (x+5,y-5), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                    )
            cv2.putText(
                        img, 
                        str(confidence), 
                        (x+5,y+h-5), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                    )  
        
        cv2.imshow('Reconheçendo...',img) 
        k = cv2.waitKey(1)

        if keyboard.is_pressed('space'):
            break
    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()
    return v
