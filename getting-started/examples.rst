Examples
========

RoboEval includes seven example scripts to help you get started. These examples are located in the ``examples/`` directory and demonstrate key functionalities from basic demo replay to VR data collection.

Example 1: Data Replay
----------------------

**File:** ``examples/1_data_replay.py``

**Purpose:** Demonstrates how to load and replay demonstrations from the DemoStore.

This example shows the complete workflow for loading pre-recorded demonstrations and replaying them in an environment. It uses the ``PickSingleBookFromTablePositionAndOrientation`` task with joint position control mode.

**Key Features:**

- Loading demos from DemoStore using metadata matching
- Setting up observation config with external camera
- Replaying demonstrations with DemoPlayer
- Visual rendering of the replay

**Code Overview:**

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    from roboeval.demonstrations.demo_player import DemoPlayer
    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    from roboeval.envs.stack_books import PickSingleBookFromTablePositionAndOrientation
    from roboeval.robots.configs.panda import BimanualPanda
    from roboeval.utils.observation_config import ObservationConfig, CameraConfig
    
    # Create environment with camera observations
    env = PickSingleBookFromTablePositionAndOrientation(
        action_mode=JointPositionActionMode(floating_base=True, absolute=True, floating_dofs=[]),
        render_mode="human",
        control_frequency=20,
        robot_cls=BimanualPanda,
        observation_config=ObservationConfig(
            cameras=[CameraConfig(name="external", rgb=True, resolution=(128, 128))]
        ),
    )
    
    # Get demonstrations from DemoStore
    metadata = Metadata.from_env(env)
    demos = DemoStore().get_demos(metadata, amount=100, frequency=20)
    
    # Replay demonstrations
    for demo in demos:
        DemoPlayer().replay_in_env(demo, env, demo_frequency=20)

**Run it:**

.. code-block:: bash

    python examples/1_data_replay.py

Example 2: Convert and Replay
------------------------------

**File:** ``examples/2_convert_and_replay.py``

**Purpose:** Demonstrates recording a demonstration with sinusoidal motion, converting it between different action modes, and replaying it.

This example shows the complete action mode conversion pipeline, including recording a demo in absolute joint position mode, converting it to different action modes (EE mode, delta mode), and replaying with trajectory visualization.

**Key Features:**

- Recording demonstrations with DemoRecorder
- Converting between action modes using DemoConverter
- Comparing requested vs. actual trajectories
- Visualization of joint positions or end-effector positions
- Support for absolute/delta and joint/EE action modes

**Conversion Options:**

- Joint absolute to EE absolute: ``DemoConverter.joint_to_ee()``
- Absolute to delta: ``DemoConverter.absolute_to_delta()``
- Joint absolute to EE delta: ``DemoConverter.joint_absolute_to_ee_delta()``

**Code Overview:**

.. code-block:: python

    import tempfile
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.demonstrations.demo import Demo
    from roboeval.demonstrations.demo_converter import DemoConverter
    from roboeval.demonstrations.demo_recorder import DemoRecorder
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.robots.configs.panda import BimanualPanda
    
    # Create environment for recording
    env = LiftPot(
        action_mode=JointPositionActionMode(floating_base=True, absolute=True, floating_dofs=[]),
        render_mode="human",
        robot_cls=BimanualPanda,
    )
    
    with tempfile.TemporaryDirectory() as temp_dir:
        demo_recorder = DemoRecorder(temp_dir)
        
        # Record demo with sinusoidal motion
        env.reset()
        demo_recorder.record(env)
        for i in range(500):
            action[0] = amplitude * np.sin(frequency * i)
            timestep = env.step(action)
            demo_recorder.add_timestep(timestep, action)
        
        demo_recorder.stop()
        demo = Demo.from_safetensors(demo_recorder.save_demo())
        
        # Convert to different action mode
        demo = DemoConverter.joint_to_ee(demo)  # Example conversion
        
        # Replay and visualize trajectories
        env = LiftPot(
            action_mode=JointPositionActionMode(floating_base=True, absolute=True, ee=True),
            robot_cls=BimanualPanda,
        )
        # ... replay and plot

**Run it:**

.. code-block:: bash

    python examples/2_convert_and_replay.py

Example 3: Load, Convert, and Replay
-------------------------------------

**File:** ``examples/3_load_convert_replay.py``

