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