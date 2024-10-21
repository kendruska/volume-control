import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)


def get_volume_control():
    """
    Retrieves the volume control object for the active audio session.

    Returns:
        volume (SimpleAudioVolume): The volume control object if found, otherwise None.
    """
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process:
            print(f"Session found: {session.Process.name()}")
        else:
            print("Unnamed session, but with volume control.")        

        if volume:
            return volume
    return None

volume_control = get_volume_control()

if not volume_control:
    print("No active volume control found.")
    exit()

def get_current_volume():
    """
    Gets the current master volume level.

    Returns:
        float: The current master volume level.
    """
    return volume_control.GetMasterVolume()

def set_volume(vol):
    """
    Sets the master volume to a specified level.

    Args:
        vol (float): The volume level to set (0.0 to 1.0).
    """
    volume_control.SetMasterVolume(vol, None)

def mute_volume(mute):
    """
    Mutes or unmutes the volume.

    Args:
        mute (bool): True to mute, False to unmute.
    """
    volume_control.SetMute(mute, None)

def fingers_are_together(landmark1, landmark2, threshold=0.05):
    """
    Checks if two fingers are together based on their landmarks.

    Args:
        landmark1 (Landmark): The first finger landmark.
        landmark2 (Landmark): The second finger landmark.
        threshold (float): The distance threshold to consider fingers together.

    Returns:
        bool: True if fingers are together, False otherwise.
    """
    distance = np.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)
    return distance < threshold

def fingers_are_separated(landmark1, landmark2, threshold=0.1):
    """
    Checks if two fingers are separated based on their landmarks.

    Args:
        landmark1 (Landmark): The first finger landmark.
        landmark2 (Landmark): The second finger landmark.
        threshold (float): The distance threshold to consider fingers separated.

    Returns:
        bool: True if fingers are separated, False otherwise.
    """
    distance = np.sqrt((landmark1.x - landmark2.x)**2 + (landmark1.y - landmark2.y)**2)
    return distance > threshold


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[4] 
            index_tip = landmarks[8]  
            middle_tip = landmarks[12]  
    
            if fingers_are_together(thumb_tip, index_tip):
                current_volume = get_current_volume()
                new_volume = max(0.0, current_volume - 0.05)
                set_volume(new_volume)
                cv2.putText(frame, "Lower Volume", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            elif fingers_are_separated(index_tip, middle_tip):
                current_volume = get_current_volume()
                new_volume = min(1.0, current_volume + 0.05) 
                set_volume(new_volume)
                cv2.putText(frame, "Raise Volume", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif fingers_are_together(index_tip, middle_tip):
                mute_volume(True)
                cv2.putText(frame, "Mute", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                mute_volume(False)
                cv2.putText(frame, "Unmute", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)


    cv2.imshow('Volume control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
