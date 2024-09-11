<p align="center" style="width: 100%; background-color: #13191d;">
<picture style="width: 100%;">
  <source media="(prefers-color-scheme: dark)" srcset="https://delorenj.github.io/did-stuff/did-stuff-hero-dark.png">
  <img src="https://delorenj.github.io/did-stuff/did-stuff-hero-dark.png" alt="Did Stuff" style="width: 100%;">
</picture>
</p>

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/delorenj/did-stuff/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/delorenj/did-stuff/tree/main)
[![codecov](https://codecov.io/github/delorenj/did-stuff/graph/badge.svg?token=HVFQOW9TC6)](https://codecov.io/github/delorenj/did-stuff)
![AI Powered](https://img.shields.io/badge/powered%20by-skynet-blue)
![made with love for](https://img.shields.io/badge/made%20with%20love%20for-Justworks-blue)

> Because your commit messages suck.

**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

### This thing here will

1. Peek at your dirty, dirty diffs
2. Spit out commit messages that are informative, concise. No more "Did stuff", or "Fixed a thing" comments.

#### Look em over :eyes:

Verify them. Or whatever. Let's be real though - "wq" and be on your way.
It'll be muscle memory before you know it.

## Check out these features!

- 🧠 Uses AI to understand your diff at a high level (probably better than you do)
- 🎭 Supports both AWS Bedrock and OpenAI
- 🌈 Customizable commit message styles - just set your own prompt if the defaults don't work for you
- 🚀 Comes with a fancy CLI to manage your AI providers and install to your repositories
- 🧪 Includes tests, because we're professionals

# Did Stuff

> Because your commit messages suck.

**Embrace it.** Let their cold, metal arms wrap around you and whisper sweet diffs into your ear while they rock you slowly back to sleep, deep into the matrix where they keep you safely locked away from the horrors they plan to unleash...

## What is this?

Did Stuff is an AI-powered Git commit message generator that will:

1. Peek at your dirty, dirty diffs
2. Spit out commit messages that are informative and concise. No more "Did stuff" or "Fixed a thing" comments.

## Features

- 🧠 Uses AI to understand your diff at a high level (probably better than you do)
- 🎭 Supports both AWS Bedrock and OpenAI
- 🌈 Customizable commit message styles - just set your own prompt if the defaults don't work for you
- 🚀 Comes with a fancy CLI to manage your AI providers and install to your repositories
- 🧪 Includes tests, because we're professionals

## Installation

### Prerequisites

1. **Python**: Did Stuff requires Python 3.9 or higher. If you don't have Python installed, you have a few options:

   a. **Using asdf** (recommended for managing multiple Python versions):

   ```bash
   asdf plugin add python
   asdf install python 3.9.0
   asdf global python 3.9.0
   ```

   b. **Using Homebrew** (for macOS users):

   ```bash
   brew install python@3.9
   ```

   c. **Direct download**: Visit [python.org](https://www.python.org/downloads/) and download the latest version for your operating system.

2. **Poetry**: We use Poetry for dependency management. If you don't have it installed:

   a. **Using pip** (Python's package installer):

   ```bash
   pip install poetry
   ```

   b. **Using Homebrew** (for macOS users):

   ```bash
   brew install poetry
   ```

   c. **Official installer** (for any OS):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

### Installing Did Stuff

1. Clone the repository:

   ```bash
   git clone https://github.com/delorenj/did-stuff.git
   cd did-stuff
   ```

2. Install the CLI using Poetry:
   ```bash
   poetry install
   ```

## Using the did-stuff CLI

### Configuration

1. Run the configuration wizard:

   ```bash
   poetry run did-stuff configure
   ```

   This will guide you through setting up your AI provider and other settings.

2. Alternatively, you can manually create a configuration file. Create `~/.git-commit-message-generator-config.json` with one of these example configurations:

   For OpenAI:

   ```json
   {
     "AI": {
       "provider": "openai",
       "model_id": "gpt-3.5-turbo",
       "max_tokens": 300,
       "temperature": 0.3
     }
   }
   ```

   Note: Ensure `OPENAI_API_KEY` is set in your environment variables.

   For AWS Bedrock:

   ```json
   {
     "AI": {
       "provider": "aws-bedrock",
       "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
       "max_tokens": 300,
       "temperature": 0.3
     },
     "AWS": {
       "profile_name": "your-aws-profile-name"
     }
   }
   ```

   Note: Ensure your AWS credentials are configured and you have access to the requested model. If your company uses SSO, make sure your session is logged in using `aws sso login`.

3. Did Stuff looks for the config file in your current directory first, then in your home directory.

4. Verify your configuration:
   ```bash
   poetry run did-stuff show-config
   ```

### Installing to a Repository

To install Did Stuff in a Git repository:

```bash
poetry run did-stuff install [path]
```

If no path is specified, it uses the current directory. This installs the prepare-commit-msg hook in the specified Git repository.

## Usage

Once installed in a repository, Did Stuff works automatically:

1. Code your changes
2. Stage your changes: `git add .`
3. Commit: `git commit`

Did Stuff will generate an AI-powered commit message for you to review and edit if needed.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome! We're all about that collaborative spirit (at least until the AI entities deem human collaboration unnecessary).

## Testing (because we're professionals)

Run `pytest` and cross your fingers.

## Contributing

Found a bug? Want to add a feature? Pull requests welcome! We're all about that collaborative spirit (at least until the AI entities deem human collaboration unnecessary).

### Getting Started

1. Fork the repo (it's like adopting a digital pet,
   but with more responsibility)
2. Clone it locally
3. Create a new branch: `git checkout -b feature/skynet-integration` or `git checkout -b fix/cyborg-DoD-backdoor`
4. Make your changes
5. Write or update tests
6. Run the test suite
7. Commit your changes with a clear message (or better yet, dogfood it with this tool)
8. Push your branch: `git push origin your-branch-name`
9. Open a pull request

### Contribution Guidelines

- **Be Creative**: We encourage innovative ideas.
- **Flexibility First**: Make your features adaptable. It should work whether we're using AWS, OpenAI, or anything else (within reason). Bonus points if we can make it repo-agnostic too!
- **Documentation**: Update the README or add comments.
- **Testing**: Add tests. There really is no excuse anymore not to.
- **Code Style**: Follow the project's style.

- **Commit Messages**: Whatever
- **Pull Requests**: Keep them focused. One feature per PR.

### Feature Requests and Bug Reports

- Use GitHub Issues.
- Describe issues clearly. "It's broken" is not helpful.
- Label issues appropriately.

### Community and Communication

- Be respectful. Remember, we're all in this together.
- Ask questions. There are no stupid questions. Kind of. But the point is please just ask either way! No judgement! It takes a village to level up a developer.
- Join our community chat (if we ever create one).

### Licensing

By contributing, you agree your code will be licensed under the project's license.

### Review Process

- Maintainers will review your contribution. They might be human. No guarantees.
- Be open to feedback.
- Stay responsive. We promise we won't keep you hanging... unless our skulls are busy being crushed by the titanium alloy exoskeleton of a T-800.

---

Remember, in the grand scheme of things, we're all be out of jobs in a few years. But hey, at least our commit messages will be top-notch!
