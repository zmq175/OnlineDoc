from __future__ import absolute_import, unicode_literals
import celery
import logging
import subprocess

import time
import os

from django.core.files import File

from OnlineDocument.models import Document

logger = logging.getLogger('django')


@celery.task(name="convert_file")
def convert_file(document_id):
    from django.conf import settings
    document = Document.objects.get(pk=document_id)
    logger.info("Task received new original file:" + document.original_file.path)
    pdf_path = settings.BASE_DIR+'/static/document/pdf/' + str(int(time.time())) + '.pdf'
    ext = os.path.splitext(document.original_file.path)[1]
    if ext == '.pdf':
        logger.info("the file itself is pdf document, save it directly!")
        document.pdf_file.save(pdf_path, File(open(document.original_file.path, 'rb')))
    else:
        command = "unoconv -f pdf" + " -o " + pdf_path + " " + document.original_file.path
        process_start_time = time.time()
        os.system(command)
        logger.info("convert file using time:" + str(time.time() - process_start_time))
        document.pdf_file.save(pdf_path, File(open(pdf_path, 'rb')))
        os.remove(pdf_path)
