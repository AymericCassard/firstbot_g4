import cv2
import numpy as np

# --- paramètres échiquier ---
# nombre de coins intérieurs par ligne et colonne
chessboard_size = (7, 6)  # ex. 7 x 6 coins détectables
square_size = 25  # taille d'une case (mm ou arbitraire)

# préparation des points 3D de l’échiquier (z=0)
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0],
                       0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

objpoints = []  # points 3D
imgpoints = []  # points 2D

# --- liste des images d’échiquier ---
images = ["images_test/image"+str(i)+".jpg" for i in range(1, 210)]

# --- boucle sur tes images ---
for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print("Impossible de lire :", fname)
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # recherche des coins
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )
        imgpoints.append(corners2)

        # affichage pour vérification
        cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
        cv2.imshow("Chessboard", img)
        cv2.waitKey(200)
    else:
        print("Echec détection sur :", fname)

cv2.destroyAllWindows()

# --- calibration ---
if len(objpoints) > 0:
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    print("Matrice caméra :\n", camera_matrix)
    print("Coeffs distorsion :\n", dist_coeffs)

    # sauvegarde
    np.savez("calibration_data.npz", camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)

    # test correction sur une image
    img = cv2.imread(images[0])
    h, w = img.shape[:2]
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

    cv2.imshow("Original", img)
    cv2.imshow("Rectified", undistorted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Pas assez d'images valides pour calibrer.")
