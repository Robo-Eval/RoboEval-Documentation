Data Collection
===============

RoboEval provides tools for collecting high-quality demonstrations using keyboard or VR teleoperation.

Keyboard Teleoperation
----------------------

Collect demonstrations using keyboard controls:

.. code-block:: bash

    python examples/6_collect_data.py

**Left Arm Controls:**

- **A/D**: Left/Right (X-axis)
- **Z/C**: Forward/Backward (Y-axis)
- **W/S**: Up/Down (Z-axis)
- **V**: Gripper open/close

**Right Arm Controls:**

- **J/L**: Left/Right (X-axis)
- **U/O**: Forward/Backward (Y-axis)
- **I/K**: Up/Down (Z-axis)
- **B**: Gripper open/close

**Recording Controls:**

- **R**: Start recording demonstration (resets environment)
- **X**: Save and stop current demonstration
- **T**: Toggle position/orientation control modes
- **G**: Toggle gripper mode (autoclose vs hold-to-close)
- **ESC**: Exit

VR Teleoperation
----------------

High-quality data collection with Oculus Quest:

**Prerequisites:**

- Oculus Quest headset (Quest 2, Quest Pro, or Quest 3)
- USB-C cable for connection
- Developer mode enabled on Oculus Quest
- ADB installed and configured

**Setup:**

1. Enable Developer Mode on Oculus Quest (via Oculus app on phone)
2. Connect Oculus Quest to computer via USB-C
3. Allow USB debugging when prompted in headset
4. Install VR dependencies:

.. code-block:: bash

    pip install -e ".[vr]"

5. Verify connection:

.. code-block:: bash

    adb devices  # Should show your Quest device

**Run data collection:**

.. code-block:: bash

    python examples/7_collect_data_oculus.py

**Controller Mapping:**

**Left Controller:**
    - **Position/Rotation**: Physical hand position/rotation controls left end-effector
    - **Trigger**: Squeeze to close gripper, release to open

**Right Controller:**
    - **Position/Rotation**: Physical hand position/rotation controls right end-effector
    - **Trigger**: Squeeze to close gripper, release to open

**Button Controls:**
    - **A Button**: Start recording demonstration
    - **B Button**: Save current demonstration
    - **Y Button**: Toggle gripper autoclose mode

Custom Data Collection
----------------------

Create your own data collection script:

.. code-block:: python

    from pathlib import Path
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    from roboeval.data_collection.keyboard_input import KeyboardTeleop
    from roboeval.envs.manipulation import LiftPot
    
    # Set up keyboard teleoperation
    demo_dir = Path("./my_demos")
    demo_dir.mkdir(exist_ok=True)
    
    teleop = KeyboardTeleop(
        env_cls=LiftPot,
        action_mode=JointPositionActionMode(
            floating_base=True,
            absolute=True,
            floating_dofs=[]
        ),
        resolution=(900, 1000),
        demo_directory=demo_dir,
        robot_cls=BimanualPanda,
        config={"env": "Lift Pot", "robot": "Bimanual Panda"}
    )
    
    # Start teleoperation (blocks until exit)
    teleop.run()

Demonstration Storage
---------------------

Demonstrations are saved in a standardized format:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations import Demo
    
    # Save demonstration
    demo_store = DemoStore()
    demo_store.save_demo(demo, metadata)
    
    # Load demonstrations
    demos = demo_store.get_demos(metadata, amount=10)

Best Practices
--------------

1. **Use control_frequency=20** for consistency with dataset
2. **Record multiple attempts** for diversity
3. **Save failed attempts** for negative examples
4. **Add metadata** (task, robot, timestamp)

Next Steps
----------

- Work with :doc:`demonstrations`
- Learn about :doc:`../advanced/metrics` for tracking custom metrics
