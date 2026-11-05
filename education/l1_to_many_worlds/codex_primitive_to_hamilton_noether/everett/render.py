"""Render the picture and mathematics pages for the three-post Everett lesson."""
from pathlib import Path
from textwrap import fill

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon

OUT = Path(__file__).parent
INK, GREEN, GREY = "#203436", "#007b75", "#81918e"
plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42})


def step(ax, x, y, dx, color):
    tip = x + dx
    neck = tip - (.18 if dx > 0 else -.18)
    ax.plot([x, neck], [y, y], color=color, lw=2.8)
    ax.add_patch(Polygon([(tip, y), (neck, y+.10), (neck, y-.10)], color=color))


def mark(ax, x, y, filled):
    ax.add_patch(Polygon([(x, y+.18), (x-.18, y-.16), (x+.18, y-.16)],
                         facecolor=INK if filled else "white", edgecolor=INK, lw=1.6))


def routes(ax, records=False, copies=False, blank=False, reader_blank=False):
    for y, dx, color in [(1.75, 1.6, INK), (.75, -1.6, GREEN)]:
        step(ax, 1.3 if dx > 0 else 2.9, y, dx, color)
        if records:
            mark(ax, 3.55, y, y < 1 and not blank)
        if copies:
            mark(ax, 4.25, y, y < 1 and not (blank or reader_blank))


def cancel(ax):
    step(ax, 1.3, 1.38, 2.3, INK)
    step(ax, 3.6, 1.15, -2.3, GREEN)
    ax.plot([1.3, 1.3], [.9, 1.58], color=GREY, lw=1)


def exit_mark(ax, click):
    ax.plot([2.4, 2.4], [.82, 1.72], color=INK, lw=2)
    if click:
        for dy in [-.34, 0, .34]:
            ax.plot([2.64, 3.00], [1.27 + dy/2, 1.27 + dy], color=GREEN, lw=2)


CAPTIONS = [
    ["Each route can reach this exit.", "Join the steps for this exit.", "Back at the start. The exit stays dark."],
    ["Start with the same blank mark.", "Give each route its own mark.", "Now this exit can click."],
    ["The detector holds the mark.", "A reader copies it.", "In Everett’s account, each reader\nremembers the matching mark."],
    ["Try again. Reverse the copying.", "Undo the route marks too.", "Join the steps again. Back to dark."],
]


def picture():
    fig, axes = plt.subplots(4, 3, figsize=(11.7, 8.3))
    fig.subplots_adjust(left=.04, right=.96, top=.95, bottom=.10, wspace=.12, hspace=.65)
    for r, row in enumerate(axes):
        for c, ax in enumerate(row):
            ax.set(xlim=(0, 5.2), ylim=(0, 2.5), aspect="equal")
            ax.axis("off")
            ax.text(.5, -.06, CAPTIONS[r][c], transform=ax.transAxes, ha="center",
                    va="top", fontsize=10, color=INK)
    routes(axes[0, 0])
    cancel(axes[0, 1])
    exit_mark(axes[0, 2], False)
    routes(axes[1, 0], records=True, blank=True)
    routes(axes[1, 1], records=True)
    exit_mark(axes[1, 2], True)
    routes(axes[2, 0], records=True)
    routes(axes[2, 1], records=True, copies=True)
    for y, filled in [(1.75, False), (.75, True)]:
        axes[2, 2].plot([2.1, 3.1], [y, y], color=GREY, lw=1)
        mark(axes[2, 2], 2.1, y, filled)
        mark(axes[2, 2], 3.1, y, filled)
    routes(axes[3, 0], records=True, copies=True, reader_blank=True)
    routes(axes[3, 1], records=True, copies=True, blank=True)
    cancel(axes[3, 2])
    return fig


SECTIONS = [
    ("Reading the marks",
     "A horizontal stroke depicts a signed contribution to the chosen exit. Two equal, opposite steps can cancel. The vertical stroke depicts the exit detector and rays depict a possible click. Open and solid triangles denote distinct record values. In paired columns the left triangle is the detector memory and the right triangle is the reader memory. The open triangle also serves as the ready value. Each strip starts a fresh run. The link between matching marks in strip 3 pairs a reader with a detector."),
    ("1   A dark exit",
     "Prepare |+⟩ = (|L⟩ + |R⟩)/√2. The recombiner tests |−⟩ = (|L⟩ − |R⟩)/√2 at the drawn exit. The two contributions to its amplitude are +1/2 and −1/2. Their sum is zero. A particle prepared in either route alone gives a click probability of 1/2. Here and below the Born rule and these input and output states are supplied."),
    ("2   Give the routes distinct records",
     "A reversible controlled flip maps |L,0⟩ to |L,0⟩ and |R,0⟩ to |R,1⟩. In the coherent superposition the dark-exit record vector becomes (|0⟩ − |1⟩)/2. Distinct ideal records are orthogonal, so its squared length is 1/2. Each joint event (dark exit, specified record) has probability 1/4. Either mark identifies the corresponding route at the tagging interaction."),
    ("3   Read the record",
     "Copy the detector bit into an initially ready reader. The joint state is (|L,0,0⟩ + |R,1,1⟩)/√2. Relative to reader value 0 the detector reads 0, and relative to reader value 1 it reads 1. Each conditional state has one matching record. Everett interprets both terms as continuing histories of the whole. In a macroscopic account, persistent copies in an environment help stabilize the records."),
    ("4   Reverse the record before testing the exit",
     "On a fresh run, reverse the reader copy and then the detector flip. Each is its own inverse. The coherent state returns to |+⟩|0,0⟩, so the exit probability returns to zero. A joint classical mixture of the two recorded alternatives instead gives 1/2 after the same reversal. This contrast requires coherent control of every copy, including any environmental record."),
]


def mathematics():
    fig = plt.figure(figsize=(11.7, 8.3))
    fig.text(.07, .92, "Two routes, one exit, and a record", fontsize=23, color=INK)
    y = .865
    for title, paragraph in SECTIONS:
        fig.text(.07, y, title, fontsize=13, weight="bold", color=GREEN, va="top")
        lines = fill(paragraph, width=114)
        fig.text(.07, y-.041, lines, fontsize=10.5, linespacing=1.36, color=INK, va="top")
        y -= .062 + .025 * len(lines.splitlines())
    return fig


if __name__ == "__main__":
    pictures, maths = picture(), mathematics()
    pictures.savefig(OUT/"pictures.png", dpi=160)
    with PdfPages(OUT/"two_sheets.pdf") as pdf:
        pdf.savefig(pictures)
        pdf.savefig(maths)
    plt.close("all")
