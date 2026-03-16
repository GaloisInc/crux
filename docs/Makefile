# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
MIR_JSON	  = ../deps/mir-json
RUSTDOCS	  = "$(BUILDDIR)/html/rust-doc"

# Put it first so that "make" without argument is like "make help".
help: setup
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile setup rust-docs

setup:
	python3 -m venv venv && \
		. ./venv/bin/activate && \
		pip install sphinx && \
		pip install sphinx_rtd_theme && \
		pip install sphinx-design && \
		pip install sphinx_copybutton && \
		cd "$(MIR_JSON)" && cargo build --release
		
rust-docs:
	D="$$PWD/$(BUILDDIR)/rust-docs" && \
		mkdir -p "$$D" && \
		pushd "$(MIR_JSON)" && \
		./target/release/mir-json-translate-libs --docs --out-dir "$$D" && \
		popd && cp -r "$$D/rlibs/doc" "$(RUSTDOCS)" && rm -rf "$$D"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@. ./venv/bin/activate && $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)