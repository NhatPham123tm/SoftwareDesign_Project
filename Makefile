LATEX=pdflatex
TEXFILE=output/filled_template.tex
OUTFILE=output/document.pdf

all: pdf

pdf:
	mkdir -p output
	$(LATEX) -output-directory=output $(TEXFILE)
