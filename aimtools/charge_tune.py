import sys
import re
from collections import OrderedDict
from decimal import Decimal
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=log.DEBUG)

class ChargedMol(object):
    "A class for correcting the sum of mol2's partial charges to an exact integer"

    def __init__(self):
        self.mol2 = None
        self.mol2_lines = None
        self.atom_charge_list = []
        self.charge_type_count_dict = OrderedDict()
        self.initial_net_charge = None
        self.current_net_charge = None
        self.charge_count_list = []
        self.charge_list = []
        self.charge_map = {}
        self.new_mol2 = 'new_charges.mol2'
    
    def correct_charges(self):
        "A workflow for loading a mol2, correcting the charges, and writing a new mol2"

        self.load_mol2()
        self.scale_charges()
        self.adjust_charges()
        self.map_charges()
        self.write_mol2()

    def load_mol2(self):
        "Loads the self.mol2 file and populates several data structures"

        with open(self.mol2, 'r') as f:
            self.mol2_lines = f.readlines()
        read = False
        for line in self.mol2_lines:
            if re.search('<TRIPOS>ATOM', line):
                read = True
                continue
            if re.search('<TRIPOS>BOND', line):
                read = False
                continue
            if read:
                cols = line.rstrip().split()
                self.atom_charge_list.append(float(cols[8]))
                key = cols[5]+' '+cols[8]
                if not key in self.charge_type_count_dict:
                    self.charge_type_count_dict[key] = 1
                else:
                    self.charge_type_count_dict[key] += 1

        self.initial_net_charge = sum(self.atom_charge_list)
        self.current_net_charge = self.initial_net_charge

        log.debug('Init net charge: {}'.format(self.initial_net_charge))
        log.debug('Targ net charge: {}'.format(round(self.initial_net_charge)))
        
        for charge_type in self.charge_type_count_dict:
            atom_type,charge = charge_type.split()
            self.charge_list.append(Decimal("{:.6f}".format(float(charge))))
            self.charge_count_list.append(self.charge_type_count_dict[charge_type])

    def scale_charges(self):
        """
        Scales the partial charges to correct for deviation of the sum from an exact integer.
        This will result in charges that are close, but usually not exactly an integer.
        """
        scale_correction = (self.initial_net_charge - round(self.initial_net_charge))
        scale_correction /= float(len(self.atom_charge_list))
        self.current_net_charge = Decimal('0.000000')
        for i,charge in enumerate(self.charge_list):
            self.charge_list[i] =  Decimal("{:.6f}".format( float(charge) - scale_correction))
            self.current_net_charge += self.charge_count_list[i] * self.charge_list[i]

        log.debug('Charges Scaled ...')
        log.debug('Curr net charge: {}'.format(self.current_net_charge))

    def adjust_charges(self):
        "Fine tune the partial charges to have exactly an integer sum"
        if check_net_charge('eq', self.current_net_charge):
            pass
        else:
            adjust_step,operator = set_adjustor(self.current_net_charge)
            i = 0
            i_incr = 1
            i_off = 0
            loops = 0
            log.debug('i= {} i_incr= {} i_off= {} loops= {} current_net_charge= {} adjust_step= {} operator= {}'.format(i,i_incr,i_off,loops,self.current_net_charge, adjust_step, operator))
            while not check_net_charge('eq', self.current_net_charge):
                if i >= len(self.charge_list):
                    i = i % len(self.charge_list)
                    log.debug('once through the loop')
                    if loops != 0 and loops % 10 == 0:
                        i_off += 1
                    if loops != 0 and loops % 30 == 0:
                        i_incr += 1
                        i_off = 0
                    loops += 1
                if loops > 500:
                    raise Exception("Five hundo loops completed and still not converged!")
                self.charge_list[i] += adjust_step
                self.current_net_charge = Decimal('0.000000')
                for j in range(len(self.charge_list)):
                    self.current_net_charge += self.charge_count_list[j] * self.charge_list[j]
                adjust_step,operator = set_adjustor(self.current_net_charge)
                log.debug('i= {} i_incr= {} i_off= {} loops= {} current_net_charge= {} adjust_step= {} operator= {}'.format(i,i_incr,i_off,loops,self.current_net_charge, adjust_step, operator))
                i += i_incr + i_off
                #log.debug('i= {} i_incr= {} loops= {} current_net_charge= {} adjust_step= {} operator= {}'.format(i,i_incr,loops,self.current_net_charge, adjust_step, operator))

        log.debug('Charges Adjusted ...')
        log.debug('Curr net charge: {}'.format(self.current_net_charge))

    def map_charges(self):
        "Map the new charges to the original charge types"
        for i,key in enumerate(self.charge_type_count_dict):
            self.charge_map[key] = self.charge_list[i]

    def write_mol2(self):
        "Write a new mol2 file with the updated charges"
        with open(self.new_mol2, 'w') as f:
            edit = False
            for line in self.mol2_lines:
                if re.search('<TRIPOS>ATOM', line):
                    edit = True
                    f.write(line)
                    continue
                if re.search('<TRIPOS>BOND', line):
                    edit = False
                    f.write(line)
                    continue
                if edit:
                    cols = line.split()
                    key = cols[5]+' '+cols[8]
                    f.write("{:>7s} {:<8s} {:9.4f} {:9.4f} {:9.4f} {:<6s} {:>4s} {:<4s} {:10.6f}\n".format(cols[0],cols[1],float(cols[2]),float(cols[3]),float(cols[4]),cols[5],cols[6],cols[7],self.charge_map[key]))
                else:
                    f.write(line)

def check_net_charge(operator, net_charge):
    "Checks with the partial charge sum matches specified criteria (=, >, <) relative to the target integer sum."
    result = None
    targ = Decimal("{:.6f}".format(round(net_charge)))
    if operator == 'lt' and net_charge - targ < 0.0:
        result = True
    elif operator == 'lt' and net_charge - targ >= 0.0:
        result = False
    elif operator == 'gt' and net_charge - targ > 0.0:
        result = True
    elif operator == 'gt' and net_charge - targ <= 0.0:
        result = False
    elif operator == 'eq' and  net_charge - targ == Decimal('0.000000'):
        result = True
    elif operator == 'eq' and  net_charge - targ != Decimal('0.000000'):
        result = False
    else:
        raise Exception('Input not understood:'+operator+' '+net_charge)
    return result

def set_adjustor(net_charge):
    "Sets the adjustment step size and appropriate comparison operator for a given charge sum relative to its target integer sum"
    if check_net_charge('lt', net_charge):
        adjust_step = Decimal('0.000001')
        operator = 'lt'
    else:
        adjust_step = Decimal('-0.000001')
        operator = 'gt'
    return adjust_step,operator

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Provide a mol2 file as argument to operate on')
    chgmol = ChargedMol()
    chgmol.mol2 = sys.argv[1]
    if len(sys.argv) == 3:
        chgmol.new_mol2 = sys.argv[2]
    chgmol.correct_charges()

