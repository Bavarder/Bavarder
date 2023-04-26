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
  configuration: configuration_data({
    'APP_ID': APPLICATION_ID,
    'RELEASE_VER': meson.project_version(),
    'VERSION': meson.project_version() + VERSION_SUFFIX,
    'BUILD_TYPE': get_option('buildtype'),
    'PROJECT_URL': PROJECT_URL,
    'DATA_DIR': conf.get('DATA_DIR'),
    'PKGDATA_DIR': PKGDATA_DIR,
    'LOCALE_DIR': conf.get('LOCALE_DIR'),
  }),
  install: true,
  install_dir: moduledir
)

bavarder_sources = [
  '__init__.py',
  'main.py',
  'preferences.py',
  'window.py',
]

PY_INSTALLDIR.install_sources(bavarder_sources, subdir: moduledir)
