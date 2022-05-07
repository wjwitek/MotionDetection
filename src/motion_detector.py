import cv2
import multiprocessing


def image_resize(width, original):
    org_shape = original.shape
    div = org_shape[1] // width
    return cv2.resize(original, (original.shape[1] // div, original.shape[0] // div))


class MotionDetector:
    def __init__(self, source=0, mask=(0.1, 0.1, 0.9, 0.7), noise_threshold=10000000, detected_area_size=1000, debug=False):
        self.source = source
        self.noise_threshold = noise_threshold
        self.detected_area_size = detected_area_size
        self.debug = debug
        self.mask = mask
        self.stream = None
        self.first_frame = None
        self.proc = None

    def stop(self):
        self.stream.release()
        cv2.destroyAllWindows()

    def main_loop(self):
        # start capturing video stream
        self.stream = cv2.VideoCapture(self.source)
        while True:
            # read from stream
            check, frame = self.stream.read()

            if self.debug:
                frame = image_resize(500, frame)

            # set points of area where movement is detected
            cut = (
                int(self.mask[0] * frame.shape[1]),
                int(self.mask[1] * frame.shape[0]),
                int(self.mask[2] * frame.shape[1]),
                int(self.mask[3] * frame.shape[0]))

            full_img = frame

            # cut image to leave only part where movement is detected
            frame = frame[cut[1]:cut[3], cut[0]:cut[2]]

            # transform image to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # add blur
            blur = cv2.GaussianBlur(gray, (21, 21), 0)

            # set reference frame
            if self.first_frame is None:
                self.first_frame = blur
                continue

            # calculate difference between reference frame and current frame
            delta_frame = cv2.absdiff(self.first_frame, blur)

            # set pixels with value lower than threshold to 0
            threshold_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]

            # dilate image,  iteration = (bigger values catches more noises)
            threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

            # find contours of moving objects
            (cntr, _) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # check = 0 for no movement detected
            check = 0

            # draw rectangles for areas of movement bigger than detected_area_size
            for contour in cntr:
                if cv2.contourArea(contour) < self.detected_area_size:
                    continue
                check = 1
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # draw rectangle showing mask where program looks for movement
            cv2.rectangle(full_img, (cut[0], cut[1]), (cut[2], cut[3]), (0, 255 * check, 255), 3)
            cv2.putText(img=full_img, text='Press q to exit', org=(5, 25), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1, color=(100, 255, 100), thickness=3)

            # draw images, depending on mode
            if not self.debug:
                cv2.imshow("window name - press 'q' to exit", full_img)
            else:
                # gray image
                cv2.imshow("Gray image", gray)
                cv2.moveWindow("Gray image", 0, 0)
                # blured image
                cv2.imshow("Blurred image", blur)
                cv2.moveWindow("Blurred image", 0, 300)
                # delta frame
                cv2.imshow("Delta frame", delta_frame)
                cv2.moveWindow("Delta frame", 0, 570)
                # threshold frame
                cv2.imshow("Threshold frame", threshold_frame)
                cv2.moveWindow("Threshold frame", 600, 0)
                # main image
                cv2.imshow("Image detection", full_img)
                cv2.moveWindow("Image detection", 600, 300)
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.stop()
                break

    def start(self):
        # start main loop
        self.proc = multiprocessing.Process(target=self.main_loop)
        self.proc.start()
        while True and self.proc.is_alive():
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.proc.terminate()
                break

    def restart(self):
        self.proc.terminate()
        self.start()

    def change_mode(self, debug=True):
        self.debug = debug
        self.restart()

    def change_mask(self, new_mask):
        self.mask = new_mask
        self.restart()

    def change_sensitivity(self, new_sensitivity):
        self.noise_threshold = new_sensitivity
        self.restart()

    def change_source(self, new_source):
        self.source = new_source
        self.restart()


# if __name__ == "__main__":
#     test = MotionDetector()
#     test.start()

