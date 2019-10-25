from ..states import _State_Dual
from ..misc import Keywords as kw


class Inje_Dual_ICV(_State_Dual):
    def build(self):
        agr = self._agr
        a = self._agr

        from ..pieces.head import head_default as head
        head(agr, self.well_name, kw.injector(), self.group_name, self.fluid,
                self.operate, self.monitor, self.geometry, self.perf)

        from ..pieces.completion import completion_dual_default as completion
        completion(agr, self.completion)

        agr.add_two(kw.shutin(), self.well_name)

        if self.on_time:
            from ..pieces.others import on_time_default as on_time
            on_time(agr, self.well_name, self.on_time)

        if self.open:
            from ..pieces.others import open_default as openn
            openn(agr, self.well_name, self.open)

        if self.layerclump:
            from ..pieces.others import layerclump_default as layerclump
            layerclump(agr, self.well_name, self.layerclump)

        if self.icv_start:
            from ..pieces.icvs import icv_deafult as icv
            icv(agr, self.well_name, self.icv_start, self.layerclump, self.icv_control)

