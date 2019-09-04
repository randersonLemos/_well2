import pathlib
from . import misc

def add_quotation_masks(stg):
    return "'{}'".format(stg)

class _Frame_Prod_Dual:
    def __init__(self, well_name, group_name):
            self.well_name = add_quotation_masks(well_name)
            self.group_name = add_quotation_masks(group_name)
            self.operate = []
            self.monitor = []
            self.completion = []
            self.layerclump = []
            self.open = None
            self.perf = None
            self.on_time = None
            self.geometry = None
            self.icv_start = None
            self.icv_control = None
            self._agr = misc.Agregator()

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

    def build(self):
        kw = misc.Keywords
        na = misc.Names
        a = self._agr

        a.add_four(kw.well(), self.well_name, kw.attachto(), self.group_name)
        a.add_two(kw.producer(), self.well_name)

        for ope in self.operate: a.add_five(kw.operate(), *ope)
        for mon in self.monitor: a.add_four(kw.monitor(), *mon)

        a.add_six(kw.geometry(), *self.geometry)
        a.add_three(kw.perf(), self.perf, self.well_name)

        for idx, com in enumerate(self.completion):
            ff = com[3]
            uba = ' '.join(com[:3])
            status = com[4]
            if idx == 0:
                a.add_seven(uba,kw.mt(),ff,status,kw.flow_to()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
                a.add_seven(uba,kw.fr(),ff,status,kw.flow_to()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
            else:
                a.add_six(uba,kw.mt(),ff,status,kw.flow_to(),'{:02d}'.format(idx))
                a.add_six(uba,kw.fr(),ff,status,kw.flow_to(),'{:02d}'.format(idx))

        a.add_two(kw.shutin(), self.well_name)

        if self.on_time:
            a.add_one('')
            a.add_two(kw.on_time(), self.well_name)
            a.add_one(1)

        if self.open:
            a.add_one('')
            a.add_one('**Trigger for openning')
            name = "'OPEN_{}'".format(self.well_name.strip("'"))
            a.add_seven(kw.trigger(), name, kw.on_elapsed()
                    , na.time(), kw.timsim(),kw.greater_than(), self.open)
            a.add_two(kw.open(), self.well_name, pre='   ')
            a.add_one(kw.end_trigger())

        if self.layerclump:
            a.add_one('')
            a.add_one('**Layerclump for ICVs')
            for idx, layer in enumerate(self.layerclump):
                name = "'{}_Z{}'".format(self.well_name.strip("'"),idx+1)
                a.add_two(kw.layerclump(), name)
                a.add_three(self.well_name, layer, kw.mt())
                a.add_three(self.well_name, layer, kw.fr())

        if self.icv_start:
            a.add_one('')
            a.add_one('**Trigger for ICV control')
            name = "'ICVs_{}'".format(self.well_name.strip("'"))
            nr1, nr2, nr3 = self.icv_start
            timsim = "{} {} {}".format(kw.timsim(), kw.greater_than(), nr1)
            increment = "{} {}".format(kw.increment(), nr2)
            apply_times = "{} {}".format(kw.apply_times(), nr3)
            a.add_seven(kw.trigger(), name, kw.on_elapsed(), na.time()
                    , timsim, increment, apply_times)
            for idx, layer in enumerate(self.layerclump):
                controls = self.icv_control[idx]
                for idx2, control in enumerate(controls):
                    conditions= ' '.join(control[:-1])
                    act = control[-1]
                    name = "'ICV_{}_Z{}_{}'".format(self.well_name.strip("'"),idx+1,idx2+1)
                    a.add_three(kw.trigger(), name, conditions, pre='   ')
                    name = "'{}_Z{}'".format(self.well_name.strip("'"),idx+1)
                    a.add_three(kw.clumpsetting(), name, act, pre='      ')
                    a.add_one(kw.end_trigger(), pre='   ')
            a.add_one(kw.end_trigger())

    def __repr__(self):
        a = self._agr
        return a.__repr__()

    def write(self, folder_to_output):
        p = pathlib.Path(folder_to_output)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as fh: fh.write(self.__repr__())


class _Frame_Inje_Dual_Wag:
    def __init__(self, well_name, group_name):
        self.well_name = {}
        self.well_name['G'] = add_quotation_masks(well_name + '_G')
        self.well_name['W'] = add_quotation_masks(well_name + '_W')
        self.group_name = add_quotation_masks(group_name)
        self.operate = {}
        self.monitor = {}
        self.completion = []
        self.layerclump = []
        self.wag = None
        self.perf = None
        self.open = None
        self.on_time = None
        self.geometry = None
        self.icv_start = None
        self.icv_control = None
        self._agr = misc.Agregator()
        self._settings()

    def _settings(self):
        self.operate['G'] = []
        self.operate['W'] = []
        self.monitor['G'] = []
        self.monitor['W'] = []

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
        if layerclump: self.layerclump.append(layerclump)

    def get_icv_start(self, icv_start):
        self.icv_start = icv_start

    def get_icv_control(self, icv_control):
        self.icv_control = icv_control

    def build(self):
        kw = misc.Keywords
        na = misc.Names
        a = self._agr

        a.add_four(kw.well(), self.well_name['G'], kw.attachto(), self.group_name)
        a.add_two(kw.injector(), self.well_name['G'])
        a.add_two(kw.incomp(), kw.gas())

        for ope in self.operate['G']: a.add_five(kw.operate(), *ope)
        for mon in self.monitor['G']: a.add_four(kw.monitor(), *mon)

        a.add_six(kw.geometry(), *self.geometry)
        a.add_three(kw.perf(), self.perf, self.well_name['G'])

        for idx, com in enumerate(self.completion):
            ff = com[3]
            uba = ' '.join(com[:3])
            status = com[4]
            if idx == 0:
                a.add_seven(uba,kw.mt(),ff,status,kw.flow_from()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
                a.add_seven(uba,kw.fr(),ff,status,kw.flow_from()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
            else:
                a.add_six(uba,kw.mt(),ff,status,kw.flow_from(),'{:02d}'.format(idx))
                a.add_six(uba,kw.fr(),ff,status,kw.flow_from(),'{:02d}'.format(idx))


        a.add_two(kw.shutin(), self.well_name['G'])

        a.add_one('')
        a.add_four(kw.well(), self.well_name['W'], kw.attachto(), self.group_name)
        a.add_two(kw.injector(), self.well_name['W'])
        a.add_two(kw.incomp(), kw.gas())

        for ope in self.operate['W']: a.add_five(kw.operate(), *ope)
        for mon in self.monitor['W']: a.add_four(kw.monitor(), *mon)

        a.add_six(kw.geometry(), *self.geometry)
        a.add_three(kw.perf(), self.perf, self.well_name['W'])

        for idx, com in enumerate(self.completion):
            ff = com[3]
            uba = ' '.join(com[:3])
            status = com[4]
            if idx == 0:
                a.add_seven(uba,kw.mt(),ff,status,kw.flow_from()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
                a.add_seven(uba,kw.fr(),ff,status,kw.flow_from()
                        ,na.surface(),kw.reflayer()
                        ,suf=" ** uba ff status connection")
            else:
                a.add_six(uba,kw.mt(),ff,status,kw.flow_from(),'{:02d}'.format(idx))
                a.add_six(uba,kw.fr(),ff,status,kw.flow_from(),'{:02d}'.format(idx))


        a.add_two(kw.shutin(), self.well_name['W'])

        if self.on_time:
            a.add_one('')
            a.add_two(kw.on_time(), self.well_name['G'])
            a.add_one(1)
            a.add_two(kw.on_time(), self.well_name['W'])
            a.add_one(1)

        if self.open:
            a.add_one('')

            mod, open = self.open

            a.add_one('**Trigger for openning')
            name = "'OPEN_{}'".format(self.well_name[mod].strip("'"))
            a.add_seven(kw.trigger(), name, kw.on_elapsed()
                    , na.time(), kw.timsim(),kw.greater_than(), open)
            a.add_two(kw.open(), self.well_name[mod], pre='   ')
            a.add_one(kw.end_trigger())

        if self.wag:
            a.add_one('')

            other = {'G':'W', 'W':'G'}
            mod, nr1, nr2, nr3 = self.wag

            a.add_one('**Trigger for WAG')
            name = "'WAG_{}'".format(self.well_name[mod].strip("'"))
            timsim = "{} {} {}".format(kw.timsim(), kw.greater_than(), nr1)
            increment = "{} {}".format(kw.increment(), nr2*2)
            apply_times = "{} {}".format(kw.apply_times(), nr3)

            a.add_seven(kw.trigger(), name, kw.on_elapsed(), na.time()
                    , timsim, increment, apply_times)
            a.add_two(kw.open(), self.well_name[mod], pre='   ')
            a.add_two(kw.shutin(), self.well_name[other[mod]], pre='   ')
            a.add_one(kw.end_trigger())

            name = "'WAG_{}'".format(self.well_name[other[mod]].strip("'"))
            timsim = "{} {} {}".format(kw.timsim(), kw.greater_than(), nr1+nr2)
            increment = "{} {}".format(kw.increment(), nr2*2)
            apply_times = "{} {}".format(kw.apply_times(), nr3)

            a.add_seven(kw.trigger(), name, kw.on_elapsed(), na.time()
                    , timsim, increment, apply_times)
            a.add_two(kw.open(), self.well_name[other[mod]], pre='   ')
            a.add_two(kw.shutin(), self.well_name[mod], pre='   ')
            a.add_one(kw.end_trigger())

    def __repr__(self):
        a = self._agr
        return a.__repr__()

    def write(self, fname):
        p = pathlib.Path(fname)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w') as fh: fh.write(self.__repr__())

    def _trigger_open_name(self, mode):
        return 'OPEN_{}'.format(self.well[mode])