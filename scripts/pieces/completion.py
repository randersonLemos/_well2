from .. import misc
from dic2.scripts import dictionary as dicc


kw = dicc.Keywords
wd = dicc.Words


def completion_dual_default(agr, completion):
    for idx, com in enumerate(completion):
        ff = com[3]
        uba = ' '.join(com[:3])
        status = com[4]
        if idx == 0:
            agr.add_seven(uba, kw.mt(), ff, status, kw.flow_to()
                    , wd.surface(), kw.reflayer()
                    , suf=" ** uba ff status connection")
            agr.add_five(uba, kw.fr(), ff, status, kw.flow_to())
        else:
            agr.add_six(uba, kw.mt(), ff, status
                    , kw.flow_to(), '{:02d}'.format(idx))
            agr.add_six(uba, kw.fr(), ff, status
                    , kw.flow_to(), '{:02d}'.format(idx))

