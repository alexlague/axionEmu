import os
# When run this script, make sure test_os_00 is in the same directory
number_cores = 60 # this number should be in consistent with number_cores variable in the 9parameters_data_collection_mp.py file
for i in range(number_cores):
    new_name = 'test_os_mp_'+str(i)
    f1=open('test_os_00', 'r')
    lines = f1.readlines()
    f1.close()
    lines[3] = 'output_root = '+'test_mp_'+str(i)+'\n'
    os.system('touch '+new_name)
    f2 = open(new_name, 'w')
    f2.writelines(lines)
    f2.close()



