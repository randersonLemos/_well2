import pathlib
from . import frames
from . import utils

def txt_to_lst(completion):
    lst = []
    for line in completion.strip().splitlines():
        words = line.split()
        lst.append(tuple(words))
    return lst

def gen_prod_icv(operate, monitor, well_completion, well_opening, well_on_time
        , icv_layerclump, icv_start, icv_control, output_folder):
    for key in well_completion:
        p = frames._Frame_Prod_Dual(key, 'PRODUCTION')

        for ope in operate:
            p.get_operate(*ope)

        for mon in monitor:
            p.get_monitor(*mon)

        p.get_geometry('*K',0.108,0.370,1.0,0.0)
        p.get_perf('*GEOA')

        for com in utils.txt_to_lst(well_completion[key]):
            p.get_completion(com)

        p.get_on_time(well_on_time[key])
        p.get_open(well_opening[key])

        for lay in icv_layerclump[key]:
            p.get_layerclump(lay)

        if icv_start:
            p.get_icv_start(icv_start[key])
            p.get_icv_control(icv_control[key])

        p.build()
        p.write(pathlib.Path(output_folder) / '{}.inc'.format(key))

def gen_inje_wag(operate, monitor,  well_completion, well_opening, well_on_time
        , well_wag, output_folder):
    for key in well_completion:
        i = frames._Frame_Inje_Dual_Wag(key, 'INJECTION')

        for ope in operate:
            i.get_operate(*ope)

        for mon in monitor:
            i.get_monitor(*mon)

        i.get_geometry('*K',0.108,0.370,1.0,0.0)
        i.get_perf('*GEOA')

        for com in utils.txt_to_lst(well_completion[key]):
            i.get_completion(com)

        i.get_on_time(well_on_time[key])
        i.get_open(*well_opening[key])

        i.get_wag(*well_wag[key])

        i.build()
        i.write(pathlib.Path(output_folder) / '{}.inc'.format(key))