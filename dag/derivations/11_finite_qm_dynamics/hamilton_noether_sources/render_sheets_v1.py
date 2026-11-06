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
VERSION = sys.argv[1] if len(sys.argv) > 1 else 'v1'
BLACK, GREEN, ORANGE, GREY = '#243439', '#087f78', '#bd4e2e', '#b8c2c5'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42})

def line(ax, a, b, color=BLACK, lw=1.9, alpha=1, dash=False):
    ax.plot([a[0],b[0]], [a[1],b[1]], color=color, lw=lw, alpha=alpha,
            linestyle=(0,(3,3)) if dash else '-', solid_capstyle='round')

def arrow(ax, a, b, color=BLACK, lw=2, alpha=1, head=.20):
    a,b=np.array(a,dtype=float),np.array(b,dtype=float)
    d=b-a; length=np.linalg.norm(d)
    if length < 1e-9: return
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
            line(ax,(x,y),(x+r*math.cos(t),y+r*math.sin(t)),GREY,dash=True)
    arrow(ax,(x,y),(x+r*math.cos(angle),y+r*math.sin(angle)),GREEN,lw=1.35,head=.15)

def patch(ax, shear):
    a=(2.3,.75); b=(5.3,.75); c=(5.3+shear,2.55); d=(2.3+shear,2.55)
    for z,w,col in [(a,b,BLACK),(b,c,BLACK),(c,d,GREEN),(d,a,GREEN)]: arrow(ax,z,w,col,head=.16)
    line(ax,a,c,GREY,lw=1.2)

