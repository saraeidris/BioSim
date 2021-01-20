
from setuptools import setup

setup(name='BioSim',
      version='0.1',
      description='A simulation of the ecosystem on Rossum Island.',
      author='Sara E Idris, Thorbjørn L Onsaker, NMBU',
      author_email='said@nmbu.no, thon@nmbu.no',
      requires=['numpy', 'matplotlib', 'scipy', 'pytest'],
      packages=['biosim'],
      scripts=['examples/check_sim_disease.py', 'examples/herbivores_one_cell.py',
               'examples/one_cell_both_species.py', 'examples/migration_test.py'])
