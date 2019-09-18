from scripts.misc import Keywords as kw

def example1(): # producer
    from scripts.utils import gen_prod_icv as gpi
    import scripts.info_producers as ip
    cont_repeat ='{} {}'.format(kw.cont(), kw.repeat())

    operate = [ (kw.max(), kw.stl(), 3000.0, cont_repeat)
               ,(kw.min(), kw.bhp(),  295.0, cont_repeat)
              ]

    monitor = [(kw.wcut(), 0.95, kw.shutin())]

    for well in ip.well_lst:
        gpi(  well
            , operate
            , monitor
            , ip.completion_dic[well]
            , ip.opening_dic[well]
            , ip.on_time_dic[well]
            , ip.layerclump_dic[well]
            , ip.icv_start_dic[well]
            , ip.icv_control_dic[well]
            , './wells'
            )

def example2(): # injector of water
    from scripts.utils import gen_inje_icv as gii
    import scripts.info_injectors as ii
    cont_repeat = '{} {}'.format(kw.cont(),kw.repeat())

    operate = [ (kw.max(), kw.stw(), 5000.0, cont_repeat)
               ,(kw.max(), kw.bhp(),  470.0, cont_repeat)
              ]

    monitor = []

    for well in ii.well_lst:
        gii(  well
            , '*WATER'
            , operate
            , monitor
            , ii.completion_dic[well]
            , ii.opening_dic[well]
            , ii.on_time_dic[well]
            , ii.layerclump_dic[well]
            , []
            , []
            , './wells'
            )

def example3(): # injector with wag
    from scripts.utils import gen_inje_wag as giw
    import scripts.info_injectors_wag as iiw
    cont_repeat = '{} {}'.format(kw.cont(),kw.repeat())

    operate = [ ('G', kw.max(), kw.stg(), 3000000.0, cont_repeat)
               ,('G', kw.max(), kw.bhp(),     540.0, cont_repeat)
               ,('W', kw.max(), kw.stw(),    5000.0, cont_repeat)
               ,('W', kw.max(), kw.bhp(),     470.0, cont_repeat)
              ]

    monitor = []

    for well in iiw.well_lst:
        giw(  well
            , operate
            , monitor
            , iiw.completion_dic[well]
            , iiw.opening_dic[well]
            , iiw.on_time_dic[well]
            , iiw.wag_dic[well]
            , iiw.layerclump_dic[well]
            , []
            , []
            , './wells'
            )

if __name__ == '__main__':
    example1()
    example2()
    example3()
