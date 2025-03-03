# Sand Simulator
![image](https://github.com/user-attachments/assets/43cc90ed-f0ae-49f2-810a-97844f7521ff)

### A sand simulator written in Python with quadtree optimization

Inspired by similar sand simulators, such as [sandspiel](https://sandspiel.club/) and [FallingSandJava](https://github.com/DavidMcLaughlin208/FallingSandJava).

This sand simulator is optimized using a quadtree to maintain active and inactive regions (i.e. it performs "lazy" updates). It can be paired with any visualizer. Here, I use pygame.

### Usage

![image](https://github.com/user-attachments/assets/8aaabc8f-9de5-42f0-be43-97c4fc907a6d)

Run the simulation.py file.

Use WASD to pan the camera, and scroll to zoom.

Click anywhere to draw with the brush. Use left and right arrow keys to cycle through different materials (including an eraser). Use up and down arrow keys to adjust brush radius.

Press the backtick key to cycle through debug modes (visualize quadtree).

### To-do

Current materials: empty, wall, sand, water, dirt, stone, smoke, fire, wood, ice, snow, lava, salt

Possible materials to add: ash, acid, oil, plant, mite, gunpowder, ...

- add inertia system?
- better liquid dispersion
- optimize!

