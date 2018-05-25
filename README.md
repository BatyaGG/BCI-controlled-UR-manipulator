# BCI-controlled-UR-manipulator 

Python efficient implementation of robotic system consisting of motor imagery noninvasive BCI control and 6 DOF UR5 manipulator modules which allows paralyzed subjects to perform reach-grasp-release actions in 3D space. The sequential axis control methodology is used in the project to resolve low Information Transfer Rate (ITR) problem, where participant have to provide several low level commands to the robot, such as position on x, y and z axes and close/release gripper actions. With the advantage of the motor imagery paradigm the system is asynchronous and timing is controlled by the operator, so commands are not prompted by the system and operator decides the durations of motions and pauses. 

<p align="center"> 
<img src="https://raw.githubusercontent.com/BatyaGG/BCI-controlled-UR-manipulator/master/images/pipeline.png" width="70%"> 
</p> 

The signal is preprocessed, translated to frequency domain and band-pass filtered. Preprocessed data is trained and classified by soft voting ensemble model, which includes state-of-art EEG classification models as well as boosting and decision tree based algorithms. Such ensemble classification approach was not previously exploited in BCI control architectures, and usually consisted of only one linear model such as Support-Vector Machines or Linear Regression models. Scenario experiments were provided in order to prove reliability of proposed system on 7 healthy subject. The experimental results shown that the proposed architecture is a potential paradigm to be used in a real world situations by disabled people and could be a state-of-art design to be improved in future. Also, experiments shown that several control sessions leads to further supervision improvement leading to smooth and relaxed execution of tasks, due to experience gain by subjects. Please take a look on robot control session captured video. 

<p align="center"> 
<a href="https://www.youtube.com/watch?v=BMP_HQ0vaPo" target="_blank"><img src="https://writelatex.s3.amazonaws.com/wndkfttkbxvm/uploads/6061/24211579/1.png?X-Amz-Expires=14400&X-Amz-Date=20180512T202539Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAJF667VKUK4OW3LCA/20180512/us-east-1/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=a90afa65536e2de596cb20322199e282dafaac0eba48c3959bad923720e72acb" 
width="70%"" border="10" /></a> 
<br> 
<i>The demo video</i> 
</p> 

## Installation 

Clone or download the project. 

Package prerequisites: numpy <1.14.3>, scikit-learn <0.19.1>, scipy <1.1.0>, pygame <1.9.3> 

Higher versions of packages should be okay. 

## Usage 

First of all g.tec BCI kit is needed, which consists of g.USBamp signal amplifier, g.GAMMAbox electrode system for 16 channel acquisition with g.tec head cap. Usually, g.tec company sells PCs together with their BCI systems with already installed software. g.tec BufferBCI is used for data acquisition together with Simulink based g.tec system launcher. Also, Universal Robot UR5 and ROBOTIQ 3-finger gripper are needed in as a controlled device. Moreover, the code can be modified for other robotic tools, such as robotic wheelchair or mouse cursor depending on your ideas. The code is ready to use and I advice to use it several times training and controlling the robot, before getting into the implementation details. Please read the "Usage" section carefully to understand the whole pipeline. 

### Training session 

To train a new model for new subject, run ```trainInterface.py``` file. The data collection process will start automatically if BufferBCI is already gathering data. The data for one subject should be collected for about 30-40 minutes depending on subject's fatigue. The interactive train interface was implemented using PyGame Python module having 3 indicators for left/right arms and legs, pause
