Stack Books
===========

Two task families involving book manipulation with shelves and tables.

StackSingleBookShelf
--------------------

Pick a book from a table and place it on a bookshelf.

.. image:: ../_static/imgs/stack_single_book_shelf.png
   :alt: Stack Single Book Shelf Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.stack_books import (
        StackSingleBookShelf,
        StackSingleBookShelfPosition,
        StackSingleBookShelfPositionAndOrientation
    )

**Variations:** 3 (Base, Position, PositionAndOrientation)

**Task Description:**

The robot must pick up a book from the table and place it on the bookshelf, ensuring it collides with either the upper or lower shelf.

**Success Criteria:**

- Book is colliding with either upper or lower shelf
- Book is not being held by either gripper
- Book is not on the floor

PickSingleBookFromTable
------------------------

Pick a book from a table and lift it while maintaining grasp.

.. image:: ../_static/imgs/pick_single_book.png
   :alt: Pick Single Book From Table Task
   :align: center
   :width: 60%

.. code-block:: python

    from roboeval.envs.stack_books import (
        PickSingleBookFromTable,
        PickSingleBookFromTablePosition,
        PickSingleBookFromTableOrientation,
        PickSingleBookFromTablePositionAndOrientation
    )

**Variations:** 4 (Base, Position, Orientation, PositionAndOrientation)

**Task Description:**

The robot must grasp a book from the table and lift it to a target height (0.77m or higher) while maintaining grasp with at least one gripper.

**Success Criteria:**

- Book height ≥ 0.77m
- At least one gripper holding the book
- Book not colliding with counter or floor

Success Criteria
----------------

- Book grasped properly
- Book placed on target location
- Book stable and upright
- No collisions

Key Skills
----------

- Precise grasping
- Bimanual coordination
- Placement accuracy
- Orientation control
