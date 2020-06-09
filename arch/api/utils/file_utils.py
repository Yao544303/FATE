#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import os
from ruamel import yaml

from cachetools import LRUCache
from cachetools import cached

from fate_flow.settings import SERVER_CONF_PATH, SERVERS

PROJECT_BASE = None


def get_project_base_directory():
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir, os.pardir))
    return PROJECT_BASE


@cached(cache=LRUCache(maxsize=10))
def load_json_conf(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


@cached(cache=LRUCache(maxsize=10))
def get_fate_env(module):
    env_path = os.path.join(get_project_base_directory(), 'fate.env')
    if not module:
        module = 'FATE'
    try:
        with open(env_path) as f:
            lines = f.readlines()
            for line in lines:
                if module in line:
                    version = line.split('=')[-1]
                    return module, version
    except:
        raise EnvironmentError("loading {} version from '{}' failed!".format(module, env_path))


def dump_json_conf(config_data, conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path, "w") as f:
            json.dump(config_data, f, indent=4)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def load_json_conf_real_time(conf_path):
    if os.path.isabs(conf_path):
        json_conf_path = conf_path
    else:
        json_conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(json_conf_path) as f:
            return json.load(f)
    except:
        raise EnvironmentError("loading json file config from '{}' failed!".format(json_conf_path))


def load_yaml_conf(conf_path):
    if not os.path.isabs(conf_path):
        conf_path = os.path.join(get_project_base_directory(), conf_path)
    try:
        with open(conf_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise EnvironmentError("loading yaml file config from {} failed:".format(conf_path), e)


def set_server_conf(config):
    federatedId = config.get('federatedId')
    data = load_json_conf_real_time(SERVER_CONF_PATH)
    manager_conf = data.get(SERVERS).get('fatemanager', {})
    if manager_conf:
        data[SERVERS]['fatemanager']['federatedId'] = federatedId
    else:
        raise Exception('there is no manager configuration')
    json_conf_path = os.path.join(get_project_base_directory(), SERVER_CONF_PATH)
    rewrite_json_file(json_conf_path, data)
    return {'federatedId': federatedId}


def rewrite_json_file(filepath, json_data):
    with open(filepath, 'w') as f:
        json.dump(json_data, f, indent=4, separators=(',', ': '))
    f.close()


if __name__ == "__main__":
    print(get_project_base_directory())
    print(load_json_conf('federatedml/transfer_variable/definition/transfer_conf.json'))
