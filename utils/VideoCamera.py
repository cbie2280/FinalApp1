import cv2

from utils.RecordingThread import RecordingThread


class VideoCamera(object):
    def __init__(self):


        # Open a camera
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None

    def __del__(self):
        self.cap.release()
        self.out.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            if self.is_record:
                if self.out == None:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    print("just once")
                    self.out = cv2.VideoWriter('./static/video1.avi', fourcc, 20.0, (640, 480))

                ret, frame = self.cap.read()
                if ret:
                    self.out.write(frame)
            else:
                if self.out != None:
                    self.out.release()
                    self.out = None

            return jpeg.tobytes()

        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        cv2.destroyAllWindows()
        if self.recordingThread != None:
            self.recordingThread.stop()
