# Setup environment
# source /afs/slac/g/reseng/rogue/master/setup_env.csh
# source /afs/slac/g/reseng/rogue/v2.2.0/setup_env.csh
# source /afs/slac/g/reseng/rogue/master/setup_env.csh
source rogue/setup_template.csh

# Package directories
setenv SURF_DIR   ${PWD}/../firmware/submodules/surf/python
setenv AXI_DIR   ${PWD}/../firmware/submodules/axi-pcie-core/python

# Setup python path
setenv PYTHONPATH ${PWD}/python:${SURF_DIR}:${AXI_DIR}:${PYTHONPATH}
