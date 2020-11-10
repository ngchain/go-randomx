# Helper script to download a precompiled binary of the wasmtime dll for the
# current platform. Currently always downloads the dev release of wasmtime.

import urllib.request
import zipfile
import tarfile
import io
import sys
import os
import shutil
import glob

urls = [
    ['randomx-x86_64-mingw.zip', 'windows-x86_64'],
    ['randomx-x86_64-linux.tar.xz', 'linux-x86_64'],
    ['randomx-x86_64-macos.tar.xz', 'macos-x86_64'],
    ['randomx-aarch64-linux.tar.xz', 'linux-aarch64'],
]

try:
    shutil.rmtree('build')
except FileNotFoundError:
    pass

os.makedirs('build')

for i, arr in enumerate(urls):
    filename, dirname = arr
    url = 'https://github.com/ngchain/RandomX/releases/download/c-api/'
    url += filename
    print('Download', url)

    with urllib.request.urlopen(url) as f:
        contents = f.read()

    if filename.endswith('.zip'):
        z = zipfile.ZipFile(file=io.BytesIO(contents))
        z.extractall()
    else:
        t = tarfile.open(fileobj=io.BytesIO(contents))
        t.extractall()

    src = filename.replace('.zip', '').replace('.tar.xz', '')
    # if i == 0:
    #     os.rename(src + '/include', 'build/include')

    # os.rename(src + '/lib', 'build/' + dirname)
    os.rename(src, 'build/' + dirname)
    # shutil.rmtree(src)

for dylib in glob.glob("build/**/*.dll"):
    os.remove(dylib)
for dylib in glob.glob("build/**/*.dylib"):
    os.remove(dylib)
for dylib in glob.glob("build/**/*.so"):
    os.remove(dylib)