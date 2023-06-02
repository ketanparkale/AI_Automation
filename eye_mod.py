import pyautogui
import cv2 as cv 
import numpy as np
import mediapipe as mp
import autopy
import mouse
import time


mp_face_mesh = mp.solutions.face_mesh
pyautogui.FAILSAFE = False
mp_face_mesh = mp.solutions.face_mesh
# left eyes indices
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 

sensitivity = 12
flag=1
# irises Indices list
LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

face_mesh= mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mouseOldX , mouseOldY = pyautogui.position()
leftEyeOldX,leftEyeOldY=0,0

def eye_module(cap):
    global leftEyeOldX
    global leftEyeOldY
    global mouseOldX 
    global mouseOldY
    global flag,img_h,img_w
    
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv.flip(frame, 1)

    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_h, img_w = rgb_frame.shape[:2]

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        

        #[print(p.x, p.y, p.z ) for p in results.multi_face_landmarks[0].landmark]
        
        mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) #normalize
        for p in results.multi_face_landmarks[0].landmark])
        
        mesh_points1=np.array([np.multiply([p.x, p.y,p.z], [img_w, img_h,img_w]).astype(int) 
        for p in results.multi_face_landmarks[0].landmark])
        
        
        # cv.polylines(rgb_frame, [mesh_points[LEFT_IRIS]], True, (0,255,0), 1, cv.LINE_AA)
        # cv.polylines(rgb_frame, [mesh_points[RIGHT_IRIS]], True, (0,255,0), 1, cv.LINE_AA)
        temp=mesh_points[LEFT_IRIS]
        
        
        (leftEyeX, leftEyeY), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
        
        (X,Y), l_eyebrow_r = cv.minEnclosingCircle(mesh_points[[65,68]])
        (u_lip_x,u_lip_y), u_lip_r = cv.minEnclosingCircle(mesh_points[[13]])
        (d_lip_x,d_lip_y), d_lip_r = cv.minEnclosingCircle(mesh_points[[14]])
        
        l_eye_lid_up_y=mesh_points1[159][1]
        l_eye_lid_down_y=mesh_points[145][1]-7
        
        r_eye_lid_up_y=mesh_points[386][1]
        r_eye_lid_down_y=mesh_points[374][1]
        
        #x1,y1=mesh_points1[145]
        
        if(not (leftEyeOldX == 0 and leftEyeOldY == 0)):
            mouseNewX = mouseOldX+sensitivity*(leftEyeX-leftEyeOldX)
            mouseNewY = mouseOldY+sensitivity*(leftEyeY-leftEyeOldY)
            
            cx,cy=(mouseNewX+mouseOldX)/2,(mouseNewY+mouseOldY)/2
            pyautogui.moveTo(mouseNewX,mouseNewY)
            
            mouseOldX = mouseNewX
            mouseOldY = mouseNewY
            
        leftEyeOldX = leftEyeX
        leftEyeOldY = leftEyeY
        
        center_left = np.array([leftEyeX, leftEyeY], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)
        
        eyebrow_left = np.array([X,Y], dtype=np.int32)
        up_lip=np.array([u_lip_x,u_lip_y], dtype=np.int32)
        down_lip=np.array([d_lip_x,d_lip_y], dtype=np.int32)
        
        ################drawing###############3
        cv.circle(rgb_frame, center_left, int(l_radius), (0,255,0), 2, cv.LINE_AA)
        cv.circle(rgb_frame, center_right, int(r_radius), (0,255,0), 2, cv.LINE_AA)
        
        cv.circle(rgb_frame, center_left, 1, (0,255,0), -1, cv.LINE_AA)
        cv.circle(rgb_frame, center_right, 1, (0,255,0), -1, cv.LINE_AA)
        cv.circle(rgb_frame, eyebrow_left, 3, (0,255,0), -1, cv.LINE_AA)
        cv.circle(rgb_frame, up_lip, 3, (0,255,155), -1, cv.LINE_AA)
        cv.circle(rgb_frame, down_lip, 3, (0,255,155), -1, cv.LINE_AA)
        
        ###########distances##############
        eye_eyebrow_dis=abs(center_left[1]-eyebrow_left[1])
        mouth_distance=down_lip[1]-up_lip[1]
        #print(abs(mesh_points1[5][2]))
        nose_distance=abs(mesh_points1[5][2]/4)
        eye_lid_distance=(mesh_points1[159][1]-mesh_points[145][1]-4)
        distance_ref=(nose_distance)*3
        #print("lip",mouth_distance)
        #distance for mouse click action as a reference
        r_eye_distance=r_eye_lid_down_y-r_eye_lid_up_y
        l_eye_distance=l_eye_lid_down_y-l_eye_lid_up_y
        ###########actions##########
        
        if((l_eye_lid_up_y>=l_eye_lid_down_y) and (r_eye_distance>5) and flag==0):
            mouse.click('left')
            flag=1
        if(l_eye_lid_up_y<l_eye_lid_down_y):
            flag=0
            
        print(r_eye_lid_up_y,r_eye_lid_down_y)
        if((r_eye_lid_up_y > r_eye_lid_down_y-6) and (l_eye_distance>3)and flag==0):
            mouse.click('right')
            flag=1
            
        if(r_eye_lid_up_y < r_eye_lid_down_y):
            flag=0
            
        if(eye_eyebrow_dis > distance_ref+4 and (mouth_distance>10)):
            
            print("scroll up")
            mouse.wheel(1)
            time.sleep(0.05)
            
        elif eye_eyebrow_dis>distance_ref+4 and mouth_distance<7:
            print("scroll down")
            mouse.wheel(-1)
            time.sleep(0.05)
            
    return rgb_frame        
      