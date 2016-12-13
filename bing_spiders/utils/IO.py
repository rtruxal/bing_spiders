import os
from datetime import datetime


def make_sure_filepath_is_coo(filepath):
    # Savefile path-validations & other os stuff.
    if filepath is None:
        filename = 'bing_link_list{}.csv'.format(str(datetime.now())[:10])
        filepth = os.path.join(os.path.realpath('bing_spiders/data/queries/'), filename)
    else:
        assert type(filepath) is str and filepath[-4:].lower() == '.csv'
        # lil' mechanism that prevents overwriting by injecting (1) or (2)... before the file prefix.
        if os.path.exists(filepath):
            copy_num = 1
            while True:
                copy_name = filepath[:-4] + '({})'.format(copy_num) + filepath[-4:]
                if os.path.exists(copy_name):
                    copy_num += 1
                elif copy_num > 100:
                    raise IOError('more than 100 copies of docname present in dir. Please specify new name.')
                else:
                    filepth = copy_name
                    print('{} already exists. \ncreating copy: {}'.format(filepath, filepth))
                    break
        else:
            filepth = filepath
    
    return filepth
    