import sensor
import image
import lcd
import time
import math
from fpioa_manager import fm
from machine import UART

########_Variables_########
count = 0
b=[]
angle = 0
rad = 0
digits = []
read_data = 10
ccenter = 270
lcenter = 162

fm.register(28, fm.fpioa.UART1_TX)  #RED cable
fm.register(29, fm.fpioa.UART1_RX)  #BROWN Cable

uart_A = UART(UART.UART1, 230400,8,0,0, timeout=1000, read_buf_len=4096)

##########_Initialize_camera_and_screen_################
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_saturation(1)
sensor.run(1)
clock = time.clock()
green_threshold = (39, 83, -42, -19, -12, 16)
while True:
    clock.tick()
    img=sensor.snapshot()
    fps = clock.fps()

    #binary = img.binary([(25, 70), (-35, -9), (-14, 5)])
    #img=img.dilate(1,threshold = 1)

    ##########_Find_Green_blob_#########
    blobs = img.find_blobs([green_threshold],x_stride=15,y_stride=5,area_threshold=2000)
    if blobs:
        for b in blobs:
            tmp=img.draw_rectangle(b[0:4])
            tmp=img.draw_cross(b[0]+b[2]//2, b[1]+b[3]//2)
            #c=img.get_pixel(b[5], b[6])
            rad = math.atan2((lcenter-(b[0]+b[2]/2)),(ccenter-(b[1]+b[3]/2)))
            angle = math.degrees(rad)
    if rad == 0.0: #rad<0.015 and rad> -0.015:
        uart_A.write("0.00000000")
    else:
        uart_A.write(str(rad))

    #read_data = uart_A.readline()
    #if read_data:
    #    print(read_data.decode('utf-8'))

    #img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)

    img.draw_string(200,2, ("%2.2fdeg" %(angle)), color=(0,128,0), scale=2)
    img.draw_line(lcenter,0,lcenter,240)
    img.draw_circle(lcenter,ccenter,205)

    #lcd.display(img)

    #print(fps)
    #print(rad)

uart_A.deinit()

del uart_A
