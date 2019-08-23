from spider.clean import clean

clean()


if __name__ == '__main__':
    import wx
    from ui.windows import MainWindows
    app = wx.App(False)
    frame = MainWindows(None, "伴奏数据查询")
    app.MainLoop()
