# client to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
Client_Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
Client_Socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
Host_Name = socket.gethostname()
Host_Ip = "127.0.0.1"
print("Host IP is ",Host_Ip)
port = 9999

#前面加b可以把str變成byte
message = b'Hello'

Client_Socket.sendto(message,(Host_Ip,port))

img_counter = 0
while True:

	packet,_ = Client_Socket.recvfrom(BUFF_SIZE)

	data = base64.b64decode(packet,' /')

	npdata = np.frombuffer(data,dtype=np.uint8)

	frame = cv2.imdecode(npdata,1)	

	X_ray_image = cv2.bitwise_not(frame)


	cv2.imshow("Receive the streaming by the Server.",frame)  
		
	cv2.imshow('Client video with filter X Ray', X_ray_image)	

	key = cv2.waitKey(1) & 0xFF
	
	#Press space to Screenshot function video with filter.
	if key %256  == 32:

        # the format for storing the images scrreenshot
		img_name = f'opencv_frame_{img_counter}'

        # saves the image as a png file
		name = './img_name_' + str(img_counter) + '.png'
		cv2.imwrite(name, X_ray_image)
		
        # the number of images automaticallly increases by 1
		img_counter += 1
	
