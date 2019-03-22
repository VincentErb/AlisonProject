# AlisonProject

## Work on the project

If you have no IDE to manage the project, you can still install some tools to help you.

First, if you don't have it, install `virtualenv`

```
pip3 install virtualenv
```

Running the script `scripts/init.sh` will then setup virtualenv and install all the requirements for the project.

Then you can use `scripts/format.sh` to format the whole project, and `pylint alison` to spot errors and bad practices in your code.

### Manage your virtual environment

When you run `scripts/init.sh` it exits with the virtual environment activated. To deactivate it, simply type `deactivate` in a terminal.
To reactivate it you just have to run the following command from the root of the project:

```
source env/bin/activate
```
