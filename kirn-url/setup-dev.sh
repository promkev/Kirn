PIP_TARGET=./.appwrite pip install -r ./requirements.txt --upgrade --ignore-installed
appwrite functions createTag \
    --functionId=60ea1071cb1da \
    --command='python main.py' \
    --code='.'