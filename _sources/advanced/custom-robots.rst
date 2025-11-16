Custom Robots
=============

Configure or add custom robot configurations to RoboEval.

Available Robots
----------------

**BimanualPanda** (Default)
    Two Franka Panda arms with Franka Hand grippers

**SinglePanda**
    Single Franka Panda arm with Franka Hand gripper

Using Robots
------------

.. code-block:: python

    from roboeval.robots.configs.panda import BimanualPanda, SinglePanda
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    
    # Use BimanualPanda (default)
    env = LiftPot(
        robot_cls=BimanualPanda,
        action_mode=JointPositionActionMode()
    )
    
    # Use SinglePanda
    env = LiftPot(
        robot_cls=SinglePanda,
        action_mode=JointPositionActionMode()
    )

Creating a Custom Robot
-----------------------

To create a custom robot, you need to define three main components:

1. **Robot Configuration Components**
2. **RobotConfig Class**
3. **Robot Class**

Step 1: Define Configuration Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create arm, gripper, and base configurations:

.. code-block:: python

    from roboeval.robots.config import ArmConfig, GripperConfig, FloatingBaseConfig, RobotConfig, RobotIKConfig
    from roboeval.const import THIRD_PARTY_PATH, HandSide
    import numpy as np
    
    # Define arm configuration
    MY_ARM = ArmConfig(
        site="attachment_site",  # Site where gripper attaches
        links=["link0", "link1", "link2", ...],  # Body links in order
        model=THIRD_PARTY_PATH / "path/to/arm_model.xml",
        joints=["joint1", "joint2", ...],  # Joint names
        actuators=["actuator1", "actuator2", ...],  # Actuator names
        wrist_dof=None,  # Optional wrist DOF
    )
    
    # Define gripper configuration
    MY_GRIPPER = GripperConfig(
        model=THIRD_PARTY_PATH / "path/to/gripper_model.xml",
        actuators=["gripper_actuator"],
        range=np.array([0, 1]),  # Control range
        pad_bodies=["left_pad", "right_pad"],  # Contact bodies
        reverse_control=False,  # Whether to reverse control
        discrete=True,  # Round to min/max
    )
    
    # Define floating base (or fixed base)
    MY_FLOATING_BASE = FloatingBaseConfig(
        dofs=[],  # Empty for fixed base
        delta_range_position=(-0.01, 0.01),
        delta_range_rotation=(-0.05, 0.05),
        offset_position=np.array([0, 0, 0]),
    )

Step 2: Create RobotConfig
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combine components into a RobotConfig:

.. code-block:: python

    MY_ROBOT_CONFIG = RobotConfig(
        delta_range=(-0.1, 0.1),  # Action delta range
        position_kp=4500,  # Position control stiffness
        pelvis_body=None,  # Base body name (None for fixed)
        floating_base=MY_FLOATING_BASE,
        gripper=MY_GRIPPER,
        arms={
            HandSide.LEFT: MY_ARM,
            HandSide.RIGHT: MY_ARM  # Or None for single arm
        },
        arm_offset={
            HandSide.LEFT: np.array([0., 0.3, 0.6]),
            HandSide.RIGHT: np.array([0., -0.3, 0.6])
        },
        arm_offset_euler={
            HandSide.LEFT: np.array([0, 0, 0]),
            HandSide.RIGHT: np.array([0, 0, 0])
        },
        actuators={
            "actuator1": True,
            "actuator2": True,
            # ... list all actuators
        },
        cameras={  # Optional camera configurations
            "head": {
                "manual": True,
                "parent": "base_link",
                "position": (0, 0, 1.5),
                "quaternion": (1, 0, 0, 0),
                "fov": 60,
            }
        },
        namespaces_to_remove=['key'],  # XML namespaces to clean
        model_name="My Custom Robot",
    )

Step 3: Create IK Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define inverse kinematics configuration:

