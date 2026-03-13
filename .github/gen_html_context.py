import os, sys

# Run this script from one of the doc checkout dirs
# (e.g. docs/ci_build_out/DIR/docs})
#
# Arguments: owner/repository current_version

d = os.listdir('../..')
bldtgt = lambda n: os.path.join('/', sys.argv[1].split('/')[1], n, 'index.html')

html_context={'current_version': sys.argv[2],
              'versions':sorted([(v, bldtgt(v)) for v in d if not v.startswith('PR_')]),
              'pull_reqs':sorted([(v, bldtgt(v)) for v in d if v.startswith('PR_')])}

print('html_context=',html_context)
