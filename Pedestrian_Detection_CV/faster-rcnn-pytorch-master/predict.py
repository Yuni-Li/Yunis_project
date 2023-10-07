
import time
import os

import cv2
import numpy as np
from PIL import Image

from frcnn import FRCNN

if __name__ == "__main__":
    #load the faster-rcnn model
    frcnn = FRCNN()
    
    #There are 3 modes for this program to detect the pedestrian:
    #mode 1: single_image          input the path of single image and do the pedestrian detection for image
    #mode 2: traverse_image        input the path of folder and the program will execute pedestrain detection for all the images in this folder
    #mode 3: video              input the path of video and do the pedestrian detection for video
    
    mode_list = ['single_image','traverse_image','video']
    mode = input('Please input the mode for pedestrian detection: ')
    
    if mode not in mode_list:
        print('wrong mode, please try again!')
    

    if mode == "single_image":
        
        while True:
            img = input('Please input the image path: ')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = frcnn.detect_image(image, crop = crop, count = count)
                r_image.show()

    elif mode == "video":
        
        video_path = input('Please input the video path: ')
        video_save_path = input('Please input the folder name you want to save the video (ending by /): ')
        video_fps = 25.0
        
        capture=cv2.VideoCapture(video_path)
        if video_save_path!="":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

        fps = 0.0
        while(True):
            t1 = time.time()
            # read frame
            ref,frame=capture.read()
            # convert BGRtoRGB
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # convert to image
            frame = Image.fromarray(np.uint8(frame))
            # detection process
            frame = np.array(frcnn.detect_image(frame))
            # convert RGBtoBGR to opencv format
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            
            fps  = ( fps + (1./(time.time()-t1)) ) / 2
            print("fps= %.2f"%(fps))
            frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("video",frame)
            c= cv2.waitKey(1) & 0xff 
            if video_save_path!="":
                out.write(frame)

            if c==27:
                capture.release()
                break
        capture.release()
        out.release()
        cv2.destroyAllWindows()

    
    elif mode == "traverse_image":
        
        from tqdm import tqdm
        dir_origin_path = input('Please input the folder name you want to travserse (ending by /): ')
        dir_save_path = input('Please input the folder name you want to save the results (ending by /): ')

        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = Image.open(image_path)
                r_image     = frcnn.detect_image(image)
                r_image.show()
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name.replace(".jpg", ".png")), quality=95, subsampling=0)

    