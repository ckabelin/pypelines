# pypelines
DevOps Pipeline with Python

This repo relies on Spec-Driven Development and Spec Kit: https://github.com/github/spec-kit

# clone
git clone http://<youruser>:<yourtoken>@github.com/ckabelin/pypelines.git
cd pypelines

- make a new branch 'feature/<whatever>'!

git checkout feature/<whatever>

create a new app under apps

# installation
sudo snap install astral-uv
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

open VSCode under newly created subdirectory <PROJECT_NAME>.

do your credential stuff

git config --global credential.helper '!f() { sleep 1; echo "username=<USERNAME> token=github_pat_<TOKEN>>"; }; f'

# get informed & watch cools stuff
https://www.youtube.com/watch?v=a9eR1xsfvHg
https://www.youtube.com/watch?v=o6SYjY1Bkzo
