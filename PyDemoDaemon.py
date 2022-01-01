# -*- coding: utf-8 -*-
# @Time : 2021/9/22
# @Author : handsomezhou
import threading
import tkinter as tk
from concurrent.futures.thread import ThreadPoolExecutor

from constant import ThreadPoolConstant, StringConstant, DaemonConstant, Constant, WindowsProgramConstant, \
    SettingConstant
from database.PyDemoSqliteSql import PyDemoSqliteSql

from util import TimeUtil, WindowsUtil, FileUtil


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.start_run_time_ms=TimeUtil.getCurrentTimeMillis()
        self.cur_time_ms=TimeUtil.getCurrentTimeMillis()

        self.pack()
        self.create_widgets()
        self.threadPoolExecutor = ThreadPoolExecutor(max_workers=ThreadPoolConstant.MAX_WORKERS)

        #用于心跳检测等与业务线程分开,避免业务线程全部持续占用导致心跳不正常
        self.baseThreadPoolExecutor= ThreadPoolExecutor(max_workers=ThreadPoolConstant.BASE_WORKERS)

        self.last_write_py_demo_daemon_heartbeat_time_ms = int(0)
        self.last_read_py_demo_heartbeat_time_ms = int(0)
        self.py_demo_sqlite_sql = PyDemoSqliteSql()

        self.try_to_start_py_demo_daemon_check()

    def create_widgets(self):
        # https://www.cnblogs.com/shwee/p/9427975.html#D1
        # https://www.tianqiweiqi.com/python-tkinter-button.html

        # """

        self.start_run_time_label_tips = tk.Label(self, text=StringConstant.start_run_time_label_tips)
        self.start_run_time_label_tips.pack()

        self.start_run_time_label = tk.Label(self, text=TimeUtil.get_log_time_by_ms(self.start_run_time_ms))
        self.start_run_time_label.pack()
        """
        self.test_btn = tk.Button(self)
        self.test_btn["text"] = "测试"
        self.test_btn["command"] = self.test
        self.test_btn.pack()
        """

    def try_to_start_py_demo_daemon_check(self):
        self.baseThreadPoolExecutor.submit(self.py_demo_daemon_check)
        return

    def py_demo_daemon_check(self):
        #print(TimeUtil.getLogTime(),Constant.COLON,"start:py_demo_daemon_check:process")
        try:

            py_demo_running=self.is_py_demo_running()

            if py_demo_running is False:
                has_installed=self.has_py_demo_installed()
                if has_installed is False:
                    force_upgrade = True
                    #print(TimeUtil.getLogTime(),Constant.COLON,"check_py_demo_upgrade",force_upgrade)
                    self.check_py_demo_upgrade(force_upgrade)
                    has_installed=self.has_py_demo_installed()

                if has_installed is True:
                    print(TimeUtil.getLogTime(),Constant.COLON,"开启PyDemo程序")
                    self.open_py_demo()
                else:
                    print(TimeUtil.getLogTime(),Constant.COLON,"PyDemo程序未安装,无法打开该程序")
            else:
                self.try_to_restart_py_demo()

        except Exception as e:
            print(TimeUtil.getLogTime(), Constant.COLON, e.__traceback__.tb_frame.f_globals[Constant.__file__],e.__traceback__.tb_lineno, " py_demo_daemon_check 异常 ", e)
        finally:
            self.try_to_update_py_demo_daemon_heartbeat()
        #print(TimeUtil.getLogTime(),Constant.COLON,"end:py_demo_daemon_check:process")

        self.start_next_py_demo_daemon_check()
        return

    def try_to_update_py_demo_daemon_heartbeat(self):
        current_time_millis = TimeUtil.getCurrentTimeMillis()
        last_update_interval_time_ms = current_time_millis - self.last_write_py_demo_daemon_heartbeat_time_ms
        if last_update_interval_time_ms > DaemonConstant.PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_MS:
            self.last_write_py_demo_daemon_heartbeat_time_ms = current_time_millis
            id = current_time_millis
            value = str(id)
            self.py_demo_sqlite_sql.insert_table_setting_data(id=id,key=SettingConstant.key_py_demo_daemon_heartbeat_time,value=value)
            print(TimeUtil.getLogTime(), Constant.COLON, "更新PyDemo守护进程心跳 [",TimeUtil.get_log_time_by_ms(current_time_millis), "] 距离上次更新时间[",TimeUtil.ms2sec(last_update_interval_time_ms), "]秒")

        else:
            print(TimeUtil.getLogTime(), Constant.COLON, "本次不更新PyDemo守护进程心跳 上次更新时间为[",TimeUtil.get_log_time_by_ms(self.last_write_py_demo_daemon_heartbeat_time_ms),"] 距离上次更新时间[", TimeUtil.ms2sec(last_update_interval_time_ms), "]秒")
        return

    def try_to_restart_py_demo(self):
        current_time_millis = TimeUtil.getCurrentTimeMillis()
        last_update_interval_time_ms = current_time_millis - self.last_read_py_demo_heartbeat_time_ms
        if last_update_interval_time_ms > DaemonConstant.PY_DEMO_DAEMON_HEARTBEAT_TIME_UPDATE_MIN_INTERVAL_TIME_MS:
            self.last_read_py_demo_heartbeat_time_ms = current_time_millis

            value = self.py_demo_sqlite_sql.load_setting_value(
                SettingConstant.key_py_demo_heartbeat_time)

            if value is not None:
                py_demo_heartbeat_time = int(value)
                last_heartbeat_interval_time_ms = current_time_millis - py_demo_heartbeat_time
                if (last_heartbeat_interval_time_ms) > DaemonConstant.PY_DEMO_HEARTBEAT_TIME_UPDATE_MAX_INTERVAL_TIME_MS:
                    print(TimeUtil.getLogTime(), Constant.COLON, "PyDemo心跳异常 上次心跳时间[",TimeUtil.get_log_time_by_ms(py_demo_heartbeat_time), "] 在[",TimeUtil.ms2sec(last_heartbeat_interval_time_ms), "]秒前,将自动重启PyDemo")
                    self.close_py_demo()
                    self.open_py_demo()
                else:
                    print(TimeUtil.getLogTime(), Constant.COLON, "PyDemo心跳正常 上次心跳时间[",TimeUtil.get_log_time_by_ms(py_demo_heartbeat_time), "] 在[",TimeUtil.ms2sec(last_heartbeat_interval_time_ms), "]秒前")

            else:
                print(TimeUtil.getLogTime(), Constant.COLON, "未读取到PyDemo心跳时间,请确保该应用存在")


        else:
            print(TimeUtil.getLogTime(), Constant.COLON, "本次不读取PyDemo心跳时间 上次读取时间 [",TimeUtil.get_log_time_by_ms(self.last_read_py_demo_heartbeat_time_ms), "] 在[",TimeUtil.ms2sec(last_update_interval_time_ms), "]秒前")

        return

    def start_next_py_demo_daemon_check(self):
        ds=DaemonConstant.PY_DEMO_DAEMON_CHECK_INTERVAL_TIME_SEC
        print(TimeUtil.getLogTime(),Constant.COLON,ds,"秒后,开启下一轮守护检测")
        t = threading.Timer(ds, self.try_to_start_py_demo_daemon_check)
        t.start()

    def is_py_demo_running(self):
        py_demo_running=WindowsUtil.checkIfProcessRunning(WindowsProgramConstant.PyDemoNameWithSuffix)
        print(TimeUtil.getLogTime(),Constant.COLON,"PyDemo是否运行中[",py_demo_running,"]")
        return py_demo_running

    def close_py_demo(self):
        close_success=WindowsUtil.closeApp(WindowsProgramConstant.PyDemoNameWithSuffix)
        return close_success

    def open_py_demo(self):
        open_success =WindowsUtil.openApp(WindowsProgramConstant.PY_DEMO_FULL_PATH_BIN)
        return open_success

    def has_py_demo_installed(self):
        has_installed = FileUtil.exists(WindowsProgramConstant.PY_DEMO_FULL_PATH_BIN)
        print(TimeUtil.getLogTime(),Constant.COLON,"PyDemo程序是否安装[",has_installed,"]")
        return has_installed

    def check_py_demo_upgrade(self, force_upgrade):
        print(TimeUtil.getLogTime(), Constant.COLON, "请拷贝相关程序到指定目录 ", WindowsProgramConstant.PY_DEMO_FULL_PATH_BIN)
        return
    def test(self):
        print(TimeUtil.getLogTime(),Constant.COLON,"test")



if __name__ == '__main__':
    root = tk.Tk()
    root.title(StringConstant.py_demo_daemon)
    root.geometry(StringConstant.main_window_geometry)
    app = Application(master=root)
    app.mainloop()
