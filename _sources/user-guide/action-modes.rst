Action Modes
============

Action modes define how you control the robot in RoboEval environments. Different action modes are suited for different use cases: data collection, policy learning, or model evaluation.

Available Action Modes
----------------------

RoboEval provides joint position control for the robot:

JointPositionActionMode
~~~~~~~~~~~~~~~~~~~~~~~

Control the robot by specifying joint positions (angles).

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    
    # Absolute positions (most common)
    action_mode = JointPositionActionMode(
        absolute=True,
        floating_base=False
    )
    
    # Delta positions (incremental control)
    action_mode = JointPositionActionMode(
        absolute=False,
        floating_base=False
    )

**Parameters:**

``absolute`` : bool, default=False
    If True, actions specify absolute joint positions. If False, actions specify position deltas.

``floating_base`` : bool, default=True
    Enable control of the robot's base position (for mobile robots).

``ee`` : bool, default=False
    If True, control end-effector poses instead of joint positions.

``block_until_reached`` : bool, default=False
    Continue stepping until target position is reached (or max steps exceeded).

``floating_dofs`` : List[PelvisDof], optional
    Which base DOFs to control. By default includes X, Y, and RZ (rotation around Z-axis).

**Use cases:**

- Replaying demonstrations
- Teleoperation data collection
- Position-based policies

Action Mode Details
-------------------

Absolute Joint Position
~~~~~~~~~~~~~~~~~~~~~~~

Specify exact joint angles directly:

.. code-block:: python

    action_mode = JointPositionActionMode(absolute=True)
    env = LiftPot(action_mode=action_mode, robot_cls=BimanualPanda)
    
    # Action: target joint positions for all joints
    action = np.array([
        0.0, -0.7, 0.0, -2.4, 0.0, 1.7, 0.8,  # Left arm
        0.0, -0.7, 0.0, -2.4, 0.0, 1.7, 0.8,  # Right arm
        0.04, 0.04  # Grippers
    ])
    
    obs, reward, terminated, truncated, info = env.step(action)

**Action space:** ``Box(low=-π, high=π, shape=(n_joints,))``

**Advantages:**

- Precise control
- Easy to replay demonstrations
- Stable for data collection

**Disadvantages:**

- Requires knowledge of joint limits
- May need inverse kinematics for end-effector control

Delta Joint Position
~~~~~~~~~~~~~~~~~~~~

Specify incremental changes to joint positions:

.. code-block:: python

    action_mode = JointPositionActionMode(absolute=False)
    env = LiftPot(action_mode=action_mode, robot_cls=BimanualPanda)
    
    # Action: change in joint positions
    action = np.array([
        0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Move first joint slightly
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0
    ])

**Action space:** ``Box(low=-0.1, high=0.1, shape=(n_joints,))``

**Advantages:**

- Easier for learning (smaller action space)
- Smoother trajectories

**Disadvantages:**

- Accumulated errors over time
- Harder to replay exact demonstrations

End-Effector Control
~~~~~~~~~~~~~~~~~~~~

Control the robot by specifying end-effector poses (position + orientation):

.. code-block:: python

    action_mode = JointPositionActionMode(absolute=True, ee=True, floating_base=False)
    env = LiftPot(action_mode=action_mode, robot_cls=BimanualPanda)
    
    # For bimanual robot: 12D action (6D per arm)
    # [left_x, left_y, left_z, left_roll, left_pitch, left_yaw,
    #  right_x, right_y, right_z, right_roll, right_pitch, right_yaw]
    action = np.array([
        0.5, 0.3, 1.0, 0.0, 0.0, 0.0,  # Left end-effector
        0.5, -0.3, 1.0, 0.0, 0.0, 0.0,  # Right end-effector
    ])

**Action space (bimanual):** ``Box(shape=(12,))`` - 6D pose per arm (position xyz + euler xyz)

**Action space (single-arm):** ``Box(shape=(6,))`` - 6D pose (position xyz + euler xyz)

**Advantages:**

- Intuitive task-space control
- Easier for teleoperation
- No need for manual inverse kinematics

**Disadvantages:**

- IK solver may fail for unreachable poses
- Slower than direct joint control
- May have singularities

Floating Base Control
---------------------

For robots with mobile bases, enable floating base control:

.. code-block:: python

    from roboeval.action_modes import PelvisDof
    
    action_mode = JointPositionActionMode(
        absolute=True,
        floating_base=True,
        floating_dofs=[PelvisDof.X, PelvisDof.Y, PelvisDof.RZ]  # Planar movement
    )
    
    env = LiftPot(action_mode=action_mode, robot_cls=BimanualPanda)

**Available DOFs:**

- ``PelvisDof.X`` - Forward/backward
- ``PelvisDof.Y`` - Left/right  
- ``PelvisDof.Z`` - Up/down
- ``PelvisDof.RZ`` - Rotation around Z-axis (yaw)

Note: The floating base DOFs use the ``PelvisDof`` enum, not strings.

**Action space:**

