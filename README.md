# BCI-controlled-UR-manipulator 

Python efficient implementation of robotic system consisting of motor imagery noninvasive BCI control and 6 DOF UR5 manipulator modules which allows paralyzed subjects to perform reach-grasp-release actions in 3D space. The sequential axis control methodology is used in the project to resolve low Information Transfer Rate (ITR) problem, where participant have to provide several low level commands to the robot, such as position on x, y and z axes and close/release gripper actions. With the advantage of the motor imagery paradigm the system is asynchronous and timing is controlled by the operator, so commands are not prompted by the system and operator decides the durations of motions and pauses. 

<p align="center"> 
<img src="https://raw.githubusercontent.com/BatyaGG/BCI-controlled-UR-manipulator/master/images/pipeline.png" width="70%"> 
</p> 

The signal is preprocessed, translated to frequency domain and band-pass filtered. Preprocessed data is trained and classified by soft voting ensemble model, which includes state-of-art EEG classification models as well as boosting and decision tree based algorithms. Such ensemble classification approach was not previously exploited in BCI control architectures, and usually consisted of only one linear model such as Support-Vector Machines or Linear Regression models. Scenario experiments were provided in order to prove reliability of proposed system on 7 healthy subject. The experimental results shown that the proposed architecture is a potential paradigm to be used in a real world situations by disabled people and could be a state-of-art design to be improved in future. Also, experiments shown that several control sessions leads to further supervision improvement leading to smooth and relaxed execution of tasks, due to experience gain by subjects. Please take a look on robot control session captured video. 

<p align="center"> 
<a href="https://www.youtube.com/watch?v=BMP_HQ0vaPo" target="_blank"><img src="https://raw.githubusercontent.com/BatyaGG/BCI-controlled-UR-manipulator/master/images/youtube.png" 
width="70%"" border="10" /></a> 
<br> 
<i>The demo video</i> 
</p> 

## Installation 

Clone or download the project. 

Package prerequisites: numpy <1.14.3>, scikit-learn <0.19.1>, scipy <1.1.0>, pygame <1.9.3> 

Higher versions of packages should be okay. 

## Usage 

First of all g.tec BCI kit is needed, which consists of [g.USBamp signal amplifier](http://www.gtec.at/Products/Hardware-and-Accessories/g.USBamp-Specs-Features), [g.GAMMAbox electrode system](http://www.gtec.at/Products/Electrodes-and-Sensors/g.Electrodes-Specs-Features) for 16 channel acquisition with g.tec head cap. Usually, g.tec company sells PCs together with their BCI systems with already installed software. [BufferBCI](https://github.com/jadref/buffer_bci) is used for data acquisition together with Simulink based g.tec system launcher. Also, Universal Robot UR5 and ROBOTIQ 3-finger gripper are needed in as a controlled device. Moreover, the code can be modified for other robotic tools, such as robotic wheelchair or mouse cursor depending on your ideas. The code is ready to use and I advice to use it several times training and controlling the robot, before getting into the implementation details. Please read the "Usage" section carefully to understand the whole pipeline. 

### Training session 

To train a new model for new subject, run ```trainInterface.py``` file. The data collection process will start automatically if BufferBCI is already gathering data. The data for one subject should be collected for about 30-40 minutes depending on subject's fatigue. The interactive train interface was implemented using PyGame Python module having 3 indicators for left/right arms and legs, pause button to be used to allow subject to rest and finish button is used to finalize data acquisition process and train the model. 

In general the script of ```trainInterface.py``` file is not hard to understand. I created custom class named ```PygameButton``` which simply draws pygame rectangle with text on current frame. The advantage of this class is ```is_pushed(self)``` function, which checks mouse click event position and compares with position of the ```pygame::rectangle``` itself. Another useful custom class is ```ClassUpdater``` which is basically used as a random iterator which determines the labels of the time windows. Returns next window label as a number from 0 to ```num_of_classes``` parameter value. The key point is that between each consecutive nonzero labels, the ```ClassUpdater``` return zero class which denotes "rest" class, to put 1 second delay between motor imagery prompts. Also, the labels are given in a random but balanced manner. The final label vector surely will be balanced, except for 0 class which will be 3 times more than imagery classes.

<p align="center"> 
<img src="https://github.com/BatyaGG/BCI-controlled-UR-manipulator/blob/master/images/train_interface.jpg" width="70%">
</p> 

Subject is guided to imagine left/right arms and leg motions by flashing indicators, using windowing approach, where one window consists of 1 second duration data of all channels. Window duration may be changed in ```trainInterface.py``` file. Each window is considered as observation or epoch and is 2D matrix of shape _freq_ X _nChan_, where _freq_ is a sampling frequency of acquisition system and _nChan_ is a number of channels used in analysis. The whole data is 3D tensor of shape _freq_ X _nChan_ X _nEpoch_, where _nEpoch_ is a number of observations or labels. There is a 1 sec empty window between each motion class considered as rest class and labeled as 0. Imagery labels are flashed using smart random sequence approach, to improve abruptness of prompts, since sequential approach had bad effects on model accuracy, due to adaptation of subjects to a specific order of flashes forming common pattern signals generated by them. Random sequence module ensures that formed data is always balanced. Moreover, due to human response lag a slight delay was introduced in acquisition session, to maximize useful samples per epoch. This is tunable parameter of BCI class module and by default is set to 50 samples delay per epoch. This default parameter was chosen empirically by comparison of several models trained on various delay attributes. When _Finish_ button is pressed, it will take about 1 minute to optimize classifier so just wait until ```train GUI``` will disappear. The script will create a folder with current date-time name in *%b_%d_%Y_%H%M* format. The folder contains gathered data and trained model to be used later in controlling the robot in ```.pickle``` extension format. 

### Control session 

To control the device run ```controlInterface.py``` script. It will initialize everything up and control session begins if BCI buffer is already gathering data. In the figure (A) below control interface can be seen. Each row of this 4x2 grid is control variant such that first row is x-axis control, second row is y-axis control, third row is z-axis control and fourth row is gripper control. Left column (-) of the grid corresponds to left arm motor imagery and right column (+) of the grid corresponds to right arm motor imagery. Left arm motor imagery (-) moves the end-effector in negative direction of current controlled axis and right arm (+) motor imagery moves in positive direction of controlled axis. Legs motor imagery is used for changing control variants sequentially such like: x -> y -> z -> g -> z -> y -> x -> y ... by ```ControlUpdater``` class. In case of subsequent "Legs class" prediction, the class blocks changing control variant for 2 seconds, to prevent accidential update.

<p align="center"> 
<img src="https://github.com/BatyaGG/BCI-controlled-UR-manipulator/blob/master/images/control_interface.jpg" width="70%"> 
<br> 
<i>A) Control interface displaying active axes B) 3D model of the UR5 robot with gripper indicating axis directions</i> 
</p> 
                                                                                      
In (B) part of the above figure, UR5 robot manipulator with indicated on gripper position the control axises where green, red and blue related to the _X_, _Y_ and _Z_ axises of the movement. Also, changing control dimension state is supported by audio indicator saying which axis is controlled now. Such assistance allows subject to be independent from screen while controlling the robot.

## Explanation report

### Signal Processing

#### Signal Detrending
