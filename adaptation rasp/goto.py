import time
import pypot.dynamixel
import dynamics
import numpy as np
#import cv2 as cv2
import math
import dynamics
import sys



ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

dxl1=1
dxl2=2

x_robot = 0
y_robot = 0
theta_robot = 0


def goto_egocentrique(xr,yr,temps_deplacement): #([m], [m], [s])

    global theta_robot

    l=0.135
    R_roue = 0.02575

    Vxr,Vyr = xr/temps_deplacement,yr/temps_deplacement

    Vtheta = 0
    Vp = 0

    if(Vxr==0):
        Va=0 #a modifier
        Vb=0 #a modifier
        print("cas particulier pas encore traité")
    elif(Vyr==0):
        Va = Vxr
        Vb = Vxr
    else:
        dtheta=2*math.atan2(Vyr,Vxr) #[rad]
        Vtheta=dtheta/temps_deplacement #[rad/s]
        dp = (xr*dtheta)/math.sin(dtheta) #[m]
        Vp=dp/temps_deplacement #[m/s]

        dA = dp + dtheta * l/2 #[m]
        Va=dA/temps_deplacement #[m/s]

        dB = dp - dtheta * l/2 #[m]
        Vb=dB/temps_deplacement #[m/s]


    dA_rad = dA/R_roue #[rad]
    dB_rad = dB/R_roue #[rad]

    dA_deg = -dA_rad*180/np.pi #[deg]
    dB_deg = dB_rad*180/np.pi #[deg]

    dxl_io.set_moving_speed({dxl1: dA_deg/temps_deplacement})
    dxl_io.set_moving_speed({dxl2: dB_deg/temps_deplacement})
    # time.sleep(temps_deplacement)
    # dxl_io.set_moving_speed({dxl1: 0})
    # dxl_io.set_moving_speed({dxl2: 0})

    theta_robot += dtheta



def goto_absolu(x0, y0, theta0, x1, y1, temps_deplacement): #([m], [m], [deg], [m], [m], [s])

    #theta0 = thetadeg0*np.pi/180

    sintheta = math.sin(theta0)
    costheta = math.cos(theta0)
    tantheta = math.tan(theta0)

    # yr=(y1-y0-(x1-x0)*tantheta)/(sintheta*tantheta+costheta)
    # xr=(x1-x0+yr*sintheta)/costheta

    xr = costheta*(x1-x0)+sintheta*(y1-y0)
    yr = -sintheta*(x1-x0)+costheta*(y1-y0)

    goto_egocentrique(xr,yr,temps_deplacement)



def bezier_curve(control_points, n_points=100):
    """
    Génère une liste de coordonnées correspondant à une courbe de Bézier.

    control_points : liste de tuples ou de listes [(x0,y0), (x1,y1), ...]
    n_points : nombre de points calculés le long de la courbe

    Retour : liste de tuples [(x,y), ...]
    """
    P = np.asarray(control_points, dtype=float)
    m, dim = P.shape
    n = m - 1
    t = np.linspace(0, 1, n_points)

    # Calcul des coefficients de Bernstein
    coeffs = np.zeros((n_points, m))
    for i in range(m):
        coeffs[:, i] = math.comb(n, i) * (t**i) * ((1 - t)**(n - i))

    # Combinaison linéaire
    curve = coeffs @ P

    # Conversion en liste de tuples
    return [tuple(pt) for pt in curve]



#goto_egocentrique(0.2,0.2, 5)
#goto_absolu(1, 1, 45, 2, 2, 5)

def goto_bezier_no_audom(x0,y0, x1,y1, x2,y2, x3,y3, temps_deplacement=1):

    #ctrl = [(0, 0), (1, 0), (0.75, 0.98), (0.5, 0.5)]
    ctrl = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
    traj = bezier_curve(ctrl, n_points=10)

    #temps_deplacement = 1
    last_time = time.time()

    for k in range(len(traj)-1):

        diff_time = time.time() - last_time
        while diff_time < temps_deplacement:  # Capture every temps_deplacement seconds
            diff_time = time.time() - last_time

        last_time = time.time()

        dxl_io.set_moving_speed({dxl1: 0})
        dxl_io.set_moving_speed({dxl2: 0})

        #print(traj[k][0], traj[k][1], theta_robot, traj[k+1][0], traj[k+1][1])
        goto_absolu(traj[k][0], traj[k][1], theta_robot, traj[k+1][0], traj[k+1][1], temps_deplacement)

    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

