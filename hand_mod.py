import handtracking as ht
import cv2
import numpy as np
import time
import autopy
import mouse
import pyautogui as pi


#######################################
wCam=500
hCam=500
wScr, hScr = autopy.screen.size()
framer = 200 # frame reduction
smoothening = 10
prevX, prevY = 0, 0
curX, curY = 0, 0
key=0
# to calculate frame rate
prevtime = 0
currtime = 0
screenshot_key=1
count=1
str_count=""
########################################
# read video stream

detector = ht.HandTracker()

def hand_module(cap):
    global prevtime,currtime
    global prevX,prevY
    global key,screenshot_key,count,str_count
#while(True):
    cap.set(3, wCam)
    cap.set(4, hCam)
    # extract image from video
    success, image = cap.read()

    imageRGB = detector.find_hands(image)  
    # print(detector.find_position(imageRGB))

    landmarks = detector.find_position(imageRGB)

    
        # to do something
    if(len(landmarks) != 0):
        x1, y1 = landmarks[8][1:]
        
        # x2, y2 = landmarks[12][1:]

        fingers = detector.fingers_up()
        # need to create a range to detect, instead of working on entire image
        cv2.rectangle(imageRGB, (framer, framer), (wCam-framer, hCam-framer), 
                                        (255, 0, 0), 3)


        
        # move cursor
        if(fingers[1] == 1 or fingers[0]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):

            x3 = np.interp(x1, (framer, wCam-framer), (0, wScr))      
            y3 = np.interp(y1, (framer, hCam-framer), (0, hScr))      
            

            # smoothen value a bit
            curX = prevX + (x3 - prevX) / smoothening
            curY = prevY + (y3 - prevY) / smoothening
            
            if (fingers[1]==1 and fingers[0]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
                autopy.mouse.move(wScr-curX, curY)

                
            cv2.circle(imageRGB,(x1, y1), 15, (255, 0, 255), cv2.FILLED)
            prevX, prevY = curX, curY

        
            
        if (fingers[1]==1 and fingers[2]==1 and fingers[0]==1 and fingers[3]==0 and fingers[4]==0):
            
            lenght1, img, lineinfo = detector.find_distance(8, 12, imageRGB)
            length2, img, lineinfo = detector.find_distance(8, 4, imageRGB)
        # click action
            if(lenght1 >30 and length2 >30):
                key=1
                
            if(key):
            # right click
            # index or middle fingre
                if(lenght1 < 40):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    time.sleep(0.70)
                    mouse.click('right')
                    print('right click')
                
                # left click
                # index or thumb
                if (length2 < 50):
                    cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0,255,0), cv2.FILLED)
                    # autopy.mouse.click()
                    mouse.click('left')
                    time.sleep(0.65)
                    print("left click")
                key=0    
        if (fingers[1]==1 and fingers[2]==1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0):
            lenght3, img, lineinfo = detector.find_distance(8, 12, imageRGB)
            if(lenght3 < 30):
                
                mouse.wheel(-1)
                time.sleep(0.05)
            else:
                mouse.wheel(1)
                time.sleep(0.05)       
        
        if(screenshot_key):
            if (fingers[1]==1 and fingers[2]==0 and fingers[0]==1 and fingers[3]==0 and fingers[4]==1):
                pi.screenshot(r"G:\screen_shot\screenshot"+str_count+".png")
                screenshot_key=0
                print("screenshot")
                count=count+1
                str_count=str(count)
                
        if fingers[4]==0:
            screenshot_key=1
    #cv2.imshow("image", imageRGB)
    # cv2.imshow("image", imageRGB)
    # press escape key to quit
    
    
    # if(cv2.waitKey(1) == 27):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     return
    
    return imageRGB

