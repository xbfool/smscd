# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

def split_message(msg, char_count_per_msg, has_prefix, postfix):
    '''
    各文本的编码由外部统一，这里不做处理 
    '''
    if len(msg) + len(postfix) <= char_count_per_msg:
        #normal: only add a postfix
        return ['%s%s' % (msg, postfix)]

    if len(postfix) >= char_count_per_msg / 3:
        #a 1/3 length postfix is too long
        return None
    elif char_count_per_msg <= 30:
        #something is wrong
        return None
    elif len(msg) >= 1000:
        #this is not a short message
        return None
        
    if has_prefix:
        return split_with_prefix(msg, char_count_per_msg, postfix)
    else:
        return split_without_prefix(msg, char_count_per_msg, postfix)
    
def split_without_prefix(msg, char_count_per_msg, postfix):
    length = char_count_per_msg - len(postfix)
    return ['%s%s' % (msg[i:i+length], postfix) for i in range(0, len(msg), length)]

def compute_total_msg_num(msg, n_per_msg):
    '''
    只在有prefix时候才有意义,已经去掉了postfix的长度
    如果n_per_msg < 7或者len(msg) > 1000则无效
    '''
    if n_per_msg <= 7 or len(msg) >= 1000:
        return 0
        
    if len(msg) <= (n_per_msg - 5) * 9:
        return (len(msg) - 1) / (n_per_msg - 5) + 1
    else:
        remain_msg_len = len(msg) - (n_per_msg - 5) * 9
        return 9 + (remain_msg_len - 1) / (n_per_msg - 7) + 1

        
def split_with_prefix(msg, char_count_per_msg, postfix):
    index = 1
    msg_total_num = compute_total_msg_num(msg, char_count_per_msg - len(postfix))
    if msg_total_num == 0:
        return []
        
    msg_remain = msg[:]
    ret = []
    while len(msg_remain) > 0:
        prefix = '(%d/%d)' % (index, msg_total_num)
        split_index = char_count_per_msg - len(postfix) - len(prefix)
        ret.append('%s%s%s' %(prefix, msg_remain[:split_index], postfix))
        msg_remain = msg_remain[split_index:]
        index += 1
    return ret
    
if __name__ == '__main__':
    print str(split_message('1234567890'*20, 60, False, 'abc'))
    print str(split_message('1234567890'*600, 60, True, 'abc'))
    print compute_total_msg_num('1234567890'*50, 57)