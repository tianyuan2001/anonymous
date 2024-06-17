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
from sync_mode import CarlaSyncMode
import random
import argparse
import os
import sys

if __name__ == '__main__':  
    IM_WIDTH = 1280
    IM_HEIGHT = 720
    actor_list = []
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    world = client.get_world() # 'Town'
    map = world.get_map()
    blueprint_library = world.get_blueprint_library()
    spawn_points = map.get_spawn_points()
    bp_camera_rgb = blueprint_library.find('sensor.camera.rgb') # carla.ActorBlueprint
    bp_camera_rgb.set_attribute('image_size_x', "{}".format(IM_WIDTH))
    bp_camera_rgb.set_attribute('image_size_y', "{}".format(IM_HEIGHT))

    ts_start_point = spawn_points[69]
    bp_vehicles = blueprint_library.filter('vehicle.carlamotors.firetruck')
    bp_ego_vehicle = bp_vehicles[0]
    ego_vehicle = world.spawn_actor(blueprint=bp_ego_vehicle,       # carla.ActorBlueprint
                                        transform=ts_start_point) 
    actor_list.append(ego_vehicle)
    view = carla.Transform(carla.Location(x=-6, y=0, z=2),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    camera_rgb = world.spawn_actor(blueprint=bp_camera_rgb,
                                       transform=view,
                                       attach_to=ego_vehicle,   # carla.Actor
                                       # attachment_type=Attachment.Rigid,
                                        )
    actor_list.append(camera_rgb)
    spectator = world.get_spectator()
    update_view(spectator=spectator, vehicle_actor=ego_vehicle, view=relative_loc)
    