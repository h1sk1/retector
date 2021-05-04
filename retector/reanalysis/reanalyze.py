import collections
import dataclasses
import hashlib
import json
import logging
import os
import struct
from dataclasses import dataclass, field
from itertools import groupby
from pathlib import Path
from time import time
from typing import Optional, Dict, List, Any, Iterator, Callable

from retector.securify2.staticanalysis import souffle
from retector.securify2.staticanalysis.factencoder import encode

def __base_dir():
    return Path(__file__).parent

def __get_dir_digest(dir_root):
    digest = hashlib.md5()
    for dirpath, dirnames, filenames in os.walk(dir_root, topdown=True):

        dirnames.sort(key=os.path.normcase)
        filenames.sort(key=os.path.normcase)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            st = os.stat(filepath)
            digest.update(struct.pack('d', st.st_mtime))
            digest.update(bytes(st.st_size))

    return digest.hexdigest()

def __get_str_digest(path):
    digest = hashlib.md5()
    digest.update(path.encode(encoding='utf-8'))
    return digest.hexdigest()

def get_facts_out(facts, file_path, **kw_args_souffle):
    path_base = __base_dir()
    path_patterns = path_base / 'souffle_analysis'
    path_facts_out = path_base / 'static_analysis_facts_out.json'

    souffle_hash = __get_dir_digest(path_patterns)
    file_hash = __get_str_digest(file_path)
    dir_hash = __get_str_digest(souffle_hash + file_hash)

    try:
        with open(path_facts_out, 'r') as f:
            cached_data = json.load(f)

            if cached_data['digest'] == dir_hash:
                return cached_data['facts_out']
    except (IOError, json.JSONDecodeError):
        pass

    souffle_output, facts_out = souffle.run_souffle(
        source_file=path_base / 'souffle_analysis' / 'analysis.dl',
        output_dir=path_base / 'facts_out',
        fact_dir=path_base / 'facts_in',
        executable_dir=path_base / 'dl-program',
        facts=facts,
        souffle_kwargs=kw_args_souffle)

    try:
        with open(path_facts_out, 'w') as f:
            json.dump({
                'digest': dir_hash,
                'facts_out': facts_out
            }, f)
    except IOError:
        pass

    return facts_out
