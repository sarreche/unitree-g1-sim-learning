# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Sarreche
# Historical local prototype developed in the unitreerobotics conversation.
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


RIGHT_ELBOW = 25

state = None


def state_handler(msg):
    global state
    state = msg


# Mismo dominio e interfaz que nuestro simulador
ChannelFactoryInitialize(1, "lo")

# Leer estado
subscriber = ChannelSubscriber("rt/lowstate", LowState_)
subscriber.Init(state_handler, 10)

# Enviar comandos
publisher = ChannelPublisher("rt/lowcmd", LowCmd_)
publisher.Init()

crc = CRC()

print("Esperando estado del G1...")

while state is None:
    time.sleep(0.1)

start_q = state.motor_state[RIGHT_ELBOW].q

print(f"Codo derecho inicial: {start_q:.3f} rad")

cmd = unitree_hg_msg_dds__LowCmd_()

# Copiar mode_machine recibido del simulador
cmd.mode_machine = state.mode_machine
cmd.mode_pr = 0

# Vamos a pedir un movimiento pequeño: +0.30 rad
target_q = start_q + 0.30

print(f"Objetivo: {target_q:.3f} rad")
print("Moviendo durante 3 segundos...")

start_time = time.time()

while time.time() - start_time < 3.0:

    motor = cmd.motor_cmd[RIGHT_ELBOW]

    motor.mode = 1
    motor.q = target_q
    motor.dq = 0.0

    # Ganancias moderadas para esta primera prueba
    motor.kp = 20.0
    motor.kd = 1.0

    motor.tau = 0.0

    cmd.crc = crc.Crc(cmd)
    publisher.Write(cmd)

    time.sleep(0.002)

print("Comando terminado.")