.. code-block:: python

    def create_my_robot_ik_config() -> RobotIKConfig:
        """Create IK config for custom robot."""
        return RobotIKConfig(
            robot_prefix="",
            root_body_name="base_link",
            torso_name="base_link",
            arm_roots=[
                "left_arm\\link0",
                "right_arm\\link0",
            ],
            arm_sites=[
                "left_arm\\attachment_site",
                "right_arm\\attachment_site",
            ],
            joint_limits={
                "left_arm/joint1": (-2.8973, 2.8973),
                "left_arm/joint2": (-1.7628, 1.7628),
                # ... define all joint limits
            },
            end_effector_exclude_word="finger",  # Exclude gripper joints
            kp=1000,  # Position gain
            solver_max_steps=40,  # Max IK iterations
        )

Step 4: Define Robot Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a Robot subclass:

.. code-block:: python

    from roboeval.robots.robot import Robot
    
    class MyCustomRobot(Robot):
        """My custom robot implementation."""
    
        @property
        def ik_config(self) -> RobotIKConfig:
            """Get robot IK configuration."""
            return create_my_robot_ik_config()
    
        @property
        def config(self) -> RobotConfig:
            """Get robot configuration."""
            return MY_ROBOT_CONFIG

Step 5: Use Your Robot
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    
    env = LiftPot(robot_cls=MyCustomRobot)

Complete Example: Bimanual Panda
---------------------------------

For reference, here's how the BimanualPanda robot is structured in ``roboeval/robots/configs/panda.py``:

.. code-block:: python

    class BimanualPanda(Robot):
        """Panda Robot with two arms."""
    
        @property
        def ik_config(self) -> RobotIKConfig:
            """Get robot IK config."""
            return create_bimanual_panda_config()
    
        @property
        def config(self) -> RobotConfig:
            """Get robot config."""
            return PANDA_CONFIG_WITH_PANDA_GRIPPER

The configuration uses:
- Franka Panda arms from MuJoCo Menagerie
- Franka Hand grippers
- Fixed base (no floating DOFs)
- Dual arm setup with symmetric offsets
- Camera configurations for head and wrist views

Required Files
--------------

To add a robot, you'll need:

1. **Robot XML/URDF Model**: MuJoCo XML or URDF file defining the robot
2. **Gripper Model**: Separate model for gripper if not embedded
3. **Configuration File**: Python file in ``roboeval/robots/configs/``
4. **Assets**: Meshes, textures in appropriate directories

Tips for Robot Integration
---------------------------

**Joint and Actuator Names:**
    - Must match names in your XML/URDF model exactly
    - Check with: ``mujoco.viewer`` or ``print(model.joint_names)``

**Coordinate Frames:**
    - RoboEval uses MuJoCo's convention (Z-up)
    - Arm offsets are in world frame
    - Quaternions are (w, x, y, z) format

**Testing:**
    - Start with a simple environment like ``LiftPot``
    - Verify joint limits don't cause collisions
    - Test both absolute and delta action modes

**Camera Setup:**
    - Define multiple viewpoints for observation
    - Wrist cameras useful for manipulation tasks
    - External cameras for full scene view

Testing Custom Robots
----------------------

RoboEval provides a comprehensive test script to validate custom robot implementations. The test script is available at ``examples/test_custom_robot.py`` and includes automated tests for:

- Robot configuration validation
- Environment integration
- All action modes (absolute/delta × joint/EE)
- Observation space structure
- Rendering (optional)

Running the Test Script
~~~~~~~~~~~~~~~~~~~~~~~

To test your custom robot:

.. code-block:: python

    from roboeval.robots.configs.my_robot import MyCustomRobot
    from examples.test_custom_robot import run_all_tests
    
    # Run full test suite
    run_all_tests(MyCustomRobot)

The script automatically detects:

- Number of arms (single-arm vs bimanual)
- Floating base configuration
- Appropriate test environment based on robot capabilities

Test Coverage
~~~~~~~~~~~~~