**Purpose:** Complete pipeline combining demo loading from DemoStore with action mode conversion for replay.

This example combines the functionality from Examples 1 and 2, showing how to load demonstrations from the DemoStore and convert them to different action modes before replaying. This is particularly useful when you have demos in one format but need them in another.

**Key Features:**

- Loading lightweight demos from DemoStore (absolute joint mode)
- Converting to target action modes (joint/EE, absolute/delta)
- Automatic conversion path selection based on target mode
- Trajectory comparison and visualization
- Support for all 4 action mode combinations

**Action Mode Configurations:**

- ``joint_absolute``: Standard joint position control
- ``joint_delta``: Delta joint positions
- ``ee_absolute``: End-effector position control
- ``ee_delta``: Delta end-effector positions

**Code Overview:**

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    from roboeval.demonstrations.demo_converter import DemoConverter
    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    from roboeval.envs.stack_books import PickSingleBookFromTablePositionAndOrientation
    
    # Create environment with target action mode
    env = PickSingleBookFromTablePositionAndOrientation(
        action_mode=JointPositionActionMode(floating_base=True, absolute=False, floating_dofs=[]),
        robot_cls=BimanualPanda,
    )
    
    # Load lightweight demos (always in joint absolute mode)
    metadata = Metadata.from_env(env)
    metadata.observation_mode = ObservationMode.Lightweight
    demos = DemoStore().get_demos(metadata, amount=5, frequency=20)
    
    # Convert to target action mode
    converted_demos = []
    for demo in demos:
        if target_is_ee_absolute:
            converted_demo = DemoConverter.joint_to_ee(demo)
        elif target_is_ee_delta:
            converted_demo = DemoConverter.joint_absolute_to_ee_delta(demo)
        elif target_is_joint_delta:
            converted_demo = DemoConverter.absolute_to_delta(demo)
        converted_demos.append(converted_demo)
    
    # Replay converted demos
    for demo in converted_demos:
        # ... replay

**Run it:**

.. code-block:: bash

    python examples/3_load_convert_replay.py

Example 4: Evaluate OpenVLA
---------------------------

**File:** ``examples/4_eval_openvla.py``

**Purpose:** Evaluate OpenVLA vision-language-action models on RoboEval bimanual tasks.

This comprehensive example demonstrates how to run OpenVLA models on RoboEval tasks, supporting both model inference and demonstration replay modes. It includes proper model loading, action prediction, video recording, and metric computation.

**Prerequisites:**

.. code-block:: bash

    pip install -e ".[examples]"  # Includes transformers, torch, prismatic, etc.

**Key Features:**

- Loading OpenVLA models from checkpoint
- Vision-language-action prediction with camera observations
- Video recording of rollouts
- Support for custom task instructions
- Configurable control frequency downsampling
- Metric tracking and reporting

**Command-Line Arguments:**

- ``--ckpt_path``: Path to OpenVLA model checkpoint (required)
- ``--dataset_path``: Path to demonstration dataset (for replay mode)
- ``--use_demos``: Use demonstration replay instead of model inference
- ``--instruction``: Task instruction for the robot
- ``--device``: Device for model inference (default: cuda:0)
- ``--downsample_rate``: Control frequency downsampling (default: 25)
- ``--max_steps``: Maximum steps per episode (default: 200)
- ``--num_episodes``: Number of episodes to run (default: 5)
- ``--fps``: FPS for output videos (default: 5)
- ``--output_dir``: Output directory for videos

**Usage Examples:**

.. code-block:: bash

    # Model inference mode
    python examples/4_eval_openvla.py --ckpt_path /path/to/model/checkpoint
    
    # Demonstration replay mode
    python examples/4_eval_openvla.py --ckpt_path /path/to/model/checkpoint \
                                       --use_demos --dataset_path /path/to/demos
    
    # Custom configuration
    python examples/4_eval_openvla.py --ckpt_path /path/to/checkpoint \
                                       --instruction "pick up the red object" \
                                       --num_episodes 10 --max_steps 300

**Code Overview:**

