import cv2

def capture():
    cam = cv2.VideoCapture(0)   
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
    
        if k%256 == 32:
            # SPACE pressed
            img_name = "opencv.jpg"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            break
    cam.release()
    cv2.destroyAllWindows()

    return img_name
