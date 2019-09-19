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
    p = frames.Frame_Prod_Dual(well, 'PRODUCTION')

    for ope in operate:
        p.get_operate(*ope)

    for mon in monitor:
        p.get_monitor(*mon)

    p.get_geometry('*K',0.108,0.370,1.0,0.0)
    p.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
        p.get_completion(com)

    p.get_on_time(on_time)
    p.get_open(opening)

    for lay in layerclump:
        p.get_layerclump(lay)

    if icv_start:
        p.get_icv_start(icv_start)
        p.get_icv_control(icv_control)

    p.build()
    p.write(pathlib.Path(output_folder) / '{}.inc'.format(well))

def gen_inje_icv(well, fluid, operate, monitor, completion, opening, on_time
        , layerclump, icv_start, icv_control, output_folder):
    p = frames.Frame_Inje_Dual(well, 'INJECTION')

    p.get_incomp(fluid)

    for ope in operate:
        p.get_operate(*ope)

    for mon in monitor:
        p.get_monitor(*mon)

    p.get_geometry('*K',0.108,0.370,1.0,0.0)
    p.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
        p.get_completion(com)

    p.get_on_time(on_time)
    p.get_open(opening)

    for lay in layerclump:
        p.get_layerclump(lay)

    if icv_start:
        p.get_icv_start(icv_start)
        p.get_icv_control(icv_control)

    p.build()
    p.write(pathlib.Path(output_folder) / '{}.inc'.format(well))

def gen_inje_wag(well, operate, monitor, completion, opening, on_time
        , wag, layerclump, icv_start, icv_control, output_folder):
    i = frames.Frame_Inje_Dual_Wag(well, 'INJECTION')

    for ope in operate:
        i.get_operate(*ope)

    for mon in monitor:
        i.get_monitor(*mon)

    i.get_geometry('*K',0.108,0.370,1.0,0.0)
    i.get_perf('*GEOA')

    for com in utils.txt_to_lst(completion):
        i.get_completion(com)

    i.get_on_time(on_time)
    i.get_open(*opening)

    for lay in layerclump:
        i.get_layerclump(lay)

    i.get_wag(*wag)

    i.build()
    i.write(pathlib.Path(output_folder) / '{}.inc'.format(well))