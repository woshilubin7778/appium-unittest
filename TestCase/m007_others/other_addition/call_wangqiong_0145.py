import time

from preconditions.BasePreconditions import LoginPreconditions, ContactsPage, CallPage, CalllogBannerPage
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags


class Preconditions(LoginPreconditions):
    """前置条件"""


class MsgAllPrior(TestCase):

    @staticmethod
    def setUp_test_call_wangqiong_0145():
        """预置条件"""

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'prior', 'high')
    def test_call_wangqiong_0145(self):
        """发起1人的多方电话--再次呼叫，网络正常重新呼叫和飞信电话"""

        # 启动App
        Preconditions.select_mobile('Android-移动')
        # 启动后不论当前在哪个页面，强制进入消息页面
        Preconditions.force_enter_message_page_631()
        # 下面根据用例情况进入相应的页面
        # 新建联系人
        contactspage = ContactsPage()
        contactspage.open_contacts_page()
        contactspage.create_contacts_if_not_exits_631("测试短信1", "13800138111")
        # 进入通话页签
        Preconditions.enter_call_page()
        # 如果存在多方通话引导页跳过引导页
        callcontact = CalllogBannerPage()
        callcontact.skip_multiparty_call()
        # 点击多方通话
        callcontact.click_free_call()
        # 选择指定联系人 点击呼叫
        from pages.components import ContactsSelector
        contactselect = ContactsSelector()
        contactselect.select_local_contacts("测试短信1")
        # 是否存在请先接听“和飞信电话”，点击“我知道了” 并自动允许和飞信管理
        callcontact.click_elsfif_ikonw()
        # 是否存在权限窗口 自动赋权
        from pages import GrantPemissionsPage
        grantpemiss = GrantPemissionsPage()
        grantpemiss.allow_contacts_permission()

        # 是否存在设置悬浮窗，存在暂不开启
        from pages.components.dialogs import SuspendedTips
        suspend = SuspendedTips()
        suspend.ignore_tips_if_tips_display()
        # 会控页面挂断和飞信电话，回到通话页
        callpage = CallPage()
        callpage.hang_up_hefeixin_call_631()

        # Checkpoint：拨打的通话记录为飞信电话 进入通话详情页，标题为飞信通话类型
        callpage.is_type_hefeixin(0, '飞信电话')
        # 进入详情页
        time.sleep(3)
        callpage.click_ganggang_call_time()
        # Checkpoint：查看详情页面是否是为飞信电话？
        callpage.page_should_contain_text('[飞信电话]')
        callpage.page_should_contain_text('拨出电话')



    def tearDown_test_call_wangqiong_0145(self):
        Preconditions.disconnect_mobile('Android-移动')