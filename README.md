## Hand Gestures Control for Robotic Arm on Arduino Uno Q
### by Jallson Suryo

![Project Setup](images/photo01.png)

Edge Impulse project link: https://studio.edgeimpulse.com/public/1019079/live

Demo Video link: https://youtu.be/rZpem5olRLM

Repo link: https://github.com/Jallson/custom_gestures_uno_q


### Introduction:

This project utilizes a local network setup where an Arduino Uno Q is connected to a USB camera and a robotic arm, with programming performed via the Arduino AppLab on our computer/laptop. The ease of using the I/O pins on the Arduino Uno Q, which are identical to those of a standard Arduino Uno, makes this project accessible and easy for anyone to carry out.
In this relatively simple project, the system will translate the position of hand detected into movements of two servos that control the pan-tilt mechanism on robotic arm, while gesture types (for example, open and close) will control the servo on the claw/gripper. The system can use an existing model (Hand Gesture) available in Arduino AppLab, or a custom model created in Edge Impulse Studio integrated within AppLab. The model will be deployed in Python code for the program logic and then passed to the Arduino Sketch to drive the servos accordingly.

This project is intended as a basic implementation of object detection in robotics, featuring real-time object tracking and intuitive robotic arm movement. It is a foundation for applications in more complex robotic systems.

#### Hardware Component:

![Hardware](images/photo02.png)

- Arduino Uno Q (2GB or 4GB)
- USB-C Power Adaptor (eg. 27W Pi 5 Power adapter)
- PC/laptop
- USB-C to USB-A hub with PD (except from Apple) or official Arduino USB-C hub (8 in 1)
- USB Camera/webcam (eg. Logitech C920/C922)
- 3 DoF Robotic arm with gripper
- 3 pcs Servos (eg. MG996r)
- Breadboard + jumper cables
- 4 x1,5V battery or 6V power supply


#### Software & Online Services:

- Arduino AppLab (v 0.8.0)
- EdgeImpulse Studio

### Steps:

#### 1. Uno Q Setup and Arduino AppLab

For the initial setup, install the Arduino App Lab on your computer and connect the Arduino Uno Q via a USB-C connection (PC-hosted mode). Once AppLab is opened, the Uno Q device will appear; select it, create an access password, and configure the Wi-Fi network so that we can use it in local network mode for convenience. After completing this process, disconnect the Uno Q and connect it to a power adapter. Open the Arduino AppLab on your computer, and the Uno Q will appear for you to access. To familiarize yourself with this ecosystem, you can select one project from Examples and press Run, which will upload and execute the chosen program on the Uno Q.