CAPS=[
 ['Bring them together.','They match.','Now there is a difference.'],
 ['Take this step.','Then take this step.','One step reaches the same end.'],
 ['A few steps.','More, smaller steps.','Follow the change more closely.'],
 ['Start together.','Turn just one.','A full turn brings it back.'],
 ['Two pieces make this patch.','Slide the top sideways.','Same area. Different shape.'],
 ['Green sets black’s next change.','Black sets green’s opposite change.','Together, the pair turns.'],
 ['New rule: slide at green’s pace.','Start farther along.','The same shift survives the move.'],
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
            if c<2:
                flow=fig.add_axes([x+.276,y+.034,.029,.012]); flow.set_xlim(0,1);flow.set_ylim(0,1);flow.axis('off')
                arrow(flow,(0,.5),(1,.5),GREY,lw=1.1,head=.2)
        axs.append(row)
    a,b,c=axs[0]
    arrow(a,(2,.5),(3.4,2.5));arrow(a,(5,.5),(6.4,2.5),GREEN)
    arrow(b,(3.7,.5),(5.1,2.5),BLACK,lw=4);arrow(b,(3.7,.5),(5.1,2.5),GREEN,lw=1.5,head=.15)
    arrow(c,(3.3,.5),(4.7,2.5));arrow(c,(3.3,.5),(6,1.6),GREEN)
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
    pair(a,2.8,1.7,origin=(2,0.7));arrow(a,(4.8,.7),(6,.7),ORANGE)
    pair(b,2.8,1.7,origin=(2,.7));arrow(b,(4.8,2.4),(4.8,1.2),ORANGE)
    for i,t in enumerate([0,.3,.6]):
        q=2.1*math.cos(t)+1.2*math.sin(t);p=1.2*math.cos(t)-2.1*math.sin(t)
        pair(c,q,p,origin=(.4+2.9*i,1.1),scale=.9)
    a,b,c=axs[6]
    pair(a,2,.65,origin=(1,2));pair(a,3.5,.65,origin=(1,.25))
    pair(b,2,.65,origin=(1,2),alpha=.2);pair(b,3.5,.65,origin=(1,.25),alpha=.2)
    pair(b,3,.65,origin=(1,2));pair(b,4.5,.65,origin=(1,.25))
    pair(c,3.65,.65,origin=(1,2));pair(c,5.15,.65,origin=(1,.25))
    for ax,q in zip(axs[7],[2,3.5,5]):pair(ax,q,1.3,origin=(1.5,.8))
    fig.text(.5,.031,'',ha='center')
    return fig

BLOCKS=[
 ('What these pictures can establish',
  'This is a supplied classical model with one degree of freedom. It makes a local Hamiltonian construction and one Noether example visible. It does not derive mechanics from marks alone, nor yet explain quantum mechanics.'),
 ('01–04 · Comparing, composing, refining, returning',
  'We supply an oriented affine plane and comparison by translation. Tip-to-tail composition is vector addition in that plane. Refinement samples a prescribed differentiable path; finite drawings do not prove a limit or smoothness. A supplied reversible rotation gives cyclic relative position. That is geometric phase, not a quantum amplitude. Colours distinguish marks; they do not specify a physical ontology.'),
 ('05 · The extra structure that makes Hamilton possible',
  'For the remaining strips we choose a state plane with dimensionless conjugate coordinates q,p and oriented area ω = dq ∧ dp. This pairing is an assumption: perpendicular ink strokes do not establish it. With physical units, p dq has units of action; momentum need not equal velocity. The patch is the object being transformed, not a background container. Its orientation matters.'),
 ('05 → 06 · The local derivation',
  'Assume an autonomous C¹ field X=(u,v), its differentiable local flow, and preservation of ω for EVERY sufficiently small cell. One sheared patch only illustrates this hypothesis. Area preservation gives u_q + v_p = 0. Hence α = ι_Xω = u dp − v dq is closed: dα = 0. On a simply connected local patch α=dH, so\n\n        q̇ = u = ∂H/∂p,                ṗ = v = −∂H/∂q.\n\nThe Hamiltonian is reconstructed up to an additive constant. This is local: topology may obstruct a globally single-valued H. Calling H physical energy requires a physical model.'),
 ('06 · An exact turning rule',
  'Choose H=(q²+p²)/2. Then q̇=p and ṗ=−q. The orange arrows depict instantaneous changes, not consecutive finite kicks. For a time h the exact update is\n\n        q′ = q cos h + p sin h,       p′ = p cos h − q sin h.\n\nIt preserves both oriented area and H. The naive Euler update (q+h p, p−h q) instead multiplies area and q²+p² by 1+h². Cyclic motion belongs to this example, not to every Hamiltonian flow.'),
 ('07 · A different rule and its continuous symmetry',
  'Now choose H=p²/2. The exact evolution is Φ_t(q,p)=(q+t p,p). Shifting the starting configuration by T_a(q,p)=(q+a,p) commutes with that evolution: Φ_t T_a=T_a Φ_t. This canonical translation leaves H unchanged. Strip 7 switches rules; the oscillator of strip 6 does NOT have this translation symmetry.'),
 ('08 · The Noether charge and why it is conserved',
  'The translation generator Y=∂q obeys ι_Yω=dp, so its charge is J=p. Hamilton’s equations give dJ/dt=ṗ=−H_q=0. In variational language, S=∫(p q̇−H)dt is invariant under constant q translations; stationarity supplies the equations and conserved momentum. The symmetry, action structure and equations jointly justify conservation. A repeated equal mark or unchanged gap alone does not prove Noether’s theorem.'),
 ('Limits and the remaining debt',
  'Supplied: affine structure, oriented pairing, regularity, model choice and variational hypotheses. Derived under those assumptions: local Hamiltonian form; two exact example flows; the translation charge and its conservation. Not established: the earlier Genesis/L1 derivation, any identity between holonomy and Noether, Born probabilities, Everett branching, Bell correlations, or an ontology of the universe. Those require further constructions and evidence.')]

def make_math():
    fig=plt.figure(figsize=(11.69,16.54),facecolor='white')
    fig.text(.07,.95,'The mathematics and the debt',fontsize=21,color=BLACK,weight='bold')
    fig.text(.07,.926,'Companion to strips 01–08 · supplied structure, derived consequences, explicit limits',fontsize=10.3,color=GREEN)
    y=.89
    for title,body in BLOCKS:
        fig.text(.07,y,title,fontsize=12,color=GREEN,weight='bold',va='top');y-=.023
        lines=[]
        for paragraph in body.split('\n'):
            lines.extend(textwrap.wrap(paragraph,width=114) if paragraph else [''])
        fig.text(.07,y,'\n'.join(lines),fontsize=10.4,color=BLACK,va='top',linespacing=1.4)
        y-=len(lines)*.0123+.025
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
    plt.close('all')
    print(f'Wrote two A3 sheets, PNG/SVG/PDF, version {VERSION}')

if __name__=='__main__':main()
