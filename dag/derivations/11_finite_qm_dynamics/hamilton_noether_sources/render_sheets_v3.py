from pathlib import Path
import math
import sys
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else 'v3'
BLACK, GREEN, ORANGE, GREY = '#243439', '#087f78', '#bd4e2e', '#b8c2c5'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42})

def line(ax, a, b, color=BLACK, lw=1.9, alpha=1, dash=False):
    ax.plot([a[0],b[0]], [a[1],b[1]], color=color, lw=lw, alpha=alpha,
            linestyle=(0,(3,3)) if dash else '-', solid_capstyle='round')

def arrow(ax, a, b, color=BLACK, lw=2, alpha=1, head=.20):
    a,b=np.array(a,dtype=float),np.array(b,dtype=float)
    d=b-a; length=np.linalg.norm(d)
    if length < 1e-9: return
    head=min(head,.35*length)
    u=d/length; n=np.array([-u[1],u[0]])
    base=b-head*u
    line(ax,a,base,color,lw,alpha)
    ax.add_patch(Polygon([b,base+.44*head*n,base-.44*head*n],closed=True,
                         facecolor=color,edgecolor=color,alpha=alpha))

def pair(ax, q, p, origin=(1,1), scale=1, alpha=1):
    x,y=origin
    arrow(ax,(x,y),(x+scale*q,y),BLACK,alpha=alpha)
    arrow(ax,(x+scale*q,y),(x+scale*q,y+scale*p),GREEN,alpha=alpha)

def rotor(ax, angle, origin=(4.7,1.8), r=1.25, ghost=False):
    x,y=origin
    arrow(ax,(x,y),(x+r,y),BLACK,lw=2.8)
    if ghost:
        for t in [math.pi/2,math.pi,3*math.pi/2]:
            arrow(ax,(x,y),(x+r*math.cos(t),y+r*math.sin(t)),GREY,lw=1,head=.14)
    arrow(ax,(x,y),(x+r*math.cos(angle),y+r*math.sin(angle)),GREEN,lw=1.35,head=.15)

def patch(ax, shear):
    a=(2.3,.75); b=(5.3,.75); c=(5.3+shear,2.55); d=(2.3+shear,2.55)
    for z,w,col in [(a,b,BLACK),(b,c,BLACK),(c,d,GREEN),(d,a,GREEN)]: arrow(ax,z,w,col,head=.16)
    line(ax,a,c,GREY,lw=1.2)

CAPS=[
 ['Bring them together.','They match.','Turn one. Compare again.'],
 ['Take this step.','Then take this step.','One step reaches the same end.'],
 ['A few steps.','More, smaller steps.','Follow the change more closely.'],
 ['Start together.','Turn just one.','Keep turning the same way.\nIt comes back.'],
 ['Two pieces make this patch.','Slide the top sideways.','Same area. Different shape.'],
 ['Now, black changes\nat green’s pace.','At that same instant, green changes\nat black’s pace, the opposite way.','Under both rules,\nthe joined arrow turns.'],
 ['New rule:\ngreen sets the slide.','Shift, then slide.','Slide, then shift.\nSame end.'],
 ['Black advances.','Green stays the same.','Every step keeps that amount.']]

