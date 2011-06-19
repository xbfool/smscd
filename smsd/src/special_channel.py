'''
Created on 2011-6-9

@author: xbfool
'''

def special_channel(channels):
    special_channel = {
      'honglian_01': (  '10657500007095555', '10690095007095555', '10690095007095555'),
      'honglian_bjyh': ('10657500007095526', '10690095007095526', '10690095007095526'),
      'honglian_jtyh':( '10657500007095559', '10690095007095559', '10690095007095559')
                       }
    number = []
    for i in channels:
        if i in special_channel.keys():
            m = special_channel[i]
            for j in m:
                number.append(j)
               
    n = [] 
    for i in number:
        if i not in n:
            n.append(i)
    return n