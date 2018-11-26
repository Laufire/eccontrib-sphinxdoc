"""
Installs the required modules for the tools to work properly.
"""
import os
from os.path import dirname

def main():

  if raw_input('Running this task might reinstall existing packages. Do you want to continue (y/n)? ') != 'y':
    return

  import pip

  pip_args = ['install', '-r', 'requirements.txt']

  proxy = os.environ.get('http_proxy')
  if proxy:
    pip_args = ['--proxy', proxy] + pip_args

  if pip.main(pip_args):
    raise Exception('Failed to install %s' % requirement)


if __name__ == '__main__':
  os.chdir(dirname(__file__))
  main()
