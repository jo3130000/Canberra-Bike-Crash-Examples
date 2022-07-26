#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary module to:
    
    1. Generate and update a CSV file with the version information of Python 
    and dependant modules, as required by the project, currently running 
    on the host system.  
    
    2. Convert the CSV file to a markdown formatted file for inclusion in 
    the project repository as system requirements and known compatible
    system configurations.

@author:  tarney
@uid:     u7378856
@created: Tue Sep 14 19:30:12 2021
"""

from pathlib import Path
import pandas as pd

from cycling_check_dependencies import *
from cycling_globals import *


##############################################################################
#                               HELPER FUNCTIONS                             #
##############################################################################


def file_exists(file_name):
    """
    Returns whether a file exists on the host system.

    Parameters
    ----------
    file_name : str
        A path to a file.

    Returns
    -------
    bool
        True or False, if the file exists.

    """
    file_path = Path(file_name)
    
    return file_path.is_file()


def read_dependencies(file_name):
    """
    Reads a dependency CSV file, as generated by 'write_dependencies',
    into a pandas DataFrame.

    Parameters
    ----------
    file_name : str
        The path to the dependency CSV file.

    Returns
    -------
    df : pd.DataFrame
        A data frame containing module version information, indexed by module 
        name, columned by host name.

    """
    file_path = Path(file_name)
    df = pd.read_csv(file_path)
    df.set_index('Module', inplace=True)
    df.fillna('unknown', inplace=True)
    return df


def write_dependencies(file_name, dependency_df):
    """
    Writes a pandas DataFrame containing dependency information to a CSV file.

    Parameters
    ----------
    file_name : str
        The path of the output CSV file..
    dependency_df : pd.DataFrame
        A data frame containing module version information, indexed by module 
        name, columned by host name.

    Returns
    -------
    None.

    """
    
    file_path = Path(file_name)
    dependency_df.to_csv(file_path)
    

def convert_dict_to_df(sys_config):
    """
    Converts a dictionary containing module version information to a pandas
    DataFrame.

    Parameters
    ----------
    module_versions : dict
        A dictionary containing {'module name': 'module version'} pairs.

    Returns
    -------
    df : pandas.DataFrame
        A data frame containing module version information, indexed by module 
        name, columned by host name..

    """
    
    module_versions = sys_config.get_system_config()
    hostname = sys_config.get_hostname()
    
    df = pd.DataFrame.from_dict(module_versions, orient='index', dtype=str,
                                columns=[hostname])
    df.sort_index(inplace=True)
    df.index.name = 'Module'
    
    return df


def read_requirements_template(file_name):
    """
    Returns the contents of a Requirements markdown template file.

    Parameters
    ----------
    file_name : str
        The path to the template file.

    Returns
    -------
    template : str
        The template file contents.

    """
    
    file_path = Path(file_name)
    
    with open(file_path) as fin:
        template = fin.read()
        
    return template


def write_requirements_file(file_name, markdown):
    """
    Writes a Requirements markdown file.

    Parameters
    ----------
    file_name : str
        The path of the output file.
    markdown : str
        The contents of the file to be written.

    Returns
    -------
    None.

    """
    
    file_path = Path(file_name)
    
    with open(file_path, 'w') as fout:
        fout.write(markdown)
    

def build_requirements_table(dependencies_file):
    """
    Returns a markdown formatted table of the contents of a dependency CSV file.

    Parameters
    ----------
    dependencies_file : str
        The path to the CSV file.

    Returns
    -------
    reqs_table : str
        The markdown formatted table.

    """
    
    df = read_dependencies(dependencies_file)
    
    module_dict = df.to_dict()
    module_names = df.index.to_list()
    module_names.sort()
    hosts = list(module_dict.keys())
    
    
    cols = len(hosts) + 1
    header_row = ['Module'] + [f'({i+1})' for i in range(len(hosts)) ]
    
    reqs_table = '| ' + ' | '.join(header_row) + ' |\n'
    reqs_table += '|--------' * cols + '|\n'
                 
    for module in module_names:
        row = [module]
        
        for host in hosts:
            row.append(module_dict[host][module])
          
        reqs_table += '| ' + ' | '.join(row) + ' |\n'

    return reqs_table


##############################################################################
#                              UTILITY FUNCTIONS                             #
##############################################################################

def update_compatible_systems_csv(sys_config, compatible_systems_csv):
    """
    Reads in a text file of dependent modules, determines the current version 
    of each module running on the host system, and adds them to a CSV file.
    If the CSV file doesn't exist it will be created.  If the host system 
    already exists in the CSV file then the details will be updated.

    Parameters
    ----------
    modules_file : str
        The path to a text file containing the list of modules.
    dependencies_file : str
        The path to a CSV file to be created or amended.

    Returns
    -------
    bool
        True if dependencies file successfully updated, False otherwise.

    """
    
    df = convert_dict_to_df(sys_config)
    hostname = sys_config.get_hostname()
    
    if file_exists(compatible_systems_csv):
        old_df = read_dependencies(compatible_systems_csv)
        
        if hostname in old_df.columns:
            old_df.drop(labels=[hostname], axis=1, inplace=True)
            
        df = df.join(old_df)
      
    print(f'System info written to: {compatible_systems_csv}')
    
    write_dependencies(compatible_systems_csv, df)


def update_requirements_doc(compatible_systems_csv, requirements_doc_template, requirements_doc):
    """
    Generates a markdown formatted requirements file from a template and a 
    CSV file of module dependencies.

    Parameters
    ----------
    requirementes_file : str
        The path to the requirements markdown file to be created.
    requirementes_template_file : str
        The path to the requirements template file.
    dependencies_file : str
        The path to the dependencies CSV file.

    Returns
    -------
    None.

    """
    
    reqs_table = build_requirements_table(compatible_systems_csv)
    reqs_template = read_requirements_template(requirements_doc_template)
    reqs_md = reqs_template + '\n' + reqs_table
    
    print(f'Requirements documentation updated: {requirements_doc}')
    
    write_requirements_file(requirements_doc, reqs_md)    
    

##############################################################################
#                                    MAIN                                    #
##############################################################################

if __name__ == '__main__':
    
        
    print()
    print('###########################################################')
    print('#                   DEPENDENCY CHECK                      #')
    print('###########################################################')
    print()
    
    root_path = Path.cwd()
    local_module_prefix = 'cycling'
    sys_config = Dependencies(root_path, ignore_module_prefix=local_module_prefix)

    if sys_config.check():
        print(sys_config)
    else:
        print('Required modules missing, please install:')
        print()
        for i, module in enumerate(sys_config.get_missing_modules()):
            print(f'  {i + 1}: {module}')
        print()
        print('Once installed, please re-run the program.')
        sys.exit()
    
    
    print()
    print('###########################################################')
    print('#              UPDATING COMPATIBLE SYSTEMS                #')
    print('###########################################################')
    print()
    
    
    compatible_systems_csv = 'compatible_systems/compatible_systems.csv'
    requirements_doc_template = 'compatible_systems/REQUIREMENTS.template'
    requirements_doc = 'REQUIREMENTS.md'
    
    update_compatible_systems_csv(sys_config, compatible_systems_csv)
    update_requirements_doc(compatible_systems_csv, requirements_doc_template, requirements_doc)