import os
import re
import time

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from library.core.utils.applicationcache import MOBILE_DRIVER_CACHE, current_mobile


class BasePage(object):
    """PageObject 应该从该基类继承"""
    ACTIVITY = ''

    @property
    def activity(self):
        return self.__class__.ACTIVITY

    @property
    def driver(self):
        return MOBILE_DRIVER_CACHE.current.driver

    @property
    def mobile(self):
        return current_mobile()

    def background_app(self, seconds):
        self.driver.background_app(seconds)

    def terminate_app(self, app_id, **options):
        self.terminate_app(app_id, **options)

    def _get_platform(self):
        try:
            platform_name = self.driver.desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()

    def _get_device_model(self):
        """获取设备型号"""
        platform = self._get_platform()
        if platform == 'android':
            model = self.execute_shell_command('getprop', 'ro.product.model')
            return model.strip()
        elif platform == 'ios':
            return 'ios'
        else:
            return 'other'

    def get_element(self, locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def get_text(self, locator):
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].text
        return None

    def is_text_present(self, text):
        """检查屏幕是否包含文本"""
        return self.mobile.is_text_present(text)

    def _is_element_present(self, locator):
        elements = self.get_elements(locator)
        return len(elements) > 0

    def _is_visible(self, locator):
        elements = self.get_elements(locator)
        if len(elements) > 0:
            return elements[0].is_displayed()
        return None

    def _is_clickable(self, locator):
        mapper = {
            'true': True,
            'false': False,
            'True': True,
            'False': False
        }
        element = self.get_element(locator)
        value = element.get_attribute('clickable')
        is_clickable = mapper[value.lower()]
        return is_clickable

    def _is_element_text_match(self, locator, pattern, full_match=True, regex=False):
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            return False
        return True

    def execute_shell_command(self, command, *args):
        """
        Execute ADB shell commands (requires server flag --relaxed-security to be set)

        例：execute_shell_command('am', 'start', '-n', 'com.example.demo/com.example.test.MainActivity')

        :param command: 例：am,pm 等等可执行命令
        :param args: 例：am,pm 等可执行命令的参数
        :return:
        """
        script = {
            'command': command,
            'args': args
        }
        return self.driver.execute_script('mobile:shell', script)

    def _is_enabled(self, locator):
        element = self.get_element(locator)
        return element.is_enabled()

    def get_source(self):
        return self.driver.page_source

    def click_element(self, locator, default_timeout=5):
        self.mobile.click_element(locator, default_timeout)

    def is_current_activity_match_this_page(self):
        return self.driver == self.__class__.ACTIVITY

    def click_text(self, text, exact_match=False):
        if self._get_platform() == 'ios':
            if exact_match:
                _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
            else:
                _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
            self.get_element((MobileBy.XPATH, _xpath)).click()
        elif self._get_platform() == 'android':
            if exact_match:
                _xpath = u'//*[@{}="{}"]'.format('text', text)
            else:
                _xpath = u'//*[contains(@{},"{}")]'.format('text', text)
            self.get_element((MobileBy.XPATH, _xpath)).click()

    def input_text(self, locator, text):
        self.mobile.input_text(locator, text)

    def select_checkbox(self, locator):
        """勾选复选框"""
        if not self.is_selected(locator):
            self.click_element(locator)

    def unselect_checkbox(self, locator):
        """去勾选复选框"""
        if self.is_selected(locator):
            self.click_element(locator)

    def is_selected(self, locator):
        el = self.get_element(locator)
        result = el.get_attribute("checked")
        if result.lower() == "true":
            return True
        return False

    def checkbox_should_be_selected(self, locator):
        # element = self.get_element(locator)
        if not self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should have been selected "
                                 "but was not.".format(locator))
        return True

    def checkbox_should_not_be_selected(self, locator):
        # element = self.get_element(locator)
        if self.is_selected(locator):
            raise AssertionError("Checkbox '{}' should not have been selected "
                                 "but was not.".format(locator))
        return True

    def swipe_by_direction(self, locator, direction, duration=None):
        """
        在元素内滑动
        :param locator: 定位器
        :param direction: 方向（left,right,up,down）
        :param duration: 持续时间ms
        :return:
        """
        element = self.get_element(locator)
        rect = element.rect
        left, right = int(rect['x']) + 1, int(rect['x'] + rect['width']) - 1
        top, bottom = int(rect['y']) + 1, int(rect['y'] + rect['height']) - 1
        width = int(rect['width']) - 2
        height = int(rect['height']) - 2

        if self._get_platform() == 'android':
            if direction.lower() == 'left':
                x_start = right
                x_end = left
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_end = right
                y_start = (top + bottom) // 2
                y_end = (top + bottom) // 2
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = bottom
                y_end = top
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_end = (left + right) // 2
                y_start = top
                y_end = bottom
                self.driver.swipe(x_start, y_start, x_end, y_end, duration)

        else:
            if direction.lower() == 'left':
                x_start = right
                x_offset = width
                y_start = (top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'right':
                x_start = left
                x_offset = width
                y_start = -(top + bottom) // 2
                y_offset = 0
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'up':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = bottom
                y_offset = -height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)
            elif direction.lower() == 'down':
                x_start = (left + right) // 2
                x_offset = 0
                y_start = top
                y_offset = height
                self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def swipe_by_percent_on_screen(self, start_x, start_y, end_x, end_y, duration):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        if self._get_platform() == 'android':
            self.driver.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.driver.swipe(x_start, y_start, x_offset, y_offset, duration)

    def page_should_contain_text(self, text):
        if not self.is_text_present(text):
            raise AssertionError("Page should have contained text '{}' "
                                 "but did not" % text)
        return True

    def page_should_not_contain_text(self, text):
        if self.is_text_present(text):
            raise AssertionError("Page should not have contained text '{}'" % text)
        return True

    def page_should_contain_element(self, locator):
        if not self._is_element_present(locator):
            raise AssertionError("Page should have contained element '{}' "
                                 "but did not".format(locator))
        return True

    def page_should_not_contain_element(self, locator):
        if self._is_element_present(locator):
            raise AssertionError("Page should not have contained element {}".format(locator))
        return True

    def element_should_be_disabled(self, locator):
        if self._is_enabled(locator):
            raise AssertionError("Element '{}' should be disabled "
                                 "but did not".format(locator))
        return True

    def element_should_be_enabled(self, locator):
        if not self._is_enabled(locator):
            raise AssertionError("Element '{}' should be enabled "
                                 "but did not".format(locator))
        return True

    def element_should_be_visible(self, locator):
        if not self.get_element(locator).is_displayed():
            raise AssertionError("Element '{}' should be visible "
                                 "but did not".format(locator))
        return True

    def element_should_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected not in actual:
            if not message:
                message = "Element '{}' should have contained text '{}' but " \
                          "its text was '{}'.".format(locator, expected, actual)
            raise AssertionError(message)
        return True

    def element_should_not_contain_text(self, locator, expected, message=''):
        actual = self.get_text(locator)
        if expected in actual:
            if not message:
                message = "Element {} should not contain text '{}' but " \
                          "it did.".format(locator, expected)
            raise AssertionError(message)
        return True

    def element_text_should_be(self, locator, expected, message=''):
        element = self.get_element(locator)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '{}' should have been '{}' but in fact it was '{}'." \
                    .format(locator, expected, actual)
            raise AssertionError(message)
        return True

    def element_text_should_match(self, locator, pattern, full_match=True, regex=False):
        """断言元素内文本，支持正则表达式"""
        return self.mobile.assert_element_text_should_match(locator, pattern, full_match, regex)

    def wait_until(self, condition, timeout=8, auto_accept_permission_alert=True):
        return self.mobile.wait_until(condition, timeout=timeout,
                                      auto_accept_permission_alert=auto_accept_permission_alert)

    def wait_condition_and_listen_unexpected(
            self,
            condition,
            timeout=8,
            auto_accept_permission_alert=True,
            unexpected=None
    ):
        return self.mobile.wait_condition_and_listen_unexpected(
            condition,
            timeout=timeout,
            auto_accept_permission_alert=auto_accept_permission_alert,
            unexpected=unexpected
        )

    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """默认使用activity作为判断页面是否加载的条件，继承类应该重写该方法"""
        self.wait_until(
            lambda d: self.driver.current_activity == self.__class__.ACTIVITY,
            timeout,
            auto_accept_alerts
        )
        return self

    def _is_text_present_contains(self, locator, pattern, full_match=False, regex=False):
        element = self.get_element(locator)
        actual = element.text
        if regex:
            if full_match:
                pt = re.compile(pattern)
                result = pt.fullmatch(actual)
            else:
                pt = re.compile(pattern)
                result = pt.search(actual)
        else:
            if full_match:
                result = pattern == actual
            else:
                result = pattern in actual
        if not result:
            return False
        return True

    def run_app_in_background(self, seconds=5):
        """让 app 进入后台运行seconds 秒"""
        self.driver.background_app(seconds)

    def get_error_code_info_by_adb(self, pattern, timeout=5):
        """通过adb log 获取错误码信息"""
        os.system("adb logcat -c")
        cmd = ' adb logcat -d |findstr %s > tmp.txt' % pattern
        n = 0
        code_info = None
        while n < timeout:
            os.system(cmd)
            with open("tmp.txt", 'r', encoding="utf-8") as f:
                code_info = f.read()
                if code_info:
                    break
                else:
                    time.sleep(1)
                    n += 1
                    continue
        if os.path.exists("tmp.txt"):
            os.remove("tmp.txt")
        return code_info

    def get_network_status(self):
        """获取网络链接状态"""
        return self.driver.network_connection

    def set_network_status(self, status):
        """设置网络
        Connection types are specified here:
        https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile#120
        Value (Alias)      | Data | Wifi | Airplane Mode
        -------------------------------------------------
        0 (None)           | 0    | 0    | 0
        1 (Airplane Mode)  | 0    | 0    | 1
        2 (Wifi only)      | 0    | 1    | 0
        4 (Data only)      | 1    | 0    | 0
        6 (All network on) | 1    | 1    | 0

        class ConnectionType(object):
            NO_CONNECTION = 0
            AIRPLANE_MODE = 1
            WIFI_ONLY = 2
            DATA_ONLY = 4
            ALL_NETWORK_ON = 6

        """
        self.driver.set_network_connection(status)

    def is_toast_exist(self, text, timeout=30, poll_frequency=0.5):
        """is toast exist, return True or False
        :Args:
         - text   - toast文本内容
         - timeout - 最大超时时间，默认30s
         - poll_frequency  - 间隔查询时间，默认0.5s查询一次
        :Usage:
         is_toast_exist("toast的内容")
        """
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
            return True
        except:
            return False

    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        """隐藏键盘"""
        self.mobile.hide_keyboard(key_name, key, strategy)
