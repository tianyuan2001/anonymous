environment.py
--sun 可设置day night sunset 光照
--weather 可设置天气 clear overcast rain
-lg设置管理哪些灯
--lights对灯光进行详细设置，on/off/intensity {xx}/color {r} {g} {b}
不要动intensity！！
--rain设置当前下雨的雨量
-pd设置路面积水的多少

--sun night

①可选地图：town01，town06 ，town10灯多，待补充
②可调整参数（environment.py  --weather rain）
    控制水坑 -pd 40 - 70 没连起来的水坑由小到大  80 - 100 路面一层水
    控制灯光 --lights color  255 127 0 黄光
            --lights color 244 207 133 默认白光
    控制雨量 rain 0-100