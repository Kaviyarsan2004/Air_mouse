import os
from math import sqrt


def are_fingers_close(thumb, finger_1, finger_2, finger_3, finger_4):
    fingers = [thumb, finger_1, finger_2, finger_3, finger_4]
    max_distance = 250 # maximum distance to check closeness
    
    # Compare each finger with every other finger
    for i in range(len(fingers)):
        for j in range(i + 1, len(fingers)):
            # Calculate the Euclidean distance between fingers[i] and fingers[j]
            distance = ((fingers[i][0] - fingers[j][0]) ** 2 + (fingers[i][1] - fingers[j][1]) ** 2) ** 0.5
            # print("Distance : ", distance)
            if distance > max_distance:
                return False  # Return False if any two fingers are further apart than max_distance
    
    return True  # Return True if all fingers are within max_distance of each other


def detectAction(hand_landmarks, image_shape):
    """
    Detects the user's action (Erasing, Drawing, or Unknown) based on hand landmarks and image shape.
    """
   
    if isDrawing(hand_landmarks, image_shape):
        return "Click"
    if isPointing(hand_landmarks, image_shape):
        return "Point"
    if isScrollingUp(hand_landmarks,image_shape):
        return "ScrollUp"
    if isScrollingDown(hand_landmarks,image_shape):
        return "ScrollDown"
    return "unknown"

def calcDistance(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)

def quadrilateral_area(coords):
    """
    Calculate the area of a quadrilateral given its vertices.
    The vertices must be ordered either clockwise or counterclockwise.
    coords: A list of tuples, where each tuple represents the coordinates of a vertex (x, y).
            It's assumed that coords[0], coords[1], coords[2], coords[3] are the vertices.
    """
    # Divide the quadrilateral into two triangles: (0, 1, 2) and (2, 3, 0)
    triangle1 = triangle_area(*coords[0], *coords[1], *coords[2])
    triangle2 = triangle_area(*coords[2], *coords[3], *coords[0])
    
    # The total area of the quadrilateral is the sum of the areas of the two triangles
    return triangle1 + triangle2

def isDrawing(hand_landmarks, image_shape):
    """
    CLICKER
    """
    w = image_shape[1]  # Image width
    h = image_shape[0]  # Image height
    thumb_tip_x = hand_landmarks.landmark[4].x * w
    thumb_tip_y = hand_landmarks.landmark[4].y * h
    knuckle_x = hand_landmarks.landmark[9].x * w
    knuckle_y = hand_landmarks.landmark[9].y * h
    threshold = (1/16) * w  # Define the threshold for "very close"
    
    # Calculate the Euclidean distance between the thumb tip and the index tip
    distance = ((thumb_tip_x - knuckle_x) ** 2 + (thumb_tip_y - knuckle_y) ** 2) ** 0.5
    print("try:",distance,threshold)
    # if distance < threshold:
    return distance < threshold

def isPointing(hand_landmarks, image_shape):
    """
    move mouse 5,6,7,8 area < X
    """
    w = image_shape[1]  # Image width
    h = image_shape[0]  # Image height
    v1 = (hand_landmarks.landmark[5].x * w,hand_landmarks.landmark[5].y * h)
    v2 = (hand_landmarks.landmark[6].x * w,hand_landmarks.landmark[6].y * h)
    v3 = (hand_landmarks.landmark[7].x * w,hand_landmarks.landmark[7].y * h)
    v4 = (hand_landmarks.landmark[8].x * w,hand_landmarks.landmark[8].y * h)
    
    threshold = (2.5) * w  # Define the threshold for "very close"
    coords =[v1,v2,v3,v4]
    area = quadrilateral_area(coords)
    if area <= threshold:
        base_f3 = (hand_landmarks.landmark[9].x * w,hand_landmarks.landmark[9].y * h)
        base_f4 = (hand_landmarks.landmark[13].x * w,hand_landmarks.landmark[13].y * h)
        base_f5 = (hand_landmarks.landmark[17].x * w,hand_landmarks.landmark[17].y * h)
        
        base_p3 = (hand_landmarks.landmark[12].x * w,hand_landmarks.landmark[12].y * h)
        base_p4 = (hand_landmarks.landmark[16].x * w,hand_landmarks.landmark[16].y * h)
        base_p5 = (hand_landmarks.landmark[20].x * w,hand_landmarks.landmark[20].y * h)

        palm =(hand_landmarks.landmark[0].x * w,hand_landmarks.landmark[0].y * h)
        
        distance1_3 = ((base_f3[0] - palm[0]) ** 2 + (base_f3[1] - palm[1]) ** 2) ** 0.5
        distance1_4 = ((base_f4[0] - palm[0]) ** 2 + (base_f4[1] - palm[1]) ** 2) ** 0.5
        distance1_5 = ((base_f5[0] - palm[0]) ** 2 + (base_f5[1] - palm[1]) ** 2) ** 0.5
        
        distance2_3 = ((base_p3[0] - palm[0]) ** 2 + (base_p3[1] - palm[1]) ** 2) ** 0.5
        distance2_4 = ((base_p4[0] - palm[0]) ** 2 + (base_p4[1] - palm[1]) ** 2) ** 0.5
        distance2_5 = ((base_p5[0] - palm[0]) ** 2 + (base_p5[1] - palm[1]) ** 2) ** 0.5
        if (distance2_3 < distance1_3 and distance2_4 < distance1_4 and distance2_5 < distance1_5):
            return True
        else:
            return False
def isScrollingUp(hand_landmarks, image_shape):
    """
    move mouse 5,6,7,8 area < X
    """
    w = image_shape[1]  # Image width
    h = image_shape[0]  # Image height
    v1 = (hand_landmarks.landmark[4].x * w,hand_landmarks.landmark[4].y * h)
    v2 = (hand_landmarks.landmark[20].x * w,hand_landmarks.landmark[20].y * h)
    
    return (v1[0]>v2[0])

def isScrollingDown(hand_landmarks, image_shape):
    """
    move mouse 5,6,7,8 area < X
    """
    w = image_shape[1]  # Image width
    h = image_shape[0]  # Image height
    v1 = (hand_landmarks.landmark[4].x * w,hand_landmarks.landmark[4].y * h)
    v2 = (hand_landmarks.landmark[20].x * w,hand_landmarks.landmark[20].y * h)
    
    return (v1[0]<v2[0])