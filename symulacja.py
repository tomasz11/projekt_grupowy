import os
import time
import math
import pybullet as p
import pybullet_data
from setup import Get_data_site


urdf_path = r"C:\Users\tomek\Desktop\studia\sem 5\projekt_grupowy\data_base\model_teleskopu_skywatcher_8_description\urdf\model_teleskopu_skywatcher_8.urdf"

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, 0)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF(urdf_path, basePosition=[0, 0, 0.05], useFixedBase=True)


num_joints = p.getNumJoints(robotId)


tube_joint_id = 1
base_joint_id = 0

slider_tube = p.addUserDebugParameter("Kat Tuby (Stopnie)", -30, 60, 0)
slider_base = p.addUserDebugParameter("Kat bazy(stopnie)", -180, 180, 0)
results = Get_data_site() 
actual_position_azimut = results[0][0]
actual_position_altidute = results[0][1]




def set_tube_angle(robot_id, base_deg,tube_deg, max_force=100):

    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=tube_joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=math.radians(tube_deg),
        maxVelocity = 0.5,
        force=max_force,
        positionGain=0.8,  
        velocityGain=20
    )
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=base_joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=math.radians(base_deg),
        maxVelocity = 0.5,
        force=max_force,
        positionGain=0.8,  
        velocityGain=20
    )

target_angle_tube = 45.0
target_angle_base = 0.0



set_tube_angle(robotId, target_angle_base, target_angle_tube)

try:
    while p.isConnected():
        delta_azimut_per_second = ((results[1][0] - results[0][0]) / 60 )
        delta_altidute_per_second = ((results[1][1] - results[0][1]) / 60 )

        gui_angle_tube = p.readUserDebugParameter(slider_tube)
        gui_angle_base = p.readUserDebugParameter(slider_base)
        set_tube_angle(robotId,actual_position_azimut, actual_position_altidute)

        #aktualizuj pozycje planety
        if actual_position_altidute > -31 and actual_position_altidute < 61:
            actual_position_azimut += delta_azimut_per_second
            actual_position_altidute += delta_altidute_per_second
        else:
            print("Nadwyrezenie osi !!!")
            break
        p.stepSimulation()
        #time.sleep(1.0 / 240.0)
        time.sleep(1.0 / 60.0)

except p.error:
    print("koniec gry")

p.disconnect()