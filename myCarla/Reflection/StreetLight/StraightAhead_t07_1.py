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
import argparse

try:
    # print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/carla')
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
except IndexError:
    pass

from agents.navigation.behavior_agent import BehaviorAgent
from sync_mode import CarlaSyncMode


# tusimple 图片大小：1280 * 720
# 地图：Town07
# 起止点：76 -> 47

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
        default=76)
    argparser.add_argument(
        '--end', '-e',
        type=int,
        default=47)
    argparser.add_argument(
        '--output', '-o',
        type=str,
        default='/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark-1/Reflection/StreetLight/StraightAhead_t07_1')
    argparser.add_argument(
        '--img_num', '-n',
        type=int,
        default=99)
    argparser.add_argument(
        '--relative_loc', '-rl',
        type=str,
        default='front')   # top, front, back, back_left, 
    args = argparser.parse_args()
    return args


def update_view(spectator, vehicle_actor, view):
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
        #ts_start_point = spawn_points[start_index]
        ts_start_point = carla.Transform(carla.Location(x=-1.860267, y=-14.206019, z=0.300000), carla.Rotation(pitch=0.000000, yaw=-89.520630, roll=0.000000))
        blueprint_library = world.get_blueprint_library()

        bp_vehicles = blueprint_library.filter('vehicle.audi.etron')
        bp_ego_vehicle = bp_vehicles[0]
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
        #ts_end_point = spawn_points[end_index]
        ts_end_point = carla.Transform(carla.Location(x=-0.570144, y=-168.396927, z=0.300000), carla.Rotation(pitch=0.000000, yaw=-89.520599, roll=0.000000))
        print(ts_end_point)
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


if __name__ == '__main__':
    args = parse_arg()
    IM_WIDTH = args.width
    IM_HEIGHT = args.height
    start_index = args.start
    end_index = args.end
    max_img_num = args.img_num
    relative_loc = args.relative_loc

    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    client.load_world('Town07')
    world = client.get_world() # 'Town'
    light_manager = world.get_lightmanager()
    lights = light_manager.get_all_lights(carla.LightGroup.Street)
    weather = world.get_weather()
    weather.sun_altitude_angle = -10
    weather.sun_azimuth_angle = 0.0
    world.set_weather(weather) # !!!!!!!!
    light_manager.turn_on(lights)

    pds = [0, 60, 70, 80]
    colors = {'wh': (244, 207, 133), 'ye': (255, 127, 0)}
    
    for pd in pds:
        for k, v in colors.items():
            print('-------------pd {} {}----------------'.format(pd, k))
            save_dir = args.output + "_{}".format(k)
            if 0 == pd:
                save_dir += '_origin'
            else:
                save_dir += "_pd{}".format(pd)
            weather.precipitation_deposits = pd
            world.set_weather(weather)  # !!!!!!!!
            light_manager.set_color(lights, carla.Color(v[0], v[1], v[2]))
            # os.system('python3 ../util/environment.py --sun night -pd {} --lights on color {} {} {}'.format(pd, v[0], v[1], v[2]))
            
            try:
                main()
            except KeyboardInterrupt:
                print('\nCancelled by user. Bye!')