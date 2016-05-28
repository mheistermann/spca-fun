#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Martin Heistermann <spca@mheistermann.de>
# Date: 2016-05-28
# License: Beerware


# Warning: this code is pretty crappy, but after it got me the right
#          result I didn't bother to improve it.

import struct
import string
from collections import Counter

def u32(s):
    return struct.unpack("<I",s)[0]

def guess_address_tables(fw, minlen=10):
    seq = []
    for off in range(0,len(fw)-4,4):
        dw = u32(fw[off:off+4])
        if dw >> 24 == 0x80:
            seq.append(dw)
        else:
            if len(seq) >= minlen:
                yield off-4*len(seq), seq
            seq = []

def guess_strings(fw, minlen=5, chars=string.printable,startaddr=0, endaddr=2**32):
    if not isinstance(chars, bytes):
        chars = chars.encode("utf-8")
    pos = 0
    subseq = []
    for pos in range(startaddr,min(len(fw), endaddr)):
        curchar = fw[pos]
        if curchar in chars:
            subseq.append(curchar)
        else:
            if len(subseq) >= minlen:
                yield pos-len(subseq), bytes(subseq)
                assert fw[pos-len(subseq)] == subseq[0]
            subseq = []


def find_corr_shitty(strs, table):
    strs_by_size = sorted(strs, key = lambda x: -len(x[1])) # longest first
    st = sorted(table)

    str_lens = [len(s) for a,s in strs]
    print("strlens: {}", sorted(str_lens)[-10:])
    max_strlen = sorted(str_lens)[-2]
    ptr_diffs = [(b-a) for a,b in zip(st, st[1:]) if (b-a) <= max_strlen]

    for a,s in strs_by_size:
        cnt = ptr_diffs.count(len(s)+1)
        print("str@0x{:x} len {} cnt: {}, {}...".format(
            a,
            len(s),
            cnt,
            s[:30]))
        if cnt == 1:
            virt = st[ptr_diffs.index(len(s)+1)]
            off = virt - a
            print("off {:x}, virt 0x{:x}".format(off,virt))



    print("ptrdiff: {}", sorted(ptr_diffs)[-50:])

def find_corr(strs, table):
    print("testing with a table of len {}".format(len(table)))
    phys = sorted(x[0] for x in strs)
    #print("phys {}".format(phys[:10]))
    phys_set = set(phys)
    virt_pointers = set(table)

    start_off = min(virt_pointers) - max(phys)
    end_off = max(virt_pointers) - min(phys)
    print("start {:x}, end {:x}".format(start_off, end_off))


    best_offset = None
    best_offset_matches = 0
    for offset in range(start_off & ~3, end_off & ~3, 4):
        if offset & 0xffff == 0:
            print("progress {}%, matches {}%".format(
                100.0 * (offset-start_off)/ (end_off - start_off),
                100.0 * best_offset_matches/len(virt_pointers)))
        matches = 0
        #trial_virts = set(offset+phy for phy in phys)
        #matches = len(trial_virts.intersection(virt_pointers))
        #trial_phys = set(virt-offset for virt in virt_pointers)
        for virt in virt_pointers:
            phys = virt - offset
            matches += phys in phys_set
        #print((list(trial_phys))[:10])
        #matches = len(trial_phys.intersection(phys_set))

        if matches > best_offset_matches:
            best_offset_matches = matches
            best_offset = offset
            print("off {:x} # matches: {}".format(offset,matches))
    print("done")
    return best_offset, best_offset_matches, 100.0*best_offset_matches/len(table)






def main(fname):
    with open(fname,"rb") as fp:
        fw = fp.read()

    strs = list(guess_strings(fw,startaddr=0x805780, endaddr=0x87dca3))
    print("found {} potential strings".format(len(strs)))
    tables = list(guess_address_tables(fw))
    print("found {} potential tables".format(len(tables)))

    str_lens = [len(s) for a,s in strs]

    strlocs = [a for a,s in strs]
    strdists = [b-a for a,b in zip(strlocs, strlocs[1:])]
    gc = Counter()
    for a,t in tables:
        if t != list(sorted(set(t))):
            continue
        virt_and_dist = [(a, b-a) for a,b in zip(t, t[1:])]
        #if len(dists) != len(set(dists)): # pretty extreme, just to try
        #    continue
        print("table @ {:x} with {} entries".format(a, len(t)))

        c = Counter()
        for virt, d in virt_and_dist:
            # we guess string len is between d-4 and d-1
            #print("dist {}".format(d))
            for phys, s in strs:
                if d-4 <= len(s) <= d-1:
                    offset = virt - phys
                    c[offset] += 1
        gc.update(c)
        print([c.most_common(5)])

        #strlen_seq = [l-1 in str_lens for l in set(dists)]
        #cont = [l-1 in str_lens for l in set(dists)]
        #print("{}/{}".format(sum(cont), len(set(dists))))
    print([gc.most_common(5)])


    global mv
    mv = locals()



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: {} <SPHOST.BRN filename>".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
