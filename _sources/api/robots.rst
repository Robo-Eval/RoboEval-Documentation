Robots API
==========

Robot configuration classes and base robot class.

BimanualPanda
-------------

.. autoclass:: roboeval.robots.configs.panda.BimanualPanda
   :members:
   :undoc-members:
   :show-inheritance:

   Two Franka Panda arms with parallel-jaw grippers, mounted on a floating base.

   **Specifications:**

   - DOF: 14 (7 per arm)
   - Grippers: 2 parallel-jaw (Franka Hand)
   - Workspace: ~1m radius per arm
   - Max payload: ~3kg per arm

   **Example:**

   .. code-block:: python

       from roboeval.robots.configs.panda import BimanualPanda
       from roboeval.envs.lift_pot import LiftPot
       
       env = LiftPot(robot_cls=BimanualPanda)

SinglePanda
-----------

.. autoclass:: roboeval.robots.configs.panda.SinglePanda
   :members:
   :undoc-members:
   :show-inheritance:

   Single Franka Panda arm with parallel-jaw gripper on a floating base.

   **Specifications:**

   - DOF: 7
   - Gripper: 1 parallel-jaw (Franka Hand)
   - Workspace: ~1m radius
   - Max payload: ~3kg

   **Example:**

   .. code-block:: python

       from roboeval.robots.configs.panda import SinglePanda
       from roboeval.envs.lift_pot import LiftPot
       
       env = LiftPot(robot_cls=SinglePanda)

Robot Base Class
----------------

.. autoclass:: roboeval.robots.robot.Robot
   :members:
   :undoc-members:
   :show-inheritance:

   Abstract base class for all robots in RoboEval. Handles robot creation, kinematics, actuator setup, and control.

   **Key Properties:**

   - ``config``: Robot configuration (``RobotConfig``)
   - ``action_mode``: Action mode defining control interface
   - ``grippers``: Dictionary mapping hand side to gripper instances
   - ``floating_base``: Floating base instance (if enabled)
   - ``qpos``: Current joint positions
   - ``qvel``: Current joint velocities
   - ``qpos_actuated``: Actuated joint positions
   - ``qvel_actuated``: Actuated joint velocities
   - ``qpos_grippers``: Gripper joint positions
   - ``qpos_initial``: Initial joint positions
   - ``pelvis``: Pelvis body element
   - ``limb_actuators``: List of limb actuators
   - ``cameras``: List of camera elements

   **Key Methods:**

   - ``forward_kinematics(joint_positions)``: Compute end-effector poses from joint positions
   - ``inverse_kinematics(...)``: Compute joint positions from end-effector poses
   - ``get_hand_pos(side)``: Get hand position for specified side
   - ``is_gripper_holding_object(geom, side, ...)``: Check if gripper is holding an object
   - ``set_pose(position, orientation)``: Set robot base pose
   - ``reset_pose()``: Reset robot to initial pose
   - ``get_limb_control_range(scale)``: Get limb control range with scaling
   - ``get_initial_joint_positions()``: Get initial joint configuration
   - ``get_keyframes(name_identifier)``: Get keyframe by name
   - ``load_keyframe_from_xml(xml_path, keyframe_name, keyframe_index)``: Load keyframe from XML

RobotConfig
-----------

.. autoclass:: roboeval.robots.config.RobotConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration dataclass for robot specifications.

   **Attributes:**

   - ``name`` (``str``): Robot name
   - ``arms`` (``dict[HandSide, ArmConfig]``): Arm configurations
   - ``model`` (``Optional[Path]``): Path to robot model file
   - ``floating_base_enabled`` (``bool``): Whether floating base is enabled

ArmConfig
---------

.. autoclass:: roboeval.robots.config.ArmConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Configuration dataclass for robot arm specifications.

   **Attributes:**

   - ``side`` (``HandSide``): Arm side (LEFT or RIGHT)
   - ``model_path`` (``Path``): Path to arm model
   - ``gripper_model_path`` (``Path``): Path to gripper model
   - ``initial_qpos`` (``list[float]``): Initial joint positions

See Also
--------

- :doc:`../advanced/custom-robots` - Creating custom robot configurations
- :doc:`core` - Core RoboEval API

