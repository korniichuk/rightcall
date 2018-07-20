#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from os import walk
from os.path import basename, exists, isfile, join
import sys

from boto3 import resource

bucket_name = 'odigo-auditor'

def upload_cwd(cwd, bucket_name):
    """Upload all files from cwd to Amazon S3 bucket.
    Input:
        cwd -- current working directory (required | type: str);
        bucket_name -- Amazon S3 bucket name (required | type: str).
    """

    output = walk(cwd, topdown=True, onerror=None, followlinks=False)
    length = sum([len(fn) for dp, dn, fn in walk(cwd)])
    i=0
    for dir_path, dir_names, file_names in output:
       for file_name in file_names:
           i+=1
           sys.stdout.write('\r')
           sys.stdout.write('uploading: %s/%s' % (i, length))
           sys.stdout.flush()
           file_name_lower = file_name.strip().lower()
           if not file_name_lower.endswith('~'):
               file_abs_path = join(dir_path, file_name)
               file_key = dir_path.replace(cwd, '')[1:] + '/' + file_name
               upload_file(file_abs_path, bucket_name, file_key)
    sys.stdout.write('\n')

def upload_file(file_abs_path, bucket_name, file_key=None):
    """Upload file to Amazon S3 bucket. If no `file_key`, file name used as
       `file_key` (example: `file_abs_path` is '/tmp/odigo.mp3' and `file_key`
       is None, that `file_key` is 'odigo.mp3').
    Input:
        file_abs_path -- file abs path (required | type: str);
        bucket_name -- Amazon S3 bucket name (required | type: str);
        file_key -- Amazon S3 bucket dst file abs path (not required |
                    type: str).

    """

    if not file_key:
        file_key = basename(file_abs_path)
    # Let's use Amazon S3
    s3 = resource('s3')
    if exists(file_abs_path) and isfile(file_abs_path):
        # Upload file to Amazon S3 bucket
        try:
            s3.Bucket(bucket_name).upload_file(file_abs_path, file_key)
        except Exception as exception:
            return 1
    else:
        return 1

# Example. Upload '/tmp/odigo.mp3' file to Amazon S3 'odigo-auditor' bucket as
# 'odigo.mp3' file
#upload_file('/tmp/odigo.mp3', 'odigo-auditor')

# Example. Upload '/tmp/odigo.mp3' file to Amazon S3 'odigo-auditor' bucket as
# 'new.mp3' file
#upload_file('/tmp/odigo.mp3', 'odigo-auditor', 'new.mp3')

# Example. Upload current working directory to Amazon S3 'odigo-auditor' bucket
#upload_cwd('/tmp', 'odigo-auditor')
