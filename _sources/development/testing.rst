Testing
=======

Guidelines for testing RoboEval.

Running Tests
-------------

Run all tests:

.. code-block:: bash

    pytest tests/

Run specific test:

.. code-block:: bash

    pytest tests/test_environments.py::test_lift_pot

With coverage:

.. code-block:: bash

    pytest --cov=roboeval tests/

Writing Tests
-------------

**Environment Tests**

.. code-block:: python

    import pytest
    from roboeval.envs.lift_pot import LiftPot
    from roboeval.action_modes import JointPositionActionMode
    from roboeval.robots.configs.panda import BimanualPanda
    
    def test_lift_pot_reset():
        env = LiftPot(
            action_mode=JointPositionActionMode(),
            robot_cls=BimanualPanda
        )
        
        obs, info = env.reset()
        
        assert 'qpos' in obs
        assert 'qvel' in obs
        assert obs['qpos'].shape[0] > 0
    
    def test_lift_pot_step():
        env = LiftPot(
            action_mode=JointPositionActionMode(),
            robot_cls=BimanualPanda
        )
        
        obs, info = env.reset()
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)

**Task Success Tests**

.. code-block:: python

    def test_lift_pot_success_conditions():
        env = LiftPot(
            action_mode=JointPositionActionMode(),
            robot_cls=BimanualPanda
        )
        
        # Test that success is detected correctly
        # (would need oracle policy or specific actions)
        pass

**Demonstration Tests**

.. code-block:: python

    from roboeval.demonstrations.demo_store import DemoStore
    from roboeval.demonstrations.utils import Metadata
    
    def test_demo_loading():
        env = LiftPot(...)
        metadata = Metadata.from_env(env)
        
        demo_store = DemoStore()
        demos = demo_store.get_demos(metadata, amount=1)
        
        assert len(demos) > 0
        assert demos[0].observations is not None

Test Organization
-----------------

.. code-block:: text

    tests/
    ├── test_environments.py      # Environment tests
    ├── test_action_modes.py      # Action mode tests
    ├── test_demonstrations.py    # Demo loading/replay
    ├── test_robots.py            # Robot configuration
    └── test_utils.py             # Utility functions

Best Practices
--------------

1. **Test edge cases** (empty actions, invalid states)
2. **Test all variations** of tasks
3. **Mock expensive operations** (rendering, long episodes)
4. **Use fixtures** for common setup
5. **Keep tests fast** (use lower control frequency)

Fixtures
--------

.. code-block:: python

    import pytest
    
    @pytest.fixture
    def lift_pot_env():
        env = LiftPot(
            action_mode=JointPositionActionMode(),
            robot_cls=BimanualPanda,
            render_mode=None  # No rendering in tests
        )
        yield env
        env.close()
    
    def test_with_fixture(lift_pot_env):
        obs, info = lift_pot_env.reset()
        assert obs is not None

Continuous Integration
----------------------

Tests run automatically on:

- Pull requests
- Commits to main branch
- Nightly builds

See Also
--------

- :doc:`contributing` - Contribution guidelines
- pytest documentation
