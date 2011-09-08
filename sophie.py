#!/usr/bin/env python
""" Tools to interact with sophie.zarb.org using JSON format
"""
import json
import urllib


class Sophie():
    def __init__(self, distribution, release, arch):
        self.site_url = "http://sophie.zarb.org/"
        #TODO: test if distribution, release and arch info are coherent
        self.distribution = distribution
        self.release = release
        self.arch = arch
        self.srpms_url = ''.join((self.site_url, "distrib/", 
                                  self.distribution, "/",
                                  self.release, "/",
                                  self.arch, "/srpms?json"))


    def retrieve_srpm_name(self, pkgid):
        """ Return list of src.rpm for the specified distritubion/release/arch
        """
        info = self.retrieve_srpm_info(pkgid)
        name = info['name']
        return name


    def retrieve_srpm_info(self, pkgid):
        """ Return list of src.rpm for the specified distritubion/release/arch
        """
        info_url = ''.join((self.site_url, "rpms/", pkgid, "?json"))
        info_json = retrieve_json(info_url)
        info = info_json['info']
        return info


    def retrieve_patch_list(self, pkgid):
        """ Return patch list from srpm
        """
        srpm_files = self.retrieve_file_list(pkgid)
        patch_list = list()
        for elem in srpm_files:
            elname = elem['filename']
            # extensions found : .patch .diff .dpatch (sometime zipped)
            if 'patch' in elname or 'fix' in elname or '.diff' in elname:
                patch_list.append(elem)
        return patch_list


    def retrieve_file_list(self, pkgid):
        """ Return patch list from srpm
        """
        url_srpm = ''.join((self.site_url, "rpms/", pkgid, "/files?json"))
        srpm_files = retrieve_json(url_srpm)
        return srpm_files


    def retrieve_srpms_list(self):
        """ Return list of src.rpm for the specified distritubion/release/arch
        """
        srpm_list = retrieve_json(self.srpms_url)
        return srpm_list

class Srpm():
    def __init__(self, name, pkgname, pkgid, patch_list):
        self.pkgid = pkgid
        self.name = name
        self.pkgname = pkgname
        self.patch_list = patch_list
        return

def retrieve_json(url):
    """ Return the content a JSON file from the url
    """
    #TODO: implement try/except for the urlopen and load
    json_file = urllib.urlopen(url)
    json_content = json.load(json_file)
    json_file.close()
    return json_content


def retrieve_patches(distribution, release, arch):
    """ Return all patches from a distribution/releas/arch
    """
    soso = Sophie(distribution, release, arch)
    patched_srpms = list()
    srpm_list = soso.retrieve_srpms_list()
    for srpm in srpm_list:
        pkgid = srpm['pkgid']
        filename = srpm['filename']
        pkgname = soso.retrieve_srpm_name(pkgid)
        patch_list = soso.retrieve_patch_list(pkgid)
        patched_srpms.append(Srpm(filename, \
                pkgname, pkgid, patch_list))
    return patched_srpms


if __name__ == "__main__":
    print retrieve_patches("Mageia", "cauldron", "x86_64")
