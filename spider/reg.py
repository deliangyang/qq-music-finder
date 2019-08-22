import re

re_lyric_name = re.compile(r'词：([^&]+)')
re_song_name = re.compile(r'曲：([^&]+)')
re_arranging_name = re.compile(r'编曲：([^&]+)')
re_split_brackets = re.compile(r'(\[[^]]+\])')  # [....]
re_info = re.compile(r'info\s+:\s+([^;]+)}\);')
re_song_data = re.compile(r'var g_SongData = ([^;]+);')
re_tag = re.compile(r'&#\d+;')
