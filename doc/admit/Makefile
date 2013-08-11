#


T = admit
F = 

help:
	@echo no help

clean:
	rm -f $(T).ps $(T).pdf $(T).dvi $(T).log

all:	$(T).pdf

$(T).pdf: $(T).tex $(F)
	latex $(T).tex                
	dvips -t letter -o $(T).ps $(T).dvi
	ps2pdf14 $(T).ps
