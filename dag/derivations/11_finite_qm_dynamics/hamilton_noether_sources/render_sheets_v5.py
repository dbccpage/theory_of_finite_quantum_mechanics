from pathlib import Path
import importlib.util
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('v4',ROOT/'render_sheets_v4.py')
v4=importlib.util.module_from_spec(spec);spec.loader.exec_module(v4)
b=v4.b;b.VERSION='v5'
b.CAPS[1][2]='Reverse the joined step.\nYou return.'
updates={
 'Repeated direction is not elapsed time; rational turns complete to a circle, not the time line.':
 'Four quarter-turns give only four positions. Admitting ALL rational turns adds Q/Z; its completion in a supplied circle metric is R/Z, not the time line.',
 'Assume a time-independent continuously differentiable flow preserves EVERY small oriented area: ∂q u+∂p v=0. Thus α=u dp−v dq is closed; on a simply connected patch α=dH, giving q̇=Hₚ and ṗ=−Hq.':
 'Supply a time-independent C¹ vector field X(q,p)=(u,v): u=q̇ and v=ṗ are continuously differentiable instantaneous rates. Assume its local flow preserves EVERY small oriented area. Then ∂q u+∂p v=0, so α=u dp−v dq is closed. On a simply connected patch (no holes), α=dH gives q̇=Hₚ and ṗ=−Hq.',
 'WDP §19A.6 starts instead with K=Q(i), matrix multiplication, an adjoint and a K-linear derivation δ satisfying Leibniz and the adjoint law. S=Σⱼδ(Eⱼ₁)E₁ⱼ gives δ=[S,·]; after skew-adjoint adjustment, H₀=iS gives δ=−i[H₀,·], unique modulo rational scalar identity.':
 'WDP §19A.6 instead supplies the FULL algebra M_d(Q(i)), its conjugate-linear adjoint, and a Q(i)-linear map δ with δ(AB)=δ(A)B+Aδ(B) and δ(A†)=δ(A)†. S=Σⱼδ(Eⱼ₁)E₁ⱼ gives δ=[S,·]. Replace S by (S−S†)/2; H₀=iS then satisfies H₀†=H₀ and δ=−i[H₀,·], unique modulo rational scalar identity.'}
for old,new in updates.items():
 assert any(old in text for _,text in b.BLOCKS),old
 b.BLOCKS=[(title,text.replace(old,new)) for title,text in b.BLOCKS]

def pictures():
 fig=v4.make_pictures()
 panels=[ax for ax in fig.axes if tuple(ax.get_xlim())==(0.,9.)]
 ax=panels[5]
 for artist in list(ax.lines)+list(ax.patches):artist.remove()
 # Same diagonal as the preceding resultant; both opposing heads remain exposed.
 v4.arrow(ax,(2.4,.5),(5.7,2.65),v4.O,lw=3,head=.38)
 v4.arrow(ax,(5.7,2.65),(2.4,.5),v4.G,lw=1.4,head=.38)
 return fig

b.make_pictures=pictures
if __name__=='__main__':b.main()
