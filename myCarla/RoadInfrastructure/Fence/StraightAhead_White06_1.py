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

try:
    # print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/carla')
except IndexError:
    pass

from agents.navigation.behavior_agent import BehaviorAgent


def parse_arg():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--width', '-w',
        type=int,
        default=1280)
    argparser.add_argument(
        '--height',
        type=int,
        default=720)
    argparser.add_argument(
        '--start', '-s',
        type=int,
        default=157)
    argparser.add_argument(
        '--end', '-e',
        type=int,
        default=338)
    argparser.add_argument(
        '--output', '-o',
        type=str,
        default='/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/RoadInfrastructure/Fence/StraightAhead_White06_1')
    argparser.add_argument(
        '--img_num', '-n',
        type=int,
        default=49)
    argparser.add_argument(
        '--town', '-t',
        type=str,
        default='Town06')
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
        
    try:
        map = world.get_map()
        spawn_points = map.get_spawn_points()
        # print('spawn points: ', spawn_points)
        # ts_start_point = random.choice(spawn_points)   # carla.Transform
        # ts_start_point = spawn_points[start_index]
        ts_start_point = carla.Transform(carla.Location(x=269.179535, y=151.032471, z=0.300000), carla.Rotation(pitch=0.000000, yaw=0.234757, roll=0.000000))
        blueprint_library = world.get_blueprint_library()

        # 初始化
        # vehicle.carlamotors.firetruck   vehicle.audi.etron
        bp_vehicles = blueprint_library.filter('vehicle.audi.etron')
        bp_ego_vehicle = bp_vehicles[0]# random.choice(bp_vehicles) # carla.ActorBlueprint   
        # bp_vehicles = blueprint_library.filter('vehicle.audi.etron')
        # bp_front_vehicle = bp_vehicles[0]# random.choice(bp_vehicles) # carla.ActorBlueprint   
        # try_spawn_actor returns None on failure instead of throwing an exception. 
        # spawn_actor returns carla.Actor
        ego_vehicle = world.spawn_actor(blueprint=bp_ego_vehicle,       # carla.ActorBlueprint
                                        transform=ts_start_point)   # carla.Transform
        print(ts_start_point)
        actor_list.append(ego_vehicle)

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
        # ts_end_point = spawn_points[end_index]
        ts_end_point = carla.Transform(carla.Location(x=410.290161, y=151.610840, z=0.300000), carla.Rotation(pitch=0.000000, yaw=0.234757, roll=0.000000))
        print('zhongdian ', ts_end_point)
        agent.set_destination(end_location=ts_end_point.location)

        # 7 ~ 106
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

                if agent.done():
                    print('The destination has been reached. Stop the simulation!')
                    break
                if i >= max_img_num:
                    print('The max img num has been reached. Stop the simulation!')
                    break
                    
                i = i + 1
        
    finally:
        for actor in actor_list:
            actor.destroy()
        print('done.')    


# tusimple 图片大小：1280 * 720
# 地图：Town06
# 起止点：157 -> 338, 不行，需要把起始点写固定
if __name__ == '__main__':
    args = parse_arg()
    IM_WIDTH = 1280
    IM_HEIGHT = 720
    start_index = 361
    end_index = 391
    max_img_num = 49
    relative_loc = args.relative_loc
    
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
########################################################################################
    save_dir = args.output + "_ClearNight"
    town_name = 'Town06'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.ClearNight)
    # os.system('python3 ../util/environment.py --weather clear -azm 0 -alt 30')    
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    # 原始场景
    save_dir = save_dir + "_origin"
    town_name = 'Town06_origin'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.ClearNight)
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
########################################################################################
    save_dir = args.output + "_CloudySunset"
    town_name = 'Town06'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.CloudySunset)
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    # 原始场景
    save_dir = save_dir + "_origin"
    town_name = 'Town06_origin'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.CloudySunset)
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
########################################################################################  
    save_dir = args.output + "_ClearNoon"
    town_name = 'Town06'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.ClearNoon)
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    # 原始场景
    save_dir = save_dir + "_origin"
    town_name = 'Town06_origin'
    client.load_world(town_name)
    world = client.get_world() 
    world.set_weather(carla.WeatherParameters.ClearNoon)
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
