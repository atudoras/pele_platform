import pytest
import sys
import os
import subprocess
from test_config import parse_template
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import PlpRotTemp.PlopRotTemp as pl
import filecmp
#from ciphers.DESchiper import convert_to_binary, DES, XOR


MAE_FILE = 'ain.mae'
ROOT = 'ain'
MAE_CONVERSION = [0,1,2,3,4,13,5,14,6,15,7,16,8,9,10,11,12,17,18,19]
TEMPLATE_CONVERSION = [0,1,2,3,4,6,8,10,12,13,14,15,16,5,7,9,11,17,18,19]
BONDS = [[0, 1], [1, 2], [1, 3], [3, 4], [3, 8], [4, 5], [4, 13], [5, 6], 
        [5, 14], [6, 7], [6, 15], [7, 8], [7, 16], [8, 9], [9, 10], [10, 11],
        [10, 12], [12, 17], [12, 18], [12, 19]]
PARENT_RESULT = [0, 1, 2, 2, 4, 5, 6, 7, 4, 9, 10, 11, 11, 5, 6, 7, 8, 13, 13, 13]
REPOS_PATH = os.path.abspath(os.path.join(__file__ ,"../.."))
TEST_PATH = os.path.join(os.path.dirname(__file__), 'data')
MAIN_PATH =  os.path.join(REPOS_PATH, 'PlpRotTemp/main.py')
OLD_MAIN_PATH = '/home/dani/repos/presentation/PlpRotTemp/main_16_9_17.py'
try:
    PYTHON_PATH = os.path.join(os.environ['SCHRODINGER'] + "/utilities/python")
except KeyError:
    print("Set SCHRODINGER environment variable path")



# @pytest.mark.parametrize("argument, expected", [
#                          ('ain.mae', 'ain'),
#                          ('~/ain.mae', 'ain'),
#                          ('/opt/schrodinger/ain.mae', 'ain'),
#                          ])
# def test_get_root(argument, expected):
#     root = pl.get_root_path(argument)
#     assert root == expected

# # @pytest.mark.parametrize("MAE_FILE, root, OPLS, hetgrp_opt, old_name, new_name, expected", [
# #                          (os.path.join(TEST_PATH, 'ain.mae'), 'ain', '2005', '', '', '', 'ain.hetgrp_ffgen'),
# #                          (os.path.join(TEST_PATH,'MI4.mae'), 'MI4', '2005', '', '', '', 'mi4.hetgrp_ffgen'),
# #                          ])
# # def test_build_template(MAE_FILE, root, OPLS, hetgrp_opt, old_name, new_name, expected):
# #     [template_file, output_template_file, mae_file_hetgrp_ffgen, files, resname] = pl.build_template(MAE_FILE, root, OPLS, hetgrp_opt, old_name, new_name)
# #     assert template_file == expected




# @pytest.mark.parametrize("mae_file, template_file, mae_expected, template_expected", [
#                          (os.path.join(TEST_PATH, 'ain.mae'), 'ain.hetgrp_ffgen' , MAE_CONVERSION, TEMPLATE_CONVERSION),
#                          ])
# def test_MatchTempMaeAtoms(mae_file, template_file, mae_expected, template_expected):
#     [mae2temp, temp2mae] = pl.MatchTempMaeAtoms(mae_file, template_file)
#     assert mae2temp == template_expected
#     assert temp2mae == mae_expected

# @pytest.mark.parametrize("mae_file, expected", [
#                          (os.path.join(TEST_PATH, 'ain.mae'), ''),
#                          (os.path.join(TEST_PATH, 'ain_repited.mae'), Exception),
#                          ])
# def test_check_repite_names(mae_file, expected):
#     atomnames = pl.find_names_in_mae(mae_file)
#     if(expected == Exception):
#         with pytest.raises(expected):
#             pl.check_repite_names(atomnames)
#     else:
#         pass



