;-----------------------------------------------------------------------------
; CLSTATS.PRO
;-----------------------------------------------------------------------------
; Find clump statistics from data cube and clump
; assignment cube as created by program clfind
;
; The output of the program is very generic for maximum flexibility.
; Because of the different units found in FITS headers, the output
; positions and sizes are in pixels. You can convert these to header
; variables using, e.g. x=crval1+(i-crpxi1)*cdelt1.
; Similarly, only the clump integrated intensity is given.
;
; 6/2/04  jpw   modified from dark ages version
;
; needs: clstats.cb      ; common block
; usage: .run,clstats    ; to compile all procedures
;-----------------------------------------------------------------------------
pro clstats,file=file,log=log
@clstats.cb
@header.cb

if NOT keyword_set(file) then begin
  print,'PROCEDURE clplot,file=filename'
  print,'-------------------------------------------------------'
  print,'filename = root name of the FITS data cube (in quotes)'
  print,'           assumes .fits and .fits.clf extensions'
  print,'/log       for screen output copied to clstats.log'
  print,'-------------------------------------------------------'
  return
endif

dfile=file+'.fits'
afile=file+'.fits.clf'
print,"------------------------------------------------------------------------"
print,"CLSTATS: ",systime()
print,"------------------------------------------------------------------------"
if keyword_set(log) then begin
  print,"Copying output to clstats.log"
  openw,1,'clstats.log'
  printf,1,"------------------------------------------------------------------------"
  printf,1,"CLSTATS: ",systime()
  printf,1,"------------------------------------------------------------------------"
endif

print,format='("Reading ",a0)',dfile
data=readfits(dfile,head,/silent)
readhd,head
nx=long(naxis1)
ny=long(naxis2)
nv=long(naxis3)
x0=crval1
y0=crval2
v0=crval3
if(n_elements(cdelt1) gt 0) then dx=cdelt1
if(n_elements(cd1_1) gt 0) then dx=cd1_1
if(n_elements(cdelt2) gt 0) then dy=cdelt2
if(n_elements(cd2_2) gt 0) then dy=cd2_2
if(n_elements(cdelt3) gt 0) then dv=cdelt3
if(n_elements(cd3_3) gt 0) then dv=cd3_3
i0=crpix1
j0=crpix2
k0=crpix3

print,format='("Reading ",a0)',afile
assign=readfits(afile,head,/silent)
; get clfind parameters
s=size(head)
nlines=s(1)
for i=0,nlines-1 do begin
  if (strpos(head(i),'level0') gt 0) then begin
    s=strmid(head(i),25,7)
    levs0=float(strtrim(s))
  endif
  if (strpos(head(i),'increment') gt 0) then begin
    s=strmid(head(i),27,7)
    dlevs=float(strtrim(s))
  endif
endfor
print,format='("Lowest contour level =",f6.2)',levs0
print,format='("Contour increment =",f6.2)',dlevs
if keyword_set(log) then begin
  printf,1,"Root filename = ",file
  printf,1,format='("Lowest contour level =",f6.2)',levs0
  printf,1,format='("Contour increment =",f6.2)',dlevs
endif
; mask out bad data (NaN replaced by -999.9)
bad=where(finite(data) eq 0,count)
if (count gt 0) then data(bad)=-999.9

print,"------------------------------------------------------------------------"
print," Ncl     x     y     v  Tpeak  FWHMx  FWHMy    R    FWHMv  Sum(T)  Npix"
print,"------------------------------------------------------------------------"
if keyword_set(log) then begin
  printf,1,"------------------------------------------------------------------------"
  printf,1," Ncl     x     y     v  Tpeak  FWHMx  FWHMy    R    FWHMv  Sum(T)  Npix"
  printf,1,"------------------------------------------------------------------------"
endif

; MAIN LOOP
ncl_tot=max(assign)
for ncl=1,ncl_tot do dostats,ncl,log=log
print,"------------------------------------------------------------------------"
if keyword_set(log) then begin
  printf,1,"------------------------------------------------------------------------"
  close,1
endif
return
end
;-----------------------------------------------------------------------------
pro dostats,ncl,log=log
; note that the sizes are no longer corrected for the beam size
; (on account of possible mismatch in units).
; Best to do this yourself later...
@clstats.cb

clump_pix=where(assign eq ncl,npix)
k=clump_pix/(nx*ny)
j=clump_pix/nx-k*ny
i=clump_pix-(j+k*ny)*nx
T=data(clump_pix)
; check to see if any pixel in the clump
; lie at the limits of the data cube
edge=0
ind=where(i eq nx-1 OR i eq 0,count)
if(count gt 0) then edge=1
ind=where(j eq ny-1 OR j eq 0,count)
if(count gt 0) then edge=edge+2
ind=where(k eq nv-1 OR k eq 0,count)
if(count gt 0) then edge=edge+4

; peak position
peak=max(T)
pos=where(data eq peak AND assign eq ncl)
k0=pos(0)/(nx*ny)
j0=pos(0)/nx-k0*ny
i0=pos(0)-(j0+k0*ny)*nx

; calculate clump integrated intensity, size, and velocity dispersion
sumT=total(T)
ibar=total(i*T)/sumT
jbar=total(j*T)/sumT
kbar=total(k*T)/sumT
sigi2=total(i*i*T)/sumT-ibar^2
sigj2=total(j*j*T)/sumT-jbar^2
sigk2=total(k*k*T)/sumT-kbar^2
if(sigk2 lt 0.0) then sigk2=0.0

; correction for beam
;unresol=0
;sigi2=sigi2-(bx/2.355)^2
;if(sigi2 gt 0.0) then sigi=sqrt(sigi2) else begin $
;    sigi=0.5*bx/2.355 & unresol=1 & endelse
;sigj2=sigj2-(by/2.355)^2
;if(sigj2 gt 0.0) then sigj=sqrt(sigj2) else begin $
;    sigj=0.5*by/2.355 & unresol=1 & endelse

; get clump size based on area on xy plane
area=intarr(nx,ny) & area(i,j)=1 & dummy=where(area eq 1,Nxy)
radius=sqrt(float(Nxy)/!pi)
;beamr=sqrt(2*bx*by*alog(peak/(nstart*inc)))/2.355
;if(radius gt beamr) then radius=sqrt(radius^2-beamr^2) else begin $
;    radius=0.5*beamr & unresol=1 & endelse

; make dispersions into FWHM
sx=2.355*sqrt(sigi2)
sy=2.355*sqrt(sigj2)
sv=2.355*sqrt(sigk2)
; FLAG clumps if they lie on an edge and/or are unresolved
flag=""
if(edge eq 1) then flag="X"
if(edge eq 2) then flag="Y"
if(edge eq 3) then flag="XY"
if(edge eq 4) then flag="V"
if(edge eq 5) then flag="XV"
if(edge eq 6) then flag="YV"
if(edge eq 7) then flag="XYV"
;if(unresol) then flag=flag+"U"
print,format='(i4,3(2x,i4),x,f8.2,4(2x,f5.2),x,f9.2,2x,i4,a4)',ncl,i0,j0,k0,peak,sx,sy,radius,sv,sumT,npix,flag
if keyword_set(log) then $
  printf,1,format='(i4,3(2x,i4),x,f8.2,4(2x,f5.2),x,f9.2,2x,i4,a4)',ncl,i0,j0,k0,peak,sx,sy,radius,sv,sumT,npix,flag

return
end
;-----------------------------------------------------------------------------
