from pages.me.MeViewUserProfile import MeViewUserProfilePage

from pages.message.Send_CardName import Send_CardNamePage
import random
from pages.components import ChatNoticeDialog, ContactsSelector
from pages.message.FreeMsg import FreeMsgPage
import os
import time

from appium.webdriver.common.mobileby import MobileBy
from dataproviders import contact2
from preconditions.BasePreconditions import LoginPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from settings import PROJECT_PATH


class Preconditions(LoginPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群返回，无群创建
        if group_name in group_names:
            sog.click_back()
            return
        sog.click_back()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.select_one_group_by_name(group_name)
            scp.wait_for_page_load()

        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_login_chenjialiang_0256():
        Preconditions.select_mobile('Android-移动', True)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_login_chenjialiang_0256(self):
        """登录"""
        Preconditions.make_already_in_one_key_login_page()
        Preconditions.login_by_one_key_login()
        #消息页点击新建消息并同意权限
        message = MessagePage()
        # message.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        message.click_add_icon()
        message.click_new_message()
        message.wait_for_page_load()
        #点击返回，并判断是否正常
        message.click_back()
        self.assertTrue(message.is_on_this_page)

    @staticmethod
    def setUp_test_me_zhangshuli_019():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_me_zhangshuli_019(self):
        """会话窗口中点击删除文本消息"""
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        # 打开‘查看并编辑个人资料’页面
        me.click_view_edit()
        # 点击分享名片
        view_user_profile_page = MeViewUserProfilePage()
        view_user_profile_page.page_down()
        view_user_profile_page = view_user_profile_page.click_share_card()
        # 选择本地联系人
        sc = SelectContactsPage()
        sc.click_phone_contact()
        local_contacts_page = SelectLocalContactsPage()
        search = local_contacts_page.search("1111111111111111")
        result = local_contacts_page.no_search_result()
        self.assertTrue(result)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0023():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0023(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), "你好，testOK !")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0036():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0036(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !'
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        element = select_contacts_page.get_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="%s"]' % msg_text))
        select_contacts_page.press(element)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        select_contacts_page.search(name)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name))
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_contacts_page.is_toast_exist('已转发')
        self.assertTrue(exist)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0037():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0037(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        element = select_contacts_page.get_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="%s"]' % msg_text))
        select_contacts_page.press(element)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))
        elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))
        self.assertTrue(len(elements) == 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0038():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0038(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        element = select_contacts_page.get_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="%s"]' % msg_text))
        select_contacts_page.press(element)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="复制"]'))
        flag = select_contacts_page.is_toast_exist('和飞信：已复制')
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0039():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0039(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        time.sleep(5)
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # message_page.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/action_add" and @class="android.widget.ImageView"]'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        element = select_contacts_page.get_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="%s"]' % msg_text))
        select_contacts_page.press(element)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="收藏"]'))
        flag = select_contacts_page.is_toast_exist('已收藏')
        self.assertTrue(flag)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0040():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0040(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')
        msg_text = '你好，testOK !' + str(random.random())
        select_contacts_page.input_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'), msg_text)
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        try:
            select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'))
        except BaseException:
            print("warn ：非首次进入，无需资费提醒确认！")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'))
        element = select_contacts_page.get_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_message" and @text="%s"]' % msg_text))
        select_contacts_page.press(element)
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="多选"]'))
        self.assertTrue(select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/multi_btn_forward')) == '转发')
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/multi_btn_delete" and @text="删除"]'))
        select_contacts_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="删除"]'))
        select_contacts_page.is_toast_exist("和飞信：删除成功")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0061():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0061(self):
        """进入免费/发送短信查看展示页面"""
        message_page = MessagePage()
        time.sleep(4)
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        title_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/title'))
        self.assertTrue(title_text == "选择联系人")

        search_bar_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/contact_search_bar'))
        self.assertTrue(search_bar_text == "搜索或输入手机号")

        hint_text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/text_hint'))
        self.assertTrue(hint_text == "选择团队联系人")

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0062():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0062(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        time.sleep(4)
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        # TODO 获取不到【放大镜图标】搜索团队联系人：【搜索内容】   > 内容

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0063():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0063(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        # 当无本地搜索结果时
        select_contacts_page.search(name + name)
        time.sleep(3)
        view_elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_list_item and @clickable=true"]'))
        self.assertTrue(len(view_elements) == 0)
        # 当搜索我的电脑相关时，不显示我的电脑
        select_contacts_page.search('我的电脑')
        time.sleep(3)
        view_elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_list_item and @clickable=true"]'))
        self.assertTrue(len(view_elements) == 0)
        # 当搜索一个手机号时
        select_contacts_page.search('13782572918')
        time.sleep(3)
        # 显示网络搜索
        view_elements = select_contacts_page.get_elements(
            (MobileBy.XPATH, '//*[contains(@text,"(未知号码)")]'))
        self.assertTrue(len(view_elements) > 0)

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0071():
        Preconditions.select_mobile('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0071(self):
        """进入免费/发送短信--选择联系人页面"""
        contacts_page = ContactsPage()
        contacts_page.open_contacts_page()
        contacts_page.wait_for_page_load()
        name = 'admin'
        contacts_page.create_contacts_if_not_exits(name, '13333333333')
        message_page = MessagePage()
        message_page.open_message_page()
        # 点击+号
        message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/action_add'))
        # 点击免费短信
        message_page.click_free_sms()
        try:
            text = message_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
            if text == "确定":
                message_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sure_btn'))
        except BaseException:
            print("warn ：非首次进入，无需确认！")
        select_contacts_page = SelectContactsPage()
        # 当有本地搜索结果时 高亮
        select_contacts_page.search(name)
        time.sleep(3)
        falg = select_contacts_page.get_element_attribute(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % name), "enabled")
        self.assertTrue(falg == "true")
        select_contacts_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item'))
        time.sleep(5)
        sms_text = select_contacts_page.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'))
        self.assertTrue(sms_text == '发送短信...')

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0076():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0076(self):
        """将自己发送的文件转发到企业群"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        element = select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        element = select_one_group_page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择一个群"]'))
            # 点击群名称  然后取消
            select_one_group_page.click_element(
                (MobileBy.XPATH,
                 '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
            select_one_group_page.click_element((MobileBy.XPATH,
                                                 '//*[@resource-id="com.chinasofti.rcs:id/btn_cancel" and @text="取消"]'))

            # 点击群名称  然后确认
            select_one_group_page.click_element(
                (MobileBy.XPATH,
                 '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="%s"]' % group_chat_name))
            select_one_group_page.click_element((MobileBy.XPATH,
                                                 '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
            select_one_group_page.is_toast_exist("已转发")
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0106():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0106(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        select_one_group_page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/text_hint" and @text="选择团队联系人"]'))
        # 点击团队名称
        team_name = Preconditions.get_team_name()
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_title_department" and @text="%s"]' % team_name))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name_personal_contactlist" and @text="admin"]'))
        exist = select_one_group_page.is_toast_exist("该联系人不可选择")
        self.assertTrue(exist)
        select_one_group_page.click_element(
            (MobileBy.ID,
             'com.chinasofti.rcs:id/btn_back'))
        select_one_group_page.click_element(
            (MobileBy.ID,
             'com.chinasofti.rcs:id/btn_back'))
        select_one_group_page.click_element(
            (MobileBy.ID,
             'com.chinasofti.rcs:id/back'))
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0125():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0125(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        select_one_group_page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        select_one_group_page.input_text(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_search_bar" and @text="搜索或输入手机号"]'),
            '我的电脑')
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="我的电脑"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0126():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0126(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        select_one_group_page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/item_rl" and @index="1"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))

    @staticmethod
    def setUp_test_msg_weifenglian_1V1_0129():
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        # 从消息进入创建团队页面
        mess.open_workbench_page()
        workbench = WorkbenchPage()
        workbench.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'))
        elements = workbench.get_elements((MobileBy.XPATH,
                                           '//*[@resource-id="com.chinasofti.rcs:id/tv_listitem" and @text="%s"]' % Preconditions.get_team_name()))

        if len(elements) == 0:
            Preconditions.enter_create_team_page()
            Preconditions.create_team()
        else:
            elements[0].click()
        Preconditions.make_already_have_my_group()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_weifenglian_1V1_0129(self):
        """会话窗口中点击删除文本消息"""
        # 推送文件到指定目录
        path = 'aaaresource'
        contact2.push_resource_dir_to_mobile_sdcard2(Preconditions.select_mobile('Android-移动'),
                                                     os.path.join(PROJECT_PATH, path))
        select_one_group_page = SelectOneGroupPage()
        group_chat_name = Preconditions.get_group_chat_name()
        select_one_group_page.select_one_group_by_name(group_chat_name)
        select_one_group_page.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="文件"]'))
        select_one_group_page.click_element(
            (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'))
        elements = select_one_group_page.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        while len(elements) == 0:
            select_one_group_page.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = select_one_group_page.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        select_one_group_page.click_element((MobileBy.XPATH,
                                             '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)
        file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        time.sleep(1)
        select_one_group_page.press(file_elements[0])
        select_one_group_page.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="转发"]'))
        # 点击我的电脑
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/item_rl" and @index="1"]'))
        select_one_group_page.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        exist = select_one_group_page.is_toast_exist("已转发")
        self.assertTrue(exist)
        # 删除所有转发信息
        wait_del_file_elements = select_one_group_page.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="2018-11-09 11-06-18-722582.log"]'))
        for file_element in wait_del_file_elements:
            select_one_group_page.press(file_element)
            select_one_group_page.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_view" and @text="删除"]'))


class Contacts_demo(TestCase):

    @staticmethod
    def setUp_test_msg_hanjiabin_0193():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()


    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0193(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        time.sleep(660)
        send_card.press_mess('给个名片2')
        mess.page_should_not_contain_element((MobileBy.XPATH, '//*[@text="删除"]'))

    @staticmethod
    def setUp_test_msg_hanjiabin_0194():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_allinfo_if_not_exits('给个名片1', '13800138200', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.create_contacts_allinfo_if_not_exits('给个名片2', '13800138300', '中软国际', '软件工程师', 'test1234@163.com')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_hanjiabin_0194(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个名片1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个名片1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'))
        mess.click_element((MobileBy.XPATH, '//*[@text="名片"]'))
        mess.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/contact_name" and @text="给个名片2"]'))
        send_card = Send_CardNamePage()
        send_card.click_share_btn()
        send_card.press_mess('给个名片2')
        mess.click_element((MobileBy.XPATH, '//*[@text="删除"]'))
        mess.page_should_not_contain_text('给个名片2')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0023():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0023(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        # 如果当前页面不存在消息，发送一条消息
        if not single._is_element_present((MobileBy.XPATH, '//*[@text ="测试一个呵呵"]')):
            single.input_text_message("测试一个呵呵")
            single.send_text()
        single.press_mess("测试一个呵呵")
        single.click_forward()
        select_page = SelectContactPage()
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        # 判断存在选择团队联系人按钮
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择一个群"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
        single.page_should_contain_element((MobileBy.XPATH, '//*[@text ="选择团队联系人"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0279():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0279(self):
        """从通话——拨号盘——输入陌生号码——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在通话模块
        call = CallPage()
        # Step 1.点击拨号盘
        if not call.is_on_the_dial_pad():
            call.click_dial_pad()
        # Checkpoint 1.调起拨号盘，输入陌生号码
        call.click_one()
        call.click_three()
        call.click_seven()
        call.click_seven()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_five()
        call.click_three()
        call.click_three()
        time.sleep(3)
        # Step 2.点击上方发送消息
        call.click_send_message()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        # Checkpoint 2.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0280():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])
        Preconditions.enter_call_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0280(self):
        call = CallPage()
        if not call.is_on_the_dial_pad():
            call.click_element((MobileBy.ID, "com.chinasofti.rcs:id/tvCall"))
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_one()
        call.click_three()
        call.click_eight()
        call.click_zero()
        call.click_zero()
        call.click_zero()
        time.sleep(3)
        call.click_call_profile()
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0285():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0285(self):
        contactdetail = ContactDetailsPage()
        contactdetail.delete_contact('测试短信1')
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()

        create_page = CreateContactPage()
        contactspage.click_add()
        create_page.wait_for_page_load()
        create_page.hide_keyboard_if_display()
        create_page.create_contact('测试短信1', '13800138111')
        contactdetail.wait_for_page_load()
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        # 若存在资费提醒对话框，点击确认
        chatdialog = ChatNoticeDialog()
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        self.assertTrue(SingleChatPage().is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0015():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0015(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        # 点击短信按钮
        SingleChatPage().click_sms()
        time.sleep(2)
        # 判断存在？标志
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断存在退出短信按钮
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))
        # 点击？按钮
        chatdialog.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断弹出资费提醒提示框
        chatdialog.page_should_contain_element((MobileBy.XPATH, '//*[@text ="资费提醒"]'))
        # 点击我知道了按钮
        chatdialog.click_element((MobileBy.XPATH, '//*[@text ="我知道了"]'))
        # 判断资费提醒对话框消失
        chatdialog.page_should_not_contain_element((MobileBy.XPATH, '//*[@text ="资费提醒"]'))

    @staticmethod
    def setUp_test_msg_huangcaizui_B_0016():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_B_0016(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        singlechat = SingleChatPage()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_tips_display():
            chatdialog.accept_and_close_tips_alert()
        # 点击短信按钮
        singlechat.click_sms()
        # 判断存在？标志
        time.sleep(2)
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/sms_direction'))
        # 判断存在退出短信按钮
        chatdialog.page_should_contain_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))
        # 点击退出短信按钮
        chatdialog.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'))
        # 判断是否进入单聊对话框
        text = singlechat.is_on_this_page()
        self.assertTrue(lambda: (text.endswith(')') and text.startswith('(')))

    @staticmethod
    def setUp_test_msg_huangcaizui_E_0022():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_E_0022(self):
        # 打开‘我’页面
        me = MePage()
        me.open_me_page()
        time.sleep(3)
        self.assertTrue(me.is_on_this_page())
        me.click_setting_menu()
        me.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/setting_sms_text'))
        SmsSettingPage().assert_menu_item_has_been_turn_on('应用内收发短信')

    @staticmethod
    def setUp_test_msg_huangmianhua_0400():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangmianhua_0400(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词给个红包1
        SearchPage().input_search_keyword("给个红包1")
        # 选择联系人进入联系人页
        mess.choose_chat_by_name('给个红包1')
        # 点击消息按钮发送消息
        ContactDetailsPage().click_message_icon()
        chatdialog = ChatNoticeDialog()
        # 若存在资费提醒对话框，点击确认
        if chatdialog.is_exist_tips():
            chatdialog.accept_and_close_tips_alert()
        single = SingleChatPage()
        single.input_text_message("测试一个呵呵")
        single.send_text()
        single.click_back()
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'))
        mess.click_element((MobileBy.ID, 'com.chinasofti.rcs:id/iv_back01'))
        mess.is_on_this_page()
        single.press_mess("给个红包1")
        mess.click_element((MobileBy.XPATH, '//*[@text ="置顶聊天"]'))
        single.press_mess("给个红包1")
        mess.click_element((MobileBy.XPATH, '//*[@text ="取消置顶"]'))
        mess.delete_message_record_by_name("给个红包1")
        mess.page_should_not_contain_text('给个红包1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0140():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0140(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_edit_group_name_back()
        groupset.wait_for_page_load()
        groupset.click_modify_group_name()
        groupset.save_group_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试群组1')
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_iv_delete_button()
        self.assertEqual(groupset.get_edit_query_text(), '请输入群聊名称')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0141():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0141(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0142():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0142(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0143():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0143(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0144():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0144(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试的")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0145():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0145(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("A")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), 'A')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0146():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0146(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), 'AABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0147():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0147(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0148():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0148(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0149():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0149(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("AABBCCDDEEAABBCCDDEEAABBCCDDEEE")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         'AABBCCDDEEAABBCCDDEEAABBCCDDEE')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0150():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0150(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0151():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0151(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '1')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0152():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0152(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("112233445511223344551122334455")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         '112233445511223344551122334455')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0153():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0153(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("1122334455112233445511223344556")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')),
                         '112233445511223344551122334455')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0154():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0154(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("测试233AA")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试233AA')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0155():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0155(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        groupset.input_new_group_name("!@#$%")
        groupset.save_group_name()
        time.sleep(10)
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '!@#$%')
        groupset.click_modify_group_name()
        time.sleep(2)
        groupset.clear_group_name()
        self.assertFalse(groupset.is_enabled_of_save_group_name_button())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0156():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0156(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_edit_group_name_back()
        groupset.wait_for_page_load()
        groupset.click_modify_group_name()
        groupset.save_group_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/group_name')), '测试群组1')
        groupset.click_modify_group_name()
        groupset.wait_for_modify_groupname_load()
        groupset.click_iv_delete_button()
        self.assertEqual(groupset.get_edit_query_text(), '请输入群聊名称')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0157():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0157(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0158():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0158(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0159():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0159(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_xiaoqiu_0160():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        """需要预置一个联系人"""
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.click_sim_contact()
        contactspage.create_contacts_if_not_exits('测试短信1', '13800138111')
        contactspage.create_contacts_if_not_exits('测试短信2', '13800138112')
        contactspage.open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_xiaoqiu_0160(self):
        mess = MessagePage()
        # 点击消息页搜索
        mess.click_search()
        # 搜索关键词测试群组1
        SearchPage().input_search_keyword("测试群组1")
        # 如果能搜到对应群组，则点击进入；否则创建群组
        if mess._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]')):
            mess.click_element(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_conv_name" and @text ="测试群组1"]'))
        else:
            ContactListSearchPage().click_back()
            contactspage = ContactsPage()
            # 打开联系人页
            contactspage.open_contacts_page()
            contactspage.wait_for_contact_load()
            contactspage.click_sim_contact()
            contactspage.open_group_chat_list()
            # 点击创建群组
            GroupListPage().click_create_group()
            mess.click_element((MobileBy.XPATH, '//*[@text ="选择手机联系人"]'))
            from pages.components import ContactsSelector
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信1"]'))
            ContactsSelector().search('测试短信')
            mess.click_element((MobileBy.XPATH, '//*[@text ="测试短信2"]'))
            mess.click_element((MobileBy.XPATH, '//*[@text ="确定(2/500)"]'))
            BuildGroupChatPage().create_group_chat('测试群组1')
        groupchat = GroupChatPage()
        groupset = GroupChatSetPage()
        groupchat.wait_for_page_load()
        groupchat.click_setting()
        time.sleep(1)
        groupset.click_modify_my_group_name()
        groupset.wait_for_modify_mygroupname_load()
        groupset.clear_group_name()
        groupset.input_new_group_name("和飞信测试和飞信测试的")
        groupset.save_group_card_name()
        groupset.wait_for_page_load()
        self.assertEqual(mess.get_text((MobileBy.ID, 'com.chinasofti.rcs:id/my_group_name')), '和飞信测试和飞信测试')

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0049():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0049(self):
        """消息-消息列表界面新建消息页面返回操作"""
        # 1.正常联网
        # 2.正常登录
        # 3.当前所在的页面是消息列表页面
        mess = MessagePage()
        # Step: 1.点击右上角的+号按钮
        mess.click_add_icon()
        mess.click_new_message()
        select_page = SelectContactPage()
        # checkpoint:1、成功进入新建消息界面
        # 判断存在选择联系人
        select_page.is_exist_select_contact_btn()
        # 判断存在搜索或输入手机号提示
        select_page.is_exist_selectorinput_toast()
        select_page.is_exist_selectortuandui_toast()
        # Setp: 2、点击左上角返回按钮
        select_page.click_back()
        # Checkpoint:2、退出新建消息，返回消息列表
        mess.wait_login_success()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0276():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["给个红包1, 13800138000"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0276(self):
        """从发送短信进入单聊"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.异网用户
        mess = MessagePage()
        # Step 1.点击右上角“+”
        mess.click_add_icon()
        # Step 2.点击发送短信
        mess.click_free_sms()
        freemsg = FreeMsgPage()
        # 若存在欢迎页面
        if freemsg.wait_is_exist_welcomepage():
            # 点击确定按钮
            freemsg.click_sure_btn()
            CallPage().wait_for_freemsg_load()
        select_page = SelectContactPage()
        # Checkpoint 进入联系人选择器（直接选择本地通讯录联系人)
        select_page.is_exist_select_contact_btn()
        # Checkpoint 进入联系人选择器（可在搜索框输入联系人姓名或电话号码搜索)
        select_page.is_exist_selectorinput_toast()
        # Checkpoint 进入联系人选择器（选择团队联系人)
        select_page.is_exist_selectortuandui_toast()
        # Step 3.任意选择一联系人
        ContactsSelector().click_local_contacts('给个红包1')
        # Checkpoint 进入短信编辑页面
        freemsg.wait_is_exist_wenhao()
        freemsg.wait_is_exist_exit()

    @staticmethod
    def setUp_test_msg_huangcaizui_A_0283():
        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page('Android-移动')
        # 下面根据用例情况进入相应的页面
        Preconditions.create_contacts_if_not_exist(["测试短信1, 13800138111", "测试短信2, 13800138112"])

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_msg_huangcaizui_A_0283(self):
        """联系——标签分组——进入单聊页面"""
        # 1.客户端已登录
        # 2.网络正常
        # 3.在联系模块
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.wait_for_contact_load()
        contactspage.click_sim_contact()
        # Step 1.点击上方标签分组图标
        contactspage.click_label_grouping()
        labelgroup = LabelGroupingPage()
        time.sleep(2)
        if '测试分组1' not in labelgroup.get_label_grouping_names():
            labelgroup.create_group('测试分组1', '测试短信1', '测试短信2')
        # Step 2.任意点击一存在多名成员的标签分组
        labelgroup.click_label_group('测试分组1')
        time.sleep(2)
        # Checkpoint 2.进入成员列表页，显示该标签分组中的所有成员
        contactspage.page_should_contain_text('测试短信1')
        contactspage.page_should_contain_text('测试短信2')
        # Step 3.任意选择一标签分组中的联系人
        BaseChatPage().click_to_do('测试短信1')
        # Checkpoint 3.进入联系人详情页面
        self.assertTrue(ContactDetailsPage().is_on_this_page())
        # Step 4.点击消息
        ContactDetailsPage().click_message_icon()
        time.sleep(2)
        # Checkpoint 4.进入单聊页面
        self.assertTrue(SingleChatPage().is_on_this_page())

