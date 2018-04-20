import aimtools
import pytest
import filecmp
import os

def test_charge_tune():
    chgmol = aimtools.charge_tune.ChargedMol()
    chgmol.mol2 = 'ante.mobley_299266.mol2'
    chgmol.new_mol2 = 'test_charge_tune.mol2'
    chgmol.correct_charges()
    assert filecmp.cmp('newchg.mobley_299266.mol2', 'test_charge_tune.mol2')
    os.remove('test_charge_tune.mol2')

