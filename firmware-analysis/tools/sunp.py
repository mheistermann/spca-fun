#!/usr/bin/env python3
# encoding: utf-8

"""Parser for SUNP BURN files, commonly distributed as SPHOSTBRN"""


__author__  = "Martin Heistermann"
__license__ = "GPL3"
__email__   = "code at mheistermann.de"


import construct as c
from construct import Struct, Magic, ULInt32, Padding, Aligned
from construct import Pointer, Array, MetaArray, String
from construct import Field, StaticField, OnDemand, Bytes
from construct import Adapter, Value

burnhdr1 = Struct("burnhdr1",
        Magic(b"SUNP BURN HDR 1"),
        Padding(1, strict=True),
        Array(9,
            Bytes("unk", 16) # mostly only first 4 bytes used, exception 12 bytes at [burnhdr+0x74], e.g. behind unk[6]
            )
        )


def _xor(s, key=0x7A):
    return bytes((x ^ key) for x in s)

class XorObfuscation(Adapter):
    def _encode(self, obj, ctx):
        return _xor(obj)

    def _decode(self, obj, ctx):
        return _xor(obj)

# not sure what this is, contains build date
burnhdr2 = Struct("burnhdr2",
        Magic(b"SUNP BURN HDR 2"),
        Padding(1),
        ULInt32("count"),
        Padding(12),
        MetaArray(lambda ctx: ctx.count,
            XorObfuscation(Bytes("mystery", 128))),
        )

# burnhdr3 contains filenames that should be backed up
burnhdr3 = Struct("burnhdr3",
        Magic(b"SUNP BURN HDR 3"),
        Padding(1),
        ULInt32("num_filenames"),
        Padding(12),
        MetaArray(lambda ctx: ctx.num_filenames,
            String("filename", 0x70, padchar=b"\x00")), # or is this 0 terminated?! cf bogus IN here: b'A:\\RO_RES\\COLD.BIN\x00IN',
        )

code = OnDemand(Bytes("code", lambda ctx: ctx.len_code))



sunp_file = Struct("sunp_file",
        Magic(b"SUNP BURN FILE"),
        Padding(2, strict=True), # guessing...
        ULInt32("file_size"),
        ULInt32("off_burnhdr1"),
        ULInt32("off_burnhdr2"),
        ULInt32("off_code"),
        ULInt32("unk_zero"),
        ULInt32("off_burnhdr3"),
        Value("len_code", lambda ctx: ctx.off_burnhdr3 - ctx.off_code),
        #Padding(472),
        Pointer(lambda ctx: ctx.off_burnhdr1, burnhdr1),
        Pointer(lambda ctx: ctx.off_burnhdr2, burnhdr2),
        Pointer(lambda ctx: ctx.off_code,     code),
        Pointer(lambda ctx: ctx.off_burnhdr3, burnhdr3),
        )

if __name__ == '__main__':
    import pprint
    import argparse

    parser = argparse.ArgumentParser(description='Parse a SUNP BURN FILE (SPHOST.BRN)')
    parser.add_argument("filename", type=str,
                        help="input file, e.g. SPHOST.BRN")
    parser.add_argument('--debug', action='store_true',
                    help='Wrap parser in Construct.Debugger()')

    args = parser.parse_args()
    if args.debug:
        sunp_file = c.Debugger(sunp_file)


    with open(args.filename, 'rb') as fp:
        sunp = sunp_file.parse_stream(fp)
        pprint.pprint(sunp)

