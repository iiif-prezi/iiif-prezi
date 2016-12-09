# Updating iiif-prezi on pypi

Notes to remind @zimeon...

iiif-prezi is at <https://pypi.python.org/pypi/iiif-prezi>

Putting up a new version
------------------------

  0. Bump version number working branch in `iiif_prezi/_version.py`
  1. Check all tests good (`python setup.py test`)
  2. Check code is up-to-date with github version
  3. Check out master and merge in working branch
  4. Check all tests good (`python setup.py test`)
  5. Make sure master README has correct travis-ci and coveralls icon links for master branch (`?branch=master`)
  6. Check branches are as expected (`git branch -a`)
  7. Check local build and version reported OK (`python setup.py build; python setup.py install`)
  8. Upload new version to pypi:

    ```
    python setup.py sdist upload
    ```

  9. Check on PyPI at <https://pypi.python.org/pypi/iiif-prezi>


