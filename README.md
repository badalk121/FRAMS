## Face Recognition Attendance Management System - FRAMS

FRAMS is a face recognition and attendance management system. It allows you to train a face recognition model using images of known individuals and then use the model to recognize and track faces in real-time video.


## Prerequisites

Before running the code, make sure you have the following installed:

- Python 3.x
- OpenCV
- NumPy
- pandas
- PIL
- tkinter

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/badalk121/FRAMS.git
   ```

2. Install the required packages:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Open the project in VS Code:

   ```shell
   code .
   ```

2. Run the `train.py` script to run the application:

   ```shell
   python train.py
   ```

3. The above script will open a windows within which the application will run. You need to enter an ID and a name for each person whose face you want to train. It will then capture images of the person's face and save them in the `TrainingImage` folder.
   
4. Then you have to click the "Train" button which will start training the model for all the images and person details that have been enrolled.
   
5. Once the model is trained, you can click the "Take Attendance" Button on the application to open a window showing the video feed. It will detect and recognize faces in the video, and display the name of the recognized person on the screen.
   
6. Then it will save the attendance details in a CSV file in the "Attendance" Folder.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
