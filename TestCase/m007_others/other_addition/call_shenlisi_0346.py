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
    def setUp_test_call_shenlisi_0346():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_shenlisi_0346(self):
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
            cp.click_five()
            cp.click_eight()
            cp.click_seven()
            cp.click_five()
            cp.click_five()
            cp.click_three()
            cp.click_seven()
            cp.click_two()
            cp.click_seven()
            cp.click_two()
            time.sleep(1)
        cp.click_call_phone()
        cp.click_voice_call()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.hang_up_voice_call()
        cp.is_type_hefeixin(0, '语音通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        cp.page_should_contain_text('语音通话')
        mess.click_back_by_android()
        mess.click_calls()
        cp = CallPage()
        cp.wait_for_page_load()
        cp.click_multi_party_video()
        cmvp = MultiPartyVideoPage()
        cmvp.input_contact_search("15875537272")
        cmvp.click_text('未知号码')
        cmvp.click_tv_sure()
        time.sleep(1)
        if cp.is_exist_go_on():
            cp.click_go_on()
        # 是否存在设置悬浮窗，存在暂不开启
        SuspendedTips().ignore_tips_if_tips_display()
        cp.hang_up_video_call()
        cp.is_type_hefeixin(0, '视频通话')
        # 进入详情页
        time.sleep(3)
        cp.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        cp.page_should_contain_text('视频通话')


    def tearDown_test_call_shenlisi_0346(self):
        Preconditions.disconnect_mobile('Android-移动')

