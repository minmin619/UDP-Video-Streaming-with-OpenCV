#server to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
Server_Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
Server_Socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
Host_Name = socket.gethostname()
Host_IP = "127.0.0.1"
print(Host_IP)
port = 9999
Socket_Address = (Host_IP,port)
Server_Socket.bind(Socket_Address)
print('Listening at:',Socket_Address)

#  replace 'XXX.mp4' with 0 for webcam
video = cv2.VideoCapture(0) 

while True:
	message,Client_Addr = Server_Socket.recvfrom(BUFF_SIZE)
	print('GOT connection from ',Client_Addr)
	WIDTH=400


	#開始傳自拍
	while(video.isOpened()):
	
		ret,frame = video.read()

		frame = imutils.resize(frame,width=WIDTH)

		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])

		message = base64.b64encode(buffer)

		Server_Socket.sendto(message,Client_Addr)		  	
    	
		X_ray_image = cv2.bitwise_not(frame)
    	   	
		resized_x_ray = cv2.resize(X_ray_image, (350,350))   			
    	
		cv2.imshow('Server original video',frame)

		cv2.imshow('Server video with filter X Ray', resized_x_ray)

		key = cv2.waitKey(1) & 0xFF
		
		
		
