LINTER = flake8
PYTESTFLAGS = -vv --verbose --tb=short

FORCE:

docs: $(DOCFILES)

%.py: FORCE
	pytest -s tests/test_$*.py

%.html: %.py
	pydoc3 -w ./$<
	git add $@

tests: lint unit

unit: FORCE
	pytest $(PYTESTFLAGS)

lint: FORCE
	$(LINTER) *.py
