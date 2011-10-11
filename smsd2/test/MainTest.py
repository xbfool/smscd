import nose

if __name__ == '__main__':
    nose.run(argv = ['', 
                     'WsgiEngineTest',
                     'YamlTest',
                     'DbTest',
                     'ContextTest',
                     'ChannelTest',
                     'ChannelListTest',
                     'SmsdCommandTest',
                     'WsgiCommandTest',
                     '--verbosity=2'])

#TODO：
