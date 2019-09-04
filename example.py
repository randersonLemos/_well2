from scripts.utils import gen_prod_icv as gpi
from scripts.utils import gen_inje_wag as giw
from scripts.misc import Keywords as kw

def example1():
    import scripts.info_producers as ip
    cont_repeat ='{} {}'.format(kw.cont(), kw.repeat())

    operate = [ (kw.max(), kw.stl(), 3000.0, cont_repeat)
               ,(kw.min(), kw.bhp(),  295.0, cont_repeat)
              ]
    monitor = [(kw.wcut(), 0.95, kw.shutin())]
    gpi(  operate
        , monitor
        , ip.well_completion
        , ip.well_opening
        , ip.well_on_time
        , ip.icv_layerclump
        , ip.icv_start
        , ip.icv_control
        , './wells'
        )

def example2():
    import scripts.info_injectors as ii
    cont_repeat = '{} {}'.format(kw.cont(),kw.repeat())
    operate = [ ('G', kw.max(), kw.stg(), 3000000.0, cont_repeat)
               ,('G', kw.max(), kw.bhp(),     540.0, cont_repeat)
               ,('W', kw.max(), kw.stw(),    5000.0, cont_repeat)
               ,('W', kw.max(), kw.bhp(),     470.0, cont_repeat)
              ]
    monitor = []
    giw(  operate
        , monitor
        , ii.well_completion
        , ii.well_opening
        , ii.well_on_time
        , ii.well_wag
        , './wells'
        )

if __name__ == '__main__':
    example1()
    example2()

