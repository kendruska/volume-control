# Volume Control with Hand Gestures

This project allows you to control the volume of your computer using hand gestures detected through your webcam. It uses OpenCV for video capture, MediaPipe for hand tracking, and Pycaw for audio control.

## Features

- **Lower Volume**: Touch your thumb and index finger together.
- **Raise Volume**: Separate your index and middle fingers.
- **Mute**: Touch your index and middle fingers together.
- **Unmute**: Ensure no fingers are touching.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- Numpy
- Pycaw

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kendruska/volume-control.git
    cd volume-control
    ```

2. Install the required packages:
    ```sh
    pip install opencv-python mediapipe numpy pycaw
    ```

## Usage

1. Run the script:
    ```sh
    python volume_control.py
    ```

2. Use the specified hand gestures to control the volume.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [Pycaw](https://github.com/AndreMiras/pycaw)
