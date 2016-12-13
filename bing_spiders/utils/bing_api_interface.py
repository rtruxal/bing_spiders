import csv
from IO import make_sure_filepath_is_coo
from bingapipy import BingSearch


def bing_news_api_to_csv(bing_api_key, q=None, pages_of_links=20, csv_file_pth=None):
    if bing_api_key == 'YOU NEED TO ENTER YOUR KEY HERE':
        raise ValueError('')
    api_key = bing_api_key
    if not q:
        q1 = 'technology'
    else:
        q1 = q
    ## MUST SPECIFY endpoint='news' TO GET DESIRED COLUMNS. uRRYTHING WILL BREAK IF U DON'T.
    Searcher = BingSearch(api_key, q1, endpoint='news')

    ## APPURRENTLY USING THE NORMAL ENDPOINT & RESPONSE FILTER, SEARCHING FOR 'technology' PRODUCES 5 WEBSITES. tHIS IS LIES.
    # Searcher.params.update({'responseFilter': 'news'})

    list_of_NewsResult_instances = Searcher.search_2_packaged_json()

    #It's pagin' time.
    page_num = 2
    while page_num <= pages_of_links:
        #TODO: if pages_of_links > 50, use sleep()
        Searcher.params.update({'offset' : min(len(list_of_NewsResult_instances), 50)})
        newlist = Searcher.search_2_packaged_json()
        list_of_NewsResult_instances += newlist
        page_num += 1

    # Now we gon' decode some links
    counter = 0
    for instance in list_of_NewsResult_instances:
        instance.url = decode_bing_response_url(instance.url)

    # Filename validations & accidental overwrite protection.
    filepth = make_sure_filepath_is_coo(csv_file_pth)

    # Lil' bit o response-string processing.
    # bingapipy will sometimes return a list of raw links when it gets confused.
    if type(list_of_NewsResult_instances[0]) == str:
        with open(filepth, 'wb') as csvfile:
            headers = ['id', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            indx_id_num = 1
            for item in list_of_NewsResult_instances:
                writer.writerow({'id' : indx_id_num, 'url' : item})
                indx_id_num += 1
            print 'Did it!\nCheck binglinks.csv for results'

    # however, most of the time it will return a list of NewsResult Instances.
    elif str(list_of_NewsResult_instances[0]) == 'NewsResult':
        with open(filepth, 'wb') as csvfile:
            cols = ['about_name', 'about_readlink', 'image_url', 'image_width', 'image_height', 'provider_type', 'provider_name', 'category', 'name', 'date_published', 'description', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=cols)
            writer.writeheader()
            print 'file created: {}\nrecords written: {}'.format(filepth, len(list_of_NewsResult_instances))
            for NRInstance in list_of_NewsResult_instances:
                valdict = {}
                # Um. So basically I wanted to access object attributes like a dictionary.
                # this ISHT works, so I'm not questioning it.
                for col in cols:
                    attribute = NRInstance.__dict__[col]
                    if bool(attribute) is False:
                        valdict.update({col : 'NULL'})
                    elif col in NRInstance.__dict__.keys():
                        if type(attribute) is unicode or type(attribute) is str:
                            # PREVENT THE GOD DAMN UnicodeEncodingErrorS THAT ARE
                            # INCESSANT AND TURRIBLE AND THE BANE OF MY MFGD EXISTENCE.
                            valdict.update({col : attribute.encode("iso-8859-15", "backslashreplace")})
                        else: valdict.update({col : attribute})
                try:
                    writer.writerow(valdict)
                except UnicodeEncodeError:
                    # KILL_YOURSELF() <--this is not a function, it's directions.
                    # import pdb
                    # pdb.set_trace()
                    print 'link {} omitted due to Unicode error'.format(NRInstance.url)
                    pass
        print 'done.'

def decode_bing_response_url(bing_encoded_url):
    import binascii
    # yes it appears to be this easy.
    if bing_encoded_url[-15] != '&':
        raise ValueError('this encoded link is not the right format for this function.')
    new_url = bing_encoded_url[153:-15].lstrip('=')
    new_new_url = new_url.replace('%3a', binascii.a2b_hex('3a'))
    new_new_new_url = new_new_url.replace('%2f', binascii.a2b_hex('2f'))
    return new_new_new_url



if __name__ == '__main__':
    bing_news_api_to_csv('YOU NEED TO ENTER YOUR KEY HERE')