import cv2
import time
import numpy as np
from urllib.request import urlopen
import argparse 
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
cap = cv2.VideoCapture(0)
count=0
while True: 
    __, frame = cap.read()
    fr3 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Use MTCNN to detect faces
    result = detector.detect_faces(frame)
    le1,le2,le3,le4 = 0,0,0,0
    re1,re2,re3,re4 = 0,0,0,0
    n1,n2,n3,n4 = 0,0,0,0
    m1,m2,m3,m4 = 0,0,0,0
    f1,f2,f3,f4 = 0,0,0,0
    if result != []:
        for person in result:
            bounding_box = person['box']
            keypoints = person['keypoints']
    
            cv2.rectangle(frame,
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                          (0,155,255),
                          2)
    
            cv2.rectangle(frame,(keypoints['left_eye'][0]-20,keypoints['left_eye'][1]-10),(keypoints['left_eye'][0]+20,keypoints['left_eye'][1]+15) , (0,155,255), 2)
            cv2.rectangle(frame,(keypoints['right_eye'][0]-20,keypoints['right_eye'][1]-10),(keypoints['right_eye'][0]+20,keypoints['right_eye'][1]+15) , (0,155,255), 2)
            cv2.rectangle(frame,(keypoints['nose'][0]-30,keypoints['nose'][1]-15),(keypoints['nose'][0]+30,keypoints['nose'][1]+15) , (0,155,255), 2) 
            cv2.rectangle(frame,(keypoints['mouth_left'][0]-10,keypoints['mouth_left'][1]-20),(keypoints['mouth_right'][0]+10,keypoints['mouth_right'][1]+10) , (0,155,255), 2)
            # cv2.circle(frame,(keypoints['mouth_left']), 2, (0,155,255), 2)
            # cv2.circle(frame,(keypoints['mouth_right']), 2, (0,155,255), 2)
            le1,le2,le3,le4 = keypoints['left_eye'][0]-20,keypoints['left_eye'][1]-10,keypoints['left_eye'][0]+20,keypoints['left_eye'][1]+15
            re1,re2,re3,re4 = keypoints['right_eye'][0]-20,keypoints['right_eye'][1]-10,keypoints['right_eye'][0]+20,keypoints['right_eye'][1]+15
            n1,n2,n3,n4 = keypoints['nose'][0]-30,keypoints['nose'][1]-15,keypoints['nose'][0]+30,keypoints['nose'][1]+15
            m1,m2,m3,m4 = keypoints['mouth_left'][0]-10,keypoints['mouth_left'][1]-20,keypoints['mouth_right'][0]+10,keypoints['mouth_right'][1]+10
            f1,f2,f3,f4 = bounding_box[0], bounding_box[1],bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]
    #display resulting frame
    frame = cv2.resize(frame, (900,500), interpolation = cv2.INTER_AREA) #resize window
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        facial = fr3 [f2:f4, f1:f3]
        eyer = fr3 [re2:re4, re1:re3]
        eyel = fr3 [le2:le4, le1:le3]
        nosu = fr3 [n2:n4, n1:n3]
        mothu = fr3 [m2:m4, m1:m3]
        cv2.imwrite(filename='face'+str(count)+'.jpg', img=facial)
        cv2.imwrite(filename='eyer'+str(count)+'.jpg', img=eyer)
        cv2.imwrite(filename='eyel'+str(count)+'.jpg', img=eyel)
        cv2.imwrite(filename='nose'+str(count)+'.jpg', img=nosu)
        cv2.imwrite(filename='mouth'+str(count)+'.jpg', img=mothu)
        count+=1
        if count==2:
            break 
    if key &0xFF == ord('q'):
        break
#When everything's done, release capture
cap.release()
cv2.destroyAllWindows()
import compare
