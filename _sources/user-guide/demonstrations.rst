Demonstrations
==============

Work with RoboEval's demonstration dataset and tools.

Loading Demonstrations
-----------------------

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    from roboeval.envs.lift_pot import LiftPot
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    
    # Create metadata for task
    metadata = Metadata.from_env(env)
    
    # Load demonstrations
    demo_store = DemoStore()
    demos = demo_store.get_demos(
        metadata=metadata,
        amount=100,
        frequency=20
    )

Replaying Demonstrations
-------------------------

.. code-block:: python

    from roboeval.demonstrations.demo_player import DemoPlayer
    
    player = DemoPlayer()
    
    for demo in demos:
        print(f"Replaying: {demo.uuid}")
        player.replay_in_env(demo, env, demo_frequency=20)

Converting Demonstrations
--------------------------

Convert between action representations:

.. code-block:: python

    from roboeval.demonstrations.demo_converter import DemoConverter
    
    converter = DemoConverter()
    
    # Convert from absolute to delta actions
    delta_demo = converter.absolute_to_delta(demo)
    
    # Convert from joint positions to end-effector control
    ee_demo = converter.joint_to_ee(demo)
    
    # Convert from delta to absolute actions  
    absolute_demo = converter.delta_to_absolute(demo)

**Note:** For converting to LeRobot or RLDS formats, see the conversion scripts in the examples directory.

Demonstration Structure
-----------------------

Each demonstration contains:

.. code-block:: python

    demo = Demo(
        metadata=Metadata(...),  # Task/robot/environment info
        timesteps=[...]          # List of DemoStep objects
    )
    
    # Access demo properties
    demo.uuid          # Unique identifier
    demo.seed          # Environment seed
    demo.timesteps     # List of timesteps
    demo.metadata      # Metadata object
    
    # Each timestep contains:
    timestep = demo.timesteps[0]
    timestep.observation         # Observation dict
    timestep.executed_action     # Action taken
    timestep.reward              # Reward received
    timestep.terminated          # Episode terminated
    timestep.truncated           # Episode truncated

Filtering Demonstrations
------------------------

.. code-block:: python

    # Filter successful demonstrations
    successful_demos = []
    for demo in demos:
        # Check last timestep
        if demo.timesteps and not demo.timesteps[-1].terminated:
            continue
        # Check if task was successful (from metadata or info)
        successful_demos.append(demo)
    
    # Load demos for specific metadata
    from roboeval.demonstrations.utils import Metadata
    from roboeval.envs.lift_pot import LiftPotPosition
    
    env = LiftPotPosition(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    metadata = Metadata.from_env(env)
    position_demos = demo_store.get_demos(metadata, amount=50, frequency=20)

Best Practices
--------------

1. **Match control frequency** when replaying
2. **Cache converted datasets** for faster loading
3. **Use metadata** for filtering and organization

Next Steps
----------

- Explore :doc:`../tasks/index`
- Learn about :doc:`../advanced/metrics`
