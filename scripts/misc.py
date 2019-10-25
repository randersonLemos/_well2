class Keywords:
    @staticmethod
    def greater_than(): return '>'

    @staticmethod
    def less_than(): return '<'

    @staticmethod
    def mt(): return '*MT'

    @staticmethod
    def fr(): return '*FR'

    @staticmethod
    def gas(): return '*GAS'

    @staticmethod
    def max(): return '*MAX'

    @staticmethod
    def min(): return '*MIN'

    @staticmethod
    def stl(): return '*STL'

    @staticmethod
    def stg(): return '*STG'

    @staticmethod
    def stw(): return '*STW'

    @staticmethod
    def bhp(): return '*BHP'

    @staticmethod
    def water(): return '*WATER'

    @staticmethod
    def cont(): return '*CONT'

    @staticmethod
    def wcut(): return '*WCUT'

    @staticmethod
    def open(): return '*OPEN'

    @staticmethod
    def well(): return '*WELL'

    @staticmethod
    def perf(): return '*PERF'

    @staticmethod
    def repeat(): return '*REPEAT'

    @staticmethod
    def shutin(): return '*SHUTIN'

    @staticmethod
    def incomp(): return '*INCOMP'

    @staticmethod
    def timsim(): return '*TIMSIM'

    @staticmethod
    def flow_to(): return '*FLOW-TO'

    @staticmethod
    def operate(): return '*OPERATE'

    @staticmethod
    def monitor(): return '*MONITOR'

    @staticmethod
    def on_time(): return '*ON-TIME'

    @staticmethod
    def trigger(): return '*TRIGGER'

    @staticmethod
    def injector(): return '*INJECTOR'

    @staticmethod
    def geometry(): return '*GEOMETRY'

    @staticmethod
    def attachto(): return '*ATTACHTO'

    @staticmethod
    def producer(): return '*PRODUCER'

    @staticmethod
    def reflayer(): return '*REFLAYER'

    @staticmethod
    def increment(): return '*INCREMENT'

    @staticmethod
    def on_elapsed(): return '*ON_ELAPSED'

    @staticmethod
    def layerclump(): return '*LAYERCLUMP'

    @staticmethod
    def apply_times(): return '*APPLY_TIMES'

    @staticmethod
    def on_ctrllump(): return '*ON_CTRLLUMP'

    @staticmethod
    def end_trigger(): return '*END_TRIGGER'

    @staticmethod
    def flow_from(): return '*FLOW-FROM'

    @staticmethod
    def clumpsetting(): return '*CLUMPSETTING'

class Words:
    @staticmethod
    def time(): return "'TIME'"

    @staticmethod
    def surface(): return "'SURFACE'"

class Slots:
    @staticmethod
    def one(one):
        return '{}'.format(one)

    @staticmethod
    def two(one, two):
        return '{} {}'.format(one, two)

    @staticmethod
    def three(one, two, three):
        return '{} {} {}'.format(one, two, three)

    @staticmethod
    def four(one, two, three, four):
        return '{} {} {} {}'.format(one, two, three, four)

    @staticmethod
    def five(one, two, three, four, five):
        return '{} {} {} {} {}'.format(one, two, three, four, five)

    @staticmethod
    def six(one, two, three, four, five, six):
        return '{} {} {} {} {} {}'.format(one, two, three, four, five, six)

    @staticmethod
    def seven(one, two, three, four, five, six, seven):
        return '{} {} {} {} {} {} {}'.format(one, two, three, four, five, six, seven)

    @staticmethod
    def eight(one, two, three, four, five, six, seven, eight):
        return '{} {} {} {} {} {} {} {}'.format(one, two, three, four, five, six, seven, eight)

    @staticmethod
    def nine(one, two, three, four, five, six, seven, eight, nine):
        return '{} {} {} {} {} {} {} {} {}'.format(one, two, three, four, five, six, seven, eight, nine)

class Agregator:
    def __init__(self):
        self._lst = []

    def add_one(self, one, pre='', suf=''):
        self._lst.append(Slots.one(self._prefix(pre,self._suffix(one,suf))))

    def add_two(self, one, two, pre='', suf=''):
        self._lst.append(Slots.two(self._prefix(pre,one), self._suffix(two,suf)))

    def add_three(self, one, two, three, pre='', suf=''):
        self._lst.append(Slots.three(self._prefix(pre,one), two, self._suffix(three,suf)))

    def add_four(self, one, two, three, four, pre='', suf=''):
        self._lst.append(Slots.four(self._prefix(pre,one), two, three, self._suffix(four,suf)))

    def add_five(self, one, two, three, four, five, pre='', suf=''):
        self._lst.append(Slots.five(self._prefix(pre,one), two, three, four, self._suffix(five,suf)))

    def add_six(self, one, two, three, four, five, six, pre='', suf=''):
        self._lst.append(Slots.six(self._prefix(pre,one), two, three, four, five, self._suffix(six,suf)))

    def add_seven(self, one, two, three, four, five, six, seven, pre='', suf=''):
        self._lst.append(Slots.seven(self._prefix(pre,one), two, three, four, five, six, self._suffix(seven,suf)))

    def add_eight(self, one, two, three, four, five, six, seven, eight, pre='', suf=''):
        self._lst.append(Slots.eight(self._prefix(pre,one), two, three, four, five, six, seven, self._suffix(eight,suf)))

    def add_nine(self, one, two, three, four, five, six, seven, eight, nine, pre='', suf=''):
        self._lst.append(Slots.nine(self._prefix(pre,one), two, three, four, five, six, seven, eight, self._suffix(nine,suf)))

    def _prefix(self, pre, stg):
        return '{}{}'.format(pre,stg)

    def _suffix(self, stg, suf):
        return '{}{}'.format(stg,suf)

    def __repr__(self):
        return '\n'.join(self._lst)