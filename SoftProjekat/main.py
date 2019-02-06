import cv2 
import os.path
from pronalazak_brojeva import PronlazakBrojeva

from neuronska_mreza import kreiraj_Sacuvaj_Cnn
from neuronska_mreza import napravi_model
from keras.models import model_from_json



if not os.path.exists('model.h5'):
    print("Model nije kreiran, potrebno ga je kreirati!")
    potvrda,loaded_model = kreiraj_Sacuvaj_Cnn()
    if potvrda == 1:
        print("Uspjesno kreiran model")
    else:
        print("Nije kreiran model")
else: 
    loaded_model = napravi_model()
    loaded_model.load_weights("model.h5")
    print("Ucitaan model sa diska")




for i in range(10):
    naziv_fajla = f'video/video-{i}.avi'

    video = cv2.VideoCapture(naziv_fajla)
    pronlazakBrojeva = PronlazakBrojeva(loaded_model)

    while(video.isOpened()):
        ret, frame = video.read()
        if ret==False:
            break 
    
        pronlazakBrojeva.obradi(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f'{naziv_fajla} : {pronlazakBrojeva.zbirBrojeva}')  
    
    video.release()
cv2.destroyAllWindows()



















