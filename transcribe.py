#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from os.path import basename

import boto3

bucket_name = 'odigo-auditor'

def transcribe_mp3(src, dst=None, job_name=None, language_code='en-US'):
    """Trinscribe mp3 file on AWS Trinscribe.
    Input:
        src -- S3 location of the src mp3 file (required | type: str). Example:
               'https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp3';
        dst -- location where the transcription is stored (not required |
               type: str);
        job_name -- the name of the job (not required | type: str);
        language_code -- language code for the language used in the input mp3
                         file (not required | type: str | default: 'en-US').

    """

    client = boto3.client('transcribe')
    if not job_name:
        job_name = basename(src).replace('mp3', '')
    if not dst:
        try:
            response = client.start_transcription_job(
                    TranscriptionJobName=job_name, Media={'MediaFileUri': src},
                    MediaFormat='mp3', LanguageCode=language_code,
                    Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 2})
        except Exception as exception:
            return 1
    else:
        try:
            response = client.start_transcription_job(
                    TranscriptionJobName=job_name, Media={'MediaFileUri': src},
                    MediaFormat='mp3', LanguageCode=language_code,
                    OutputBucketName = dst,
                    Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 2})
        except Exception as exception:
            return 1
    return response

# Example. Trinscribe
# 'https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp3' file
#transcribe_mp3('https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp3')

# Example. Trinscribe
# 'https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp3' file to
# 'odigo-auditor' bucket on AWS S3
#transcribe_mp3('https://s3-eu-west-1.amazonaws.com/examplebucket/example.mp3',
#               'odigo-auditor')