.. code-block:: python

    import argparse
    from transformers import AutoModelForVision2Seq
    from prismatic.extern.hf.modeling_prismatic import OpenVLAForActionPrediction
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.robots.configs.panda import BimanualPanda
    
    # Parse arguments and create config
    config = EvaluationConfig.from_args(parse_arguments())
    
    # Load OpenVLA model
    model = OpenVLAForActionPrediction.from_pretrained(
        config.ckpt_path,
        device_map=config.device
    )
    
    # Create environment
    env = LiftPot(
        action_mode=JointPositionActionMode(floating_base=True, absolute=True),
        robot_cls=BimanualPanda,
        control_frequency=CONTROL_FREQUENCY_MAX // config.downsample_rate,
    )
    
    # Run evaluation episodes
    for episode in range(config.num_episodes):
        obs, info = env.reset()
        for step in range(config.max_steps):
            # Get action from model
            action = model.predict_action(obs["rgb_external"], config.instruction)
            obs, reward, terminated, truncated, info = env.step(action)

**Run it:**

.. code-block:: bash

    python examples/4_eval_openvla.py --ckpt_path /path/to/checkpoint

Example 5: Gather Metrics
-------------------------

**File:** ``examples/5_gather_metrics.py``

**Purpose:** Comprehensive script for loading demonstrations and computing detailed metrics.

This utility script provides extensive functionality for analyzing demonstrations, including trajectory efficiency, coordination quality, success rates, and custom metrics. It can load demos from various sources and compute both demo-based and rollout-based metrics.

**Key Features:**

- Loading demos from multiple sources (files, directories, DemoStore)
- Computing trajectory efficiency metrics
- Analyzing bimanual coordination quality
- Rollout-based success rate computation
- Statistical summaries and reports
- Support for batch processing multiple tasks

**Loading Options:**

- ``--demos_dir``: Load all demos from a directory
- ``--demo_files``: Load specific demo files
- ``--use_demo_store``: Load from DemoStore with metadata filtering
- ``--dataset_path``: Path to demonstration dataset

**Metric Types:**

- Demo-based metrics (from recorded data)
- Rollout metrics (replay in environment)
- Task-specific metrics (defined by environment)
- Coordination metrics (bimanual synchronization)

**Usage Examples:**

.. code-block:: bash

    # Load demos from directory and compute metrics
    python examples/5_gather_metrics.py --demos_dir /path/to/demos --env_name LiftPot
    
    # Load from DemoStore and analyze
    python examples/5_gather_metrics.py --use_demo_store --env_name LiftPot --amount 50
    
    # Compute metrics from specific files
    python examples/5_gather_metrics.py --demo_files demo1.safetensors demo2.safetensors
    
    # Generate detailed report
    python examples/5_gather_metrics.py --demos_dir /path/to/demos \
                                         --output_report metrics_report.json

**Code Overview:**

.. code-block:: python

    from roboeval.demonstrations.demo import Demo
    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.demo_player import DemoPlayer
    from roboeval.utils.metric_rollout import MetricRolloutEval
    from tools.shared.utils import ENVIRONMENTS
    
    class DemoMetricsComputer:
        """Comprehensive demo loading and metrics computation."""
        
        def __init__(self):
            self.demo_store = DemoStore()
            
        def create_environment(self, env_name: str):
            """Create environment for metric computation."""
            env_class = ENVIRONMENTS[env_name]
            env = env_class(
                action_mode=JointPositionActionMode(floating_base=True, absolute=True),
                robot_cls=BimanualPanda,
            )
            return env
        
        def compute_metrics(self, demos: List[Demo], env: RoboEvalEnv):
            """Compute metrics from demonstrations."""
            # Replay demos and collect metrics
            for demo in demos:
                DemoPlayer().replay_in_env(demo, env)
                if isinstance(env, MetricRolloutEval):
                    metrics = env.get_metrics()
            return metrics

**Run it:**

.. code-block:: bash

    python examples/5_gather_metrics.py --use_demo_store --env_name LiftPot

Example 6: Data Collection (Keyboard)
--------------------------------------

**File:** ``examples/6_collect_data.py``

**Purpose:** Collect demonstrations using keyboard-based teleoperation.

This example sets up keyboard teleoperation for collecting bimanual demonstrations with the Franka Panda robot. It provides an intuitive control scheme for both arms and includes recording capabilities.

**Key Features:**

- Keyboard-based bimanual control
- Demonstration recording with DemoRecorder
- Multiple control modes (position/orientation)
- Gripper control (autoclose or manual)
- Demo replay verification

