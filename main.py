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