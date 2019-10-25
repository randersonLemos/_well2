from .. import misc


kw = misc.Keywords


def head_default(agr, well_name, well_type, group_name, fluid, operate_lst, monitor_lst
        , geometry, perf):
   agr.add_four(kw.well(), well_name, kw.attachto(), group_name)
   agr.add_two(well_type, well_name)
   agr.add_two(kw.incomp(), fluid)

   for ope in operate_lst: agr.add_five(kw.operate(), *ope)
   for mon in monitor_lst: agr.add_four(kw.monitor(), *mon)

   agr.add_six(kw.geometry(), *geometry)
   agr.add_three(kw.perf(), perf, well_name)
