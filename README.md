Pygame 3D Wireframes with Software Rendering
============================================

Introduction
------------

This sample project and library demonstrates basic rendering of wireframes in 3D
in software only. No hardware acceleration is used. Currently, no z-buffering or
clipping is performed. This may change if I decide to implement them (or if you
decide to implement these features for your own edification).

This is a continuation of a final project for CIS 192 at the University of
Pennsylvania. The primary purpose of this project is to be __educational__. This
is probably not intended for production usage, but you are more than welcome to
use it for that purpose.


Setup and Installation
----------------------

This project should work with the latest versions of `numpy` and `pygame`. You
can refer to the websites of those respective packages for installation help.

Simply download the project sources and run `main.py`.

This project does not rely on hardware 3D, so it should run on any system.


Running the Sample Viewer
-------------------------

Simply running `python main.py` will launch a basic viewer, which can be
interacted with `WASD` and the mouse.

Run `python main.py --help` for command-line usage options.


Project and Library Structure
-----------------------------

The sample viewer follows a MVC design. The file `game.py` contains the `Game`
controller, which manipulates the underlying view, which is given as a
constructor argument. There are currently two different kinds of cameras
provided to render scenes: `OrthographicViewport` and `PerspectiveViewport`,
utilizing orthographic projection and perspective projection, respectively.

Creating your own custom viewport is rather simple. Simply extend `Viewport`,
and override the relevant functions (most likely just `update_projection_matrix`
and `to_view_coords`).

A wireframe model (classes extending `Model` from `model.py`) is simply a
collection of edges, and represents that object in its own coordinate system
with its own scale. Drawable objects should extend `Model` (c.f. `Cube` in
`shapes.py`).


Licensing
---------

You can use the code of this project in full (or any part thereof) in any
commercial or non-commercial code. You might want to check with your instructor
if you want to use the code within a homework assignment.