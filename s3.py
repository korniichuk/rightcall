#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from os import walk
from os.path import basename, exists, isfile, join
import sys

from boto3 import resource

bucket_name = 'odigo-auditor'

def upload_dir(dir_abs_path, bucket_name):
    """Upload all files from directory (recursively) to Amazon S3 bucket.
    Input:
        dir_abs_path -- directory absolute path (required | type: str).
                        Example: '/tmp/' or '/tmp';
        bucket_name -- Amazon S3 bucket name (required | type: str).

    """

    if not dir_abs_path.endswith('/'):
        dir_abs_path += '/'
    length = sum([len(fn) for dp, dn, fn in walk(dir_abs_path)])
    output = walk(dir_abs_path, topdown=True, onerror=None, followlinks=False)
    i = 0
    for dir_path, dir_names, file_names in output:
       for file_name in file_names:
           if not file_name.strip().endswith('~'):
               file_abs_path = join(dir_path, file_name)
               file_key = join(dir_path.replace(dir_abs_path, ''), file_name)
               i += 1
               sys.stdout.write('\r')
               sys.stdout.write('uploading: %s/%s' % (i, length))
               sys.stdout.flush()
               upload_file(file_abs_path, bucket_name, file_key)
    sys.stdout.write('\n')
    sys.stdout.flush()

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

# Example. Upload directory (recursively) to Amazon S3 'odigo-auditor' bucket
#upload_dir('/tmp/', 'odigo-auditor')
