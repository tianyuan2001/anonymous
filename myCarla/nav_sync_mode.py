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

try:
    # print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass

from agents.navigation.behavior_agent import BehaviorAgent


def parse_arg():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--width', '-w',
        type=int,
        default=1912)
    argparser.add_argument(
        '--height',
        type=int,
        default=1028)
    argparser.add_argument(
        '--start', '-s',
        type=int,
        default=1)
    argparser.add_argument(
        '--end', '-e',
        type=int,
        default=10)
    argparser.add_argument(
        '--output', '-o',
        type=str,
        default='/home/wanglu/Documents/carla_imgs/temp')
        #default='/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/vehicle/right-firetruck-dis10-azm240-alt55')
    argparser.add_argument(
        '--img_num', '-n',
        type=int,
        default=200)
    argparser.add_argument(
        '--relative_loc', '-rl',
        type=str,
        default='front')   # top, front, back, back_left, 
    args = argparser.parse_args()
    return args


def update_view(spectator, vehicle_actor, view):
    '''
    更新观察视角
        :param spectator
        :param vehicle(carla.Actor): 要跟踪的汽车
        :param view(str): 跟踪视角。[top, in]
    '''
    loc = vehicle_actor.get_transform().location
    rot = vehicle_actor.get_transform().rotation
    if view == 'top':
        spectator.set_transform(
            carla.Transform(carla.Location(x=loc.x+0, y=loc.y+0, z=loc.z+40),
                            carla.Rotation(pitch=-90))
        )
    elif view == 'front':
        spectator.set_transform(
            carla.Transform(carla.Location(x=loc.x+1, y=loc.y+0, z=loc.z+3),
                            rot)
        )
    elif view == 'back':
        spectator.set_transform(
            carla.Transform(carla.Location(x=loc.x-6, y=loc.y+0, z=loc.z+2),
                            rot)
        )
    elif view == 'back_left':
        spectator.set_transform(
            carla.Transform(carla.Location(x=loc.x-10, y=loc.y-3, z=loc.z+2),
                            rot)
        )
    else:
        print('errorrrrrr......')


