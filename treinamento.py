import cv2 
import numpy as np 
from PIL import Image 
import os
import shutil

def Treinamento(id_, nome):
# Path for face image database 

    user = str(id_)+"_"+nome
    appdata_path = os.getenv('APPDATA')
    file_path = os.path.join(appdata_path, "PontoLog\\dataFace\\")
    caminho_appdata = os.path.join(appdata_path, "PontoLog\\dataset\\"+user)

	# Caminho completo para a pasta "AppData" do usuário (Unix-like)
	# Caminho completo da pasta que você deseja criar

	# Caminho completo para a pasta "AppData" do usuário (Unix-like)
	# Caminho completo da pasta que você deseja criar
    reconhecer =  cv2.face.LBPHFaceRecognizer_create() 
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    # função para obter as imagens e os dados do rótulo 
    def getImagesAndLabels(path): 
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]      
        faceSamples=[] 
        ids = [] 
        for imagePath in imagePaths : 
            PIL_img = Image.open(imagePath).convert('L') # tons de cinza 
            img_numpy = np.array(PIL_img,'uint8') 
            id = int(os.path.split(imagePath)[-1].split(".")[1]) 
            faces = detector.detectMultiScale(img_numpy) 
            for (x,y,w,h) in faces: 
                faceSamples.append(img_numpy[y:y+h,x:x+w]) 
                ids.append (id) 
        return faceSamples,ids
    faces,ids = getImagesAndLabels(caminho_appdata)
    reconhecer.train(faces, np.array(ids))
    # Salve o modelo em trainer/trainer.yml 
    reconhecer.write(file_path+"\\"+str(id_)+"_"+nome+".yml")    
    caminho_appdata = os.path.join(appdata_path, "PontoLog\\dataset\\"+user)
    shutil.rmtree(caminho_appdata)
    # Imprima o número de faces treinadas e finalize o programa 
    return "sim"