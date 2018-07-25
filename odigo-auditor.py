#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 1. Download mp3 files from www.prosodie.com to local machine.
# 2. Upload mp3 files from local machine to 'mp3.odigo-auditor' AWS S3 bucket.
# 3. Trinscribe mp3 files from 'mp3.odigo-auditor' AWS S3 bucket to
# 'transcribe.odigo-auditor' AWS S3 bucket.
# 4. Save data to Google Sheets.

import json
from os import remove
from os.path import basename

import boto3

from comprehend import get_sentiment

bucket_name = 'transcribe.odigo-auditor'

def main(bucket_name):
    """Auditor for Odigo tool"""

    result = {}
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        if bucket.name == bucket_name:
            i = 0
            for key in bucket.objects.all():
                if key.key.endswith('.json'):
                    result[i] = {}
                    reference = basename(key.key).replace('.json', '')
                    result[i]['reference'] = reference
                    # Download json file
                    try:
                        s3.Bucket(bucket_name).download_file(key.key, key.key)
                    except Exception as exception:
                        return 1
                    # Get text
                    with open(key.key, 'r') as f:
                        data = json.load(f)
                    text = data['results']['transcripts'][0]['transcript']
                    result[i]['text'] = text
                    # Get sentiment
                    sentiment = get_sentiment(text)
                    result[i]['sentiment'] = sentiment
                    # Remove json file
                    remove(key.key)
                    i += 1
