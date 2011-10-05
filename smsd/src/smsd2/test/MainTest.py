import nose

if __name__ == '__main__':
    nose.run(argv = ['', 
                     'WsgiEngineTest',
                     'YamlTest',
                     'DbTest',
                     'ContextTest',
                     '--verbosity=2'])