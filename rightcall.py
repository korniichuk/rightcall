#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 1. Download mp3 files from www.prosodie.com to local machine.
# 2. Upload mp3 files from local machine to 'mp3.rightcall' AWS S3 bucket.
# 3. Trinscribe mp3 files from 'mp3.rightcall' AWS S3 bucket to
# 'transcribe.rightcall' AWS S3 bucket.
# 4. Save data to Google Sheets.

import json
from os import remove
from os.path import basename, join

import boto3

from comprehend import get_sentiment
from sheets import append_row
from text import check_promo

transcribe_bucket_name = 'transcribe.rightcall'
mp3_bucket_name = 'mp3.rightcall'

def main(transcribe_bucket_name, mp3_bucket_name):
    """Right Call/Contact Center Monitoring written in Python"""

    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        if bucket.name == transcribe_bucket_name:
            for key in bucket.objects.all():
                if key.key.endswith('.json'):
                    r = {}
                    # Get reference number
                    reference = basename(key.key).replace('.json', '')
                    r['ref'] = reference
                    # Get URL
                    location = boto3.client('s3') \
                            .get_bucket_location(
                            Bucket=mp3_bucket_name)['LocationConstraint']
                    base_url = join('https://s3-%s.amazonaws.com' % location,
                            mp3_bucket_name)
                    url = join(base_url, key.key.replace('.json', '.mp3'))
                    r['url'] = url
                    # Download json file
                    try:
                        s3.Bucket(transcribe_bucket_name) \
                          .download_file(key.key, key.key)
                    except Exception as exception:
                        return 1
                    # Get text
                    with open(key.key, 'r') as f:
                        data = json.load(f)
                    text = data['results']['transcripts'][0]['transcript']
                    r['text'] = text
                    # Get sentiment
                    sentiment = get_sentiment(text)
                    r['sentiment'] = sentiment
                    # Check promotion
                    promo = check_promo(text)
                    r['promo'] = promo
                    # Save to Gooogle Sheets
                    values = [r['ref'], r['text'], r['promo'], r['sentiment'],
                              r['url']]
                    append_row(values)
                    # Remove tmp json file from local machine
                    remove(key.key)

main(transcribe_bucket_name, mp3_bucket_name)