def goto_bezier_audom():

    f = open("positions_goto.txt", "w+")

    temps_deplacement = 1
    last_time = time.time()
    last_time_odom = time.time()

    x_odom=0
    y_odom=0
    theta_odom=-np.pi/2

    for k in range(len(traj)-1):
    #for k in range(1):

        diff_time = time.time() - last_time
        while diff_time < temps_deplacement:  # Capture every temps_deplacement seconds
            diff_time = time.time() - last_time

            diff_time_odom = time.time() - last_time_odom
            if diff_time_odom > 0.1:  # Capture every 0.1 seconds
                last_time_odom = time.time()
                x_odom, y_odom, theta_odom = dynamics.detect_path(f, "g", diff_time_odom, x_odom, y_odom, theta_odom, dxl_io, dxl1, dxl2)


        last_time = time.time()

        dxl_io.set_moving_speed({dxl1: 0})
        dxl_io.set_moving_speed({dxl2: 0})

        print(" x_odom = ", y_odom," y_odom = ", -x_odom," theta_odom = ", np.pi/2 + theta_odom," theta_robot = ", theta_robot ," traj[k+1][0] = ", traj[k+1][0]," traj[k+1][1] = ", traj[k+1][1])
        goto_absolu(x_odom, y_odom, np.pi/2 + theta_odom, traj[k+1][0], traj[k+1][1], temps_deplacement)

    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

    f.close()



# goto_absolu(0, 0, 0, 0.5, 0.5, 5)
# print("fin courbe", theta_robot*180/np.pi)
# goto_absolu(0.5, 0.5, theta_robot, 1, 1, 5)
# print("fin courbe", theta_robot*180/np.pi)
# goto_absolu(1, 1, theta_robot, 1.1, 0.01, 5)
# print("fin courbe", theta_robot*180/np.pi)
# goto_absolu(1.1, 0.01, theta_robot, 0.01, 0.01, 5)
# print("fin courbe", theta_robot*180/np.pi)

print("Pret")

dxl_io.set_moving_speed({dxl1: 0})
dxl_io.set_moving_speed({dxl2: 0})

if len(sys.argv) < 2:
    print("Usage: python3 mon_script.py <argument>")
    sys.exit(1)

argument = sys.argv[1]
if argument == "arc_cercle":
    entree = input("Entrée (x, y, temps de deplacement) : ")
    liste_entree = entree.split(",")
    liste_entree = [float(ent) for ent in liste_entree]
    print(liste_entree)

    goto_egocentrique(liste_entree[0],liste_entree[1],liste_entree[2])
    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

if argument == "goto_absolu":
    entree = input("Entrée (x0, y0, theta0, x1, y1, temps de deplacement) : ")
    liste_entree = entree.split(",")
    liste_entree = [float(ent) for ent in liste_entree]
    print(liste_entree)

    goto_absolu(liste_entree[0], liste_entree[1], liste_entree[2], liste_entree[3], liste_entree[4], liste_entree[5])
    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

if argument == "bezier_no_odom":
    entree = input("Entrée (x0,y0, x1,y1, x2,y2, x3,y3, temps_deplacement): ")
    liste_entree = entree.split(",")
    liste_entree = [float(ent) for ent in liste_entree]
    print(liste_entree)

    goto_bezier_no_audom(liste_entree[0], liste_entree[1], liste_entree[2], liste_entree[3], liste_entree[4], liste_entree[5], liste_entree[6], liste_entree[7], liste_entree[8])
    dxl_io.set_moving_speed({dxl1: 0})
    dxl_io.set_moving_speed({dxl2: 0})

