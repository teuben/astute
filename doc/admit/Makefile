#


T1 = admit
T2 = xmldesign

F = 

help:
	@echo no help

clean:
	rm -f $(T1).ps $(T1).pdf $(T1).dvi $(T1).log
	rm -f $(T2).ps $(T2).pdf $(T2).dvi $(T2).log

all:	$(T1).pdf $(T2).pdf

$(T1).pdf: $(T1).tex $(F)
	latex $(T1).tex                
	dvips -t letter -o $(T1).ps $(T1).dvi
	ps2pdf14 $(T1).ps

$(T2).pdf: $(T2).tex $(F)
	latex $(T2).tex                
	dvips -t letter -o $(T2).ps $(T2).dvi
	ps2pdf14 $(T2).ps
