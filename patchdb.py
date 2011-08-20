#!/usr/bin/env python
from sqlalchemy import create_engine, MetaData, Table, Column, \
                       Integer, String, Date
import datetime
import sophie


class PatchDB():
    """ Class containing database of patches for one RPM
    distribution/release/arch
    """


    def __init__(self, distribution, release, arch):
        self.distribution = distribution
        self.release = release
        self.arch = arch
        db_name = "_".join(self.distribution, 
                           self.release,
                           self.arch,
                           "patch.db")
        self.database = create_engine("".join('sqlite:///', db_name), echo=True)
        self.metadata = MetaData(self.database)

    def first_population(self):
        self.patch_table = Table('patch', self.metadata,
            Column('key_num', Integer, primary_key=True),
            Column('patch_name', String(100)),
            Column('srpm_name', String(100)),
            Column('status', Integer),
            Column('date', Date),
        )
        self.patch_table.create()
        key_count = 0
        patch_insertion = self.patch_table.insert()
        patch_list = sophie.retrieve_patches(self.distribution,
                                             self.release,
                                             self.arch)
        patches = list()
        for patch in patch_list:
            patches.append({'key_num': key_count,
                            'patch_name': patch[1],
                            'srpm_name': patch[0],
                            'status': 0,
                            'date': datetime.date.today()})
            key_count += 1
        patch_insertion.execute(patches)


if __name__ == "__main__":
    Mageia_Db = PatchDB("Mageia", "cauldron", "x86_64")
    Mageia_Db.first_population()
