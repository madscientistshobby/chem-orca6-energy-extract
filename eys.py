#!/usr/bin/env python3
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("prefix", nargs="?", default="YS", help="파일 이름 prefix (기본: YS)")
args = parser.parse_args()

# 하위폴더까지 포함 (recursive=True)
for file in sorted(glob.glob(f"**/{args.prefix}*.out", recursive=True)):
    fname = str(file)
    try:
        with open(fname, "r") as f:
            outfile = f.readlines()

        ESCF, ZPE, S, TS, nIF = 0, 0, 0, 0, 0

        for line in outfile:
            if "aborting" in line:
                print(f"{fname}: Failed")

            if "FINAL SINGLE POINT ENERGY" in line:
                ESCF = format(float(line.split()[-1]) * 27.2114 + 0.08159, ".3f")

            if "Total correction" in line:
                ZPE = line.split()[-2]

            if "Total entropy correction" in line:
                S = format(float(line.split()[-2]) * (-3.354), ".2f")
                TS = format(float(line.split()[-2]), ".2f")

            if "imaginary mode" in line:
                nIF += 1

        if nIF != 0:
            print(f"{fname}: {nIF}IF detected!")

        if ZPE != 0:
            print(f"{fname}: ESCF = {ESCF}, ZPE = {ZPE}, S = {S}") #, TS = {TS}")
        else:
            print(f"{fname}: ESCF = {ESCF}")

    except Exception:
        pass
