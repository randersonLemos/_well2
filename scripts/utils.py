import pathlib
from . import frames
from . import utils

def txt_to_lst(completion):
    lst = []
    for line in completion.strip().splitlines():
        words = line.split()
        lst.append(tuple(words))
    return lst

def gen_prod_icv(well, operate, monitor, completion, opening, on_time
        , layerclump, icv_start, icv_control, output_folder):
    w = frames.Frame_Prod_Dual(well, 'PRODUCTION')

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
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

def gen_inje_icv(well, fluid, operate, monitor, completion, opening, on_time
        , layerclump, icv_start, icv_control, output_folder):
    w = frames.Frame_Inje_Dual(well, 'INJECTION')

    w.get_incomp(fluid)

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
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
    w = frames.Frame_Inje_Dual_Wag(well, 'INJECTION')

    w.get_incomp('W','*WATER')
    w.get_incomp('G','*GAS')

    for ope in operate:
        w.get_operate(*ope)

    for mon in monitor:
        w.get_monitor(*mon)

    w.get_geometry('*K',0.108,0.370,1.0,0.0)
    w.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
        w.get_completion(com)

    w.get_on_time(on_time)
    w.get_open(*opening)

    for lay in layerclump:
        w.get_layerclump(lay)

    w.get_wag(*wag)

    w.build()
    w.write(pathlib.Path(output_folder) / '{}.inc'.format(well))