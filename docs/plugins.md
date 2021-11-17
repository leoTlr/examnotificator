# Developing plugins

## flow
- poetry new examnotificator-<*your plugin name*>
- poetry add examnotificator
- `from examnotificator.fetchers import ExamFetcher, FetchingError, ParsingError`
    - base class for fetcher plugin, inherit from this
    - instruct the users of your plugin to add the necessary information for fetching in the config file of examnotificator
- edit pyproject.toml (`poetry install` afterwards): 
    - to tell poetry under which name to load your plugin. This will also 
    be the name that you pass the `--fetcher` cli argument
    - Use the namespace "examnotificator.fetchers.plugins"
- publish your plugin on PyPI
- create a pull request to add your plugin as optional dependency of examnotificator
