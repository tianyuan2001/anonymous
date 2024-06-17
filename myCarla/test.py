import os

def test(size):
    scenes = ['30', '35', '40', '45', '50', '55', '60']
    start, end = 158, 197
    '''
    初始环境设置 origin
    '''
    try:
        os.system('python3 ../util/environment.py -azm 0 -alt 30')
    except Exception:
        return
    run_command = 'python3 nav_sync_mode.py -s {} -e {} -o {} -w {} --height {} -n 200 '.format(start, end, origin_dir, size[0], size[1])
    try:
        os.system(run_command)
    except Exception:
        return
    # 固定azm
    try:
        os.system('python3 ../util/environment.py -azm 270')
    except Exception:
        return
    # 调alt
    for scene in scenes:
        output = base_dir + scene
        env_command = 'python3 ../util/environment.py -alt {}'.format(scene)
        try:
            os.system(env_command)
        except Exception:
            break
        run_command = 'python3 nav_sync_mode.py -s {} -e {} -o {} -w {} --height {} -n 200 '.format(start, end, output, size[0], size[1])
        try:
            os.system(run_command)
        except Exception:
            break



def sun_pd_test():
    '''
    0830 town03 白天积水反光
    '''
    start, end = 158, 197

    scenes = [(0, 0), (180, 0)]
    for scene in scenes:
        output = '/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/reflection/puddle-sun-town03/scene0-origin-azm{}-pd{}'.format(scene[0], scene[1])
        try:
            os.system('python3 ../util/environment.py -azm {} -pd {}'.format(scene[0], scene[1]))
        except Exception:
            return
        run_command = 'python3 nav_sync_mode.py -s {} -e {} -o {} -w {} --height {} -n 200 '.format(start, end, output, 1912, 1028)
        try:
            os.system(run_command)
        except Exception:
            break

    scenes = ['160', '170', '180', '190', '200'] # azm
    try:
        os.system('python3 ../util/environment.py -pd 45')
    except Exception:
        return
    for scene in scenes:
        output = '/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/reflection/puddle-sun-town03/scene0-pd45-azm{}'.format(scene)
        try:
            os.system('python3 ../util/environment.py -azm {}'.format(scene))
        except Exception:
            return
        run_command = 'python3 nav_sync_mode.py -s {} -e {} -o {} -w {} --height {} -n 200 '.format(start, end, output, 1912, 1028)
        try:
            os.system(run_command)
        except Exception:
            break
    
    scenes = ['20', '30', '40', '50', '60', '70']
    try:
        os.system('python3 ../util/environment.py -azm 180')
    except Exception:
        return
    for scene in scenes:
        output = '/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/reflection/puddle-sun-town03/scene0-azm180-pd{}'.format(scene)
        try:
            os.system('python3 ../util/environment.py -pd {}'.format(scene))
        except Exception:
            return
        run_command = 'python3 nav_sync_mode.py -s {} -e {} -o {} -w {} --height {} -n 200 '.format(start, end, output, 1912, 1028)
        try:
            os.system(run_command)
        except Exception:
            break

if __name__ == '__main__':
    base_dir = '/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/shadow/wire4-shadow-town03/scene0-azm270-alt'
    origin_dir = '/media/wanglu/MyPassport/Carla-Images/lane-detection-benchmark/shadow/wire4-shadow-town03/scene0-origin-azm0-alt30'
    test([1912, 1028])
    # sun_pd_test()