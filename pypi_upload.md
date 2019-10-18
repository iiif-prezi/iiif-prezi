# Updating iiif-prezi on pypi

Notes to remind @zimeon...

  * master copy of code is https://github.com/iiif-prezi/iiif-prezi
  * on PyPi iiif-prezi is at <https://pypi.org/project/iiif-prezi/>

Putting up a new version
------------------------

  0. Bump version number working branch in `iiif_prezi/_version.py`
  1. Check all tests good (`python setup.py test`)
  2. Check code is up-to-date with master github version
  3. Check out master and merge in working branch
  4. Check all tests good (`python setup.py test`)
  5. Check branches are as expected (`git branch -a`)
  6. Check local build and version reported OK (`python setup.py build; python setup.py install`)
  7. Upload new version to pypi using Python 3.x:

    ```
    pip install --upgrade setuptools wheel twine
    python setup.py sdist bdist_wheel
    ls dist
    twine upload dist/*
    ```

  8. Check on PyPI at <https://pypi.org/project/iiif-prezi/>

