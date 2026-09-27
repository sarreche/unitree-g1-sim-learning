# SPDX-License-Identifier: BSD-3-Clause
# Derived from Unitree SDK2 Python G1 example; experimental local modifications.
# Copyright (c) 2016-2024 HangZhou YuShu TECHNOLOGY CO.,LTD.
# Cleaned 2026-09-27. Full terms: ../licenses/unitree_sdk2_python.txt
# SIMULATION ONLY: domain 1 / lo. Not validated for physical hardware.
import time
from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
from unitree_sdk2py.core.channel import ChannelSubscriber
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_
from unitree_sdk2py.utils.crc import CRC
from unitree_sdk2py.utils.thread import RecurrentThread
import math
G1_NUM_MOTOR = 29
Kp = [60, 60, 60, 100, 40, 40, 60, 60, 60, 100, 40, 40, 60, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
Kd = [1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

class G1JointIndex:
    LeftHipPitch = 0
    LeftHipRoll = 1
    LeftHipYaw = 2
    LeftKnee = 3
    LeftAnklePitch = 4
    LeftAnkleB = 4
    LeftAnkleRoll = 5
    LeftAnkleA = 5
    RightHipPitch = 6
    RightHipRoll = 7
    RightHipYaw = 8
    RightKnee = 9
    RightAnklePitch = 10
    RightAnkleB = 10
    RightAnkleRoll = 11
    RightAnkleA = 11
    WaistYaw = 12
    WaistRoll = 13
    WaistA = 13
    WaistPitch = 14
    WaistB = 14
    LeftShoulderPitch = 15
    LeftShoulderRoll = 16
    LeftShoulderYaw = 17
    LeftElbow = 18
    LeftWristRoll = 19
    LeftWristPitch = 20
    LeftWristYaw = 21
    RightShoulderPitch = 22
    RightShoulderRoll = 23
    RightShoulderYaw = 24
    RightElbow = 25
    RightWristRoll = 26
    RightWristPitch = 27
    RightWristYaw = 28

class Mode:
    PR = 0
    AB = 1

class Custom:

    def __init__(self):
        self.time_ = 0.0
        self.control_dt_ = 0.002
        self.duration_ = 3.0
        self.counter_ = 0
        self.mode_pr_ = Mode.PR
        self.mode_machine_ = 0
        self.low_cmd = unitree_hg_msg_dds__LowCmd_()
        self.low_state = None
        self.update_mode_machine_ = False
        self.crc = CRC()

    def Init(self):
        """Connect simulation LowCmd publisher and LowState subscriber."""
        self.lowcmd_publisher_ = ChannelPublisher('rt/lowcmd', LowCmd_)
        self.lowcmd_publisher_.Init()
        self.lowstate_subscriber = ChannelSubscriber('rt/lowstate', LowState_)
        self.lowstate_subscriber.Init(self.LowStateHandler, 10)

    def Start(self):
        """Wait for the first state before starting the 2 ms control loop."""
        self.lowCmdWriteThreadPtr = RecurrentThread(interval=self.control_dt_, target=self.LowCmdWrite, name='control')
        while self.update_mode_machine_ == False:
            time.sleep(1)
        if self.update_mode_machine_ == True:
            self.lowCmdWriteThreadPtr.Start()

    def LowStateHandler(self, msg: LowState_):
        """Keep the latest state and report quaternion-derived Euler angles."""
        self.low_state = msg
        if self.update_mode_machine_ == False:
            self.mode_machine_ = self.low_state.mode_machine
            self.update_mode_machine_ = True
        self.counter_ += 1
        if self.counter_ % 500 == 0:
            self.counter_ = 0
            q = self.low_state.imu_state.quaternion
            w = q[0]
            x = q[1]
            y = q[2]
            z = q[3]
            sinr_cosp = 2.0 * (w * x + y * z)
            cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
            roll = math.atan2(sinr_cosp, cosr_cosp)
            sinp = 2.0 * (w * y - z * x)
            sinp = max(-1.0, min(1.0, sinp))
            pitch = math.asin(sinp)
            siny_cosp = 2.0 * (w * z + x * y)
            cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
            yaw = math.atan2(siny_cosp, cosy_cosp)
            print('roll={:.2f}° pitch={:.2f}° yaw={:.2f}°'.format(math.degrees(roll), math.degrees(pitch), math.degrees(yaw)))

    def LowCmdWrite(self):
        """Publish the recovered posture experiment; not a validated balance controller."""
        self.time_ += self.control_dt_
        stand_pose = [-0.1, 0.0, 0.0, 0.3, -0.2, 0.0, -0.1, 0.0, 0.0, 0.3, -0.2, 0.0]
        for i in range(G1_NUM_MOTOR):
            self.low_cmd.mode_pr = Mode.PR
            self.low_cmd.mode_machine = self.mode_machine_
            self.low_cmd.motor_cmd[i].mode = 1
            self.low_cmd.motor_cmd[i].tau = 0.0
            self.low_cmd.motor_cmd[i].dq = 0.0
            self.low_cmd.motor_cmd[i].kp = Kp[i]
            self.low_cmd.motor_cmd[i].kd = Kd[i]
        for i in range(12):
            self.low_cmd.motor_cmd[i].q = stand_pose[i]
        for i in range(12, G1_NUM_MOTOR):
            self.low_cmd.motor_cmd[i].q = 0.0
        self.low_cmd.crc = self.crc.Crc(self.low_cmd)
        self.lowcmd_publisher_.Write(self.low_cmd)
if __name__ == '__main__':
    print('WARNING: Please ensure there are no obstacles around the robot while running this example.')
    input('Press Enter to continue...')
    ChannelFactoryInitialize(1, 'lo')
    custom = Custom()
    custom.Init()
    custom.Start()
    while True:
        time.sleep(1)
