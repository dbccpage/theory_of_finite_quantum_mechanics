"""Independent numerical verification of every equation used in the paper."""
import numpy as np
rng = np.random.default_rng(7)

def rand_c(): return rng.normal()+1j*rng.normal()
def ket(dim):
    v = rng.normal(size=dim)+1j*rng.normal(size=dim); return v/np.linalg.norm(v)

# 1. Cross term identity: |a+b|^2 = |a|^2+|b|^2+2Re(a* b)
for _ in range(1000):
    a,b = rand_c(), rand_c()
    assert np.isclose(abs(a+b)**2, abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b))
print("1. cross-term identity OK")

# 2. Detector-overlap formula: |Psi> = a|L>|dL> + b|R>|dR>, screen amplitude at x collapses to
#    vector  a|dL> + b|dR> in detector space; P = ||a dL + b dR||^2 = |a|^2+|b|^2+2Re(a* b <dL|dR>)
for _ in range(1000):
    a,b = rand_c(), rand_c()
    dL,dR = ket(4), ket(4)
    gamma = np.vdot(dL,dR)   # <dL|dR>
    P = np.linalg.norm(a*dL+b*dR)**2
    assert np.isclose(P, abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b*gamma))
print("2. detector-overlap formula OK  (P = |a|^2+|b|^2+2 Re(a* b <dL|dR>))")

# 2b. Same thing via the reduced density matrix (partial trace over detector):
#     rho_S = sum_ij c_i conj(c_j) <d_j|d_i> |i><j|  (QM_094 Thm 2.1 form), screen = projector onto (|L>+|R>)/sqrt2 etc.
for _ in range(300):
    a,b = rand_c(), rand_c(); n=np.sqrt(abs(a)**2+abs(b)**2); a/=n; b/=n
    dL,dR = ket(3), ket(3)
    psi = np.kron(np.array([1,0]), a*dL) + np.kron(np.array([0,1]), b*dR)   # |L>=e0,|R>=e1
    rho = np.outer(psi, psi.conj()).reshape(2,3,2,3)
    rhoS = np.einsum('ikjk->ij', rho)           # partial trace over detector
    g = np.vdot(dL,dR)
    expected = np.array([[abs(a)**2, a*np.conj(b)*np.conj(g)],[np.conj(a)*b*g, abs(b)**2]])
    # check: rhoS_{LR} = a conj(b) <dR|dL> = a conj(b) conj(g)
    assert np.allclose(rhoS, expected)
    # a screen point whose amplitude sums the two paths with weights (1,1): P = <+|rhoS|+> *2 with |+>=(1,1)/sqrt2
    plus = np.array([1,1])/np.sqrt(2)
    P_screen = 2*np.real(plus.conj()@rhoS@plus)
    assert np.isclose(P_screen, abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b*g))
print("2b. reduced-density-matrix route agrees (off-diagonal carries <dL|dR>)")

# 3. Limiting cases
a=b=1/np.sqrt(2)
for g,label in [(1,"indistinguishable"),(0,"orthogonal"),(0.5,"partial")]:
    phis=np.linspace(0,2*np.pi,721)
    P=[abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b*np.exp(1j*phi)*g) for phi in phis]
    V=(max(P)-min(P))/(max(P)+min(P))
    print(f"3. |<dL|dR>|={g}: {label:17s} visibility V={V:.3f}")
    assert np.isclose(V, g)

# 4. Englert: for equal-weight paths and pure marker states, V=|<dL|dR>|, D=sqrt(1-|<dL|dR>|^2) (trace distance), V^2+D^2=1
for _ in range(300):
    dL,dR = ket(5), ket(5)
    g=abs(np.vdot(dL,dR))
    rhoL=np.outer(dL,dL.conj()); rhoR=np.outer(dR,dR.conj())
    ev=np.linalg.eigvalsh(0.5*(rhoL-rhoR)); D=np.sum(np.abs(ev))   # trace distance = max which-way guessing bias
    assert np.isclose(D, np.sqrt(1-g**2)) and np.isclose(g**2+D**2,1)
print("4. Englert pure-marker case: V^2 + D^2 = 1 with V=|<dL|dR>|, D=sqrt(1-|<dL|dR>|^2) OK")

# 5. Hadamard interferometer (repo witness): weights identical before mixing, different after
H=np.array([[1,1],[1,-1]])          # unnormalized, as in lean4/InterferenceNonDescent.lean
for v,name in [((1,1),"(1,1)"),((1,-1),"(1,-1)")]:
    v=np.array(v); w=np.abs(v)**2; out=H@v; wout=np.abs(out)**2
    print(f"5. {name}: weights before mixing {tuple(w)}, after Hadamard mixing {tuple(wout)}")
# With a perfectly distinguishing marker the mixed readout no longer depends on the sign:
dL,dR=np.array([1,0]),np.array([0,1])
for v,name in [((1,1),"(1,1)"),((1,-1),"(1,-1)")]:
    psi = np.kron(np.array([1,0]), v[0]*dL)+np.kron(np.array([0,1]), v[1]*dR)   # path (x) marker
    out = np.kron(H,np.eye(2))@psi
    w0 = np.linalg.norm(out.reshape(2,2)[0])**2; w1=np.linalg.norm(out.reshape(2,2)[1])**2
    print(f"5m. marked {name}: readout after mixing = ({w0:.0f}, {w1:.0f})  (sign no longer readable)")
# Normalized form: P(0)= (1+Re(e^{i phi} <d0|d1>))/2
for phi in [0,np.pi/3,np.pi]:
    for g in [1,0.5,0]:
        assert np.isclose((1+np.real(np.exp(1j*phi)*g))/2, (1+g*np.cos(phi))/2)
print("5n. normalized two-output formula P(0) = (1 + Re(e^{i phi} <d0|d1>))/2 OK")

# 6. Sorkin-type: phase averaging over phi of the cross term gives the classical sum (unconditioned)
phis=np.linspace(0,2*np.pi,3601)[:-1]
print("6. mean over random phase of cross term:", np.round(np.mean(2*np.cos(phis)),12))

# 7. Eraser bookkeeping: orthogonal markers, condition on marker measured in basis (|d0>±|d1>)/sqrt2
a=b=1/np.sqrt(2); phis=np.linspace(0,2*np.pi,361)
for sgn,name in [(+1,'+'),(-1,'-')]:
    Pcond=[abs(a*1+ sgn*b*np.exp(1j*phi))**2/2 for phi in phis]   # joint prob with marker outcome ±
    print(f"7. eraser subset {name}: fringe P ranges {min(Pcond):.3f}..{max(Pcond):.3f}")
Ptot=[abs(a)**2+abs(b)**2 for phi in phis]
Psum=[abs(a+b*np.exp(1j*phi))**2/2+abs(a-b*np.exp(1j*phi))**2/2 for phi in phis]
assert np.allclose(Ptot,Psum)
print("7. the two conditional fringe sets are shifted by half a period and sum to the flat total: OK")
