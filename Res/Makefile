CO=xkubis03

all:
	latex $(CO).tex
	latex $(CO).tex
	dvips $(CO).dvi
	ps2pdf $(CO).ps

clean:
	rm -f *.dvi *.ps *.aux *.log *.out
	rm -f *.pdf
	rm -f *~

pack:
	tar czvf xkubis03-fit.tar.gz *.tex Makefile *.eps *.sty
