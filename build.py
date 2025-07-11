import subprocess


#process = subprocess.Popen(['sam', 'build','--template', ''])

#    C:\Users\sevic\AppData\Local\Temp\temp-template8194715229466200704.yaml --build-dir D:\Work\Python\awstelegraf\.aws-sam\build
#
#
# sam package \
#   --template-file template.yaml \
#   --s3-bucket my-artifacts-bucket \
#   --output-template-file packaged.yaml
#
# # Then deploy
# aws cloudformation deploy \
#   --template-file packaged.yaml \
#   --stack-name my-stack-name \
#   --capabilities CAPABILITY_IAM