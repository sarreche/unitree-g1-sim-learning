# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Sarreche
# Historical local prototype developed in the unitreerobotics conversation.
# Recovered 2026-09-27; original behavior preserved. SIMULATION ONLY.
# Read README.md in this directory before interpreting this experiment.
import time

from unitree_sdk2py.core.channel import (
    ChannelFactoryInitialize,
    ChannelSubscriber,
)
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowState_


last_print = 0


def low_state_handler(msg: LowState_):
    global last_print

    # Imprimir solamente una vez por segundo
    now = time.time()
    if now - last_print < 1:
        return

    last_print = now

    print("\n--- G1 LowState ---")

    for i, motor in enumerate(msg.motor_state):
        print(
            f"Motor {i:02d}: "
            f"q={motor.q:8.4f}  "
            f"dq={motor.dq:8.4f}  "
            f"tau={motor.tau_est:8.4f}"
        )

    print("IMU RPY:", msg.imu_state.rpy)


ChannelFactoryInitialize(1, "lo")

subscriber = ChannelSubscriber(
    "rt/lowstate",
    LowState_
)

subscriber.Init(low_state_handler, 10)

print("Escuchando al G1 simulado... Ctrl+C para terminar.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFin.")