def make_pictures():
    fig=plt.figure(figsize=(11.69,16.54),facecolor='white')
    axs=[]
    for r in range(8):
        row=[]
        y=.87-r*.113
        fig.text(.035,y+.045,f'{r+1:02}',fontsize=10,color=GREY)
        for c in range(3):
            x=.07+c*.31
            ax=fig.add_axes([x,y,.27,.085]); ax.set_xlim(0,9); ax.set_ylim(-.25,3.65)
            ax.set_aspect('equal'); ax.axis('off'); row.append(ax)
            fig.text(x+.135,y-.006,CAPS[r][c],ha='center',va='top',fontsize=10.3,color=BLACK)
            if c<2 and not (r==5 and c==0) and not (r==6 and c==1):
                flow=fig.add_axes([x+.276,y+.034,.029,.012]); flow.set_xlim(0,1);flow.set_ylim(0,1);flow.axis('off')
                arrow(flow,(0,.5),(1,.5),GREY,lw=1.1,head=.2)
        axs.append(row)
    a,b,c=axs[0]
    arrow(a,(2,.5),(3.4,2.5));arrow(a,(5,.5),(6.4,2.5),GREEN)
    arrow(b,(3.7,.5),(5.1,2.5),BLACK,lw=4);arrow(b,(3.7,.5),(5.1,2.5),GREEN,lw=1.5,head=.15)
    arrow(c,(3.3,.5),(4.7,2.5))
    radius=math.hypot(1.4,2)
    arrow(c,(3.3,.5),(3.3+radius*math.cos(.37),.5+radius*math.sin(.37)),GREEN)
    for k,ax in enumerate(axs[1]):
        arrow(ax,(2.4,.5),(5.7,.5))
        if k>0: arrow(ax,(5.7,.5),(5.7,2.65),GREEN)
        if k>1: arrow(ax,(2.4,.5),(5.7,2.65),ORANGE)
    for ax,n in zip(axs[2],[2,4,12]):
        ts=np.linspace(0,1,n+1); pts=[(1.6+5.5*t,.7+1.8*math.sin(math.pi*t)) for t in ts]
        for j in range(n): arrow(ax,pts[j],pts[j+1],BLACK,head=.13 if n<5 else .09,lw=1.7)
    rotor(axs[3][0],0);rotor(axs[3][1],math.pi/2);rotor(axs[3][2],2*math.pi,ghost=True)
    for ax,s in zip(axs[4],[0,.8,1.5]):patch(ax,s)
    a,b,c=axs[5]
    pair(a,2.1,1.2,origin=(2,1.3));arrow(a,(4.1,1.3),(5.3,1.3),ORANGE)
    pair(b,2.1,1.2,origin=(2,1.3));arrow(b,(4.48,2.5),(4.48,.4),ORANGE)
    for i,t in enumerate([0,.5,1.]):
        q=2.1*math.cos(t)+1.2*math.sin(t);p=1.2*math.cos(t)-2.1*math.sin(t)
        origin=(3.2,1.9)
        opacity=[.25,.5,1][i]
        pair(c,q,p,origin=origin,alpha=opacity)
        arrow(c,origin,(origin[0]+q,origin[1]+p),ORANGE,alpha=opacity)
    a,b,c=axs[6]
    pair(a,2,.65,origin=(1.5,1))
    arrow(a,(3.5,1),(4.15,1),ORANGE)
    for ax,intermediate in [(b,3.5),(c,2.65)]:
        pair(ax,2,.65,origin=(1.5,1),alpha=.15)
        pair(ax,intermediate,.65,origin=(1.5,1),alpha=.4)
        pair(ax,4.15,.65,origin=(1.5,1))
        first,second=(GREY,ORANGE) if intermediate==3.5 else (ORANGE,GREY)
        arrow(ax,(3.5,2.25),(1.5+intermediate,2.25),first,lw=1.2,head=.13)
        arrow(ax,(1.5+intermediate,2.25),(5.65,2.25),second,lw=1.2,head=.13)
    for ax,q in zip(axs[7],[2,2.65,3.3]):pair(ax,q,.65,origin=(1.5,.8))
    fig.text(.5,.031,'',ha='center')
    return fig

