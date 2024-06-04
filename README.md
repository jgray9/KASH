# KASH
This program uses the pygame module for creating interactive visual objects: https://www.pygame.org/docs/  

Pygame represents visual objects with the `Surface` class. Images, text, and even the window itself are all represented by these objects. Pygame has a `blit` function which draws one `Surface` onto another. This is how this program draws objects onto the screen (remember the screen is a `Surface` object).

All items that can appear on screen are sorted using the `Scene` class. Each `Scene` instance has a list of `SceneElement` instances, which handle the rendering of different types of things that can appear on screen.

Note that the `Scene` and `SceneElement` classes are not a part of the pygame module, and are defined by this program in the `elements.py` file.

## kash.py

This is the file that starts the program.

First, it initalizes a bunch of `Scene` instances and puts them in a dictionary to assign each of them a name. Every `SceneElement` has an attribute called `next_scene`, which is the name/key of the scene that the program will transition to after that element is clicked. Some elements shouldn't do anything when clicked., in which `next_scene` would be `None`. The event loop keeps track of the current scene with a variable named `current_scene`.

After the scenes are initalized and put in a dictionary, `kash.py` starts an event loop. Every loop the program calls `pygame.event.get()`, which returns a list of every `pygame.event` that occured since its last call. The program looks for events it cares about by checking the `event.type` attribute, which is a unique integer ID given to each event.

There are 3 events the program watches for:
- The `pygame.QUIT` event, which is triggered when the user closes the window. When this event is recieved, the event loop terminates and the program stops.
- The `pygame.MOUSEBUTTONDOWN` event, which is when the user clicks somewhere with the mouse. The mouse position from the event is passed to the current scenes `click(x,y)` function.
- The `elements.SCENECHANGEEVENT`, which is triggered by the `SceneElement` class. The new scene is taken from the events attributes and the `current_scene` variable is updated.

## elements.py

Below are all of the classes created in this program. These classes are defined in `elements.py`, which is then imported by `kash.py`, where the program actually runs.

<details><summary>Scene</summary>

The `Scene` class contains a list of `SceneElement` instances. It handles mouse input and is responsible for drawing the elements it contains.
```
__init__(list<SceneElement> elements) -> None
```
Initialization function. `elements` is a list of `SceneElement` instances that are in the scene.
```
click(int x, int y) -> string
```
Iterates through every element and calls their `click(x, y)` function
```
draw_all() -> None
```
Iterates through every element and calls their `draw()` function

</details>

<details><summary>SceneElement</summary>

The `SceneElement` class represents a generic element with a `draw()` function and a `click(x,y)` function, both of which are used in the `Scene` class. The `draw()` function should be overridden.
```
__init__(Surface screen, int x, int y, int w, int h, int opacity, string next_scene = None) -> None
```
Each element contains a pointer to the screen in order to call the `blit` function. `x` is the distance from the left of the screen and `y` is distance from the top of the screen. `w` and `h` are the size of the object, being the width and height respectively. `next_scene` is the name of the scene that should be displayed after the element is clicked on. `next_scene` should be `None` (its default value) if the element is not clickable.
```
click(int x, int y) -> bool
```
Checks if the coordinates `(x, y)` are inside of the element and if `next_scene` is not `None`. If both of these conditions are true, it triggers a change scene event.
```
draw() -> None
```
A generic draw function to be overridden by child classes. Although every implementation will eventually use `blit`, the method of turning text/images/other into a `Surface` object will differ, hence the need for other classes.

</details>

<details><summary>ImageElement</summary>

Inherits the `SceneElement` class.  
The `ImageElement` class takes care of the process of loading an image from a file and drawing it on the screen.
```
__init__(Surface screen, string filename, int x, int y, int opacity, string next_scene = None) -> None
```
A `Surface` object is created from the file at `filename` (meaning `filename` should also include the path of the file).
```
draw() -> None
```
Uses `blit` to draw the image surface onto the screen

</details>

<details><summary>TextElement</summary>

Inherits the `SceneElement` class.  
The `TextElement` class takes care of loading blocks of text onto the screen.
```
__init__(Surface screen, string text, int text_size, string text_color, int x, int y, int w, int opacity) -> None
```
The process of converting text into a `Surface` does not support multiple lines. Therefore, a list of `Surface` objects representing each line of text is stored instead.
```
draw() -> None
```
Iterates through all of the `Surface` objects and uses `blit` to draw them onto the screen

</details>

<details>
<summary>TitleElement</summary>

Inherits the `SceneElement` class.  
The `TitleElement` class is similar to the `TextElement` class, except the the text should be centered, instead of left aligned.  
```
__init__(Surface screen, string text, int text_size, string text_color, int x, int y, int w) -> None
```
A `Surface` object is rendered using `text` with size `text_size`. A title is not expected to have multiple lines.
```
draw() -> None
```
Draws the text surface onto the screen using `blit`. The location of the text is shifted slighty right so the text is aligned at the center of the element.

</details>

## text.json

All text in this program is pulled from the `departments.json` file. Centralizing the location of text to a seperate file allows editing names/descriptions of things without having to hunt down where they are located in the code.