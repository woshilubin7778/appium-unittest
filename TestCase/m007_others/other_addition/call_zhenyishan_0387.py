import time
import unittest
from pages.components.dialogs import SuspendedTips
from appium.webdriver.common.mobileby import MobileBy

import preconditions
from dataproviders import contact2
from pages.components import ChatNoticeDialog, SearchBar, ContactsSelector
from pages.components.PickGroup import PickGroupPage
from pages.components.SearchGroup import SearchGroupPage
from pages.message.FreeMsg import FreeMsgPage
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *

class Preconditions(LoginPreconditions):
    """前置条件"""


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_call_zhenyishan_0387():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_zhenyishan_0387(self):
        """仅消息通知提示条时，进行拨打语音通话，两个提示条共存"""
        # 网络正常
        mess = MessagePage()
        # Step 2、进行拨打语音通话
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        pad = cp.is_on_the_dial_pad()
        if not pad:
            cp.click_dial_pad()
            time.sleep(1)
            cp.click_one()
            cp.click_three()
            cp.click_eight()
            cp.click_zero()
            cp.click_zero()
            cp.click_one()
            cp.click_three()
            cp.click_eight()
            cp.click_two()
            cp.click_zero()
            cp.click_zero()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        time.sleep(1)

        cp.click_call_cancel()
        time.sleep(2)
        cp.click_ganggang_call_time()
        cp.page_should_contain_text('中软国际')


    def tearDown_test_call_zhenyishan_0387(self):
        Preconditions.disconnect_mobile('Android-移动')
