Lift Pot
========

Grasp a kitchen pot by both handles and lift it above the table without tilting.

.. image:: ../_static/imgs/lift_pot.png
   :alt: Lift Pot Task
   :align: center
   :width: 60%

Task Description
----------------

The robot must:

1. Grasp the pot by both handles using both grippers
2. Lift the pot at least 0.10 m above its initial height
3. Keep the pot's symmetry axis within 20° of vertical
4. Avoid colliding with surrounding cabinets

**Key Skills:**

- Bimanual coordination
- Symmetric grasping
- Orientation control
- Spatial awareness

Success Criteria
----------------

- Pot not colliding with either cabinet
- Pot lifted ≥ 0.10 m above starting height (SUCCESS_HEIGHT = INITIAL_HEIGHT + 0.1)
- Pot orientation within 20° of vertical (phi and theta angles checked)

**Failure Conditions:**

- Pot colliding with floor

Task Stages
-----------

.. glossary::

    Stage 0
        Initial state - pot on table, robot ready

    Stage 1
        Left gripper grasping the pot handle

    Stage 2
        Right gripper grasping the pot handle

    Stage 3
        Pot lifted at least 0.10 m above table

    Stage 4
        Complete success - pot stable and level

Variations
----------

LiftPot (Base)
~~~~~~~~~~~~~~

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPot
    
    env = LiftPot(
        action_mode=JointPositionActionMode(),
        robot_cls=BimanualPanda
    )

**Characteristics:**

- Pot always appears in same position
- Same orientation every episode
- Good for initial learning

LiftPotPosition
~~~~~~~~~~~~~~~

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPotPosition

**Randomization:**

- Position: Random within 0.2m radius
- Orientation: Fixed

LiftPotOrientation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPotOrientation

**Randomization:**

- Position: Fixed
- Orientation: ±30° around Z-axis

LiftPotPositionAndOrientation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPotPositionAndOrientation

**Randomization:**

- Position: Random within workspace
- Orientation: ±30° around Z-axis
- Most challenging variation

Common Challenges
-----------------

**Symmetric Grasping**
    Both grippers must grasp handles simultaneously for balanced lift

**Collision Avoidance**
    Cabinets on both sides require careful arm movements

**Orientation Control**
    Maintaining pot level while lifting requires coordination

Example Usage
-------------

.. code-block:: python

    from roboeval.envs.lift_pot import LiftPotPositionAndOrientation
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    env = LiftPotPositionAndOrientation(
        action_mode=JointPositionActionMode(absolute=True),
        render_mode="human",
        robot_cls=BimanualPanda,
        control_frequency=20
    )
    
    obs, info = env.reset()
    
    for step in range(1000):
        action = policy.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        
        if 'metrics' in info:
            print(f"Stage: {info['metrics']['stage']}")
        
        if terminated or truncated:
            print(f"Success: {info.get('success', False)}")
            break

Metrics
-------

Standard metrics provided:

- ``success``: Task completion
- ``stage``: Current progression stage (0-4)
- ``pot_height``: Current pot height above table
- ``pot_tilt``: Pot orientation deviation from vertical
- ``collision``: Whether collision occurred

Access metrics:

.. code-block:: python

    obs, reward, terminated, truncated, info = env.step(action)
    
    if 'metrics' in info:
        metrics = info['metrics']
        print(f"Pot height: {metrics['pot_height']:.3f}m")
        print(f"Pot tilt: {metrics['pot_tilt']:.1f}°")

Demonstrations
--------------

Load demonstrations for this task:

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    
    metadata = Metadata.from_env(env)
    demo_store = DemoStore()
    
    # Get demonstrations for base task
    demos = demo_store.get_demos(metadata, amount=50)
    
    # Or specify task variation
    demos = demo_store.get_demos_for_task("LiftPotPosition", amount=50)

Tips
----

1. **Grasp handles symmetrically** for better balance
2. **Lift slowly** to maintain orientation
3. **Start with base variation** before trying randomized versions
4. **Use stage information** to debug partial successes

See Also
--------

- :doc:`index` - All tasks overview
- :doc:`../user-guide/environments` - Environment configuration
- :doc:`../advanced/metrics` - Detailed metrics guide