def get_relative_tf(view):
    if view == 'top':
        return carla.Transform(carla.Location(x=0, y=0, z=40),
                               carla.Rotation(pitch=-90))
    if view == 'front':
        return carla.Transform(carla.Location(x=1, y=0, z=3),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    if view == 'back':
        return carla.Transform(carla.Location(x=-6, y=0, z=2),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    if view == 'back_left':
        return carla.Transform(carla.Location(x=-10, y=-3, z=2),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    if view == 'follow':
        return carla.Transform(carla.Location(x=7, y=0, z=0),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    if view == 'follow_right':
        return carla.Transform(carla.Location(x=7, y=3, z=0),
                               carla.Rotation(pitch=0, roll=0, yaw=0))
    print('errorrrrrr......')


def main():
    actor_list = []

    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    world = client.get_world() # 'Town'

    
    try:
        map = world.get_map()
        spawn_points = map.get_spawn_points()
        # print('spawn points: ', spawn_points)
        # ts_start_point = random.choice(spawn_points)   # carla.Transform
        ts_start_point = spawn_points[start_index]
        blueprint_library = world.get_blueprint_library()

        # 初始化
        # vehicle.carlamotors.firetruck   vehicle.audi.etron
        bp_vehicles = blueprint_library.filter('vehicle.carlamotors.firetruck')
        bp_ego_vehicle = bp_vehicles[0]# random.choice(bp_vehicles) # carla.ActorBlueprint   
        # bp_vehicles = blueprint_library.filter('vehicle.audi.etron')
        # bp_front_vehicle = bp_vehicles[0]# random.choice(bp_vehicles) # carla.ActorBlueprint   
        # try_spawn_actor returns None on failure instead of throwing an exception. 
        # spawn_actor returns carla.Actor
        ego_vehicle = world.spawn_actor(blueprint=bp_ego_vehicle,       # carla.ActorBlueprint
                                        transform=ts_start_point)   # carla.Transform
        actor_list.append(ego_vehicle)

        '''base_loc = ego_vehicle.get_transform().location
        base_rot = ego_vehicle.get_transform().rotation
        rel = get_relative_tf(view=relative_loc)
        rel_loc = rel.location
        rel_rot = rel.rotation'''
        '''front_vehicle = world.spawn_actor(blueprint=bp_front_vehicle,
                                          transform=carla.Transform(carla.Location(x=base_loc.x+rel_loc.x, y=base_loc.y+rel_loc.y, z=base_loc.z+rel_loc.z),
                                                                    carla.Rotation(pitch=base_rot.pitch, roll=base_rot.roll, yaw=base_rot.yaw)),
                                          )'''
        '''front_vehicle = world.spawn_actor(blueprint=bp_front_vehicle,
                                          transform=rel,
                                          attach_to=ego_vehicle)
        actor_list.append(front_vehicle)'''

        bp_camera_rgb = blueprint_library.find('sensor.camera.rgb') # carla.ActorBlueprint
        bp_camera_rgb.set_attribute('image_size_x', "{}".format(IM_WIDTH))
        bp_camera_rgb.set_attribute('image_size_y', "{}".format(IM_HEIGHT))

        camera_rgb = world.spawn_actor(blueprint=bp_camera_rgb,
                                       transform=get_relative_tf(view=relative_loc),
                                       attach_to=ego_vehicle,   # carla.Actor
                                       # attachment_type=Attachment.Rigid,
                                        )
        actor_list.append(camera_rgb)

        spectator = world.get_spectator()
        update_view(spectator=spectator, vehicle_actor=ego_vehicle, view=relative_loc)

        # 自动规划
        agent = BehaviorAgent(vehicle=ego_vehicle, behavior='normal')
        ts_end_point = spawn_points[end_index]
        agent.set_destination(end_location=ts_end_point.location)

        with CarlaSyncMode(world, camera_rgb, fps=10) as sync_mode:
            i = 0
            while True:
                # Advance the simulation and wait for the data.
                snapshot, image_rgb = sync_mode.tick(timeout=2.0)

                # 处理数据
                image_rgb.save_to_disk(os.path.join(save_dir, '{:06d}.png'.format(i))) # image_rgb.frame

                # 更新观察视角
                update_view(spectator=spectator, vehicle_actor=ego_vehicle, view=relative_loc)

                # 下一步路径规划
                # agent.update_information(ego_vehicle) 这一步被包括进了run_step中 怪
                control = agent.run_step(debug=False)
                ego_vehicle.apply_control(control)

                '''base_loc = ego_vehicle.get_transform().location
                base_rot = ego_vehicle.get_transform().rotation
                rel = get_relative_tf(view=relative_loc)
                rel_loc = rel.location
                rel_rot = rel.rotation
                front_vehicle.set_transform(blueprint=bp_front_vehicle,
                                                transform=carla.Transform(carla.Location(x=base_loc.x+rel_loc.x, y=base_loc.y+rel_loc.y, z=base_loc.z+rel_loc.z),
                                                                            carla.Rotation(pitch=base_rot.pitch, roll=base_rot.roll, yaw=base_rot.yaw)),
                                                )'''

                if agent.done():
                    print('The destination has been reached. Stop the simulation!')
                    break
                if i >= max_img_num:
                    print('The max img num has been reached. Stop the simulation!')
                    break
                    
                i = i + 1
        
    finally:
        for actor in actor_list:
            print('hhhh')
            actor.destroy()
        print('done.')    


if __name__ == '__main__':
    args = parse_arg()
    IM_WIDTH = args.width
    IM_HEIGHT = args.height
    start_index = args.start
    end_index = args.end
    save_dir = args.output
    max_img_num = args.img_num
    relative_loc = args.relative_loc
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


