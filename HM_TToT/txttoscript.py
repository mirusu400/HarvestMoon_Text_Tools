# -*- coding:utf-8 -*-
# TToT Use Int-Size Pointer(4Bytes) But GB Use Short-Size Pointer(2Bytes)
# So A little bit different With GB
import sys
import os
import struct as s
import binascii

# TToT Use 4 Bytes to Read Pointers
TTOT_FLAG = 4
# GB Use 2 Bytes to Read Pointers
GB_FLAG = 2
POINTER_FLAG = GB_FLAG
TBLFILE = './HM_TToT/TToT_jpn.tbl'


class table():
    def __init__(self, file):
        self.file = file
        self.tblword = []
        self.tblhex = []
        self.readtable()

    def readtable(self):
        with open(self.file, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                tline = line.replace("\n", "").split("=")
                if (tline == ['']):
                    break
                # BOM Error fix
                tline[0] = tline[0].replace(u"\ufeff", '')
                if line[-1] == "=":
                    self.tblword.append(line[-1])
                else:
                    self.tblword.append(tline[1])
                self.tblhex.append(tline[0].upper())
        return

    def cv(self, char):
        if len(char) == 1:
            idx = self.tblword.index(char)
            data = self.tblhex[idx]
            return data
        else:
            idx = self.hex.index(char)
            data = self.tblword[idx]
            return data


def hextodatas(chex):
    writehex = binascii.unhexlify(chex)
    return writehex


def readshort(file):
    return s.unpack("<H", file.read(2))[0]


def readint(file):
    return s.unpack("<I", file.read(4))[0]


def writeint(num):
    return s.pack("<I", num)


def writeshort(num):
    return s.pack("<H", num)


def convert(file, tbl):
    texts = []
    hexs = []
    pos = []
    size = []

    out = os.path.splitext(file)[0] + ".hav"
    count = 0
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                continue
            else:
                count += 1
                texts.append(line.replace("\n", ""))
    for i in range(count):
        text = texts[i]
        tmp = []
        outbuf = ""

        # Get hexes in one line
        for idx, char in enumerate(text):
            if idx in tmp:
                continue
            tbuf = ""
            # If char starts with '[' (제어코드)
            if char == "[":
                tidx = idx
                tmp.append(tidx)
                while True:
                    tidx += 1
                    tmp.append(tidx)
                    tbuf += text[tidx]
                    if text[tidx] == "]":
                        break
                tbuf = tbuf.replace("]", "")
            else:
                tbuf = tbl.cv(char)
            outbuf += tbuf

        size.append(len(outbuf))
        hexs.append(outbuf)

        if i != 0:
            pos.append(pos[i-1] + (size[i-1] // 2))
        else:
            pos.append(count * POINTER_FLAG)

    with open(out, "wb") as f:
        # Write pointer(position)
        for i in range(count):
            if POINTER_FLAG == GB_FLAG:
                f.write(writeshort(pos[i]))
            elif POINTER_FLAG == TTOT_FLAG:
                f.write(writeint(pos[i]))

        for i in range(count):
            chex = hexs[i]
            buf = hextodatas(chex)
            f.write(buf)
    return


if __name__ == '__main__':
    TBLFILE = sys.argv[1]
    TINPUT = sys.argv[2]
    t = table(TBLFILE)

    if os.path.isdir(TINPUT):
        file_list = os.listdir(TINPUT)
        for file in file_list:
            ofile = str(TINPUT) + "/" + str(file)
            convert(ofile, t)
    else:
        convert(TINPUT, t)

