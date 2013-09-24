#


T1 = bench
T2 = report

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
	pdflatex $(T2).tex                


# frozen xmldesign.pdf was taken from the ../admit/ directory
final-report.pdf:  report.pdf  bench.pdf xmldesign.pdf
	pdftk report.pdf bench.pdf xmldesign.pdf cat output final-report.pdf
	@echo A new final-report.pdf was created, 
	@echo the version sent to NRAO was called Mundy-report.pdf

final:	final-report.pdf

