# Contributing to Cognitive Engine

Thank you for your interest in contributing to the Cognitive Engine! This document outlines the guidelines and requirements for contributing to the project.

## Contributor License Agreement (CLA)

By contributing to the Cognitive Engine project, you agree to the following terms:

### Grant of License

You hereby grant to the Cognitive Engine project maintainers and their successors a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute your contributions and such derivative works.

### Patent License

You hereby grant to the Cognitive Engine project maintainers and their successors a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer your contributions, where such license applies only to those patent claims licensable by you that are necessarily infringed by your contributions alone or by combination of your contributions with the work to which such contributions were submitted.

### Representation

You represent that you are legally entitled to grant the above licenses. If your employer(s) has rights to intellectual property that you create that includes your contributions, you represent that you have received permission to make contributions on behalf of that employer, that your employer has waived such rights for your contributions, or that your employer has executed a separate Contributor License Agreement.

### Disclaimer

You provide your contributions on an "AS IS" basis, without warranties or conditions of any kind, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing your contributions and assume any risks associated with your exercise of permissions under this Agreement.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find that the bug has already been reported. When creating a bug report, please include as many details as possible:

- **Description**: A clear and concise description of what the bug is
- **Reproduction Steps**: Steps to reproduce the behavior
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: 
  - OS: [e.g. Ubuntu 20.04, Windows 10, macOS 12]
  - Python version: [e.g. 3.9, 3.10]
  - Cognitive Engine version: [e.g. v1.0.0]

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Description**: A clear and concise description of the enhancement
- **Motivation**: Why would this enhancement be useful?
- **Use Cases**: Specific use cases where this enhancement would be beneficial
- **Alternatives**: Any alternative solutions or features you've considered

### Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style guidelines in [DEVELOPMENT.md](pages/DEVELOPMENT.md)
3. **Write tests** for your changes
4. **Ensure all tests pass** (`pytest`)
5. **Update documentation** as needed
6. **Commit your changes** with a clear message following conventional commits format
7. **Push to your fork** and submit a pull request

### Code Review Process

All pull requests must be reviewed and approved by maintainers before merging. The review process may include:

- Code style checks (Black, flake8)
- Test coverage requirements
- Documentation review
- Security review for sensitive changes
- Architecture review for significant changes

## Code Style Guidelines

Please follow the code style guidelines outlined in [DEVELOPMENT.md](pages/DEVELOPMENT.md):

- Use Black for code formatting (120 character line length)
- Use flake8 for linting
- Include type hints for all functions
- Write Google-style docstrings
- Follow naming conventions (PascalCase for classes, snake_case for functions)

## Development Guidelines

### Testing

All contributions must include appropriate tests:

- Unit tests for new functions/classes
- Integration tests for new features
- Update existing tests if behavior changes
- Maintain test coverage above 80%

### Documentation

Update the following documentation as needed:

- [README.md](pages/README.md) for user-facing changes
- [API.md](pages/API.md) for API changes
- [ARCHITECTURE.md](pages/ARCHITECTURE.md) for architectural changes
- [DEVELOPMENT.md](pages/DEVELOPMENT.md) for development process changes

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Example:
```
feat(generator): add thought refinement capability

Add ability to refine thoughts based on identified weaknesses.
This improves the quality of generated thoughts over iterations.

Closes #123
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Communication

- Be clear and concise in your communications
- Use GitHub issues for bugs and feature requests
- Use discussions for questions and general topics
- Be patient with maintainers and other contributors

## Getting Started

### Setting Up Development Environment

See [DEVELOPMENT.md](pages/DEVELOPMENT.md) for detailed setup instructions.

### First Contribution

For your first contribution, we recommend:

1. Start with documentation improvements
2. Fix a simple bug labeled "good first issue"
3. Add a small enhancement
4. Review existing pull requests to understand the process

## Recognition

Contributors who make significant contributions will be recognized in:

- The project's CONTRIBUTORS file
- Release notes for their contributions
- Project documentation

## License

By contributing to the Cognitive Engine, you agree that your contributions will be licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Questions?

If you have questions about contributing:

- Check existing GitHub issues and discussions
- Review the [API documentation](pages/API.md)
- Review the [architecture documentation](pages/ARCHITECTURE.md)
- Create a GitHub discussion for your question

## Additional Resources

- [Development Guide](pages/DEVELOPMENT.md)
- [API Documentation](pages/API.md)
- [Architecture Documentation](pages/ARCHITECTURE.md)
- [Deployment Guide](pages/DEPLOYMENT.md)

Thank you for contributing to the Cognitive Engine!
