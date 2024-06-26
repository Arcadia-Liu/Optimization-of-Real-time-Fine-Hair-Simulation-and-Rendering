import cv2
import socket

def Facedetection():
    host = '127.0.0.1'
    port = 6000
    addr = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    face_cascade = cv2.CascadeClassifier(".\Hxml\haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier('.\Hxml\haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('.\Hxml\haarcascade_smile.xml')
    # 调用摄像头摄像头
    cap = cv2.VideoCapture(0)
    while (True):
        # 获取摄像头拍摄到的画面
        ret, frame = cap.read()
        faces = face_cascade.detectMultiScale(frame, 1.3, 2)
        img = frame
        for (x, y, w, h) in faces:
            # 画出人脸框，蓝色
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
            face_area = img[y:y + h, x:x + w]

            ## 人眼检测
            # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
            eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
            for (ex, ey, ew, eh) in eyes:
                # 画出人眼框，绿色，画笔宽度为1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
            ## 微笑检测
            smiles = smile_cascade.detectMultiScale(face_area, scaleFactor=1.16, minNeighbors=65, minSize=(25, 25),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)
            for (ex, ey, ew, eh) in smiles:
                # 画出微笑框，红色（BGR色彩体系），画笔宽度为1
                cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
                cv2.putText(img, 'Smile', (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                sock.sendto('smile'.encode('utf-8'), addr)
                if (ex>0 and ey>0 and ew>0 and eh>0):
                    ret, frame = cap.read()
                    if ret:
                        cv2.imshow("capture", frame)
                        file_name = "picture.jpeg"
                        cv2.imwrite(file_name, frame)
                        break
                break
        # 实时展示效果画面
        cv2.imshow('frame2', img)


        # 每5毫秒监听一次键盘动作
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    # 最后，关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Facedetection()




