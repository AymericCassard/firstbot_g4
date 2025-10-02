import time
import pypot.dynamixel
import dynamics
import numpy as np
#import cv2 as cv2
import math

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

dxl1=1
dxl2=2

def goto_egocentrique(xr,yr,temps_deplacement): #([m], [m], [s])

    l=0.135
    R_roue = 0.02575

    Vxr,Vyr = xr,yr
    print(Vxr, Vyr)

    if(Vxr==0):
        Va=0 #a modifier
        Vb=0 #a modifier
        print("cas particulier pas encore traité")
    elif(Vyr==0):
        Va = Vxr
        Vb = Vxr
    else:
        Vtheta=2*math.atan2(Vyr,Vxr)
        Vp=(Vxr*Vtheta)/math.sin(Vtheta)
        print(Vtheta,Vp)

        Va=Vp+Vtheta*l/2 #[m/s]
        Vb=Vp-Vtheta*l/2 #[m/s]
        print(Va,Vb)


    Va_rad = Va/R_roue #[rad/s]
    Vb_rad = Vb/R_roue #[rad/s]

    Va_deg = -Va_rad*180/np.pi #[deg/s]
    Vb_deg = Vb_rad*180/np.pi #[deg/s]

    dxl_io.set_moving_speed({dxl1: Va_deg/temps_deplacement})
    dxl_io.set_moving_speed({dxl2: Vb_deg/temps_deplacement})
    time.sleep(temps_deplacement)
    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

def goto_absolu(x0, y0, thetadeg0, x1, y1, temps_deplacement): #([m], [m], [deg], [m], [m], [s])

    theta0 = thetadeg0*np.pi/180

    sintheta = math.sin(theta0)
    costheta = math.cos(theta0)
    tantheta = math.tan(theta0)

    yr=(y1-y0-(x1-x0)*tantheta)/(sintheta*tantheta+costheta)
    xr=(x1-x0+yr*sintheta)/costheta

    goto_egocentrique(xr,yr,temps_deplacement)

goto_egocentrique(0.2,0.2, 5)
#goto_absolu(1, 1, 45, 2, 2, 5)
print("fin1")

dxl_io.set_moving_speed({dxl1: 0})
dxl_io.set_moving_speed({dxl2: 0})