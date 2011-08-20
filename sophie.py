#!/usr/bin/env python
""" Tools to interact with sophie.zarb.org using JSON format
"""
import json
import urllib


def retrieve_patches(distribution, release, arch):
    """ Return all patches from a distribution/releas/arch
    """
    patches = list()
    srpm_list = retrieve_srpm_list(distribution, release, arch)
    for srpm in srpm_list:
        srpm_name = srpm['filename']
        if srpm['filename'][0] == 'z':
            patch_list = retrieve_patch_list(srpm)
            for patch in patch_list:
                patches.append({srpm_name : patch['filename']})
    return patches


def retrieve_patch_list(srpm):
    """ Return patch list from srpm
    """
    url_srpm = "http://sophie.zarb.org/rpms/" + srpm['pkgid'] \
        + "/files?json"
    srpm_files = retrieve_json(url_srpm)
    patch_list = list()
    for elem in srpm_files:
        elname = elem['filename']
        # extensions trouvees : .patch .dif .dpatch (certain sont zipes)
        if 'patch' in elname or 'fix' in elname or '.diff' in elname:
            patch_list.append(elem)
    return patch_list

def retrieve_srpm_list(distribution, release, arch):
    """ Return list of src.rpm for the specified distritubion/release/arch
    """
    url_list = "http://sophie.zarb.org/distrib/" + distribution + "/" \
        + release + "/" + arch + "/srpms?json"
    srpm_list = retrieve_json(url_list)
    return srpm_list

def retrieve_json(url):
    """ Return the content a JSON file from the url
    """
    json_file = urllib.urlopen(url)
    json_content = json.load(json_file)
    json_file.close()
    return json_content

if __name__ == "__main__":
    print retrieve_patches("Mageia", "cauldron", "x86_64")
