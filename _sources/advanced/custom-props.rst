Creating Custom Props
=====================

Learn how to create custom objects (props) for your tasks.

Prop Basics
-----------

Props are objects in the environment (cubes, pots, books, etc.).

Available Props
---------------

RoboEval includes many pre-built props:

- ``Cube`` - Basic cube object
- ``Table`` - Surface for placing objects
- ``KitchenPot`` - Pot with handles
- ``Book`` - Book object for stacking
- ``Shelf`` - Bookshelf
- ``Valve`` - Rotatable valve wheel
- ``Box`` - Container for packing
- ``Tray`` - Tray for carrying objects

Using Existing Props
--------------------

.. code-block:: python

    from roboeval.envs.props.items import Cube
    from roboeval.envs.props.tables import Table
    
    # In your task's _initialize_env method
    self.table = Table(self._mojo)
    self.cube = Cube(self._mojo)
    
    # Position props using set_pose
    self.cube.set_pose(position=np.array([0.5, 0.0, 1.0]))

Creating Custom Props
---------------------

Create a new prop class by inheriting from ``Prop`` or ``KinematicProp``:

.. code-block:: python

    from pathlib import Path
    from roboeval.envs.props.prop import KinematicProp
    from roboeval.const import ASSETS_PATH
    
    class MyCustomProp(KinematicProp):
        """My custom prop."""
        
        @property
        def _model_path(self) -> Path:
            """Path to the prop's XML/URDF model."""
            return ASSETS_PATH / "props/my_prop/my_prop.xml"
        
        def _on_loaded(self, model):
            """Optional: Customize prop after loading."""
            # Modify the model before it's finalized
            pass
        
        def _post_init(self):
            """Optional: Customize prop after initialization."""
            # Additional setup after prop is created
            pass

**Prop vs KinematicProp:**

- ``Prop``: Base class for all props (abstract)
- ``KinematicProp``: Kinematic collidable props (default for most objects)
  - Sets ``_KINEMATIC = True``
  - Sets ``_CACHE_COLLIDERS = True``
  - Use for objects that should collide and be manipulated

Using 3D Models
---------------

Props can use URDF or MuJoCo XML models:

.. code-block:: xml

    <!-- my_prop.xml -->
    <mujoco>
      <worldbody>
        <body name="prop_body">
          <geom type="box" size="0.05 0.05 0.05" 
                rgba="1 0 0 1" mass="0.1"/>
        </body>
      </worldbody>
    </mujoco>

Best Practices
--------------

1. Use existing props when possible
2. Keep collision meshes simple
3. Set appropriate mass and inertia
4. Add visual markers for grasping points

See Also
--------

- :doc:`custom-tasks` - Use props in tasks
- MuJoCo documentation for XML format
