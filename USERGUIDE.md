# 🖥️ Plagiarism Checker - Desktop Application

## Professional PC Application for Plagiarism Detection

A full-featured desktop application with a modern graphical interface for detecting plagiarism in documents. Similar to Turnitin, built as a native PC application.

![Application Type: Desktop GUI](https://img.shields.io/badge/Type-Desktop%20GUI-blue)
![Platform: Windows/Mac/Linux](https://img.shields.io/badge/Platform-Cross--Platform-green)
![Language: Python](https://img.shields.io/badge/Language-Python-yellow)

---

## 📋 Table of Contents

1. [Features](#features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [User Guide](#user-guide)
6. [Screenshots](#screenshots)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## ✨ Features

### Core Features
- ✅ **Modern Desktop GUI** - Professional, user-friendly interface
- ✅ **Multiple File Formats** - Support for DOCX, PDF, and TXT files
- ✅ **Drag & Drop** - Easy file selection
- ✅ **Real-time Analysis** - Background processing with progress indication
- ✅ **Visual Results** - Color-coded similarity scores
- ✅ **Detailed Reports** - Comprehensive plagiarism analysis
- ✅ **Export Capability** - Save reports as text files
- ✅ **Cross-Platform** - Works on Windows, macOS, and Linux

### Advanced Detection
- 🔍 **Cosine Similarity Analysis** - Advanced mathematical comparison
- 🔍 **Sequence Matching** - Finds exact and near-exact matches
- 🔍 **Multi-Source Detection** - Compares against multiple references
- 🔍 **Statistical Analysis** - Word count, match percentage, unique content

### User Experience
- 🎨 **Clean Interface** - Intuitive two-panel design
- 🎨 **Color-Coded Results** - Green (low), Orange (medium), Red (high)
- 🎨 **Instant Feedback** - Status bar and progress indicators
- 🎨 **Professional Reports** - Formatted export with recommendations

---

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Windows 7/10/11, macOS 10.12+, or Linux
- **Python**: Version 3.7 or higher
- **RAM**: 512 MB
- **Disk Space**: 50 MB
- **Display**: 1024x768 resolution

### Recommended
- **Python**: Version 3.9 or higher
- **RAM**: 2 GB
- **Display**: 1920x1080 resolution

### Required Software
- Python 3.7+ with Tkinter (usually included)
- pip (Python package manager)

### Optional Dependencies
- `python-docx` - For Microsoft Word (.docx) support
- `pypdf` or `pdfplumber` - For PDF file support

---

## 🚀 Installation

### Step 1: Check Python Installation

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Install Tkinter (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter is usually included with Python

**Windows:**
Tkinter is usually included with Python

### Step 3: Install Optional Dependencies

Run the setup script:

**Windows:**
```cmd
python setup.py
```

**macOS/Linux:**
```bash
python3 setup.py
```

Or manually install:
```bash
pip install python-docx pypdf pdfplumber --break-system-packages
```

---

## 🎯 Quick Start

### Option 1: Using Launch Scripts

**Windows:**
1. Double-click `run.bat`
2. The application window will open

**macOS/Linux:**
1. Open terminal in the application folder
2. Run: `./run.sh`
3. Or double-click the file if executable permissions are set

### Option 2: Direct Python Execution

**Windows:**
```cmd
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

---

## 📖 User Guide

### Main Interface

The application has two main panels:

**Left Panel - Document Input:**
- File upload area
- Text paste area
- Check button

**Right Panel - Results:**
- Similarity score (large percentage)
- Statistics (words, sources, unique content)
- Detailed match list
- Export button

### Step-by-Step Usage

#### 1. **Upload a Document**

**Method A: File Upload**
- Click "📁 Choose File" button
- Select your document (.txt, .docx, or .pdf)
- File name will appear below the button

**Method B: Paste Text**
- Click in the text area
- Paste or type your text (minimum 50 characters)

#### 2. **Run Analysis**

- Click "🔍 Check for Plagiarism" button
- Wait for analysis (usually 1-3 seconds)
- Status bar shows progress

#### 3. **Review Results**

**Similarity Score:**
- **0-15%** (Green) = Low similarity - Acceptable
- **15-30%** (Orange) = Moderate similarity - Review needed
- **30%+** (Red) = High similarity - Significant concern

**Statistics:**
- **Total Words** - Number of words analyzed
- **Sources Found** - Number of matching sources
- **Unique Content** - Percentage of original content

**Detailed Matches:**
- Lists each matching source
- Shows similarity percentage
- Displays matched text sequences
- Provides source URLs

#### 4. **Export Report**

- Click "💾 Export Report" button
- Choose save location
- Report saved as .txt file with:
  - Summary statistics
  - Interpretation
  - Detailed matches
  - Recommendations

### Understanding Results

#### Low Similarity (0-15%)
```
✓ Acceptable for academic submission
✓ Shows good citation practices
✓ Minimal revision needed
```

#### Moderate Similarity (15-30%)
```
⚠ Review highlighted matches
⚠ Check citation practices
⚠ Consider paraphrasing
```

#### High Similarity (30%+)
```
✗ Significant revision needed
✗ Review all matches carefully
✗ Ensure proper citations
✗ Rewrite highly similar sections
```

---

## 📸 Screenshots

### Main Application Window
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Plagiarism Checker                                      │
│  Advanced similarity detection for academic integrity       │
├──────────────────────┬──────────────────────────────────────┤
│  📄 Document Input   │  📊 Analysis Results                 │
├──────────────────────┼──────────────────────────────────────┤
│                      │                                      │
│  No file selected    │           45%                        │
│  [Choose File]       │     (Moderate Similarity)            │
│  [Clear]             │                                      │
│                      │  ┌────────┬────────┬────────┐       │
│  Or paste text:      │  │  281   │   3    │ 55.0%  │       │
│  ┌────────────────┐  │  │ Total  │Sources │Unique  │       │
│  │                │  │  │ Words  │ Found  │Content │       │
│  │                │  │  └────────┴────────┴────────┘       │
│  │                │  │                                      │
│  │                │  │  Detailed Matches:                   │
│  │                │  │  ━━ Match #1 ━━                     │
│  └────────────────┘  │  Source: Wikipedia                   │
│                      │  Similarity: 57.27%                  │
│  [Check Plagiarism]  │  • "academic integrity is..."        │
│                      │                                      │
│                      │  [Export Report]                     │
└──────────────────────┴──────────────────────────────────────┘
│ Ready                                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Application Won't Start

**Problem:** "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

**Problem:** "Python not found"
- Install Python from [python.org](https://www.python.org/)
- Make sure Python is in system PATH

#### 2. Cannot Read DOCX Files

**Solution:**
```bash
pip install python-docx --break-system-packages
```

#### 3. Cannot Read PDF Files

**Solution:**
```bash
pip install pypdf pdfplumber --break-system-packages
```

#### 4. Application Crashes on File Upload

**Check:**
- File is not corrupted
- File size is reasonable (< 10 MB)
- File format is supported (.txt, .docx, .pdf)

#### 5. Results Not Showing

**Try:**
- Ensure document has at least 50 characters
- Check status bar for error messages
- Restart the application

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Failed to read file" | File format issue | Check file is not corrupted |
| "Unsupported file format" | Wrong file type | Use .txt, .docx, or .pdf |
| "Analysis failed" | Processing error | Check file content is valid text |

---

## ❓ FAQ

### General Questions

**Q: Is this application free?**
A: Yes, completely free and open-source.

**Q: Does it require internet connection?**
A: No, all processing is done locally on your computer.

**Q: Is my data stored anywhere?**
A: No, all data stays on your computer. Nothing is uploaded.

**Q: Can I check multiple documents at once?**
A: Currently one document at a time. Check each separately.

### Technical Questions

**Q: What formats are supported?**
A: Text (.txt), Microsoft Word (.docx), and PDF (.pdf) files.

**Q: How accurate is the detection?**
A: Uses industry-standard algorithms (cosine similarity, sequence matching). Accuracy depends on the reference database.

**Q: Can I add my own reference documents?**
A: Yes, modify the `get_sample_database()` function in the code to add custom references.

**Q: What's the maximum file size?**
A: Recommended maximum is 10 MB. Larger files may slow down processing.

### Usage Questions

**Q: What similarity percentage is acceptable?**
A: Generally under 15% is acceptable, 15-30% needs review, over 30% is concerning.

**Q: Should I include citations in the check?**
A: Yes, but properly cited content should be reviewed differently than uncited matches.

**Q: Can this replace Turnitin?**
A: This is a local tool for initial checking. Institutional tools like Turnitin have larger databases.

---

## 🎓 Best Practices

### For Students

1. **Check Before Submission**
   - Run checks on draft versions
   - Review all flagged matches
   - Ensure proper citations

2. **Understand Results**
   - High similarity ≠ plagiarism if properly cited
   - Review context of matches
   - Paraphrase properly when needed

3. **Use as Learning Tool**
   - Understand what triggers detection
   - Improve paraphrasing skills
   - Learn proper citation practices

### For Educators

1. **Set Clear Standards**
   - Define acceptable similarity ranges
   - Explain proper citation requirements
   - Provide example documents

2. **Review Manually**
   - Don't rely solely on automated tools
   - Check context of matches
   - Verify citation quality

3. **Use for Education**
   - Teach students about plagiarism
   - Demonstrate detection tools
   - Encourage academic integrity

---

## 🔄 Updates and Support

### Getting Updates
Check for new versions by reviewing the source code repository.

### Reporting Issues
If you encounter bugs or have suggestions:
1. Document the issue clearly
2. Include error messages
3. Note your system details (OS, Python version)

### Contributing
Feel free to improve the code:
- Add new features
- Improve detection algorithms
- Enhance the user interface
- Add support for more file formats

---

## 📝 License

This tool is for educational purposes. Use responsibly and maintain academic integrity.

---

## 🙏 Acknowledgments

Built with:
- Python 3
- Tkinter (GUI)
- python-docx (Word support)
- pypdf/pdfplumber (PDF support)

---

## 📞 Quick Reference Card

### Keyboard Shortcuts
- `Ctrl+O` - Open file (if implemented)
- `Ctrl+E` - Export report (if implemented)
- `Ctrl+Q` - Quit application (if implemented)

### File Formats
- `.txt` - Always supported
- `.docx` - Requires python-docx
- `.pdf` - Requires pypdf or pdfplumber

### Similarity Ranges
- `0-15%` - ✅ Acceptable
- `15-30%` - ⚠️ Review
- `30%+` - ❌ Concern

### Support
- Read this guide first
- Check troubleshooting section
- Review FAQ

---

**Made with ❤️ for academic integrity**

Version 1.0 - Desktop Application