**Keyboard Controls:**

**Left Arm Movement:**

- A/D: Left/Right (X-axis)
- Z/C: Forward/Backward (Y-axis)
- W/S: Up/Down (Z-axis)
- V: Gripper open/close

**Right Arm Movement:**

- J/L: Left/Right (X-axis)
- U/O: Forward/Backward (Y-axis)
- I/K: Up/Down (Z-axis)
- B: Gripper open/close

**Recording Controls:**

- R: Start/stop recording demonstration
- X: Save current demonstration
- T: Toggle between position/orientation control modes
- G: Toggle gripper mode (autoclose vs hold-to-close)
- ESC: Exit

**Code Overview:**

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    from roboeval.data_collection.keyboard_input import KeyboardTeleop
    from roboeval.demonstrations.demo_recorder import DemoRecorder
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.robots.configs.panda import BimanualPanda
    
    # Set up keyboard teleoperation
    teleop = KeyboardTeleop(
        env_cls=LiftPot,
        action_mode=JointPositionActionMode(floating_base=True, absolute=True, floating_dofs=[]),
        resolution=(900, 1000),
        demo_directory="./demonstrations",
        robot_cls=BimanualPanda,
        config={"env": "Lift Pot", "robot": "Bimanual Panda"}
    )
    
    # Run teleoperation interface
    teleop.run()

**Run it:**

.. code-block:: bash

    python examples/6_collect_data.py

**Output:**

Demonstrations are saved to ``./demonstrations/`` directory in SafeTensors format.

Example 7: Data Collection (Oculus VR)
---------------------------------------

**File:** ``examples/7_collect_data_oculus.py``

**Purpose:** Collect high-quality demonstrations using Oculus Quest VR teleoperation.

This example provides immersive VR-based data collection where your hand movements are directly mapped to the robot's end-effectors. This creates more natural and intuitive demonstrations compared to keyboard control.

**Prerequisites:**

- Oculus Quest headset (Quest 2, Quest Pro, or Quest 3)
- USB-C cable for connecting headset to computer
- Developer mode enabled on Oculus Quest
- ADB installed and configured

**Installation:**

.. code-block:: bash

    # Install VR dependencies
    pip install -e ".[vr]"
    
    # Enable Developer Mode on Oculus Quest:
    # 1. Open Oculus app on phone
    # 2. Go to Settings > Developer Mode
    # 3. Toggle Developer Mode ON
    
    # Connect Quest via USB-C and verify:
    adb devices

**VR Controls (in headset):**

**Left Controller:**

- Position: Physical hand position controls left gripper position
- Rotation: Physical hand rotation controls left gripper orientation
- Trigger: Squeeze to close gripper, release to open

**Right Controller:**

- Position: Physical hand position controls right gripper position
- Rotation: Physical hand rotation controls right gripper orientation
- Trigger: Squeeze to close gripper, release to open

**Recording Controls:**

- A Button (right controller): Start/stop recording demonstration
- B Button (right controller): Save current demonstration
- X Button (left controller): Reset environment
- Y Button (left controller): Toggle gripper autoclose mode
- Thumbstick: Adjust robot base position (if floating base enabled)

**Code Overview:**

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    from roboeval.data_collection.oculus_input import OculusTeleop
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.robots.configs.panda import BimanualPanda
    
    # Set up Oculus VR teleoperation
    teleop = OculusTeleop(
        env_cls=LiftPot,
        action_mode=JointPositionActionMode(floating_base=True, absolute=True),
        robot_cls=BimanualPanda,
        demo_directory="./vr_demonstrations"
    )
    
    # Run VR teleoperation interface
    teleop.run()

**Run it:**

.. code-block:: bash

    python examples/7_collect_data_oculus.py

**Output:**

High-quality demonstrations saved to ``./vr_demonstrations/`` directory with rich metadata including controller tracking data.

**Troubleshooting:**

- If ADB connection fails, try: ``adb kill-server && adb start-server``
- For GLIBC version errors, use Ubuntu 20.10+ or Docker with newer base image
- See ``roboeval/data_collection/README.md`` for detailed VR setup instructions

Quick Start Guide
-----------------

**For Beginners:**

