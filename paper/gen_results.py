"""Paper results generator: (1) modified-wavenumber (Fourier) analysis of the
derivative operators, (2) deformational-benchmark comparison incl. a 3rd-order
upwind (OE-1998 class). Writes paper/results.md."""
import sys, numpy as np
sys.path.insert(0,"/Users/sankar/projects/tb_science/compact-advection-diffusion/_dev")
import advdiff as A, sharp as Sh, bp_compact as BP

# ---------- (1) modified wavenumber k'(k)*h vs k*h ----------
def modwave(kh):
    s=np.sin; c=np.cos
    return {
      "central2": s(kh),
      "central4": (8*s(kh)-s(2*kh))/6,
      "central6": (45*s(kh)-9*s(2*kh)+s(3*kh))/30,
      "compact4": 1.5*s(kh)/(1+0.5*c(kh)),
      "compact6": ((14/9)*s(kh)+(1/9)/2*s(2*kh))/(1+(2/3)*c(kh)),
      "exact": kh,
    }
def resolving_kh(name):  # largest kh where |k'h-kh|/pi < 0.01  (resolving efficiency)
    g=np.linspace(1e-3,np.pi,2000); best=0
    for kh in g:
        if abs(modwave(kh)[name]-kh)/np.pi < 0.01: best=kh
        else: break
    return best/np.pi  # as fraction of pi

# ---------- (2) deformational benchmark: slotted cylinder, advection-dominated ----------
def upwind3(c,vel,h,axis):
    a=np.moveaxis(c,axis,-1); p=np.pad(a,((0,0),(2,2)),mode="reflect")
    back=(2*p[:,3:-1]+3*p[:,2:-2]-6*p[:,1:-3]+p[:,:-4])/(6*h)        # u>0 (3rd-order upwind)
    fwd =-(2*p[:,1:-3]+3*p[:,2:-2]-6*p[:,3:-1]+p[:,4:])/(6*h)        # u<0
    back=np.moveaxis(back,-1,axis); fwd=np.moveaxis(fwd,-1,axis)
    return np.where(vel>=0,back,fwd)

def solve_uw3(N,T,tc,dt,**ick):
    x=np.linspace(0,1,N); h=x[1]-x[0]; X,Y=np.meshgrid(x,x); c=Sh.slotted_cylinder(X,Y,**ick)
    nst=int(round(tc/dt)); dt=tc/nst
    def rhs(c,t):
        u,v=A.velocity(X,Y,t,T); return -(u*upwind3(c,u,h,1)+v*upwind3(c,v,h,0))
    for n in range(nst):
        t=n*dt
        k1=rhs(c,t);k2=rhs(c+.5*dt*k1,t+.5*dt);k3=rhs(c+.5*dt*k2,t+.5*dt);k4=rhs(c+dt*k3,t+dt)
        c=c+dt/6*(k1+2*k2+2*k3+k4)
    return c,h

N=129;T=3.0;tc=1.5;dt=0.004
R=Sh.exact_reference(N,T,tc); hh=1/(N-1)
def met(c):
    l2=np.sqrt(np.sum((c-R)**2)/np.sum(R**2)); a=c>0.5;b=R>0.5
    return l2,c.min(),c.max(),(a&b).sum()/max((a|b).sum(),1),c.sum()*hh*hh
rows=[]
for nm,fn in [("upwind-1",lambda:BP.solve(N,T,tc,0,dt,"upwind")[0]),
              ("upwind-3 (OE-98)",lambda:solve_uw3(N,T,tc,dt)[0]),
              ("compact-4 (plain)",lambda:BP.solve(N,T,tc,0,dt,"compact")[0]),
              ("BP-compact (ours)",lambda:BP.solve_bpf(N,T,tc,0,dt)[0])]:
    l2,mn,mx,iou,mass=met(fn()); rows.append((nm,l2,mn,mx,iou,mass))

lines=["# Paper results (auto-generated)\n","## 1. Modified-wavenumber resolving efficiency",
  "(largest k·h, as fraction of π, where the modified wavenumber matches the true one within 1%)\n",
  "| scheme | resolving k·h / π |","|---|---|"]
for nm in ("central2","central4","central6","compact4","compact6"):
    lines.append(f"| {nm} | {resolving_kh(nm):.2f} |")
lines+=["","sample k'h vs kh:","| kh/π | central2 | central4 | compact4 | compact6 | exact |","|---|---|---|---|---|---|"]
for frac in (0.25,0.5,0.75,0.9):
    kh=frac*np.pi; m=modwave(kh)
    lines.append(f"| {frac:.2f} | {m['central2']:.2f} | {m['central4']:.2f} | {m['compact4']:.2f} | {m['compact6']:.2f} | {kh:.2f} |")
lines+=["","## 2. Deformational benchmark — slotted cylinder (advection-dominated, t=T/2, N=129)",
  "| scheme | rel L2 | min | max | IoU(>0.5) | mass |","|---|---|---|---|---|---|"]
for nm,l2,mn,mx,iou,mass in rows:
    lines.append(f"| {nm} | {l2:.3f} | {mn:+.3f} | {mx:.3f} | {iou:.3f} | {mass:.4f} |")
lines+=["",f"(exact reference mass = {R.sum()*hh*hh:.4f}; IC max = 1.0)"]
open("/Users/sankar/projects/tb_science/compact-advection-diffusion/paper/results.md","w").write("\n".join(lines))
print("\n".join(lines))
