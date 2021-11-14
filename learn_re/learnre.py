import re

if __name__ == '__main__':
    line = 'm12345dmm45'
    regex_str = 'm(\d{2}).*'
    match_obj = re.match(regex_str, line)
    # print(match_obj.groups())
    p_t = '(1[3456789][0-9]{9})'
    phone_str = '13000012312'
    m_obj = re.match(p_t, phone_str)
    # m_obj = re.match(pt, str_t)
    # print(m_obj.groups())

    str_s = '您__好'
    p_t = '(您\W+好)'
    # print(re.match(p_t,str_s).groups())
    pt = '([\u4E00-\u9FA5]+)'
    str_s = '你好啊'
    # print(re.match(pt, str_s).groups())
    pt = '.*?([\u4E00-\u9FA5]+)'
    str_s = 'hi,Timmy你好啊, Nice to see you~'
    print(re.match(pt, str_s).groups())