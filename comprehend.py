#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json

import boto3

bucket_name = 'transcribe.odigo-auditor'

comprehend = boto3.client('comprehend')
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    if bucket.name == bucket_name:
        for key in bucket.objects.all():
            if key.key.endswith('.json'):
                result = {}
                # Download json file
                try:
                    s3.Bucket(bucket_name).download_file(key.key, key.key)
                except Exception as exception:
                    #return 1
                    pass
                # Get text
                with open(key.key, 'r') as f:
                    data = json.load(f)
                text = data['results']['transcripts'][0]['transcript']
                result['text'] = text
                # Get sentiment
                r = comprehend.detect_sentiment(Text=text, LanguageCode='en')
                sentiment = r['Sentiment'].lower()
                result['sentiment'] = sentiment
