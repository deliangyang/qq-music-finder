import wx
import os
import datetime
from spider.task.runner import Runner
from spider.utils.logger import logger
from spider.error import with_error_stack


class MainPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.label_thread_num = wx.StaticText(self, -1, "开启线程数：", size=(80, 30), pos=(270, 110))
        self.sizer.Add(self.label_thread_num,  0, wx.Center, border=10)
        self.text_thread_num = wx.TextCtrl(self, value='3', size=(100, 30), pos=(350, 105),)
        self.sizer.Add(self.text_thread_num, 0, wx.Center, border=10)

        self.label_beat_id = wx.StaticText(self, -1, "开始伴奏ID：", size=(80, 30), pos=(270, 155), )
        self.sizer.Add(self.label_beat_id, 0, wx.Center, border=10)
        self.text_beat_id = wx.TextCtrl(self, value='0', size=(100, 30), pos=(350, 150), )
        self.sizer.Add(self.text_beat_id, 0, wx.Center, border=10)

        self.btn = wx.Button(self, 1, "查询伴奏数据", size=(100, 30), pos=(350, 200))
        self.status_bar = parent.status_bar
        self.sizer.Add(self.btn, 0, wx.CENTER, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_get_file, self.btn)

        self.filename = ''
        self.dirname = ''

    def on_get_file(self, e):
        try:
            thread_num = int(self.text_thread_num.GetValue())
            if thread_num <= 0 or thread_num > 10:
                dlg = wx.MessageDialog(None, '线程数必须大于0，小于等于10的整数', '错误', wx.YES_NO)
                if dlg.ShowModal() == wx.ID_YES:
                    pass
                dlg.Destroy()
                return False
        except Exception as ex:
            logger.error(ex)
            dlg = wx.MessageDialog(None, '线程数必须大于0，小于等于10的整数', '错误', wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            dlg.Destroy()
            return False

        try:
            start_beat_id = int(self.text_beat_id.GetValue())
        except Exception as ex:
            logger.error(ex)
            start_beat_id = 0

        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.xlsx;*.xls", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
            return
        self.filename = dlg.GetFilename()
        self.dirname = dlg.GetDirectory()
        dlg.Destroy()
        self.btn.Disable()
        self.init_status_bar()
        self.status_bar.SetStatusText(u"状态：处理中...", 0)
        thread = Runner(
            filename=self.dirname + os.sep + self.filename,
            save_file=self.get_storage_path(),
            cb=self.after_parse,
            start=start_beat_id,
            thread_num=thread_num
        )
        thread.start()

    def get_storage_path(self):
        dirname = os.path.join(
            self.get_desktop_path(),
            '伴奏列表'
        )
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return os.path.join(
            dirname,
            (str(datetime.datetime.now()) + '.xlsx').replace(' ', '-').replace(':', '')
        )

    def after_parse(self, message):
        self.btn.Enable()

        if message == 'exist':
            dlg = wx.MessageDialog(None, '处理关闭，软件即将退出', '信息', wx.YES_NO)
            if dlg.ShowModal() == wx.ID_YES:
                pass
            dlg.Destroy()
            wx.Exit()

        try:
            thread_num = int(self.text_thread_num.GetValue()) or 3
            beat_id = int(self.text_beat_id.GetValue()) or 0
            self.status_bar.SetStatusText(u"开始ID %d, 线程数: %d" % (beat_id, thread_num), 0)
            self.status_bar.SetStatusText(message, 1)
        except Exception as e:
            logger.error(with_error_stack(e))
            self.status_bar.SetStatusText(u"开始ID %d, 线程数: %d" % (3, 0), 0)
            self.status_bar.SetStatusText(message, 1)

    @classmethod
    def get_desktop_path(cls):
        return os.path.join(os.path.expanduser("~"), 'Desktop')

    def init_status_bar(self):
        try:
            thread_num = int(self.text_thread_num.GetValue()) or 3
            beat_id = int(self.text_beat_id.GetValue()) or 0
        except Exception as e:
            logger.error(with_error_stack(e))
            thread_num = 0
            beat_id = 0
        self.status_bar.SetStatusText(u"开始ID %d, 线程数: %d" % (beat_id, thread_num), 0)
        self.status_bar.SetStatusText(u"文件路径：", 1)
