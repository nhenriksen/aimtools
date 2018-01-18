import parmed as pmd
from aimtools.unique_types import *
import filecmp
import pytest

def test_unique_types():
    parm = pmd.amber.LoadParm('thf.prmtop')
    uniq_types = assign_uniq_types(parm,'thf.EQUIVATOMS.DAT')
    write_unique_frcmod(parm,uniq_types,'thf.uniq.frcmod')
    assert filecmp.cmp('REF.thf.uniq.frcmod','thf.uniq.frcmod')




