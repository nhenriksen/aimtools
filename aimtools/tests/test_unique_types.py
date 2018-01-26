import parmed as pmd
from aimtools.unique_types import *
import filecmp
import pytest


def test_unique_types():
    parm = pmd.amber.LoadParm('thf.prmtop')
    unique_types = create_unique_type_list(parm,'thf.EQUIVATOMS.DAT')
    write_unique_frcmod_mol2s(parm,unique_types,'thf.uniq.frcmod',name_list='thf.uniq')
    assert filecmp.cmp('REF.thf.uniq.frcmod','thf.uniq.frcmod')
    assert filecmp.cmp('REF.thf.uniq.mol2','thf.uniq.mol2')

def test_batch_unique_types():
    parm_list = []
    equiv_list = []

    mol_list = 'thf bcb'.split()
    [mol_list.append('trp') for i in range(29)]

    for i,mol in enumerate(mol_list):
        parm_list.append(pmd.amber.LoadParm(mol+'.prmtop'))
        parm_list[i].load_rst7(mol+'.rst7')
        equiv_list.append(mol+'.EQUIVATOMS.DAT')

    unique_types = create_unique_type_list(parm_list, equiv_list)
    write_unique_frcmod_mol2s(parm_list, unique_types, 'batch.frcmod')
    assert filecmp.cmp('REF.batch.frcmod','batch.frcmod')





