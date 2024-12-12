# Cursion CLI (command line interface)

![Static Badge](https://img.shields.io/badge/CLI-Available-mint)

This is the CLI repo for the Cursion API, an error detection service designed to run front-end tests on web applications.

Copyright © Cursion 2024

### Usage
> Reference <a target="_blank" href="https://docs.cursion.dev/guides/cli.html">Cursion Docs</a> for usage instructions

---

### Installation
```shell
pip install cursion
```

### Basic Setup
```shell
cursion setup
cursion check
```

---

## Docker CLI Image

This docker image provides easy access to the CLI and priorities single use commands for simple integration with CI/CD tools


### Usage

```shell
docker run cursiondev/cli test-site \ 
    <site-id> \
    --threshold 85 \
    --max-wait-time 120 \
    --api-key <api_key> 
```

**For a full list of commands:**

```shell
docker run cursiondev/cli --help
```

### LICENSE
```license
The MIT License

Copyright (c) Cursion.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

# Support
Please open [issues in Github](https://github.com/Cursion-dev/cli/issues) or send questions to [Cursion support](mailto:hello@cursion.dev)