BLOCKS=[
 ('What these pictures can establish',
  'A proof sketch for a supplied classical model with one degree of freedom: local Hamiltonian structure and a Noether example. This is not a derivation of mechanics from marks alone, nor of quantum mechanics or the supplied alpha paper.'),
 ('01–04 · Comparing, composing, refining, returning',
  'We supply an affine plane, comparison by translation, and reversible rotations. Tip-to-tail composition gives vector addition. Strip 3 samples a prescribed differentiable path; drawings alone do not prove a smooth limit. Strip 4 introduces cyclic position (angular phase), not the specialized geometric phase of transport/holonomy, and not a quantum amplitude. It shows three intermediate directions and a return.'),
 ('05 · The extra structure that makes Hamilton possible',
  'We now supply a STATE plane with dimensionless conjugate coordinates q,p and oriented area ω=dq ∧ dp. In strips 6–8 black measures q (right positive), green measures p (up positive); left/down are negative. The green tip locates the state relative to the black tail. These are state components, not spatial directions. Conjugacy is assumed, not established by a right angle. In physical units p dq has units of action. Momentum need not equal velocity.'),
 ('05 → 06 · The local derivation',
  'Let u,v be rates: a dot means change per unit time. Assume an autonomous (time-independent), C¹ (continuously differentiable) rule preserving oriented area for EVERY small cell. Local expansion must cancel: ∂u/∂q + ∂v/∂p=0. A partial derivative is a slope holding the other coordinate fixed. This lets one function H generate both rates. Formally, α=u dp−v dq is closed: its integral around any sufficiently small closed loop vanishes. On a simply connected patch (no holes), integrating α is path-independent and gives H. Thus\n\n        q̇ = u = ∂H/∂p,                ṗ = v = −∂H/∂q.\n\nH is fixed up to a constant. Strip 5 illustrates the area hypothesis; it does not prove it for every rule. Topology can obstruct a global H. Physical energy needs a physical model.'),
 ('06 · An exact turning rule',
  'Choose H=(q²+p²)/2. The two rate panels use the SAME state (2.1,1.2), at the SAME instant. Orange lengths are 1.2 and 2.1 on a common rate scale. They are not successive kicks. The last panel joins each pair as in strip 2: three exact states at times 0, 0.5, 1 share one origin and scale; pale means earlier. The exact evolution is\n\n        q′=q cos h+p sin h,       p′=p cos h−q sin h.\n\nThis preserves ω and H. The Euler assignment (q+h p,p−h q) multiplies area and q²+p² by 1+h² instead. Circles belong to this chosen example and scaling, not every Hamiltonian system.'),
 ('07 · A different rule and its continuous symmetry',
  'Switch to H=p²/2: Φ_t(q,p)=(q+t p,p). The shift T_a(q,p)=(q+a,p) preserves the specified area (is canonical) and H, so Φ_t T_a=T_a Φ_t. Both orders start at (2,0.65), use shift a=1.5 and time t=1, and end at (4.15,0.65). Pale intermediate q values are 3.5 and 2.65. Grey always means shift; orange means slide. Strip 8 repeats the unshifted run at times 0,1,2. The oscillator does NOT have this translation symmetry.'),
 ('08 · The Noether charge and why it is conserved',
  'Translation is generated by Y=∂/∂q; its pairing with ω gives dp, so the charge is J=p. Since H has no q dependence, dJ/dt=ṗ=−∂H/∂q=0. Equivalently, use S=∫(p q̇−H)dt. Independent interior variations of q,p, with δq=0 at time endpoints, give Hamilton’s equations. Constant q translations preserve the action and map endpoint data to translated data; they are not fixed-endpoint variations. Noether conservation holds along stationary trajectories. Equal drawn marks alone do not prove this theorem.'),
 ('Limits and the remaining debt',
  'Supplied: geometry, oriented pairing, regularity, the two model rules and variational hypotheses. Derived conditionally: local Hamiltonian form, exact example flows and conserved translation charge. Not derived: the earlier Genesis/L1 result, an identity of holonomy with Noether, quantization, Born weights, Everett branching or Bell correlations. Novice comprehension remains to be tested.')]

def make_math():
    fig=plt.figure(figsize=(11.69,16.54),facecolor='white')
    fig.text(.07,.95,'Mathematics and assumptions',fontsize=21,color=BLACK,weight='bold')
    fig.text(.07,.926,'Companion to strips 01–08 · supplied structure, derived consequences, explicit limits',fontsize=10.3,color=GREEN)
    y=.89
    for title,body in BLOCKS:
        fig.text(.07,y,title,fontsize=12,color=GREEN,weight='bold',va='top');y-=.023
        lines=[]
        for paragraph in body.split('\n'):
            lines.extend(textwrap.wrap(paragraph,width=114) if paragraph else [''])
        fig.text(.07,y,'\n'.join(lines),fontsize=10.4,color=BLACK,va='top',linespacing=1.4)
        y-=len(lines)*.0123+.017
    if y<.025: raise ValueError(f'Math sheet overflow: {y}')
    return fig

def main():
    pictures=make_pictures();mathsheet=make_math()
    for name,fig in [('picture_sheet',pictures),('math_sheet',mathsheet)]:
        fig.savefig(ROOT/f'{name}_{VERSION}.png',dpi=160)
        fig.savefig(ROOT/f'{name}_{VERSION}.svg')
        fig.savefig(ROOT/f'{name}_{VERSION}.pdf')
    with PdfPages(ROOT/f'two_sheets_{VERSION}.pdf') as pdf:
        pdf.savefig(pictures);pdf.savefig(mathsheet)
    (ROOT/f'math_sheet_{VERSION}.md').write_text('# The mathematics and assumptions\n\n'+'\n\n'.join('## '+title+'\n\n'+body for title,body in BLOCKS)+'\n',encoding='utf-8')
    (ROOT/f'panel_captions_{VERSION}.md').write_text('# Picture-sheet captions\n\n| Strip | Left | Middle | Right |\n|---|---|---|---|\n'+'\n'.join('| '+str(i+1)+' | '+' | '.join(c.replace('\n',' ') for c in row)+' |' for i,row in enumerate(CAPS))+'\n',encoding='utf-8')
    plt.close('all')
    print(f'Wrote two A3 sheets, PNG/SVG/PDF, version {VERSION}')

if __name__=='__main__':main()
