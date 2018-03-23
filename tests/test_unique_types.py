import parmed as pmd
from aimtools.unique_types import *
import filecmp
import pytest
import os
import shutil


def test_unique_types():
    out_dir = 'thf_uniq_output'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    parm = pmd.amber.LoadParm('thf.prmtop')
    unique_types = create_unique_type_list(parm,'thf.EQUIVATOMS.DAT')
    write_unique_frcmod_mol2s(parm,unique_types,'thf.uniq.frcmod',names='thf.uniq',path=out_dir)
    assert filecmp.cmp('REF.thf.uniq.frcmod',out_dir+'/thf.uniq.frcmod')
    assert filecmp.cmp('REF.thf.uniq.mol2',out_dir+'/thf.uniq.mol2')
    shutil.rmtree(out_dir)

def test_batch_unique_types():
    out_dir = 'batch_uniq_output'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    parm_list = []
    equiv_list = []

    mol_list = 'thf bcb'.split()
    ### Trying a bunch of molecules at the same time to force execution of code
    [mol_list.append('trp') for i in range(39)]

    for i,mol in enumerate(mol_list):
        parm_list.append(pmd.amber.LoadParm(mol+'.prmtop'))
        parm_list[i].load_rst7(mol+'.rst7')
        equiv_list.append(mol+'.EQUIVATOMS.DAT')

    unique_types = create_unique_type_list(parm_list, equiv_list)
    write_unique_frcmod_mol2s(parm_list, unique_types, 'batch.frcmod',path=out_dir)
    assert filecmp.cmp('REF.batch.frcmod',out_dir+'/batch.frcmod')
    shutil.rmtree(out_dir)





