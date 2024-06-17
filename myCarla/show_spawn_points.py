import os
import sys
import glob

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


if __name__ == '__main__':
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    world = client.get_world()
    map = world.get_map()
    spawn_points = map.get_spawn_points()

    for i, spawn_point in enumerate(spawn_points):
        # Draw in the spectator window the spawn point index
        world.debug.draw_string(spawn_point.location, str(i), life_time=100)
        # We can also draw an arrow to see the orientation of the spawn point
        # (i.e. which way the vehicle will be facing when spawned)
        world.debug.draw_arrow(spawn_point.location, spawn_point.location + spawn_point.get_forward_vector(), life_time=100)

    '''
    life_time (float - seconds) - Shape's lifespan. 
    By default it only lasts one frame. 
    Set this to 0 for permanent shapes. 
    '''
