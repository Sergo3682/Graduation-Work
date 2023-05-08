from string import Template
import subprocess
import re
from bitvector import BitVector
import logging as log


class Tester:
    def __init__(self, subckt: str, parent_lib, my_lib, input_names, bitvector: BitVector):
        self.bv = bitvector
        self.subckt = subckt
        self.input_names = input_names.copy()
        self.input_names.reverse()
        self.path = 'testbench/'
        self.tb_name = f'tb_{self.subckt}.sp'
        self.log_name = f'tb_{self.subckt}.log'
        self.sub = {
            'subckt': self.subckt,
            'parent_lib': parent_lib,
            'my_lib': my_lib,
            'vdd': 1.8,
            'vss': 0,
            'tper': '100n',
            'trf': '1n',
            'cons': ' '.join(input_names)
        }
        self.vout = dict()

    def gen_pulse(self):
        res = ''
        cntr = 1
        for name in self.input_names:
            res += f"Vin{name} {name} VSS PULSE ('vss' 'vdd' '{cntr}*tper/2'" \
                   f" 'trf' 'trf' '{cntr}*tper/2' '{cntr}*tper')\n"
            cntr *= 2
        self.sub['vpulse'] = res
        return cntr // 2

    def gen_tran(self, cntr):
        res = f".tran 1n '{cntr}*tper'"
        self.sub['tran'] = res

    def gen_meas(self, k):
        res = ''
        stt = 0.25
        stp = k - stt
        num = 0
        while stt <= stp:
            res += f".meas tran v{num} find v(q) at='{stt}*tper'\n"
            stt += 0.5
            num += 1
        self.sub['meas'] = res

    def run_batch(self):
        log.info('Running ngspice in batch mode...')
        temp = subprocess.check_output(f'ngspice -b {self.path}{self.tb_name} -o {self.path}{self.log_name}', shell=True)

    def get_results(self):
        fd = open(f'{self.path}{self.log_name}', 'r')
        lines = ''.join(fd.readlines())
        res = re.findall(r'v[0-9]+.+=\s{2}.?[0-9]+.[0-9]+.+', lines)
        for r in res:
            name = re.search(r'v[0-9]+', r).group(0)
            val = re.search(r'\s{2}.?[0-9].+', r).group(0)

            if abs(round(float(val), 1)) == float(self.sub['vdd']):
                self.vout[name] = '1'
            elif abs(round(float(val))) == 0:
                self.vout[name] = '0'

    def get_new_bv(self):
        res = ''
        for d in self.vout:
            res = self.vout[d] + res
        res = '0b' + res
        return BitVector(int(res, 2), len(self.vout))

    def comparing(self, bv):
        log.info('Comparing original bitvector with results...')
        green = '\x1b[0;32m'
        reset = "\x1b[0m"
        red = '\x1b[1;31m'
        if self.bv == bv:
            log.info(f'{green}The comparison was successful!{reset}')
        else:
            log.warning(f'{red}The comparison was unsuccessful.{reset}')

    def test_bench(self):
        log.info('Creating test bench file...')
        fd = open(f'{self.path}{self.tb_name}', 'w')
        res = Template(
            '* Test for $subckt\n\n'
            '.lib $parent_lib tt\n'
            '.include "../$my_lib"\n\n'
            '.param vdd=$vdd\n'
            '.param vss=$vss\n'
            '.param tper=$tper\n'
            '.param trf=$trf\n\n'
            "Vvdd VDD 0 'vdd'\n"
            "Vvss VSS 0 'vss'\n"
            "Cload Q VSS 10f\n\n"
            # Device Under Test
            "XDUT Q $cons VDD VSS VSS VDD $subckt\n\n"
            '$vpulse\n'
            '$tran\n\n'
            '$meas'
        )

        k = self.gen_pulse()
        self.gen_tran(k)
        self.gen_meas(k)

        fd.write(res.substitute(self.sub))
        fd.close()
        self.run_batch()
        self.get_results()
        self.comparing(self.get_new_bv())
