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



