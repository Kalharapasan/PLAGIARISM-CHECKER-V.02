#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import re
import math
from pathlib import Path
from typing import List, Dict
from collections import Counter
import difflib
import threading
from datetime import datetime

class PlagiarismEngine:
    def __init__(self):
        self.min_match_length = 5
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
            'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
            'some', 'any', 'no', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 's', 't', 'just', 'now'
        }
    
    def extract_text_from_txt(self, filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def extract_text_from_docx(self, filepath: str) -> str:
        try:
            from docx import Document
            doc = Document(filepath)
            return '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])
        except ImportError:
            import zipfile
            with zipfile.ZipFile(filepath) as docx:
                xml_content = docx.read('word/document.xml')
                text = re.sub(r'<[^>]+>', ' ', xml_content.decode('utf-8'))
                return ' '.join(text.split())
        
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        try:
            import pdfplumber
            text = []
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except ImportError:
            try:
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                return '\n'.join(text)
            except ImportError:
                raise Exception("PDF support requires pdfplumber or pypdf. Install with: pip install pdfplumber")
    
    
    def extract_text(self, filepath: str) -> str:
        ext = Path(filepath).suffix.lower()
        if ext == '.txt':
            return self.extract_text_from_txt(filepath)
        elif ext == '.docx':
            return self.extract_text_from_docx(filepath)
        elif ext == '.pdf':
            return self.extract_text_from_pdf(filepath)
        else:
            raise Exception(f"Unsupported file format: {ext}")
        
    def tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-z0-9]+\b', text.lower())
    
    def calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        freq1 = Counter(words1)
        freq2 = Counter(words2)
        
        all_words = set(freq1.keys()).union(set(freq2.keys()))
        vec1 = [freq1.get(word, 0) for word in all_words]
        vec2 = [freq2.get(word, 0) for word in all_words]
        
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return (dot_product / (magnitude1 * magnitude2)) * 100
    
    def find_common_sequences(self, text1: str, text2: str) -> List[Dict]:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        matcher = difflib.SequenceMatcher(None, words1, words2)
        matches = []
        
        for match in matcher.get_matching_blocks():
            if match.size >= self.min_match_length:
                matched_text = ' '.join(words1[match.a:match.a + match.size])
                matches.append({
                    'text': matched_text,
                    'length': match.size,
                    'position': match.a
                })
        
        return matches
    
    def check_plagiarism(self, text: str, database: List[Dict]) -> Dict:
        results = {
            'overall_similarity': 0,
            'total_words': len(self.tokenize(text)),
            'matches': []
        }
        
        for doc in database:
            doc_text = doc.get('text', '')
            similarity = self.calculate_cosine_similarity(text, doc_text)
            
            if similarity > 5:
                sequences = self.find_common_sequences(text, doc_text)
                results['matches'].append({
                    'source': doc.get('source', 'Unknown'),
                    'url': doc.get('url', ''),
                    'similarity': round(similarity, 2),
                    'matched_sequences': sequences[:5]
                })
        
        if results['matches']:
            total_weight = sum(m['similarity'] for m in results['matches'])
            weighted_sum = sum(m['similarity'] ** 2 for m in results['matches'])
            results['overall_similarity'] = round(
                weighted_sum / total_weight if total_weight > 0 else 0, 2
            )
        
        results['matches'].sort(key=lambda x: x['similarity'], reverse=True)
        return results

def get_sample_database() -> List[Dict]:
    return [
        {
            'source': 'Wikipedia - Academic Integrity',
            'url': 'https://en.wikipedia.org/wiki/Academic_integrity',
            'text': '''Academic integrity is the moral code or ethical policy of academia. 
            It includes values such as avoidance of cheating or plagiarism, maintenance of 
            academic standards, and honesty and rigor in research and academic publishing.'''
        },
        {
            'source': 'Educational Research Journal',
            'url': 'https://example.com/research/plagiarism',
            'text': '''Plagiarism is the representation of another author's language, thoughts, 
            ideas, or expressions as one's own original work. Students must understand proper attribution.'''
        },
        {
            'source': 'University Writing Guide',
            'url': 'https://example.com/writing-guide',
            'text': '''When students use someone else's ideas or words, they must give credit 
            to the original source. Failure to cite sources properly is considered plagiarism.'''
        },
        {
            'source': 'Research Ethics Handbook',
            'url': 'https://example.com/ethics',
            'text': '''Original research demonstrates critical thinking and deep understanding 
            of the subject matter. Students should develop their own ideas and arguments.'''
        },
        {
            'source': 'Academic Standards Guide',
            'url': 'https://example.com/standards',
            'text': '''Teachers take academic integrity seriously because it ensures students 
            are held to high ethical standards and that their work is trustworthy and credible.'''
        }
    ]


class PlagiarismCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plagiarism Checker - Academic Integrity Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        self.setup_styles()
        self.engine = PlagiarismEngine()
        self.database = get_sample_database()
        self.current_file = None
        self.current_text = None
        self.results = None
        self.create_ui()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), 
                       background='#667eea', foreground='white')
        style.configure('Subtitle.TLabel', font=('Arial', 10), 
                       background='#667eea', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), 
                       background='#f0f0f0')
        style.configure('Info.TLabel', font=('Arial', 10), 
                       background='#f0f0f0')
        style.configure('Primary.TButton', font=('Arial', 11, 'bold'))  
    
    def create_ui(self):
        header_frame = tk.Frame(self.root, bg='#667eea', height=100)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text="🔍 Plagiarism Checker", 
                 style='Title.TLabel').pack(pady=(15, 5))
        ttk.Label(header_frame, text="Advanced similarity detection for academic integrity", 
                 style='Subtitle.TLabel').pack()
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        left_frame = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        input_header = tk.Frame(left_frame, bg='#f7fafc', height=50)
        input_header.pack(fill='x')
        input_header.pack_propagate(False)
        
        ttk.Label(input_header, text="📄 Document Input", 
                 style='Header.TLabel', background='#f7fafc').pack(pady=15, padx=15, anchor='w')
        upload_frame = tk.Frame(left_frame, bg='white')
        upload_frame.pack(fill='x', padx=15, pady=15)
        
        self.file_label = ttk.Label(upload_frame, text="No file selected", 
                                    style='Info.TLabel')
        self.file_label.pack(pady=(0, 10))
        
        button_frame = tk.Frame(upload_frame, bg='white')
        button_frame.pack()
        
        ttk.Button(button_frame, text="📁 Choose File", 
                  command=self.select_file).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ Clear", 
                  command=self.clear_file).pack(side='left', padx=5)
        ttk.Label(upload_frame, text="Supported: DOCX, PDF, TXT", 
                 style='Info.TLabel', foreground='gray').pack(pady=(10, 0))
        ttk.Label(left_frame, text="Or paste text directly:", 
                 style='Info.TLabel', background='white').pack(padx=15, pady=(10, 5), anchor='w')
        
        self.text_input = scrolledtext.ScrolledText(left_frame, height=15, 
                                                    font=('Arial', 10), wrap='word')
        self.text_input.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.check_button = tk.Button(left_frame, text="🔍 Check for Plagiarism", 
                                     bg='#48bb78', fg='white', font=('Arial', 12, 'bold'),
                                     command=self.run_check, cursor='hand2', relief='flat',
                                     activebackground='#38a169', activeforeground='white')
        self.check_button.pack(fill='x', padx=15, pady=(0, 15))
        right_frame = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        right_frame.pack(side='right', fill='both', expand=True)
        results_header = tk.Frame(right_frame, bg='#f7fafc', height=50)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        ttk.Label(results_header, text="📊 Analysis Results", 
                 style='Header.TLabel', background='#f7fafc').pack(pady=15, padx=15, anchor='w')
        self.score_frame = tk.Frame(right_frame, bg='white', height=150)
        self.score_frame.pack(fill='x', pady=20)
        self.score_frame.pack_propagate(False)
        
        self.score_label = tk.Label(self.score_frame, text="--", 
                                    font=('Arial', 48, 'bold'), bg='white', fg='#718096')
        self.score_label.pack(pady=10)
        
        self.score_desc = ttk.Label(self.score_frame, text="Upload a document to begin", 
                                   style='Info.TLabel', background='white', 
                                   foreground='#718096')
        self.score_desc.pack()
        self.stats_frame = tk.Frame(right_frame, bg='#f7fafc')
        self.stats_frame.pack(fill='x', padx=15, pady=10)
        ttk.Label(right_frame, text="Detailed Matches:", 
                 style='Info.TLabel', background='white').pack(padx=15, pady=(10, 5), anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(right_frame, height=15, 
                                                     font=('Arial', 9), wrap='word',
                                                     state='disabled')
        self.results_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.results_text.tag_config('header', font=('Arial', 10, 'bold'), foreground='#2d3748')
        self.results_text.tag_config('source', font=('Arial', 9, 'bold'), foreground='#667eea')
        self.results_text.tag_config('match', background='#fef5e7', foreground='#c53030')
        self.export_button = tk.Button(right_frame, text="💾 Export Report", 
                                      bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                                      command=self.export_report, cursor='hand2', relief='flat',
                                      state='disabled', activebackground='#5a67d8',
                                      activeforeground='white')
        self.export_button.pack(fill='x', padx=15, pady=(0, 15))
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief='sunken', 
                                  anchor='w', bg='#e2e8f0', font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
    
    def select_file(self):
        filetypes = [
            ('All Supported', '*.txt *.docx *.pdf'),
            ('Text Files', '*.txt'),
            ('Word Documents', '*.docx'),
            ('PDF Files', '*.pdf'),
            ('All Files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Document",
            filetypes=filetypes
        )
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=f"📎 {Path(filename).name}")
            self.text_input.delete(1.0, tk.END)  # Clear text input
            self.status_bar.config(text=f"File selected: {Path(filename).name}")
    
    def clear_file(self):
        self.current_file = None
        self.file_label.config(text="No file selected")
        self.status_bar.config(text="Ready")
        
    def run_check(self):
        if self.current_file:
            self.status_bar.config(text="Extracting text from file...")
            try:
                text = self.engine.extract_text(self.current_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
                self.status_bar.config(text="Error reading file")
                return
        else:
            text = self.text_input.get(1.0, tk.END).strip()
        
        if not text or len(text) < 50:
            messagebox.showwarning("Warning", "Please provide a document or text (minimum 50 characters)")
            return
        
        self.current_text = text
        self.check_button.config(state='disabled', text="⏳ Analyzing...")
        self.status_bar.config(text="Analyzing document for plagiarism...")
        thread = threading.Thread(target=self.perform_check)
        thread.daemon = True
        thread.start()
    
    def perform_check(self):
        try:
            results = self.engine.check_plagiarism(self.current_text, self.database)
            self.results = results
            self.root.after(0, self.display_results)
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.check_button.config(state='normal', text="🔍 Check for Plagiarism"))

    def display_results(self):
        if not self.results:
            return
        score = self.results['overall_similarity']
        self.score_label.config(text=f"{score}%")
        if score < 15:
            color = '#48bb78'  # Green
            desc = "Low Similarity - Acceptable"
        elif score < 30:
            color = '#ed8936'  # Orange
            desc = "Moderate Similarity - Review Needed"
        else:
            color = '#f56565'  # Red
            desc = "High Similarity - Significant Concern"
        
        self.score_label.config(fg=color)
        self.score_desc.config(text=desc, foreground=color)
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = [
            ("Total Words", self.results['total_words']),
            ("Sources Found", len(self.results['matches'])),
            ("Unique Content", f"{max(0, 100 - score):.1f}%")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_box = tk.Frame(self.stats_frame, bg='white', relief='solid', bd=1)
            stat_box.pack(side='left', expand=True, fill='both', padx=5, pady=5)
            
            tk.Label(stat_box, text=str(value), font=('Arial', 16, 'bold'),
                    bg='white', fg='#667eea').pack(pady=(10, 0))
            tk.Label(stat_box, text=label, font=('Arial', 8),
                    bg='white', fg='#718096').pack(pady=(0, 10))
        
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        if self.results['matches']:
            for idx, match in enumerate(self.results['matches'], 1):
                self.results_text.insert(tk.END, f"\n━━ Match #{idx} ━━\n", 'header')
                self.results_text.insert(tk.END, f"Source: {match['source']}\n", 'source')
                if match['url']:
                    self.results_text.insert(tk.END, f"URL: {match['url']}\n")
                self.results_text.insert(tk.END, f"Similarity: {match['similarity']}%\n\n")
                
                if match['matched_sequences']:
                    self.results_text.insert(tk.END, "Matched Sequences:\n")
                    for seq in match['matched_sequences'][:3]:
                        text = seq['text'][:100] + '...' if len(seq['text']) > 100 else seq['text']
                        self.results_text.insert(tk.END, f"• ", 'match')
                        self.results_text.insert(tk.END, f"\"{text}\" ({seq['length']} words)\n", 'match')
                
                self.results_text.insert(tk.END, "\n")
        else:
            self.results_text.insert(tk.END, "\n✓ No significant matches found.\n\n")
            self.results_text.insert(tk.END, "The document appears to be largely original content.\n")
        
        self.results_text.config(state='disabled')
        self.check_button.config(state='normal', text="🔍 Check for Plagiarism")
        self.export_button.config(state='normal')
        self.status_bar.config(text=f"Analysis complete - {score}% similarity detected")
    
    def export_report(self):
        if not self.results:
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not filename:
            return
        
        report = []
        report.append("=" * 70)
        report.append("PLAGIARISM DETECTION REPORT")
        report.append("=" * 70)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Document: {Path(self.current_file).name if self.current_file else 'Pasted Text'}")
        report.append("")
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Overall Similarity Score: {self.results['overall_similarity']}%")
        report.append(f"Total Words Analyzed: {self.results['total_words']}")
        report.append(f"Number of Sources Matched: {len(self.results['matches'])}")
        report.append("")
        score = self.results['overall_similarity']
        report.append("INTERPRETATION")
        report.append("-" * 70)
        if score < 15:
            report.append("✓ LOW SIMILARITY - Acceptable level for academic work")
        elif score < 30:
            report.append("⚠ MODERATE SIMILARITY - Review recommended")
        else:
            report.append("✗ HIGH SIMILARITY - Significant concern")
        report.append("")


def main():
    root = tk.Tk()
    app = PlagiarismCheckerApp(root)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
