Integrations
============

Integrate RoboEval with learning frameworks and datasets.

LeRobot Integration
-------------------

Convert demonstrations to LeRobot format by processing timesteps:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    
    # Load demonstrations
    demo_store = DemoStore()
    demos = demo_store.get_demos(metadata, amount=100)
    
    # Process demos into LeRobot format
    lerobot_data = {
        'observations': [],
        'actions': [],
        'episode_ids': []
    }
    
    for episode_idx, demo in enumerate(demos):
        for timestep in demo.timesteps:
            lerobot_data['observations'].append(timestep.observation)
            lerobot_data['actions'].append(timestep.action)
            lerobot_data['episode_ids'].append(episode_idx)

Train with LeRobot:

.. code-block:: python

    from lerobot.common.policies.act.policy import ACTPolicy
    
    policy = ACTPolicy.from_pretrained("path/to/checkpoint")
    
    # Evaluate on RoboEval
    from roboeval.envs.manipulation import LiftPot
    
    env = LiftPot()
    obs, info = env.reset()
    
    for step in range(1000):
        action = policy.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            break

RLDS Integration
----------------

Convert to RLDS format by processing timesteps:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    
    demo_store = DemoStore()
    demos = demo_store.get_demos(metadata, amount=100)
    
    # Process demos into RLDS-compatible format
    rlds_data = []
    
    for demo in demos:
        episode_data = {
            'steps': []
        }
        
        for timestep in demo.timesteps:
            step_data = {
                'observation': timestep.observation,
                'action': timestep.action,
                'reward': timestep.reward,
                'is_first': timestep == demo.timesteps[0],
                'is_last': timestep == demo.timesteps[-1],
                'is_terminal': timestep == demo.timesteps[-1]
            }
            episode_data['steps'].append(step_data)
        
        rlds_data.append(episode_data)

OpenVLA Integration
-------------------

Evaluate OpenVLA models:

.. code-block:: python

    from transformers import AutoModel, AutoProcessor
    from roboeval.envs.manipulation import LiftPot
    
    # Load OpenVLA model
    processor = AutoProcessor.from_pretrained("openvla/openvla-7b")
    model = AutoModel.from_pretrained("openvla/openvla-7b")
    
    # Create environment
    env = LiftPot()
    
    num_episodes = 10
    for episode in range(num_episodes):
        obs, info = env.reset()
        
        for step in range(1000):
            # Get action from model
            inputs = processor(obs)
            action = model.predict(inputs)
            
            obs, reward, terminated, truncated, info = env.step(action)
            
            if terminated or truncated:
                print(f"Episode {episode}: Success = {info['task_success']}")
                break

Custom Integration
------------------

Create custom integration by processing Demo timesteps:

.. code-block:: python

    class CustomDatasetConverter:
        """Convert RoboEval demos to custom format."""
        
        def convert(self, demos):
            """Convert list of Demo objects to custom format.
            
            Args:
                demos: List of Demo objects, each with metadata and timesteps
            
            Returns:
                Custom dataset dictionary
            """
            dataset = {
                'observations': [],
                'actions': [],
                'rewards': [],
                'episode_ids': []
            }
            
            for episode_idx, demo in enumerate(demos):
                # Each demo has metadata and timesteps
                for timestep in demo.timesteps:
                    dataset['observations'].append(timestep.observation)
                    dataset['actions'].append(timestep.action)
                    dataset['rewards'].append(timestep.reward)
                    dataset['episode_ids'].append(episode_idx)
            
            return dataset

See Also
--------

- Example 2 (convert_and_replay.py)
- Example 4 (eval_openvla.py)