For the next step, create our project by duplicating "Detect Objects from Camera" from the Examples, because it’s using similar bricks. Open it and click Copy and edit (in the upper right corner), then rename it as desired, for example: "Custom Hand Gestures Detection." Next, select the AI models tab and click Train new AI model, which will allow you to access Edge Impulse Studio using your Arduino account (sign in or create one if you don't have one yet). Then, you will be redirected to the Edge Impulse Studio by clicking Start to Train your AI model. We will discuss the stages within Edge Impulse Studio in the next step below.

![Connect Uno Q](images/photo03.png)
![App Examples](images/photo04.png)
![Train New AI](images/photo05.png)
![Sign in or Create Account](images/photo06.png)
![Connected](images/photo07.png)


#### 2. Collecting Data

Before we start uploading the photos, we will create three labels/classes: a closed hand (neutral), and a scissor-like hand gesture (open and close). Capture these photos using your camera or your laptop's built-in webcam. I recommend taking a variety of 30–40 photos for each type, which should be sufficient for this project. Save them in folders, and we will continue in the Edge Impulse Studio.
For those who are not familiar with Edge Impulse Studio, choose Images project option, then Object detection. In Dashboard > Project Info, choose Bounding Boxes for labeling method and Uno Q for target device. Then in Data acquisition, click on Upload Data tab. Choose you saved folder then upload.

![Choose Bounding Boxes](images/photo08.png)
![Upload Data](images/photo09.png)

#### 3. Labeling

The next step is labeling, now click on Data Acquisition, click on Labeling queue tab, then start drag a box around an object and label it and Save. Repeat.. until all images labelled.

After labeling, it’s recommended to split the data into training and testing sets, around an 80/20 ratio. If you haven't done this yet, click on Train / Test Split to automate this process.

![Manual labeling](images/photo10.png)
![Split Data to 80/20](images/photo11.png)

#### 4. Train, Build, Deploy

Once your labelled dataset is ready, go to Impulse Design > Create Impulse, and set the image width and height (eg. 320x320). Choose Fit shortest axis, then select Image and Object Detection as the learning blocks, and click Save Impulse. Next, navigate to the Image Parameters section, select RGB as the color depth, and press Save parameters. After that, click on Generate, where you’ll be able to see a graphical distribution.
Now, move to the Object Detection section and configure the training settings. Select GPU and set the training cycles to around 100, learning rate to 0.001 and medium for model size. Choose YOLO-Pro or MobileNetV2 SSD FPN-Lite as the NN architecture. Once done, start training by pressing Start, and monitor the progress.
If everything goes well; eg MAP@50 = 1.0 or the precision result is more than 90%, proceed to the next step. Go to the Model Testing section, click Classify all, and if the MAP@50 = 1.0 or the accuracy is around 90%, you can move on to Deployment. Select deployment target Arduino Uno Q, select quantized (int 98) then click Build. Next step will be on Arduino AppLab.

![Learning blocks](images/photo12.png)
![Generate features](images/photo13.png)
![NN setting & result](images/photo14.png)
![Model Testing](images/photo15.png)
![Deployment](images/photo16.png)


#### 5. Test on Uno Q

After the model has been built, return to the Arduino AppLab, you will find the custom model we built in Edge Impulse Studio earlier—click the Download icon and select it. Now, our custom model is ready to use. To test it, don't forget to connect the USB-C to USB-A hub and the USB camera to yout Uno Q. Then, click Run in AppLab; the upload and execution process on the Uno Q will begin. If everything goes smoothly, the WebUI-HTML program will display live object detection inference in your computer's browser. Try the 3 types of gestures from our model to ensure it is working properly.

![Download your Custom Model](images/photo17.png)
![Live inferencing](images/inferencing.gif)


#### 6. Build Your System: Uno Q + usb camera + robotic arm + program

![Complete Setup](images/diagram.png)

To control the robotic arm using hand gestures, you must ensure that everything is properly connected as shown in the diagram above. Additionally, before creating your Python or Sketch programs, you need to download several Sketch Libraries. Click Add Sketch Library, then search for and download them one by one: Servo 1.3.0, MsgPack 0.4.2, DebugLog 0.8.4, ArxContainer 0.7.0, and ArxTypeTraits 0.3.1 (or their latest updated versions).
Below is a screenshot of the Python code. It is important to adjust/calibrate the servo angles to match the physical configuration of your specific robotic arm. In this Python code, the logic is as follows: if the "neutral" gesture is detected, the horizontal position is mapped to the pan servo angle, while the size of the bounding box is interpreted as a change in the tilt servo angle. The "opening" and "closing" gestures translate to the movement/angle change of the claw servo. Meanwhile, the Sketch file determines which pins are used; in this case, pins 9, 10, 11. Servos angle standard setup and handles the output display on the LED matrix (a smiley face) whenever a hand gesture is detected.
All Python and Sketch files can be downloaded from the GitHub link below, then you can click Add File icon on AppLab then mod/adjust for your needs.

![Add Sketch Library](images/photo18.png)
![Python main code](images/photo19.png)
![Sketch.ino](images/photo20.png)

Files/codes can be accessed at:
https://github.com/Jallson/custom_gestures_uno_q


### Conclusion:

This project successfully demonstrates a basic Edge AI vision system that connects real-time object detection to physical actuation by deploying an Edge Impulse custom gestures model with reliable accuracy and low latency. The project validated the end-to-end pipeline from camera input, spatial mapping, and actuator control in a single embedded system. This project highlights the practical integration of Edge AI with robotics and serves as a foundation for more advanced applications.
