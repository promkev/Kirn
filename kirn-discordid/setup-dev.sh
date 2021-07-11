PIP_TARGET=./.appwrite pip install -r ./requirements.txt --upgrade --ignore-installed
appwrite functions createTag \
    --functionId=60e9fd9f2a6bb \
    --command='python main.py' \
    --code='.'