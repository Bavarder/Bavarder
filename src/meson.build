pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'bavarder')
gnome = import('gnome')

python = import('python')

configure_file(
  input: 'bavarder.in',
  output: 'bavarder',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

bavarder_sources = [
  '__init__.py',
  'main.py',
]

PY_INSTALLDIR.install_sources(bavarder_sources, subdir: moduledir)

subdir('providers')
subdir('views')