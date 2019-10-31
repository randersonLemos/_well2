import pathlib


def gen_inje_icv(well, fluid, operate, monitor, completion, opening, on_time
        , layerclump, icv_start, icv_control, output_folder):
    from well.scripts.frames.inje_dual_icv import Inje_Dual_ICV
    w = Inje_Dual_ICV(well, 'INJECTION')

    w.get_incomp(fluid)

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in completion:
        w.get_completion(com)

    w.get_on_time(on_time)
    w.get_open(opening)

    for lay in layerclump:
        w.get_layerclump(lay)

    if icv_start:
        w.get_icv_start(icv_start)
        w.get_icv_control(icv_control)

    w.build()
    w.write(pathlib.Path(output_folder) / '{}.inc'.format(well))

def gen_inje_wag(well, operate, monitor, completion, opening, on_time
        , wag, layerclump, output_folder):
    from well.scripts.frames.inje_dual_wag import Inje_Dual_Wag
    w = Inje_Dual_Wag(well, 'INJECTION')

    w.get_incomp('W','*WATER')
    w.get_incomp('G','*GAS')

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in completion:
        w.get_completion(com)

    w.get_on_time(on_time)
    w.get_open(*opening)

    for lay in layerclump:
        w.get_layerclump(lay)

    w.get_wag(*wag)

    w.build()
    w.write(pathlib.Path(output_folder) / '{}.inc'.format(well))

def gen_prod_icv(well, operate, monitor, completion, opening, on_time
        , layerclump, icv_start, icv_control, output_folder):
    from well.scripts.frames.prod_dual_icv import Prod_Dual_ICV
    w = Prod_Dual_ICV(well, 'PRODUCTION')

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in completion:
        w.get_completion(com)

    w.get_on_time(on_time)
    w.get_open(opening)

    for lay in layerclump:
        w.get_layerclump(lay)

    if icv_start:
        w.get_icv_start(icv_start)
        w.get_icv_control(icv_control)

    w.build()
    w.write(pathlib.Path(output_folder) / '{}.inc'.format(well))


if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    from dictionary.scripts.dictionary import Keywords as kw

    well = 'AWESOME'

    completion = []
    completion.append(('25', '10', '01', '1.0', '*OPEN'))
    completion.append(('25', '10', '02', '1.0', '*OPEN'))
    completion.append(('25', '10', '03', '1.0', '*OPEN'))
    completion.append(('25', '10', '04', '1.0', '*OPEN'))
    completion.append(('25', '10', '05', '1.0', '*OPEN'))

    layerclump = []
    layerclump.append('25 10 01:11')
    layerclump.append('25 10 14:19')

    operate = []
    operate.append((kw.max(), kw.stl(), 3000.0, '*CONT *REPEAT'))
    operate.append((kw.min(), kw.bhp(),  295.0, '*CONT *REPEAT'))

    monitor = []
    monitor.append((kw.wcut(), 0.95, kw.shutin()))

    openn = 1704

    on_time = 1.0

    icv_nr = 3

    icv_start = (2008, 183, 200)

    icv_control = [(('*ON_CTRLLUMP __LAYER__ *GOR > 750','AND','*ON_CTRLLUMP _LAYER_ *GOR < 1250',0.0),('*ON_CTRLLUMP __LAYER__ *WCUT > 0.95',0.0))]*icv_nr

    gen_prod_icv(  well
                 , operate
                 , monitor
                 , completion
                 , openn
                 , on_time
                 , layerclump
                 , icv_start
                 , icv_control
                 , './wells/producers'
                 )

    operate = []
    operate.append((kw.max(), kw.stw(),    5000.0, '*CONT *REPEAT'))
    operate.append((kw.max(), kw.bhp(),     470.0, '*CONT *REPEAT'))

    monitor = []

    gen_inje_icv(  well
                 , '*WATER'
                 , operate
                 , monitor
                 , completion
                 , openn
                 , on_time
                 , layerclump
                 , icv_start
                 , icv_control
                 , './wells/injectors'
                 )


    operate = []
    operate.append(('G', kw.max(), kw.stg(), 3000000.0, '*CONT *REPEAT'))
    operate.append(('G', kw.max(), kw.bhp(),     540.0, '*CONT *REPEAT'))
    operate.append(('W', kw.max(), kw.stw(),    5000.0, '*CONT *REPEAT'))
    operate.append(('W', kw.max(), kw.bhp(),     470.0, '*CONT *REPEAT'))

    monitor = []

    openn = ('W', 1734.0)

    wag_cycle = ('G', 1918.0, 183.0, 100)

    gen_inje_wag(  well
                 , operate
                 , monitor
                 , completion
                 , openn
                 , on_time
                 , wag_cycle
                 , layerclump
                 , './wells/injectors_wag'
                 )
