import cv2, time

from numpy import full

video = cv2.VideoCapture(0)

first_frame = None

noise_threshold = 50
detected_area_size = 1000

# (0, 0) cords are at the left top
# (x1, y1, x2, y2) 
# in crop ratio put values in 0-1 scale
crop_ratio = (0.1, 0.4, 0.9, 0.6)

while True:
    check, frame = video.read()
    cut = (
        int(crop_ratio[0]*frame.shape[1]), 
        int(crop_ratio[1]*frame.shape[0]), 
        int(crop_ratio[2]*frame.shape[1]),
        int(crop_ratio[3]*frame.shape[0]))
    full_img = frame

    frame = frame[cut[1]:cut[3], cut[0]:cut[2]]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    if first_frame is None:
        first_frame = gray
        print(full_img.shape)
        continue
    delta_frame = cv2.absdiff(first_frame, gray)
    # (delta_frame, density, color)
    threshold_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    # iteration = (bigger values catches more noises)
    threshold_frame = cv2.dilate(threshold_frame, None, iterations = 2)

    (cntr,_) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cntr:
        # if area of movement is too small ignore it
        if cv2.contourArea(contour) < detected_area_size:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
    
    cv2.rectangle(full_img, (cut[0], cut[1]), (cut[2], cut[3]), (0, 0, 255), 3)
    cv2.putText(img=full_img, text='Press q to exit', org=(5, 25), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 20, 100),thickness=3)

    cv2.imshow("window name - press 'q' to exit", full_img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()