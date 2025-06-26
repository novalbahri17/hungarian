# Contributing to Hungarian Method Calculator

Terima kasih atas minat Anda untuk berkontribusi! Panduan ini akan membantu Anda memulai.

## 🚀 Quick Start

1. Fork repository ini
2. Clone fork Anda:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hungarian.git
   cd hungarian
   ```
3. Buat virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```bash
   python app/main.py
   ```

## 📋 Types of Contributions

### 🐛 Bug Reports
- Gunakan GitHub Issues
- Sertakan langkah reproduksi
- Berikan informasi environment (OS, Python version, browser)
- Sertakan screenshot jika memungkinkan

### ✨ Feature Requests
- Jelaskan use case yang jelas
- Berikan contoh implementasi jika ada
- Diskusikan di Issues sebelum mulai coding

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test improvements

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Commit Messages
Gunakan format conventional commits:
```
type(scope): description

feat(calculator): add matrix validation
fix(ui): resolve button alignment issue
docs(readme): update installation guide
test(hungarian): add edge case tests
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Branch Naming
```
feature/description
bugfix/description
docs/description
refactor/description
```

Contoh:
- `feature/matrix-export`
- `bugfix/calculation-error`
- `docs/api-documentation`

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_hungarian.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Writing Tests
- Add tests for new features
- Test edge cases
- Maintain good test coverage
- Use descriptive test names

Contoh:
```python
def test_hungarian_method_with_square_matrix():
    """Test Hungarian method with valid square matrix."""
    # Test implementation
    pass

def test_hungarian_method_with_invalid_input():
    """Test Hungarian method handles invalid input gracefully."""
    # Test implementation
    pass
```

## 📁 Project Structure

```
hungarian/
├── api/                 # Vercel entry point
├── app/                 # Main application
│   ├── main.py         # Flask app
│   ├── hungarian.py    # Algorithm implementation
│   ├── config.py       # Configuration
│   ├── utils.py        # Utility functions
│   └── templates/      # HTML templates
├── tests/              # Test files
├── data/               # Sample data
├── static/             # Static assets
└── docs/               # Documentation
```

## 🔄 Pull Request Process

1. **Before Starting**
   - Check existing issues and PRs
   - Discuss major changes in issues first
   - Ensure your idea aligns with project goals

2. **Development**
   - Create feature branch from `main`
   - Make small, focused commits
   - Write/update tests
   - Update documentation if needed

3. **Before Submitting**
   - Test your changes thoroughly
   - Run existing tests
   - Check code style
   - Update CHANGELOG if applicable

4. **Submitting PR**
   - Use descriptive title
   - Fill out PR template
   - Link related issues
   - Request review from maintainers

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🎯 Areas for Contribution

### High Priority
- Performance optimizations
- Mobile responsiveness improvements
- Error handling enhancements
- Test coverage improvements

### Medium Priority
- UI/UX improvements
- Additional export formats
- Algorithm visualizations
- Accessibility improvements

### Low Priority
- Code refactoring
- Documentation improvements
- Example additions
- Internationalization

## 📚 Resources

### Learning Resources
- [Hungarian Algorithm Explanation](https://en.wikipedia.org/wiki/Hungarian_algorithm)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Testing with pytest](https://docs.pytest.org/)

### Tools
- [Visual Studio Code](https://code.visualstudio.com/) with Python extension
- [Git](https://git-scm.com/) for version control
- [Postman](https://www.postman.com/) for API testing

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct

## ❓ Questions?

Jika ada pertanyaan:
1. Check existing documentation
2. Search existing issues
3. Create new issue with "question" label
4. Tag maintainers if urgent

---

**Happy Contributing! 🎉**