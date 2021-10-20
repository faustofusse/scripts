import pysrt

def parse_sub_to_utf8(subtitles):
    subs = pysrt.open(subtitles, encoding='iso-8859-1')
    subs.save(subtitles, encoding='utf-8')

parse_sub_to_utf8(input('Subtitle file: '))