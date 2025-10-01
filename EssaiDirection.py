import time

dxl1 = 1  # roue gauche
dxl2 = 2  # roue droite

base_speed = 360  # vitesse max quand tout droit

color= [-20, 0, 40]
while ()

# Intensité du virage entre 0 et 1
    intensity = abs(value) / 50  

    if value < 0:  # tourne à gauche
        left_speed = base_speed * (1 - intensity)
        right_speed = base_speed
    elif value > 0:  # tourne à droite
        left_speed = base_speed
        right_speed = base_speed * (1 - intensity)
    else:  # tout droit
        left_speed = right_speed = base_speed

    return left_speed, right_speed

for v in color:
    left_speed, right_speed = compute_turn(v, base_speed)

# Durée (en secondes) pour chaque valeur
step_time = 2  

dxl_io.set_moving_speed({dxl1: left_speed})
dxl_io.set_moving_speed({dxl2: right_speed})

time.sleep(step_time)  # attendre avant de passer à la suivante