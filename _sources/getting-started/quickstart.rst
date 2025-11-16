Quick Start
===========

This guide will help you get started with RoboEval in just a few minutes.

Basic Environment Usage
-----------------------

Here's how to create and run a simple environment:

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    # Create environment
    env = LiftPot(
        action_mode=JointPositionActionMode(absolute=True),
        render_mode="human",
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    
    # Reset environment
    obs, info = env.reset()
    
    # Run episode
    for step in range(1000):
        # Sample random action
        action = env.action_space.sample()
        
        # Step environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            print(f"Episode finished after {step} steps")
            print(f"Success: {info.get('task_success', False)}")
            break
    
    env.close()

Understanding Observations
--------------------------

The observation space contains robot state information:

.. code-block:: python

    from roboeval.utils.observation_config import ObservationConfig, CameraConfig
    
    # Configure observations with camera
    obs_config = ObservationConfig(
        cameras=[
            CameraConfig(
                name="external",
                rgb=True,
                depth=False,
                resolution=(128, 128),
            )
        ],
        proprioception=True,
    )
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        observation_config=obs_config,
        robot_cls=BimanualPanda
    )
    
    obs, info = env.reset()
    
    # Access different observation components
    print("Proprioception (qpos+qvel):", obs["proprioception"].shape)
    print("Gripper positions:", obs["proprioception_grippers"].shape)
    if "external_rgb" in obs:
        print("Camera image shape:", obs["external_rgb"].shape)

Action Modes
------------

RoboEval supports joint position control for robot manipulation:

**Joint Position Control**

.. code-block:: python

    from roboeval.action_modes import JointPositionActionMode
    
    # Absolute joint positions
    action_mode = JointPositionActionMode(
        absolute=True,
        floating_base=False
    )
    
    # Delta (incremental) joint positions
    action_mode = JointPositionActionMode(
        absolute=False,
        floating_base=False
    )

**With Floating Base**

Enable floating base for robot mobility:

.. code-block:: python

    action_mode = JointPositionActionMode(
        floating_base=True,
        absolute=True,
        floating_dofs=[]  # Empty list allows all DOFs (x, y, z, roll, pitch, yaw)
    )

Task Variations
---------------

Most tasks have multiple variations with different randomization levels:

.. code-block:: python

    from roboeval.envs.lift_pot import (
        LiftPot,                              # Static position
        LiftPotPosition,                      # Position randomization
        LiftPotOrientation,                   # Orientation randomization
        LiftPotPositionAndOrientation         # Both randomized
    )
    
    # Try different variations
    env_static = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda
    )
    
    env_random = LiftPotPositionAndOrientation(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda
    )

Replaying Demonstrations
-------------------------

Load and replay human demonstrations:

.. code-block:: python

    from roboeval.demonstrations.demo_player import DemoPlayer
    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    
    # Create environment
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    
    # Get demonstrations
    metadata = Metadata.from_env(env)
    demo_store = DemoStore()
    demos = demo_store.get_demos(metadata, amount=10, frequency=20)
    
    # Replay first demo
    player = DemoPlayer()
    for demo in demos[:1]:
        print(f"Replaying demo: {demo.uuid}")
        player.replay_in_env(demo, env, demo_frequency=20)

Accessing Metrics
-----------------

RoboEval provides task-specific metrics beyond binary success:

.. code-block:: python

    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda
    )
    
    obs, info = env.reset()
    
    for step in range(1000):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Access task success from info dict
        print(f"Task success: {info.get('task_success', 0.0)}")
        
        # Additional task-specific metrics may be available
        # depending on the environment implementation
        for key, value in info.items():
            if key != 'task_success':
                print(f"{key}: {value}")
        
        if terminated or truncated:
            break

Common Patterns
---------------

**Running Multiple Episodes**

.. code-block:: python

    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda
    )
    
    num_episodes = 10
    success_count = 0
    
    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        
        for step in range(1000):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            episode_reward += reward
            
            if terminated or truncated:
                if info.get('task_success'):
                    success_count += 1
                print(f"Episode {episode}: Reward={episode_reward:.2f}, Success={info.get('task_success', False)}")
                break
    
    print(f"Success rate: {success_count/num_episodes:.2%}")
    env.close()

**Collecting Observations**

.. code-block:: python

    observations = []
    actions = []
    rewards = []
    
    obs, info = env.reset()
    
    for step in range(100):
        action = env.action_space.sample()
        
        observations.append(obs)
        actions.append(action)
        
        obs, reward, terminated, truncated, info = env.step(action)
        rewards.append(reward)
        
        if terminated or truncated:
            break

Next Steps
----------

- Explore all :doc:`../tasks/index` available in RoboEval
- Learn about :doc:`../user-guide/data-collection` with VR or keyboard
- Understand :doc:`../user-guide/action-modes` in detail
- Create your own :doc:`../advanced/custom-tasks`
