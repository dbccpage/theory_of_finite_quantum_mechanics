from pathlib import Path
import importlib.util
import math
import numpy as np
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('base',ROOT/'render_sheets_v3.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
b.VERSION='v4'
arrow,line,pair,patch=b.arrow,b.line,b.pair,b.patch
B,G,O,X=b.BLACK,b.GREEN,b.ORANGE,b.GREY
b.CAPS=[
 ['Bring them together.','They match.','Turn one. Compare again.'],
 ['Take one step, then another.','One step reaches the same end.','Follow a step back. You return.'],
 ['Same lengths. Opposite green.','Turn both joined arrows\nthe same way.','Different horizontal lengths.'],
 ['Two amounts.','Move some from left to right.','Join them: the same total.'],
 ['Turn once.','Turn again: reversed.','Twice more: returned.'],
 ['Two triangles make a patch.','Slide the top sideways.','Same area. Different shape.'],
 ['Now, black changes\nat green’s pace.','At that same instant, green changes\nat black’s pace, the opposite way.','Under both rules,\nthe joined arrow turns.'],
 ['New rule: green sets the slide.','Shift, then slide.','Slide, then shift. Same end.'],
 ['Black advances.','Green stays the same.','Every step keeps that amount.']]

def make_pictures():
 fig=b.plt.figure(figsize=(11.69,16.54),facecolor='white');axs=[]
 for r in range(9):
  row=[];y=.88-r*.100
  for c in range(3):
   x=.065+c*.313
   ax=fig.add_axes([x,y,.275,.072]);ax.set_xlim(0,9);ax.set_ylim(-.25,3.65);ax.set_aspect('equal');ax.axis('off');row.append(ax)
   fig.text(x+.1375,y-.004,b.CAPS[r][c],ha='center',va='top',fontsize=9.7,color=B)
   if c<2 and not(r==6 and c==0) and not(r==7 and c==1):
    flow=fig.add_axes([x+.279,y+.030,.026,.009]);flow.set_xlim(0,1);flow.set_ylim(0,1);flow.axis('off');arrow(flow,(0,.5),(1,.5),X,lw=1,head=.2)
  axs.append(row)
 a,c,d=axs[0]
 arrow(a,(2,.5),(3.4,2.5));arrow(a,(5,.5),(6.4,2.5),G)
 arrow(c,(3.7,.5),(5.1,2.5),B,lw=4);arrow(c,(3.7,.5),(5.1,2.5),G,lw=1.5,head=.15)
 arrow(d,(3.3,.5),(4.7,2.5));rad=math.hypot(1.4,2);arrow(d,(3.3,.5),(3.3+rad*math.cos(.37),.5+rad*math.sin(.37)),G)
 for k,ax in enumerate(axs[1][:2]):
  arrow(ax,(2.4,.5),(5.7,.5));arrow(ax,(5.7,.5),(5.7,2.65),G)
  if k:arrow(ax,(2.4,.5),(5.7,2.65),O)
 ax=axs[1][2];arrow(ax,(2.7,1.5),(6,1.5),B,lw=4);arrow(ax,(6,1.5),(2.7,1.5),G,lw=1.6)
 # Same two origins and scale throughout the mixing row.
 for sign,x in [(1,2),(-1,6)]:
  origin=(x,1.65);q=.9;p=sign*1.2
  pair(axs[2][0],q,p,origin)
  v=np.array([q,p]);u=np.array([[.6,.8],[-.8,.6]])@v
  arrow(axs[2][1],origin,(x+q,1.65+p),X,lw=1.3)
  arrow(axs[2][1],origin,(x+u[0],1.65+u[1]),O)
  pair(axs[2][2],u[0],u[1],origin)
 # Redistribution: lengths 3+1 -> 2+2, then head-to-tail total 4.
 ax=axs[3][0];arrow(ax,(1,1.1),(4,1.1));arrow(ax,(5,1.1),(6,1.1),G)
 ax=axs[3][1];arrow(ax,(1,1.1),(3,1.1));arrow(ax,(5,1.1),(7,1.1),G);arrow(ax,(3,2.25),(4,2.25),O);arrow(ax,(4.2,2.25),(5.7,2.25),X,lw=1)
 ax=axs[3][2];arrow(ax,(2,2.2),(5,2.2));arrow(ax,(5,2.2),(6,2.2),G);arrow(ax,(2,.8),(4,.8));arrow(ax,(4,.8),(6,.8),G)
 # A supplied quarter-turn; grey strokes retain preceding positions.
 for ax,t,ghosts in [(axs[4][0],math.pi/2,[0]),(axs[4][1],math.pi,[0,math.pi/2]),(axs[4][2],2*math.pi,[math.pi,3*math.pi/2])]:
  org=(4.5,1.55)
  for s in ghosts:arrow(ax,org,(4.5+1.3*math.cos(s),1.55+1.3*math.sin(s)),X,lw=1)
  arrow(ax,org,(4.5+1.3*math.cos(t),1.55+1.3*math.sin(t)),G)
 for ax,s in zip(axs[5],[0,.8,1.5]):patch(ax,s)
 a,c,d=axs[6];pair(a,2.1,1.2,(2,1.3));arrow(a,(4.1,1.3),(5.3,1.3),O)
 pair(c,2.1,1.2,(2,1.3));arrow(c,(4.48,2.5),(4.48,.4),O)
 for t,opacity in [(0,.2),(.5,.5),(1,1)]:
  q=2.1*math.cos(t)+1.2*math.sin(t);p=1.2*math.cos(t)-2.1*math.sin(t);org=(3.2,1.9)
  pair(d,q,p,org,alpha=opacity);arrow(d,org,(org[0]+q,org[1]+p),O,alpha=opacity)
 a,c,d=axs[7];pair(a,2,.65,(1.5,1));arrow(a,(3.5,1),(4.15,1),O)
 for ax,mid in [(c,3.5),(d,2.65)]:
  for q,opacity in [(2,.15),(mid,.4),(4.15,1)]:pair(ax,q,.65,(1.5,1),alpha=opacity)
  colors=(X,O) if mid==3.5 else (O,X)
  arrow(ax,(3.5,2.25),(1.5+mid,2.25),colors[0],lw=1.2,head=.13);arrow(ax,(1.5+mid,2.25),(5.65,2.25),colors[1],lw=1.2,head=.13)
 for ax,q in zip(axs[8],[2,2.65,3.3]):pair(ax,q,.65,(1.5,.8))
 return fig

b.BLOCKS=[
 ('Reading the pictures',
 'Read each strip left to right; row numbers here count from the top. Black and green distinguish contributions. Orange shows a result, transferred piece or rate as specified below. Grey shows a prior position or shift; arrows in the gutters indicate reading order. Drawn geometry is a chosen representation. No background axes, physical observer at infinity, or quantum amplitudes are required to read the pictures.'),
 ('1–2 · Comparison, composition and cancellation',
 'Supply an oriented affine plane and comparison by translation. Tip-to-tail joining defines vector addition; following a step by its reverse gives zero net displacement. WDP §§1.1–1.4 requires a declared comparison structure. Its §17.7 constructs signed histories after alternative formation and additive completion are admitted. Geometric reverse steps illustrate cancellation; they do not prove every physical operation reversible. WDP §17.8 constructs g(a,b)=L(a)ᵀL(b) from a supplied additive report L, with radical ker L; that pairing is observer-relative, not selected by bare difference.'),
 ('3 · A report can forget what the next move needs',
 'Inputs ψ±=(3,±4)/5 have equal component-length reports (3/5,4/5). Apply the SAME orthogonal matrix U=((3,4),(−4,3))/5: Uψ+=(1,0), Uψ−=(−7,−24)/25. The picture uses scale 1.5 throughout. Middle-panel grey is the old joined vector; orange is the rotated vector; the last panel resolves it into components. Equal old reports give different new ones, so no report-only update works for both. A supplied square report gives (9/25,16/25) initially and first outputs 1 versus 49/625. This is not Born uniqueness, nor a failure of the l1 norm to retain signs. Sources: FQM §13.8; Proofs §§1.2–1.4.'),
 ('4–5 · Balance first; a quarter-turn as an added move',
 'Redistribute lengths (3,1)→(2,2); both total 4. More generally zₖ₊₁=zₖ+d₀* jₖ preserves the vertex sum because each internal edge contributes opposite signs. For a closed cycle γ, ⟨A+d₀λ,γ⟩=⟨A,γ⟩. These are balance and repair-invariance identities, not Noether’s theorem (WDP §5.12). Row 5 supplies J(x,y)=(−y,x): J²=−I and J⁴=I. With an admitted rational pairing g and g(Jx,y)=−g(x,Jy), WDP §17.9 derives the Q(i) action (a+ib)x=ax+bJx and Hermitian form h=g+i g(J·,·). J and its compatibility are inputs. Repeated direction is not elapsed time; rational turns complete to a circle, not the time line.'),
 ('6 · The extra structure for classical Hamilton',
 'Now supply a STATE plane with dimensionless conjugate coordinates q,p and area ω=dq∧dp. The two triangles form a patch of area 5.4; the shown shears preserve it. In rows 7–9 black is q, green is p; right/up are positive. Their right angle does not derive conjugacy. Assume a time-independent continuously differentiable flow preserves EVERY small oriented area: ∂q u+∂p v=0. Thus α=u dp−v dq is closed; on a simply connected patch α=dH, giving q̇=Hₚ and ṗ=−Hq. H is local, unique up to a constant. The sampled shears illustrate this hypothesis; they do not establish it for arbitrary flows.'),
 ('7 · A continuous rule makes the arrow turn',
 'Choose H=(q²+p²)/2, hence q̇=p and ṗ=−q simultaneously. Both rate panels show (2.1,1.2); orange rate lengths are 1.2 and 2.1 on the same scale, not successive kicks. The last panel shows exact states at t=0,0.5,1: q(t)=q₀ cos t+p₀ sin t, p(t)=p₀ cos t−q₀ sin t. It preserves H and ω. Smaller snapshots alone do not prove continuity or select a generator. This clockwise oscillator uses −J from row 5; reversing the orientation is explicit.'),
 ('8–9 · A different rule, its symmetry, and the Noether charge',
 'Switch to H=p²/2: Φt(q,p)=(q+tp,p). Translations Ta(q,p)=(q+a,p) preserve ω and H, and commute with Φt. Both orderings start at (2,0.65), use a=1.5, t=1, and end at (4.15,0.65); grey means shift, orange means slide. Row 9 is the unshifted run t=0,1,2. Translation pairs with ω to give dp, so its charge is p; ṗ=−Hq=0. For S=∫(pq̇−H)dt, independent interior variations with δq=0 at endpoints give Hamilton’s equations. Constant translations preserve S and map endpoint data to translated data. Noether conservation holds on stationary trajectories; equal marks alone do not prove it.'),
 ('The separate algebraic Hamiltonian route and remaining limits',
 'WDP §19A.6 starts instead with K=Q(i), matrix multiplication, an adjoint and a K-linear derivation δ satisfying Leibniz and the adjoint law. S=Σⱼδ(Eⱼ₁)E₁ⱼ gives δ=[S,·]; after skew-adjoint adjustment, H₀=iS gives δ=−i[H₀,·], unique modulo rational scalar identity. This constructs an algebraic generator, not a clock or flow, and is distinct from row 6’s classical theorem. Neither route selects physical energy from marks. The sheets do not derive the Born rule, Everett, Bell, a unique Hilbert geometry or physical laws. Novice comprehension remains untested.')]

def make_math():
 fig=b.plt.figure(figsize=(11.69,16.54),facecolor='white')
 fig.text(.065,.96,'Mathematics and assumptions',fontsize=20,color=B,weight='bold')
 fig.text(.065,.936,'Companion to the nine picture strips · constructions and their added premises',fontsize=10,color=G)
 y=.904
 for title,body in b.BLOCKS:
  fig.text(.065,y,title,fontsize=11.2,color=G,weight='bold',va='top');y-=.021
  lines=b.textwrap.wrap(body,width=122)
  fig.text(.065,y,'\n'.join(lines),fontsize=9.8,color=B,va='top',linespacing=1.32)
  y-=len(lines)*.01085+.017
 if y<.025:raise ValueError(f'overflow {y}')
 return fig

b.make_pictures=make_pictures;b.make_math=make_math
if __name__=='__main__':b.main()
