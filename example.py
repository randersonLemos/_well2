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
        , wag, layerclump, icv_start, icv_control, output_folder):
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

    import infos.producers as ip
    gpi = gen_prod_icv
    cont_repeat ='{} {}'.format(kw.cont(), kw.repeat())

    operate = [ (kw.max(), kw.stl(), 3000.0, cont_repeat)
               ,(kw.min(), kw.bhp(),  295.0, cont_repeat)
              ]

    monitor = [(kw.wcut(), 0.95, kw.shutin())]

    for well in ip.well_lst:
        completion = [tuple(line.split()) for line in ip.completion_dic[well].strip().splitlines()]

        gpi(  well
            , operate
            , monitor
            , completion
            , ip.opening_dic[well]
            , ip.on_time_dic[well]
            , ip.layerclump_dic[well]
            , ip.icv_start_dic[well]
            , ip.icv_control_dic[well]
            , './wells/producers'
            )

    import infos.injectors as ii
    gii = gen_inje_icv
    cont_repeat = '{} {}'.format(kw.cont(),kw.repeat())

    operate = [ (kw.max(), kw.stw(), 5000.0, cont_repeat)
               ,(kw.max(), kw.bhp(),  470.0, cont_repeat)
              ]

    monitor = []

    for well in ii.well_lst:
        completion = [tuple(line.split()) for line in ii.completion_dic[well].strip().splitlines()]

        gii(  well
            , '*WATER'
            , operate
            , monitor
            , completion
            , ii.opening_dic[well]
            , ii.on_time_dic[well]
            , ii.layerclump_dic[well]
            , []
            , []
            , './wells/injectors'
            )

    import infos.injectors_wag as iiw
    giw = gen_inje_wag
    cont_repeat = '{} {}'.format(kw.cont(),kw.repeat())

    operate = [ ('G', kw.max(), kw.stg(), 3000000.0, cont_repeat)
               ,('G', kw.max(), kw.bhp(),     540.0, cont_repeat)
               ,('W', kw.max(), kw.stw(),    5000.0, cont_repeat)
               ,('W', kw.max(), kw.bhp(),     470.0, cont_repeat)
              ]

    monitor = []

    for well in iiw.well_lst:
        completion = [tuple(line.split()) for line in iiw.completion_dic[well].strip().splitlines()]

        giw(  well
            , operate
            , monitor
            , completion
            , iiw.opening_dic[well]
            , iiw.on_time_dic[well]
            , iiw.wag_dic[well]
            , iiw.layerclump_dic[well]
            , []
            , []
            , './wells/injectors_wag'
            )
