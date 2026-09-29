"""Retain the six mathematical illustrations, separately from the text questions."""
import argparse
from pathlib import Path
import pymupdf

FIGURES = {
    'calculus-Q107': (41, (416, 558, 505, 644)),
    'calculus-Q179': (68, (392, 70, 526, 155)),
    'calculus-Q191': (72, (372, 92, 508, 181)),
    'calculus-Q374': (144, (168, 104, 431, 208)),
    'calculus-Q385': (149, (132, 331, 448, 438)),
    'calculus-Q612': (240, (417, 481, 506, 575)),
}

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('pdf');args=p.parse_args()
    out=Path(__file__).resolve().parents[1]/'frontend/figures/workbook';out.mkdir(parents=True,exist_ok=True)
    with pymupdf.open(args.pdf) as doc:
        for key,(page,rect) in FIGURES.items():
            doc[page-1].get_pixmap(clip=pymupdf.Rect(rect),matrix=pymupdf.Matrix(4,4)).save(out/(key+'.png'))