**Configuration Tests:**
    - Validates ``config`` and ``ik_config`` properties
    - Checks arm, gripper, and base configurations
    - Verifies joint limits and actuator definitions
    - Validates camera setup

**Environment Integration Tests:**
    - Tests robot in all 4 action modes:
        * Absolute Joint Control
        * Delta Joint Control
        * Absolute End-Effector Control
        * Delta End-Effector Control
    - Validates environment reset and step
    - Checks action and observation spaces
    - Runs multiple episode rollouts

**Observation Tests:**
    - Validates observation dictionary structure
    - Checks all observation keys and shapes
    - Verifies data types and dimensions

**Rendering Tests (Optional):**
    - Tests human rendering mode
    - Validates RGB array rendering
    - Checks frame dimensions

Example Test Output
~~~~~~~~~~~~~~~~~~~

When testing BimanualPanda, you'll see output like:

.. code-block:: text

    ============================================================
    Testing BimanualPanda Configuration
    ============================================================
    
    ✓ Testing config property...
      - Model name: Panda Robot
      - Arms: [<HandSide.LEFT: 0>, <HandSide.RIGHT: 1>]
      - Gripper: panda_hand.xml
    
    ✓ Testing ik_config property...
      - Arm roots: ['left_arm\\panda0_link0', 'right_arm\\panda0_link0']
      - Arm sites: ['left_arm\\attachment_site', 'right_arm\\attachment_site']
      - Joint limits defined: 14 joints
    
    ✓ Testing arm configuration...
      - LEFT arm:
        • Model: panda_nohand.xml
        • Joints: 7 joints
        • Actuators: 7 actuators
        • Links: 9 links
      - RIGHT arm:
        • Model: panda_nohand.xml
        • Joints: 7 joints
        • Actuators: 7 actuators
        • Links: 9 links
    
    ============================================================
    ✓ BimanualPanda configuration tests passed!
    ============================================================

Individual Test Functions
~~~~~~~~~~~~~~~~~~~~~~~~~

You can also run specific tests:

.. code-block:: python

    from examples.test_custom_robot import (
        test_robot_configuration,
        test_robot_in_environment,
        test_robot_observations,
        test_robot_rendering
    )
    
    # Test only configuration
    test_robot_configuration(MyCustomRobot)
    
    # Test in specific environment
    from roboeval.envs.lift_pot import LiftPot
    test_robot_in_environment(MyCustomRobot, env_cls=LiftPot)
    
    # Test observations
    test_robot_observations(MyCustomRobot)
    
    # Test rendering (can be slow)
    test_robot_rendering(MyCustomRobot)

Troubleshooting Failed Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Configuration Errors:**
    - Verify all joint/actuator names match XML model
    - Check that arm sites and roots exist in model
    - Ensure joint limits are within physical bounds

**Environment Integration Errors:**
    - Confirm robot has required DOFs for task
    - Single-arm robots need single-arm tasks
    - Bimanual robots can use both single and dual-arm tasks

**Action Mode Errors:**
    - EE control requires proper IK configuration
    - Joint limits must allow collision-free movement
    - Delta ranges should be appropriate for control frequency

**Observation Errors:**
    - Check camera configurations are valid
    - Verify sensor sites exist in model
    - Ensure observation keys match expected structure

Using Test Script as Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The test script can serve as a template for your own validation:

1. Copy ``examples/test_custom_robot.py`` to your project
2. Modify ``run_all_tests()`` to add custom checks
3. Add domain-specific validation tests
4. Create regression tests for known issues

The script's ``get_test_env_for_robot()`` function shows how to automatically select appropriate environments based on robot capabilities, which is useful for building flexible robot configurations.

See Also
--------

- :doc:`custom-tasks` - Use robots in custom tasks
- ``examples/test_custom_robot.py`` - Comprehensive robot testing script
- MuJoCo Menagerie for pre-built robot models
- ``roboeval/robots/configs/panda.py`` - Complete reference implementation
