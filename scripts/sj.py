import codecs
import os
import subprocess
import sys
import shutil
import tempfile
from tempfile import NamedTemporaryFile
import glob
import os
from tempfile import mkdtemp
import time
from subprocess import Popen, PIPE
import webbrowser

def mkempty(f):
    """
    Create f as an empty file
    """
    open(f, 'w').close() 

def find_node():
    return "node"

def encode_input(input):
    if input.startswith(codecs.BOM_UTF16):
        return input.decode('utf-16').encode('utf-8')
    elif input.startswith(codecs.BOM_UTF16_BE):
        return input.decode('utf-16-be').encode('utf-8')
    elif input.startswith(codecs.BOM_UTF16_LE):
        return input.decode('utf-16-le').encode('utf-8')
    return input

def execute_return(script, **kwargs):
    """Execute script and returns output string"""
    saveStdErr = kwargs['savestderr'] if 'savestderr' in kwargs else False
    cmd = [find_node()] + script.split()
    print(' '.join(cmd))
    with NamedTemporaryFile() as f:
         try:
             subprocess.check_call(cmd,stdout=f, 
                                   stderr=f if saveStdErr else open(os.devnull, 'wb'),bufsize=1000)
             f.seek(0)
             return f.read()
         except subprocess.CalledProcessError as e:
             f.seek(0)
             return f.read()

def execute_return_np(script, **kwargs):
    """Execute script and returns output string"""
    saveStdErr = kwargs['savestderr'] if 'savestderr' in kwargs else False
    cmd = [find_node()] + script.split()
    with NamedTemporaryFile() as f:
         try:
             subprocess.check_call(cmd,stdout=f,
                                   stderr=f if saveStdErr else open(os.devnull, 'wb'),bufsize=1000)
             f.seek(0)
             return f.read()
         except subprocess.CalledProcessError as e:
             f.seek(0)
             return f.read()

def execute(script, stdin=None, env=None, quiet=False):
    """Execute script and print output"""
    try:
        cmd = [find_node()] + script.split(' ')
        sub_env = os.environ.copy()

        print("Cmd", str(cmd))

        if env:
            for key in env.keys():
                if key != None:
                    sub_env[key] = env[key]

        print(' '.join(cmd))
        p = Popen(cmd, env=sub_env, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)
        stdout = p.communicate(input=encode_input(stdin) if stdin else None)[0]
        if not quiet:
            print(stdout)
        return stdout
    except subprocess.CalledProcessError as e:
        print(e.output)

def execute_np(script, *args):
    """Execute script and print output"""
    cmd = [find_node()] + script.split()
    return subprocess.call(cmd)

WORKING_DIR = os.getcwd()
    
JALANGI_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

INSTRUMENTATION_SCRIPT = JALANGI_HOME + "/src/js/commands/esnstrument_cli.js"

INST_DIR_SCRIPT = JALANGI_HOME + "/src/js/commands/instrument.js"

ANALYSIS_SCRIPT = JALANGI_HOME + "/src/js/commands/direct.js"

JALANGI_SCRIPT = JALANGI_HOME + "/src/js/commands/jalangi.js"


def create_and_cd_jalangi_tmp():
    try:
        shutil.rmtree("jalangi_tmp")
    except: pass
    os.mkdir("jalangi_tmp")
    os.chdir("jalangi_tmp")

def cd_parent():
    os.chdir('..')        

def full_path(file):
    return os.path.abspath(file)
