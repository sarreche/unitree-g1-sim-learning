# SPDX-License-Identifier: BSD-3-Clause
# Derived from unitree_rl_gym MuJoCo deploy; keyboard experiment cleaned 2026-09-27.
# Copyright (c) 2016-2023 HangZhou YuShu TECHNOLOGY CO.,LTD.
# Full terms: ../licenses/unitree_rl_gym.txt
import time

import mujoco.viewer
import mujoco
import numpy as np
from legged_gym import LEGGED_GYM_ROOT_DIR
import torch
import yaml

import sys
import select
import termios
import tty

def get_gravity_orientation(quaternion):
    qw = quaternion[0]
    qx = quaternion[1]
    qy = quaternion[2]
    qz = quaternion[3]

    gravity_orientation = np.zeros(3)

    gravity_orientation[0] = 2 * (-qz * qx + qw * qy)
    gravity_orientation[1] = -2 * (qz * qy + qw * qx)
    gravity_orientation[2] = 1 - 2 * (qw * qw + qz * qz)

    return gravity_orientation


def pd_control(target_q, q, kp, target_dq, dq, kd):
    """Calculates torques from position commands"""
    return (target_q - q) * kp + (target_dq - dq) * kd


if __name__ == "__main__":
    # get config file name from command line
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to YAML configuration")
    args = parser.parse_args()
    config_file = args.config
    with open(config_file, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        policy_path = config["policy_path"].replace("{LEGGED_GYM_ROOT_DIR}", LEGGED_GYM_ROOT_DIR)
        xml_path = config["xml_path"].replace("{LEGGED_GYM_ROOT_DIR}", LEGGED_GYM_ROOT_DIR)

        simulation_duration = config["simulation_duration"]
        simulation_dt = config["simulation_dt"]
        control_decimation = config["control_decimation"]

        kps = np.array(config["kps"], dtype=np.float32)
        kds = np.array(config["kds"], dtype=np.float32)

        default_angles = np.array(config["default_angles"], dtype=np.float32)

        ang_vel_scale = config["ang_vel_scale"]
        dof_pos_scale = config["dof_pos_scale"]
        dof_vel_scale = config["dof_vel_scale"]
        action_scale = config["action_scale"]
        cmd_scale = np.array(config["cmd_scale"], dtype=np.float32)

        num_actions = config["num_actions"]
        num_obs = config["num_obs"]
        
        cmd = np.array(config["cmd_init"], dtype=np.float32)

    # define context variables
    action = np.zeros(num_actions, dtype=np.float32)
    target_dof_pos = default_angles.copy()
    obs = np.zeros(num_obs, dtype=np.float32)

    counter = 0

    # Load robot model
    m = mujoco.MjModel.from_xml_path(xml_path)
    d = mujoco.MjData(m)
    m.opt.timestep = simulation_dt

    # load policy
    policy = torch.jit.load(policy_path)

    if not sys.stdin.isatty():
        raise RuntimeError("Use an interactive Linux terminal for keyboard input")
    old_settings = termios.tcgetattr(sys.stdin)

    def get_key():
        """Read one key without blocking; commands persist until another key."""
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1).lower()
        return None

    try:
        tty.setcbreak(sys.stdin.fileno())
        with mujoco.viewer.launch_passive(m, d) as viewer:
            # Close the viewer automatically after simulation_duration wall-seconds.
            start = time.time()
            while viewer.is_running() and time.time() - start < simulation_duration:
    
                key = get_key()
    
                if key == "w":
                    cmd[:] = [0.3, 0.0, 0.0]
    
                elif key == "s":
                    cmd[:] = [-0.3, 0.0, 0.0]
    
                elif key == "a":
                    cmd[:] = [0.0, 0.0, 0.4]
    
                elif key == "d":
                    cmd[:] = [0.0, 0.0, -0.4]
    
                elif key == "q":
                    cmd[:] = [0.0, 0.2, 0.0]
    
                elif key == "e":
                    cmd[:] = [0.0, -0.2, 0.0]
    
                elif key == " ":
                    cmd[:] = [0.0, 0.0, 0.0]
    
                elif key == "x":
                    break
    
                step_start = time.time()
                tau = pd_control(target_dof_pos, d.qpos[7:], kps, np.zeros_like(kds), d.qvel[6:], kds)
                d.ctrl[:] = tau
                # mj_step can be replaced with code that also evaluates
                # a policy and applies a control signal before stepping the physics.
                mujoco.mj_step(m, d)
    
                counter += 1
                if counter % control_decimation == 0:
                    # Apply control signal here.
    
                    # create observation
                    qj = d.qpos[7:]
                    dqj = d.qvel[6:]
                    quat = d.qpos[3:7]
                    omega = d.qvel[3:6]
    
                    qj = (qj - default_angles) * dof_pos_scale
                    dqj = dqj * dof_vel_scale
                    gravity_orientation = get_gravity_orientation(quat)
                    omega = omega * ang_vel_scale
    
                    period = 0.8
                    count = counter * simulation_dt
                    phase = count % period / period
                    sin_phase = np.sin(2 * np.pi * phase)
                    cos_phase = np.cos(2 * np.pi * phase)
    
                    obs[:3] = omega
                    obs[3:6] = gravity_orientation
                    obs[6:9] = cmd * cmd_scale
                    obs[9 : 9 + num_actions] = qj
                    obs[9 + num_actions : 9 + 2 * num_actions] = dqj
                    obs[9 + 2 * num_actions : 9 + 3 * num_actions] = action
                    obs[9 + 3 * num_actions : 9 + 3 * num_actions + 2] = np.array([sin_phase, cos_phase])
                    obs_tensor = torch.from_numpy(obs).unsqueeze(0)
                    # policy inference
                    action = policy(obs_tensor).detach().numpy().squeeze()
                    # transform action to target_dof_pos
                    target_dof_pos = action * action_scale + default_angles
    
                # Pick up changes to the physics state, apply perturbations, update options from GUI.
                viewer.sync()
    
                # Rudimentary time keeping, will drift relative to wall clock.
                time_until_next_step = m.opt.timestep - (time.time() - step_start)
                if time_until_next_step > 0:
                    time.sleep(time_until_next_step)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
