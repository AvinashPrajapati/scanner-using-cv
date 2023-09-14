import cv2
from pyzbar import pyzbar
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from pyzbar.pyzbar import decode, ZBarSymbol
import time




def getFrame(*args, **kwargs):
    MainWindowObj = args[0]
    running = True
    success, _ = MainWindowObj.video.read()
    if not success:
        MainWindowObj.start.setDisabled(True)
        MainWindowObj.video = cv2.VideoCapture(0)

        MainWindowObj.start.setText("started")

    MainWindowObj.start.setText("started")
    MainWindowObj.start.setDisabled(True)

    MainWindowObj.stop.setText("STOP CAM")
    MainWindowObj.stop.setDisabled(False)
    while running:
        cv2.waitKey(0)
        success, frame = MainWindowObj.video.read()  #-> true
        if success:
            # time.sleep(3)
            # print("exc 2")
            pass
        else:
            # print('exc 3')
            running = False
            return
        if success:
            Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FlippedImage = cv2.flip(Image, 1)

            # process image
            for code in decode(FlippedImage, symbols=[ZBarSymbol.QRCODE]):
                data = code.data.decode("utf-8")
                pts = np.array([code.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                pts2 = code.rect
                if data is None:
                    cv2.putText(
                        FlippedImage,
                        "Invalid !",
                        (pts2[0], pts2[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2,
                    )
                cv2.polylines(FlippedImage, [pts], True, (110, 252, 88), 5)
                
                print(data)
                # MainWindowObj.plainTextEdit.setPlainText(str(data))
                # QrData = tuple(mydata.split("+"))
                # print(QrData)
                # DataSize = len(QrData)

            #  Convert cv image in Qt image data
            ConvertToQtFormat = QImage(
                FlippedImage.data,
                FlippedImage.shape[1],
                FlippedImage.shape[0],
                QImage.Format_RGB888,
            )
            Pic = ConvertToQtFormat.scaled(480, 420)
            
            MainWindowObj.FeedLabel.setPixmap(QPixmap.fromImage(Pic))
    return


def stop(*args, **kwargs):
    MainWindowObj = args[0]
    checkValue2 = MainWindowObj.stop.text()
    started = MainWindowObj.start.text()
    if started == 'START CAM':
        return
    if checkValue2 == 'STOP CAM':

        MainWindowObj.start.setDisabled(False)
        MainWindowObj.start.setText('START CAM')

        MainWindowObj.stop.setText("stopped")
        MainWindowObj.stop.setDisabled(True)
        MainWindowObj.video.release()

        
        # video = None