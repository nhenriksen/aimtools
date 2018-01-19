import parmed as pmd
from aimtools.unique_types import *
import filecmp
import pytest

path = '.'

def test_unique_types():
    parm = pmd.amber.LoadParm(path+'/thf.prmtop')
    uniq_types = assign_uniq_types(parm,path+'/thf.EQUIVATOMS.DAT')
    write_unique_frcmod(parm,uniq_types,path+'/thf.uniq.frcmod')
    assert filecmp.cmp(path+'/REF.thf.uniq.frcmod',path+'/thf.uniq.frcmod')




