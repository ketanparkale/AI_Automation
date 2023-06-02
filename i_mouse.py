import pyautogui
import tkinter as tk
import eye_mod
import hand_mod
import cv2
from PIL import Image, ImageTk

temp=True
def eye_call():
    global temp
    temp=True
   
def hand_call():
    global temp
    temp=False


cap = cv2.VideoCapture(0)
eye_flag=False
hand_flag=True
window = tk.Tk()
window.title("OpenCV Frame Display")

# Create a label widget to display the frame
label = tk.Label(window)
label.pack()
bt_eye=tk.Button(window, text="Hand Module",activebackground='red',width=30,bd='10',command=eye_call)
bt_eye.pack(ipady = 10)

bt_hand=tk.Button(window ,text="Eye Module",activebackground='red',width=30,fg='black',bd='10',command=hand_call)
bt_hand.pack( ipady = 10)


def close_win(e):
   window.destroy()

def display_frame(frames):
    # Convert the OpenCV frame to PIL format
    image = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image)

    # Create a Tkinter-compatible photo image
    photo = ImageTk.PhotoImage(image_pil)
    
    # Update the label with the new image
    label.configure(image=photo)
    label.image = photo



def update_frame():
    
    if(temp):
        images=hand_mod.hand_module(cap)
        display_frame(images)
               
    else:
        frame=eye_mod.eye_module(cap)
        display_frame(frame)
                
               
    # cv.imshow('Mask', mask)     
    # cv.imshow('img', frame)    
    window.after(1,update_frame)
    
window.bind('<Escape>',lambda e: close_win(e))

update_frame()
window.mainloop()
cap.release()
cv2.destroyAllWindows()