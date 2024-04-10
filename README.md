# KASH
This program requires the pygame module: https://www.pygame.org/docs/  

## kash.py

Pygame represents visuals as `Surface` objects. Images, text, and the screen itself are all represented by these objects. Pygame has a `blit()` function which draws one `Surface` onto another. This is how this program draws objects onto the screen.

All items that can appear on screen are sorted into `Scene` objects. Only one `Scene` should be "active" at any time, which this file keeps track of. In each `Scene`, there are `SceneElement` objects, which handle the rendering of different types of things that can appear on screen.

The program first initalizes a bunch of `Scene` instances and puts them in a dictionary to assign each of them a name. Every `SceneElement` has a attribute called `next_scene`, which is the name/key of the `Scene` that should be activated after that element is clicked. Some elements shouldn't do anything when clicked., in which `next_scene` would be `None`.

 `Scene` and `SceneElement` classes are not a part of the pygame module, and are defined by this program in the `elements.py` file.

## elements.py

Below are all of the classes created in this program. These classes are defined in `elements.py`, which is then imported by `kash.py`, where the program actually runs.

<details><summary>Scene</summary>

The `Scene` class contains a list of `SceneElement` instances. It handles mouse input and is responsible for drawing the elements it contains.
```
__init__(list<SceneElement> elements) -> None
```
Initialization function. `elements` is a list of `SceneElement` instances that are in the scene.
```
click(int mouse_x, int mouse_y) -> string
```
Iterates through every element in the list, and checks if the coordinates `(mouse_x, mouse_y)` are inside the elements hitbox using the `SceneElement.click()` function. If the function returns true and the element is clickable, the name of the next scene to be displayed is returned. This name is stored as a variable in the `SceneElement` class. If the element is not clickable, `next_scene` will be `None` and the function will ignore that element during while iterating.
```
draw() -> None
```
Iterates through every element and calls their `draw()` function

</details>

<details><summary>SceneElement</summary>

The `SceneElement` class represents a generic element with a `draw()` function and a `contains_point()` function, both of which are used in the `Scene` class. The `draw()` function should be overridden.
```
__init__(Surface screen, int x, int y, int w, int h, string next_scene = None) -> None
```
Each element contains a pointer to the screen in order to call the `blit()` function. `x` is the distance from the left of the screen and `y` is distance from the top of the screen. `w` and `h` are the size of the object, being the width and height respectively. `next_scene` is the name of the scene that should be displayed after the element is clicked on. `next_scene` should be `None` (its default value) if the element is not clickable.
```
contains_point(int x, int y) -> bool
```
Checks if the coordinates `(x, y)` are inside of the element. Returns `True` if they are and `False` otherwise.
```
draw() -> None
```
A generic draw function to be overridden by child classes. Although every implementation will eventually use `blit()`, the method of turning text/images/other into a `Surface` object will differ, hence the need for other classes.

</details>

<details><summary>ImageElement</summary>

Inherits the `SceneElement` class.  
The `ImageElement` class takes care of the process of loading an image from a file and drawing it on the screen.
```
__init__(Surface screen, int x, int y, int w, int h, string filename, string next_scene = None) -> None
```
A `Surface` object is created from the file at `filename` (meaning `filename` should also include the path of the file).
```
draw() -> None
```
Uses `blit()` to draw the image surface onto the screen

</details>

<details><summary>TextElement</summary>

Inherits the `SceneElement` class.  
The `TextElement` class takes care of loading blocks of text onto the screen.
```
__init__(Surface screen, int x, int y, int w, int h, string text, int text_size, string next_scene = None) -> None
```
The process of converting text into a `Surface` does not support multiple lines. Therefore, a list of `Surface` objects representing each line of text is stored instead.
```
draw() -> None
```
Iterates through all of the `Surface` objects and uses `blit()` to draw them onto the screen

</details>

<details>
<summary>TitleElement</summary>

Inherits the `SceneElement` class.  
The `TitleElement` class is similar to the `TextElement` class, except the the text should be centered, instead of left aligned.  
```
__init__(Surface screen, int x, int y, int w, int h, string text, int text_size, string next_scene = None) -> None
```
A `Surface` object is rendered using `text` with size `text_size`. A title is not expected to have multiple lines.
```
draw() -> None
```
Draws the text surface onto the screen using `blit()`. The location of the text is shifted slighty right so the text aligned at the center of the element.

</details>

## text.json

All text in this program is pulled from the `text.json` file. Centralizing the location of text to a seperate file allows editing names/descriptions of things without having to hunt down where they are located in the code.