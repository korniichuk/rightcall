#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from os.path import basename, exists, isfile

from boto3 import resource

bucket_name = 'odigo-auditor'

def upload_file(bucket_name, file_abs_path, file_key=None):
    """Upload file to Amazon S3 bucket. If no `file_key`, file name used as
       `file_key` (example: `file_abs_path` is '/tmp/odigo.mp3' and `file_key`
       is None, that `file_key` is 'odigo.mp3').
    Input:
        bucket_name -- Amazon S3 bucket name (required | type: str);
        file_abs_path -- file abs path (required | type: str);
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
