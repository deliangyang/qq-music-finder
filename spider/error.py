
ERROR_MESSAGE_OFF_LINE = 'QQ音乐已下架'
ERROR_MESSAGE_NOT_FOUND = 'QQ音乐搜索不到该伴奏'
ERROR_MESSAGE_FORBIDDEN = '歌名歌手错误或禁歌下架'
ERROR_MESSAGE_NOT_COMPANY_INFO = 'QQ音乐无唱片公司信息'
ERROR_MESSAGE_UNKNOWN = '未知异常，待分析'


class ErrorForbidden(Exception):

    def __init__(self):
        pass


def with_error_stack(e):
    return {
        'error': e,
        'file': e.__traceback__.tb_frame.f_globals['__file__'],
        'line': e.__traceback__.tb_lineno,
    }
