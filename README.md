# PV Simulator Challenge

An application which, among other tasks, generates simulated PV (photovoltaic)
power values (in kW).

## Getting Started

### Dependencies

- Python `2.7`, `3.3`, `3.4`, `3.5`, `3.6` or PyPy
- RabbitMQ

### Makefile

The project includes a `Makefile` to automate tasks.

List available targets with:

```bash
$ make list
```

## Installation

Make sure to create a new virtualenv before installing Python dependencies with:

```bash
$ make setup
```

Then run the tests:

```bash
$ make test
```

See how much of it is covered:

```bash
$ make coverage
```

Make sure it works with all supported Python versions:

```bash
$ make tox
```

## Running

#### Config

There's a `config.sample.toml` file as a reference, please make a copy or rename
it to `config.toml` and adapt it.

#### Run

After creating the configuration file, simply:

```bash
$ make run
```

## Docs

To generate documentation:

```bash
$ make docs
```

## License

[MIT][mit] © [Pablo Santiago Blum de Aguiar][author]

[mit]:             http://opensource.org/licenses/MIT
[author]:          https://github.com/scorphus
