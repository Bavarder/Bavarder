gnome = import('gnome')

python = import('python')

blueprints = custom_target('blueprints',
  input: files(
    'gtk/help-overlay.blp',
    'views/preferences_window.blp',
    'views/window.blp',
    'widgets/thread_item.blp',
    'widgets/item.blp',
    'widgets/model_item.blp',
    'widgets/download_row.blp',
    'widgets/code_block.blp',
    'providers/provider_item.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@']
)

gnome.compile_resources('bavarder',
  'bavarder.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: PKGDATA_DIR,
  dependencies: blueprints
)

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
  install_dir: MODULE_DIR
)

bavarder_sources = [
  '__init__.py',
  'main.py',
  'threading.py'
]

PY_INSTALLDIR.install_sources(bavarder_sources, subdir: MODULE_DIR)

subdir('views')
subdir('widgets')
subdir('providers')