.. code-block:: python

    # With floating_dofs=[PelvisDof.X, PelvisDof.Y, PelvisDof.RZ]
    action_space = Box(shape=(n_floating_dofs + n_joints,))
    
    # First N elements: floating base DOFs
    # Remaining: joint positions or gripper positions

Choosing an Action Mode
------------------------

**For Replaying Demonstrations:**

.. code-block:: python

    action_mode = JointPositionActionMode(
        absolute=True,
        floating_base=True,  # If demos include base movement
        floating_dofs=[]  # Match demo configuration
    )

**For Data Collection:**

.. code-block:: python

    # Keyboard teleoperation
    action_mode = JointPositionActionMode(
        absolute=False,  # Incremental control
        floating_base=True,
        floating_dofs=[PelvisDof.X, PelvisDof.Y, PelvisDof.RZ]
    )
    
    # VR teleoperation
    action_mode = JointPositionActionMode(
        absolute=True,  # Direct IK control
        floating_base=True
    )

**For Policy Learning:**

.. code-block:: python

    # Behavior cloning from demos
    action_mode = JointPositionActionMode(
        absolute=True  # Match demo format
    )
    
    # Reinforcement learning
    action_mode = JointPositionActionMode(
        absolute=False  # Easier action space
    )

Action Normalization
--------------------

Actions are automatically normalized/denormalized:

.. code-block:: python

    # Your policy outputs actions in [-1, 1]
    normalized_action = np.array([0.5, -0.3, 0.8, ...])
    
    # Environment automatically scales to valid range
    obs, reward, terminated, truncated, info = env.step(normalized_action)

To access raw (unnormalized) action space:

.. code-block:: python

    # Normalized (default, for learning)
    env.action_space  # Box(low=-1, high=1, ...)
    
    # Unnormalized (actual joint ranges)
    env.action_mode.get_action_space()  # Box(low=-π, high=π, ...)

Gripper Control
---------------

Grippers are controlled as part of the action vector:

.. code-block:: python

    # For BimanualPanda (14 arm joints + 2 gripper joints)
    action = np.zeros(16)
    
    # Arm joints
    action[:14] = arm_positions
    
    # Gripper control (last 2 elements)
    action[14] = 0.04  # Left gripper (open)
    action[15] = 0.04  # Right gripper (open)
    
    # To close grippers
    action[14] = 0.0  # Left gripper (closed)
    action[15] = 0.0  # Right gripper (closed)

Common Patterns
---------------

**Smooth Trajectories with Delta Mode:**

.. code-block:: python

    action_mode = JointPositionActionMode(absolute=False)
    env = LiftPot(action_mode=action_mode, robot_cls=BimanualPanda)
    
    obs, info = env.reset()
    
    # Move smoothly to target
    target = np.array([...])  # Target joint positions
    # Extract current positions from proprioception (qpos is first half)
    n_joints = len(env.robot.qpos)
    current_pos = obs["proprioception"][:n_joints]
    
    for step in range(100):
        delta = (target - current_pos) * 0.1  # 10% of distance
        delta = np.clip(delta, -0.05, 0.05)  # Limit speed
        
        obs, reward, terminated, truncated, info = env.step(delta)
        current_pos = obs["proprioception"][:n_joints]

**Switching Between Action Modes:**

.. code-block:: python

    # Collect data with one mode
    collect_mode = JointPositionActionMode(absolute=True, floating_base=True)
    env_collect = LiftPot(action_mode=collect_mode, robot_cls=BimanualPanda)
    
    # Train with another mode
    train_mode = JointPositionActionMode(absolute=False)
    env_train = LiftPot(action_mode=train_mode, robot_cls=BimanualPanda)

**Action Masking for Subsets of Joints:**

.. code-block:: python

    # Control only one arm
    action = env.action_space.sample()
    # Get current joint positions from observation
    n_joints = len(env.robot.qpos)
    current_qpos = obs["proprioception"][:n_joints]
    
    action[:7] = desired_left_arm_pos
    action[7:14] = current_qpos[7:14]  # Keep right arm fixed

Best Practices
--------------

1. **Use absolute mode** for replaying demonstrations
2. **Use delta mode** for smoother learning policies
3. **Match control frequency** to action mode (20 Hz for demos, higher for RL)
4. **Enable floating base** only if needed (adds action dimensions)
5. **Clip actions** when using delta mode to prevent large jumps
6. **Normalize actions** to [-1, 1] for neural network policies

Troubleshooting
---------------

**Action space mismatch:**

.. code-block:: python

    # Check action space
    print(env.action_space)
    
    # Ensure action matches
    action = env.action_space.sample()

**Robot moves erratically:**

- Reduce control frequency
- Use smaller deltas in delta mode
- Check action normalization

**Cannot reproduce demonstrations:**

- Verify action mode matches demo collection settings
- Check floating_base configuration
- Ensure control_frequency matches

Next Steps
----------

- Configure :doc:`observations` for your task
- Learn about :doc:`data-collection` with different action modes
- Explore :doc:`demonstrations` replay and conversion
- See :doc:`../advanced/custom-tasks` for implementing custom action modes
