import re
import pathlib
from . import misc


def add_quotation_masks(stg):
    return "'{}'".format(stg)


class _State_Dual:
    def __init__(self, well_name, group_name):
            self.well_name = add_quotation_masks(well_name)
            self.group_name = add_quotation_masks(group_name)
            self.operate = []
            self.monitor = []
            self.completion = []
            self.layerclump = []
            self.open = None
            self.perf = None
            self.fluid = None
            self.on_time = None
            self.geometry = None
            self.icv_start = None
            self.icv_control = None
            self._agr = misc.Agregator()

    def get_incomp(self, fluid):
        kw = misc.Keywords
        if not(fluid == kw.gas() or fluid == kw.water()):
            raise NameError('pass to function *GAS or *WATER')
        self.fluid = fluid

    def get_operate(self, cond, const, value, action):
       self.operate.append((cond, const, value, action))

    def get_monitor(self, const, value, action):
        self.monitor.append((const, value, action))

    def get_geometry(self, dir, rad, geofac, wfac, skin):
        self.geometry = (dir, rad, geofac, wfac, skin)

    def get_perf(self, indexes):
        self.perf = indexes

    def get_completion(self, completion):
        self.completion.append(completion)

    def get_on_time(self, value):
        self.on_time = value

    def get_open(self, value):
        self.open = value

    def get_layerclump(self, layerclump):
        self.layerclump.append(layerclump)

    def get_icv_start(self, icv_start):
        self.icv_start = icv_start

    def get_icv_control(self, icv_control):
        self.icv_control = icv_control

    def write(self, folder_to_output):
        p = pathlib.Path(folder_to_output)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as fh: fh.write(self.__repr__())

    def __repr__(self):
        a = self._agr
        return a.__repr__()


class _State_Dual_Two_Modes:
    def __init__(self, base_name, group_name, key_mode1, key_mode2):
        self.well_name = {}
        self.well_name[key_mode1] = add_quotation_masks(base_name + '_{}'.format(key_mode1))
        self.well_name[key_mode2] = add_quotation_masks(base_name + '_{}'.format(key_mode2))
        self.group_name = add_quotation_masks(group_name)
        self.operate = {}
        self.monitor = {}
        self.completion = []
        self.layerclump = []
        self.wag = None
        self.perf = None
        self.open = None
        self.fluid = {}
        self.on_time = None
        self.geometry = None
        self.icv_start = None
        self.icv_control = None
        self._key_mode1 = key_mode1
        self._key_mode2 = key_mode2
        self._agr = misc.Agregator()
        self._settings()

    def _settings(self):
        self.fluid[self._key_mode1] = []
        self.fluid[self._key_mode2] = []
        self.operate[self._key_mode1] = []
        self.operate[self._key_mode2] = []
        self.monitor[self._key_mode1] = []
        self.monitor[self._key_mode2] = []

    def get_incomp(self, mode, fluid):
        kw = misc.Keywords
        if not(fluid == kw.gas() or fluid == kw.water()):
            raise NameError('pass to function *GAS or *WATER')
        self.fluid[mode] = fluid

    def get_operate(self, mode, cond, const, value, action):
        self.operate[mode].append((cond, const, value, action))

    def get_monitor(self, mode, const, value, action):
        self.monitor[mode].append((const, value, action))

    def get_geometry(self, dir, rad, geofac, wfac, skin):
        self.geometry = (dir, rad, geofac, wfac, skin)

    def get_perf(self, indexes):
        self.perf = indexes

    def get_completion(self, completion):
        self.completion.append(completion)

    def get_on_time(self, value):
        self.on_time = value

    def get_open(self, mode, value):
        self.open = (mode, value)

    def get_wag(self, start_mode, timsim, change_cycle, apply_times):
        self.wag = (start_mode, timsim, change_cycle, apply_times)

    def get_layerclump(self, layerclump):
        self.layerclump.append(layerclump)

    def get_icv_start(self, icv_start):
        self.icv_start = icv_start

    def get_icv_control(self, icv_control):
        self.icv_control = icv_control

    def __repr__(self):
        a = self._agr
        return a.__repr__()

    def write(self, fname):
        p = pathlib.Path(fname)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as fh: fh.write(self.__repr__())