1. **Start with Example 1** to understand demo loading and replay
2. **Try Example 6** to collect your own demonstrations with keyboard
3. **Run Example 2** to learn about action mode conversion
4. **Use Example 5** to analyze your collected demonstrations

**For Advanced Users:**

1. **Example 3** for complete conversion pipelines
2. **Example 4** for model evaluation workflows
3. **Example 7** for high-quality VR data collection

Running Examples in Sequence
-----------------------------

To run all examples (except VR which requires hardware):

.. code-block:: bash

    # Make sure you have all dependencies
    pip install -e ".[examples]"
    
    # Run demo replay examples
    python examples/1_data_replay.py
    python examples/2_convert_and_replay.py
    python examples/3_load_convert_replay.py
    
    # Run metrics example
    python examples/5_gather_metrics.py --use_demo_store --env_name LiftPot
    
    # Collect data with keyboard (interactive)
    python examples/6_collect_data.py

Additional Usage Patterns
--------------------------

**Batch Demo Conversion**

Convert multiple demos to different action modes:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.demo_converter import DemoConverter
    from roboeval.demonstrations.utils import Metadata, ObservationMode
    
    # Load lightweight demos (joint absolute mode)
    demo_store = DemoStore()
    metadata = Metadata(...)
    metadata.observation_mode = ObservationMode.Lightweight
    demos = demo_store.get_demos(metadata, amount=100)
    
    # Convert all to EE delta mode
    converted_demos = []
    for demo in demos:
        converted = DemoConverter.joint_absolute_to_ee_delta(demo)
        converted_demos.append(converted)

**Custom Environment Evaluation**

Evaluate a policy on a custom environment configuration:

.. code-block:: python

    from roboeval.envs.manipulation import StackTwoBlocks
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    def evaluate_policy(policy, num_episodes=100):
        env = StackTwoBlocks(
            action_mode=JointPositionActionMode(floating_base=True, absolute=True),
            robot_cls=BimanualPanda,
            control_frequency=20
        )
        
        successes = 0
        for episode in range(num_episodes):
            obs, info = env.reset()
            
            for step in range(1000):
                action = policy.predict(obs)
                obs, reward, terminated, truncated, info = env.step(action)
                
                if terminated or truncated:
                    if reward > 0.25:  # Success threshold
                        successes += 1
                    break
        
        return successes / num_episodes

**Loading Demos for Multiple Tasks**

Load and process demos across multiple task variations:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    from tools.shared.utils import ENVIRONMENTS
    
    demo_store = DemoStore()
    task_names = ['LiftPot', 'StackTwoBlocks', 'PackBox']
    
    for task_name in task_names:
        env_class = ENVIRONMENTS[task_name]
        env = env_class(robot_cls=BimanualPanda)
        
        metadata = Metadata.from_env(env)
        demos = demo_store.get_demos(metadata, amount=10, frequency=20)
        
        print(f"Loaded {len(demos)} demos for {task_name}")
        env.close()

Tips and Best Practices
------------------------

**Environment Setup:**

- Use ``render_mode="human"`` for visual debugging
- Set ``control_frequency=20`` for most tasks (matches demo frequency)
- Enable cameras only when needed to improve performance

**Demo Collection:**

- Start with keyboard (Example 6) before VR (Example 7)
- Save demonstrations with descriptive metadata
- Test replay immediately after collection to verify quality
- Use VR for tasks requiring precise bimanual coordination

**Action Mode Selection:**

- Use **joint absolute** for most applications (default in demos)
- Use **EE mode** for tasks requiring precise end-effector control
- Use **delta mode** for incremental control or model training
- Convert between modes as needed using DemoConverter

**Performance:**

- Disable rendering (``render_mode=None``) for batch processing
- Use lightweight observation mode when cameras aren't needed
- Monitor GPU usage during model evaluation
- Use multiprocessing for batch demo analysis

**Debugging:**

- Check ``info`` dict after each step for task-specific metrics
- Use ``env.get_metrics()`` if environment supports MetricRolloutEval
- Enable verbose logging in DemoStore and DemoPlayer
- Visualize trajectories with matplotlib (see Example 2)

Next Steps
----------

- Dive deeper into :doc:`../user-guide/environments`
- Learn about :doc:`../user-guide/data-collection`
- Explore :doc:`../tasks/index` for all available tasks
- Read :doc:`../advanced/custom-tasks` to create your own
