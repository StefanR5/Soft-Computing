import numpy as np
import cv2 

import math

from scipy import ndimage     #multi dimenzionalno procesiranje slike
from vector import distance, pnt2line



import matplotlib.pyplot as plt 
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 16,12 # za prikaz većih slika i plotova, zakomentarisati ako nije potrebno


class PronlazakBrojeva:
    
    def __init__(self, cnn_model):
        
        self.cnn_model = cnn_model
        self.kernel = np.ones((2,2),np.uint8)

        dolje = np.array([230, 230, 230])
        gore = np.array([255, 255, 255])
        self.dolje = np.array(dolje, dtype = "uint8")
        self.gore = np.array(gore, dtype = "uint8")

        self.elements = []
        self.zbirBrojeva = 0

        self.id = -1
        self.prviFrejm = True
        self.line = 0

    def obradi(self,image):
            
        img_org = image.copy()
        gray = cv2.cvtColor(img_org, cv2.COLOR_BGR2GRAY)        #greyscale
        
        if self.prviFrejm:    
            line = self.houghTrans(gray,image)         #da detektuje liniju         
            self.prviFrejm = 1
        
        
        #provjerava da li se elementi array matrice(image) nalaze izmedju elemenata dvaju drigih array matrica ili polja(dolje i gore)
        mask = cv2.inRange(image, self.dolje, self.gore)    
        img = 1.0*mask

        img = cv2.dilate(img,self.kernel)     #dilatiranje(sirenje slike) slike pomocu odredjenog elementa struktuiranja koji odredjuje
        img = cv2.dilate(img,self.kernel)     #oblik susjednih piksela preko kojih se uzima maksimum

        labeled, nmbr_of_objects = ndimage.label(img)           #radi se labeliranje slike predstavljenog kao niz(array)
        objects = ndimage.find_objects(labeled)             #pronalazenje objekata u labeliranom nizu
        
        for i in range(nmbr_of_objects):
            
            location = objects[i]
            x1 = location[1].stop
            y1 = location[1].start
            xc = int((x1 + y1)/2)
            
            x2 = location[0].stop
            y2 = location[0].start
            yc = int((x2 + y2)/2)
            
            c1 = x1 - y1
            c2 = x2 - y2
            
            if(c1>10 or c2>10):
                
                cv2.circle(image, (xc,yc), 16, (25, 25, 255), 1)
                element = {'center':(xc,yc), 'size':(c1,c2)}    

                lista = self.da_li_le_u_Rasponu(element)
                duzina = len(lista)

                if duzina == 0:
                    self.id += 1
                    element['id'] = self.id
                    element['pass'] = False
                    xc1 = xc
                    yc1 = yc
                    element['history'] = [{'center':(xc1,yc1), 'size':(c1,c2)}]
                    element['future'] = [] 
                    element['number'] = None
                    self.elements.append(element)

                elif duzina == 1:
                    lista[0]['center'] = element['center']
                    xc1 = xc
                    yc1 = yc
                    lista[0]['history'].append({'center':(xc1,yc1), 'size':(c1,c2)}) 
                    lista[0]['future'] = [] 
            
        for el in self.elements:
    
                if el['number'] is None:
                    
                    b =self.selectReg(img_org,el['center'])
                    br = self.vratiBroj(b)

                
                dist, pnt, greska = pnt2line(el['center'], (line[0],line[1]), (line[2],line[3]))
                
                erorr = greska
                if erorr>0:
                    if(dist<9):
                        
                        if el['pass'] == False:
                            el['pass'] = True
                            b=self.selectReg(img_org,el['center'])
                            brr = self.vratiBroj(b)
                            self.zbirBrojeva += brr
                         
     


    def houghTrans(self,imageG,image_org):

        edges = cv2.Canny(imageG,50,150,apertureSize = 3)
        a=50
        b=10
        c=np.pi / 180
        linesP = cv2.HoughLinesP(edges, 1,c, 50, None, a, b)     #pronalazi segmente linije u binarnoj slici koristeci probablisticku  Hough Transform
        
        #for i in range(0, len(linesP)):
        #print('----%d' % len(linesP)) 
        
        if (len(linesP)>0):   
            l = linesP[1][0]
            cv2.line(image_org, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv2.LINE_AA)  #crta segment linije izmedju pt1 i pt2
                
        return l


    def selectReg(self,image_org,centar):        

        gray = cv2.cvtColor(image_org, cv2.COLOR_BGR2GRAY) 
        x_crop = 12
        if centar[1]- 12< 0:
            x_crop = 0

        y_crop = 12
        if centar[0]- 12 < 0:
            y_crop = 0

        region = gray[centar[1]-x_crop:centar[1]+12,centar[0]-y_crop:centar[0]+12]
        picturesRegion = []
        region1 = cv2.resize(region,(28,28), interpolation = cv2.INTER_NEAREST)
        picturesRegion.append(region1)

        return picturesRegion


    def vratiBroj(self,pictures,):
    
        pictures = np.asarray(pictures)

        pictures = pictures.reshape(pictures.shape[0], 1, 28, 28)

        pictures = pictures.astype('float32')

        pictures /= 255
        
        result = self.cnn_model.predict(np.array(pictures[0:1], np.float32))    #generise predvidjanja izlaza za ulazne uzroke
        
        return np.argmax(result[0])


    def da_li_le_u_Rasponu(self, item):
        retVal = []
        for obj in self.elements:
            distanca = distance(item['center'], obj['center'])
            if(distanca<21):
                retVal.append(obj)
        return retVal

