# Onyx Local Development

## Fist run



#### Backend: Python requirements

1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create python 3.11 virtal environment, OUTSIDE OF THE PROJECT FOLDER (onyx recommendation):

```bash
uv venv --python 3.11

# in wsl:
source .venv/bin/activate
```

3. Install python dependencies:

```bash
uv pip install -r danibot-onyx/backend/requirements/default.txt
uv pip install -r danibot-onyx/backend/requirements/dev.txt
uv pip install -r danibot-onyx/backend/requirements/model_server.txt
```

4. Install Playwright for Python (headless browser required by the Web Connector)

```bash
playwright install
```

#### Frontend dependencies

```bash
cd danibot-onyx/web
npm i
```

### Open IDE in danibot-onyx directory


1. **Environment Setup**:
   - Copy `.vscode/.env.template` to `.vscode/.env`
   - Fill in the necessary environment variables in `.vscode/.env`
2. **launch.json**:
   - Copy `.vscode/launch.template.jsonc` to `.vscode/launch.json`

## Using the Debugger

Before starting, make sure the Docker Daemon is running.


1. Open the Debug view in VSCode (Cmd+Shift+D on macOS)
2. From the dropdown at the top, select "Clear and Restart External Volumes and Containers" and press the green play button
3. From the dropdown at the top, select "Run All Onyx Services" and press the green play button
<!-- 4. CD into web, run "npm i" followed by npm run dev. -->
5. Now, you can navigate to onyx in your browser (default is http://localhost:3000) and start using the app
6. You can set breakpoints by clicking to the left of line numbers to help debug while the app is running
7. Use the debug toolbar to step through code, inspect variables, etc.

> If debug scripts fail, remeber to select the right python interpreter"
> in vscode/cursor command line find `>Python: Select Interpreter` and choose your venv

## Features

- Hot reload is enabled for the web server and API servers
- Python debugging is configured with debugpy
- Environment variables are loaded from `.vscode/.env`
- Console output is organized in the integrated terminal with labeled tabs