from .. import misc


kw = misc.Keywords
na = misc.Names


def on_time_default(agr, well_name, on_time):
    agr.add_two(kw.on_time(), well_name)
    agr.add_one(on_time)


def open_default(agr, well_name, open):
    agr.add_one('**Opening')
    name = "'OPEN_{}'".format(well_name.strip("'"))
    agr.add_seven(kw.trigger(), name, kw.on_elapsed()
            , na.time(), kw.timsim(),kw.greater_than(), open)
    agr.add_two(kw.open(), well_name, pre='   ')
    agr.add_one(kw.end_trigger())


def layerclump_default(agr, well_name, layerclump):
    for idx, layer in enumerate(layerclump):
        name = "'{}_Z{}'".format(well_name.strip("'"),idx+1)
        agr.add_two(kw.layerclump(), name)
        agr.add_three(well_name, layer, kw.mt())
        agr.add_three(well_name, layer, kw.fr())

