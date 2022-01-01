# -*- coding: utf-8 -*-
# @Time : 2021/5/25
# @Author : handsomezhou
from util import TimeUtil

PY_DEMO_DAEMON_CHECK_INTERVAL_TIME_SEC = int(15)
PY_DEMO_CHECK_INTERVAL_TIME_SEC = int(20)


#PyDemo心跳时间更新最小间隔时间秒
PY_DEMO_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_SEC=int(30)
#PyDemo心跳时间更新最小间隔时间毫秒
PY_DEMO_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_MS=TimeUtil.sec2ms(PY_DEMO_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_SEC)
#PyDemo心跳时间更新最大间隔时间秒
PY_DEMO_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_SEC=int(120)
#PyDemo心跳时间更新最大间隔时间毫秒
PY_DEMO_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_MS=TimeUtil.sec2ms(PY_DEMO_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_SEC)




#PyDemo守护进程心跳时间更新最小间隔时间秒
PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_SEC=int(30)
#PyDemo守护进程心跳时间更新最小间隔时间毫秒
PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_MS=TimeUtil.sec2ms(PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_SEC)
#PyDemo守护进程心跳时间更新最大间隔时间秒
PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_SEC=int(120)
#PyDemo守护进程心跳时间更新最大间隔时间毫秒
PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_MS=TimeUtil.sec2ms(PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_SEC)