# @pytest.mark.parametrize("rotamer_library", [
#                          (os.path.join(TEST_PATH,'ain_vdw')),
#                          ])
# def test_check_replace_vdwr(rotamer_library):
#     pl.replace_vdwr_from_library(rotamer_library)
#     radius_vdw_info, start_index, end_index = pl.parse_nonbonded(rotamer_library)
#     for i, rdw_line in enumerate(radius_vdw_info):
#         NBOND_info = rdw_line.split()
#         rdw = float(NBOND_info[1])/2.0
#         if(rdw== 0):
#             assert 0
 

@pytest.mark.parametrize("input_file", [
                          (MAE_FILE),
                          ('MI4.mae'),
                          ('1o3p_ligand.mae'),
                          ('1.mae'),('2.mae'),('3.mae'),('4.mae'),('5.mae'),('6.mae'),('7.mae'),('8.mae'),('9.mae'),('10.mae'),
                          ('11.mae'),('12.mae'),('13.mae'),('14.mae'),('15.mae'),('16.mae'),('17.mae'),('18.mae'),('19.mae'),('20.mae'),
                          ('21.mae'),('22.mae'),('23.mae'),('24.mae'),('25.mae'),('26.mae'),('27.mae'),('28.mae'),('29.mae'),('30.mae'),
                          ('100.mae'),('101.mae'),('102.mae'),('103.mae'),('104.mae'),('105.mae'),('106.mae'),('107.mae'),('108.mae'),('109.mae'),('110.mae'),
                          ('110.mae'),('111.mae'),('112.mae'),('113.mae'),('114.mae'),('115.mae'),('116.mae'),('117.mae'),('118.mae'),('119.mae'),('120.mae'),
                          ('120.mae'),('121.mae'),('122.mae'),('123.mae'),('124.mae'),('125.mae'),('126.mae'),('127.mae'),('128.mae'),('129.mae'),('130.mae'),
                          ('131.mae'),('132.mae'),('133.mae'),('134.mae'),('135.mae'),('136.mae'),('137.mae'),('138.mae'),('139.mae'),('140.mae'),
                          ('141.mae'),('142.mae'),('143.mae'),('144.mae'),('145.mae'),('146.mae'),('147.mae'),('148.mae'),('149.mae'),('150.mae'),
                          ('151.mae'),('152.mae'),('153.mae'),('154.mae'),('155.mae'),('156.mae'),('157.mae'),('158.mae'),('159.mae'),('160.mae'),
                          ('161.mae'),('162.mae'),('163.mae'),('164.mae'),('165.mae'),('166.mae'),('167.mae'),('168.mae'),('169.mae'),('170.mae'),
                          ('171.mae'),('172.mae'),('173.mae'),('174.mae'),('175.mae'),('176.mae'),('177.mae'),('178.mae'),('179.mae'),('180.mae'),
                          ('181.mae'),('182.mae'),('183.mae'),('184.mae'),('185.mae'),('186.mae'),('187.mae'),('188.mae'),('189.mae'),('190.mae'),
                          ('191.mae'),('192.mae'),('193.mae'),('194.mae'),('195.mae'),('196.mae'),('197.mae'),('198.mae'),('199.mae'),('200.mae'),
                          ('199.mae'),

                         ])
def test_PlopRotTempGroup(input_file):
    try:
        os.remove(os.path.join(REPOS_PATH,'group.dat'))
        os.remove(os.path.join(REPOS_PATH,"GROUP.dat"))
    except OSError:
        pass
    #res_name = find_resnames_in_mae(os.path.join(TEST_PATH, input_file))[0]
    subprocess.call([PYTHON_PATH, MAIN_PATH, os.path.join(TEST_PATH, input_file)])
    subprocess.call([PYTHON_PATH, OLD_MAIN_PATH, os.path.join(TEST_PATH, input_file)])
    #new_sections = parse_template(os.path.join(REPOS_PATH,res_name.upper()), res_name.upper())
    #old_sections = parse_template(os.path.join(REPOS_PATH,res_name.lower()), res_name.upper())
    
    file1 = os.path.join(REPOS_PATH,'group.dat')
    file2 = os.path.join(REPOS_PATH,"GROUP.dat")


    assert filecmp.cmp(file1, file2)
