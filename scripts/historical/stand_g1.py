# SPDX-License-Identifier: BSD-3-Clause
# Historical experiment with gains from the Unitree SDK2 Python G1 example.
# Copyright (c) 2016-2024 HangZhou YuShu TECHNOLOGY CO.,LTD.
# Attribution and full terms: ../../licenses/unitree_sdk2_python.txt
# Recovered 2026-09-27; original behavior preserved. SIMULATION ONLY.
# Read README.md in this directory before interpreting this experiment.
import time

from unitree_sdk2py.core.channel import (
    ChannelFactoryInitialize,
    ChannelPublisher,
    ChannelSubscriber,
)
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_, LowState_
from unitree_sdk2py.utils.crc import CRC


NUM_MOTORS = 29

Kp = [
    60, 60, 60, 100, 40, 40,       # pierna izquierda
    60, 60, 60, 100, 40, 40,       # pierna derecha
    60, 40, 40,                     # cintura
    40, 40, 40, 40, 40, 40, 40,    # brazo izquierdo
    40, 40, 40, 40, 40, 40, 40     # brazo derecho
]

Kd = [
    1, 1, 1, 2, 1, 1,
    1, 1, 1, 2, 1, 1,
    1, 1, 1,
    1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1
]

state = None


def state_handler(msg):
    global state
    state = msg


ChannelFactoryInitialize(1, "lo")

subscriber = ChannelSubscriber("rt/lowstate", LowState_)
subscriber.Init(state_handler, 10)

publisher = ChannelPublisher("rt/lowcmd", LowCmd_)
publisher.Init()

crc = CRC()

print("Esperando al G1...")

while state is None:
    time.sleep(0.01)

cmd = unitree_hg_msg_dds__LowCmd_()

cmd.mode_pr = 0
cmd.mode_machine = state.mode_machine

print("Manteniendo postura de pie.")
print("Ctrl+C para terminar.")

try:
    while True:

        for i in range(NUM_MOTORS):
            cmd.motor_cmd[i].mode = 1
            cmd.motor_cmd[i].q = 0.0
            cmd.motor_cmd[i].dq = 0.0
            cmd.motor_cmd[i].kp = Kp[i]
            cmd.motor_cmd[i].kd = Kd[i]
            cmd.motor_cmd[i].tau = 0.0

        cmd.crc = crc.Crc(cmd)
        publisher.Write(cmd)

        time.sleep(0.002)

except KeyboardInterrupt:
    print("\nControl detenido.")
