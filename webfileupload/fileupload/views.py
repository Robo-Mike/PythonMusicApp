from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from django.contrib.auth.decorators import login_required
import os
import boto3
@login_required
def index(request):
    #Could use view class with get and post method instead of this
    if request.method == 'POST':
        form = FileUploadForm(request.POST , request.FILES)
        if form.is_valid():
            #noop for moment
            filetoupload = request.FILES['file']
            response_text = upload_file(filetoupload)
            response_text = add_queue_message(filetoupload.name)
            return HttpResponse('successfully uploaded, response = {0}'.format(response_text))
        else:
            response_text = "form invalid"
            if form.errors:
                 for field in form:
                     for error in field.errors:
                        response_text += error + '({0})'.format(field.name)
            return HttpResponse(response_text)
    else:
        form = FileUploadForm()
    return render(request,'file_upload.html',{'form': form})

#requires AWS_ACCESS_KEY,AWS_SECRET_KEY, AWS_BUCKET_NAME
#todo should live somewhere else
def upload_file(f):
    cloud_filename = 'MusicAppUploads/' + f.name
    bucket_name = 'elasticbeanstalk-eu-west-2-823411548735'
    #detect if on aws
    if 'RDS_HOSTNAME' in os.environ:
        #no credentials specified it will use the IAM role of teh ec2 instance which has s3 access
        s3 = boto3.client('s3')
        s3.upload_fileobj(f, bucket_name, cloud_filename)
        return ''
    else:
        return 'no upload - not on AWS'


def add_queue_message(file_name):
    # Get the service resource
    sqs = boto3.resource('sqs', region_name='us-west-2')
    # Get the queue. This returns an SQS.Queue instance
    queue = sqs.get_queue_by_name(QueueName='MusicApp')
    response = queue.send_message(MessageBody='file {0} added'.format(file_name))
    return response
