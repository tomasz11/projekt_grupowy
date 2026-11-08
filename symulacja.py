import os
import time
import math
import pybullet as p
import pybullet_data


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
slider_base = p.addUserDebugParameter("Kat bazy(stopnie)", 0, 360, 0)


def set_tube_angle(robot_id, base_deg,tube_deg, max_force=500):

    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=tube_joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=math.radians(tube_deg),
        force=max_force
    )
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=base_joint_id,
        controlMode=p.POSITION_CONTROL,
        targetPosition=math.radians(base_deg),
        force=max_force
    )

target_angle_tube = 45.0
target_angle_base = 0.0



set_tube_angle(robotId, target_angle_base, target_angle_tube)

try:
    while p.isConnected():

        gui_angle_tube = p.readUserDebugParameter(slider_tube)
        gui_angle_base = p.readUserDebugParameter(slider_base)
        set_tube_angle(robotId,gui_angle_base, gui_angle_tube)
        
        p.stepSimulation()
        time.sleep(1.0 / 240.0)

except p.error:
    print("koniec gry")

p.disconnect()