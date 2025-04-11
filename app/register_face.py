import cv2
import os

def capture_new_face(name,save_dir="models",nb_images=10):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erreur : Impossible d’accéder à la webcam.")
        return False
    #creation du dossier 
    user_path = os.path.join(save_dir,name)
    os.makedirs(user_path,exist_ok=True)

    print(f"[INFO] Capture de {nb_images} images pour {name}...")

    count = 0 
    while count < nb_images :
        ret, frame = cam.read()
        if not ret:
            print("[ERREUR] Lecture frame échouée.")
            break

        cv2.imshow("Capture du visage - Appuie sur Q pour quitter", frame)

        #enregistrement de limage 
        img_path = os.path.join(user_path,f"{count}.jpg")
        cv2.imwrite(img_path,frame)
        print(f"[INFO] Image {count+1} enregistrée : {img_path}")
        count += 1 

        #quitter avec q 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return True