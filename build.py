import subprocess


#process = subprocess.Popen(['sam', 'build','--template', ''])

# sam package \
#   --template-file template.yaml \
#   --s3-bucket my-artifacts-bucket \
#   --output-template-file telegraf-packaged.yaml
#
# # Then deploy
# aws cloudformation deploy \
#   --template-file telegraf-packaged.yaml \
#   --stack-name my-stack-name \
#   --capabilities CAPABILITY_IAM