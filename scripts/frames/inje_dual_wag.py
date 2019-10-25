from ..states import _State_Dual_Two_Modes
from ..misc import Keywords as kw


class Inje_Dual_Wag(_State_Dual_Two_Modes):
    def __init__(self, well_name, group_name):
        super().__init__(well_name, group_name, 'W', 'G')

    def build(self):
        agr = self._agr

        from ..pieces.head import head_default as head
        head(agr, self.well_name['G'], kw.injector(), self.group_name,
                self.fluid['G'], self.operate['G'], self.monitor['G'],
                 self.geometry, self.perf)

        from ..pieces.completion import completion_dual_default as completion
        completion(agr, self.completion)

        agr.add_two(kw.shutin(), self.well_name['G'])

        from ..pieces.head import head_default as head
        head(agr, self.well_name['W'], kw.injector(), self.group_name,
                self.fluid['W'], self.operate['W'], self.monitor['W'],
                 self.geometry, self.perf)

        from ..pieces.completion import completion_dual_default as completion
        completion(agr, self.completion)

        agr.add_two(kw.shutin(), self.well_name['W'])

        if self.on_time:
            from ..pieces.others import on_time_default as on_time
            on_time(agr, self.well_name['G'], self.on_time)
            on_time(agr, self.well_name['W'], self.on_time)

        if self.open:
            mod, open = self.open
            from ..pieces.others import open_default as openn
            openn(agr, self.well_name[mod], open)

        if self.wag:
            from ..pieces.others import start_wag_default as start_wag
            start_wag(agr, self.well_name, self.wag)

        if self.layerclump:
            from ..pieces.others import layerclump_wag_default as layerclump
            layerclump(agr, self.well_name, self.layerclump)

