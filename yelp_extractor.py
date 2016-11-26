#coding=utf8
'''
    util that extract the specific data of yelp
'''
import json

def get_filename(ext_type):
    dir_ = 'data/yelp/2016/'
    if ext_type == 'review':
        return dir_ + 'yelp_academic_dataset_review.json'
    if ext_type == 'business':
        return dir_ + 'yelp_academic_dataset_business.json'
    if ext_type == 'user':
        return dir_ + 'yelp_academic_dataset_user.json'

def extract_from_json(ext_type='review', is_simapling=False):
    file_path = get_filename(ext_type)

    lines = open(file_path).readlines()
    res = []
    for l in lines:
        item_info = json.loads(l.strip())
        res.append(item_info)
        if is_simapling and len(res) > 100:
            break
    print 'extract %s, total=%s' % (ext_type, len(res))
    return res
