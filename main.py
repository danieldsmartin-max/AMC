import sys
import math
import re
import csv
import json
from datetime import datetime
import sympy as sp
import numpy as np

# PySide6 UI & Keyboard Imports
from PySide6.QtCore import Qt, Signal, QSize, QSettings
from PySide6.QtGui import QFont, QIcon, QKeySequence, QShortcut, QAction, QColor, QPalette, QKeyEvent
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QSplitter,
    QListWidget, QListWidgetItem, QStackedWidget, QFrame, QComboBox,
    QCheckBox, QSpinBox, QDoubleSpinBox, QGraphicsDropShadowEffect, QToolButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox,
    QGroupBox, QInputDialog, QPlainTextEdit
)

# Matplotlib Qt Integration
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# STYLESHEETS & BRANDING
# ==========================================

DARK_THEME = """
QMainWindow, QWidget#CentralWidget {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
QFrame#Sidebar {
    background-color: #0B0F19;
    border-right: 1px solid #1E293B;
}
QPushButton#NavButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
}
QPushButton#NavButton:hover {
    background-color: #1E293B;
    color: #00F0FF;
}
QPushButton#NavButton:checked {
    background-color: #1A2634;
    color: #00F0FF;
    border-left: 3px solid #00F0FF;
}
QLineEdit#DisplayInput {
    background-color: #1E293B;
    color: #00F0FF;
    border: 2px solid #334155;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 15px;
    font-family: 'Consolas', monospace;
}
QLineEdit#DisplayInput:focus {
    border: 2px solid #00F0FF;
}
QTextEdit#DisplayResult {
    background-color: #182232;
    color: #38BDF8;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    font-family: 'Consolas', monospace;
}
QPushButton#CalcBtn {
    background-color: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#CalcBtn:hover {
    background-color: #334155;
    border-color: #00F0FF;
    color: #00F0FF;
}
QPushButton#CalcBtnPrimary {
    background-color: #00F0FF;
    color: #0B0F19;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#CalcBtnPrimary:hover {
    background-color: #38BDF8;
}
QPushButton#BitBtn {
    background-color: #1E293B;
    color: #64748B;
    border: 1px solid #334155;
    border-radius: 4px;
    font-size: 11px;
    font-family: 'Consolas', monospace;
}
QPushButton#BitBtn[active="true"] {
    background-color: #00F0FF;
    color: #0B0F19;
    font-weight: bold;
}
QTabWidget::pane {
    border: 1px solid #1E293B;
    border-radius: 6px;
}
QTabBar::tab {
    background: #1E293B;
    color: #94A3B8;
    padding: 8px 14px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background: #00F0FF;
    color: #0B0F19;
    font-weight: bold;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px;
}
QTableWidget {
    background-color: #182232;
    color: #F8FAFC;
    gridline-color: #334155;
    border: 1px solid #334155;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #1E293B;
    color: #00F0FF;
    padding: 6px;
    border: 1px solid #334155;
}
QListWidget {
    background-color: #182232;
    color: #F8FAFC;
    border: 1px solid #334155;
    border-radius: 6px;
    font-family: 'Consolas', monospace;
}
QStatusBar {
    background-color: #0B0F19;
    color: #64748B;
    border-top: 1px solid #1E293B;
}
QGroupBox {
    border: 1px solid #334155;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #00F0FF;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget#CentralWidget {
    background-color: #F8FAFC;
    color: #0F172A;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
QFrame#Sidebar {
    background-color: #F1F5F9;
    border-right: 1px solid #E2E8F0;
}
QPushButton#NavButton {
    background-color: transparent;
    color: #475569;
    border: none;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
}
QPushButton#NavButton:hover {
    background-color: #E2E8F0;
    color: #0284C7;
}
QPushButton#NavButton:checked {
    background-color: #E0F2FE;
    color: #0284C7;
    border-left: 3px solid #0284C7;
}
QLineEdit#DisplayInput {
    background-color: #FFFFFF;
    color: #0284C7;
    border: 2px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 15px;
    font-family: 'Consolas', monospace;
}
QLineEdit#DisplayInput:focus {
    border: 2px solid #0284C7;
}
QTextEdit#DisplayResult {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    font-family: 'Consolas', monospace;
}
QPushButton#CalcBtn {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#CalcBtn:hover {
    background-color: #F1F5F9;
    border-color: #0284C7;
    color: #0284C7;
}
QPushButton#CalcBtnPrimary {
    background-color: #0284C7;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#CalcBtnPrimary:hover {
    background-color: #0369A1;
}
QPushButton#BitBtn {
    background-color: #FFFFFF;
    color: #64748B;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    font-size: 11px;
    font-family: 'Consolas', monospace;
}
QPushButton#BitBtn[active="true"] {
    background-color: #0284C7;
    color: #FFFFFF;
    font-weight: bold;
}
QTabWidget::pane {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
}
QTabBar::tab {
    background: #E2E8F0;
    color: #475569;
    padding: 8px 14px;
}
QTabBar::tab:selected {
    background: #0284C7;
    color: #FFFFFF;
    font-weight: bold;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 5px;
}
QTableWidget {
    background-color: #FFFFFF;
    color: #0F172A;
    gridline-color: #CBD5E1;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
}
QHeaderView::section {
    background-color: #E2E8F0;
    color: #0284C7;
    padding: 6px;
    border: 1px solid #CBD5E1;
}
QListWidget {
    background-color: #FFFFFF;
    color: #0F172A;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    font-family: 'Consolas', monospace;
}
QStatusBar {
    background-color: #F1F5F9;
    color: #64748B;
    border-top: 1px solid #E2E8F0;
}
QGroupBox {
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #0284C7;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
"""

# ==========================================
# ERROR ANALYSIS & MATH ENGINE
# ==========================================

class ErrorAnalyzer:
    @staticmethod
    def analyze(expr: str, exception: Exception) -> dict:
        err_msg = str(exception)
        if expr.count('(') != expr.count(')'):
            diff = abs(expr.count('(') - expr.count(')'))
            side = "closing ')'" if expr.count('(') > expr.count(')') else "opening '('"
            return {
                "title": "Syntax Error: Unbalanced Parentheses",
                "details": f"Missing {diff} {side} parenthesis.",
                "suggestion": "Check your brackets. Every opening '(' must have a matching closing ')'."
            }
        if re.search(r'[\+\-\*\/\^]{2,}', expr.replace('**', '^')):
            return {
                "title": "Syntax Error: Consecutive Operators",
                "details": "Two or more consecutive math operators detected.",
                "suggestion": "Remove double operators like '++' or '*/'."
            }
        if "division by zero" in err_msg.lower() or "zoo" in err_msg:
            return {
                "title": "Math Error: Division by Zero",
                "details": "The expression evaluated a denominator equal to 0.",
                "suggestion": "Ensure terms in denominators evaluate to a non-zero number."
            }
        return {
            "title": "Engine Evaluation Error",
            "details": f"Raw Output: {err_msg}",
            "suggestion": "Review expression formatting and verify input syntax."
        }

class MathEngine:
    def __init__(self):
        self.angle_mode = "DEG"
        self.last_answer = 0
        self.memory = 0
        self.history = []

    def evaluate(self, expr: str) -> dict:
        if not expr.strip():
            return {"status": "empty", "result": ""}
        try:
            raw = expr.strip()
            clean_expr = (raw.replace("×", "*").replace("÷", "/")
                          .replace("π", "pi").replace("Ans", str(self.last_answer)))
            # Support calculator-style factorial and percent.
            clean_expr = re.sub(r"(\d+(?:\.\d+)?|\([^()]+\))!", r"factorial(\1)", clean_expr)
            clean_expr = re.sub(r"(\d+(?:\.\d+)?|\([^()]+\))%", r"(\1/100)", clean_expr)
            # Explicit safe function namespace; implicit multiplication handles 2pi, 2(x), etc.
            namespace = {
                "pi": sp.pi, "E": sp.E, "e": sp.E,
                "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
                "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
                "sqrt": sp.sqrt, "log": sp.log, "ln": sp.log, "exp": sp.exp,
                "abs": sp.Abs, "factorial": sp.factorial, "floor": sp.floor, "ceil": sp.ceiling
            }
            transformations = sp.parsing.sympy_parser.standard_transformations + (
                sp.parsing.sympy_parser.implicit_multiplication_application,)
            parsed = sp.parsing.sympy_parser.parse_expr(clean_expr, local_dict=namespace, transformations=transformations, evaluate=True)
            # Apply angle conversion to trig atoms without fragile regex replacement.
            if self.angle_mode != "RAD":
                factor = sp.pi/180 if self.angle_mode == "DEG" else sp.pi/200
                trig = (sp.sin, sp.cos, sp.tan)
                for fn in trig:
                    parsed = parsed.replace(lambda z: z.func == fn, lambda z: fn(z.args[0] * factor))
            exact_val = sp.simplify(parsed)
            numeric_val = sp.N(exact_val, 15)
            self.last_answer = float(numeric_val) if numeric_val.is_real else numeric_val
            item_str = f"{raw} = {sp.N(exact_val, 10)}"
            self.history.append(item_str)
            return {"status":"success","exact":str(exact_val),"numeric":str(numeric_val),
                    "pretty":sp.pretty(exact_val),"raw":numeric_val,"history_item":item_str}
        except Exception as e:
            return {"status":"error", "analysis":ErrorAnalyzer.analyze(expr, e)}


# ==========================================
# 1. UPGRADED CALCULATOR VIEW (With History Tape)
# ==========================================

class CalculatorView(QWidget):
    def __init__(self, engine: MathEngine, status_cb):
        super().__init__()
        self.engine = engine
        self.status_cb = status_cb
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left Column: Keypad & Input
        left_box = QVBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setObjectName("DisplayInput")
        self.input_field.setPlaceholderText("Type expression or use keypad...")
        self.input_field.returnPressed.connect(self.calculate)

        self.result_display = QTextEdit()
        self.result_display.setObjectName("DisplayResult")
        self.result_display.setReadOnly(True)
        self.result_display.setFixedHeight(90)

        left_box.addWidget(self.input_field)
        left_box.addWidget(self.result_display)

        grid = QGridLayout()
        grid.setSpacing(5)

        buttons = [
            ('MC', 0, 0), ('MR', 0, 1), ('M+', 0, 2), ('M-', 0, 3), ('C', 0, 4),
            ('←', 8, 0),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('asin', 1, 3), ('acos', 1, 4),
            ('atan', 2, 0), ('sinh', 2, 1), ('cosh', 2, 2), ('tanh', 2, 3), ('abs', 2, 4),
            ('ln', 3, 0), ('log', 3, 1), ('sqrt', 3, 2), ('exp', 3, 3), ('!', 3, 4),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('÷', 4, 3), ('^', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('×', 5, 3), ('π', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3), ('Ans', 6, 4),
            ('0', 7, 0, 1, 2), ('.', 7, 2), ('%', 7, 3), ('±', 7, 4)
        ]

        for item in buttons:
            txt = item[0]
            r, c = item[1], item[2]
            r_span = item[3] if len(item) > 3 else 1
            c_span = item[4] if len(item) > 4 else 1

            btn = QPushButton(txt)
            btn.setFocusPolicy(Qt.NoFocus)
            if txt == '=':
                btn.setObjectName("CalcBtnPrimary")
                btn.clicked.connect(self.calculate)
            else:
                btn.setObjectName("CalcBtn")
                btn.clicked.connect(lambda _, t=txt: self.handle_btn(t))
            btn.setFixedHeight(34)
            grid.addWidget(btn, r, c, r_span, c_span)

        left_box.addLayout(grid)
        main_layout.addLayout(left_box, stretch=3)

        # Right Column: Calculation History Tape
        right_box = QVBoxLayout()
        right_box.addWidget(QLabel("📜 History Tape (Double-click to insert):"))
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.use_history_item)
        right_box.addWidget(self.history_list)

        btn_clear_hist = QPushButton("Clear History")
        btn_clear_hist.setObjectName("CalcBtn")
        btn_clear_hist.setFocusPolicy(Qt.NoFocus)
        btn_clear_hist.clicked.connect(self.clear_history)
        right_box.addWidget(btn_clear_hist)

        main_layout.addLayout(right_box, stretch=2)

    def focus_input(self):
        self.input_field.setFocus()

    def handle_btn(self, txt):
        if txt == 'C':
            self.input_field.clear()
            self.result_display.clear()
        elif txt == 'MC':
            self.engine.memory = 0
            self.status_cb("Memory Cleared")
        elif txt == 'MR':
            self.input_field.insert(str(self.engine.memory))
        elif txt == 'M+':
            res = self.engine.evaluate(self.input_field.text())
            if res.get("status") == "success":
                self.engine.memory += float(res["raw"])
                self.status_cb(f"Memory: {self.engine.memory}")
        elif txt == 'M-':
            res = self.engine.evaluate(self.input_field.text())
            if res.get("status") == "success":
                self.engine.memory -= float(res["raw"])
                self.status_cb(f"Memory: {self.engine.memory}")
        elif txt == '←':
            self.input_field.backspace()
        elif txt == '±':
            text = self.input_field.text()
            if text:
                self.input_field.setText(f'-({text})')
        elif txt == '%':
            self.input_field.insert('/100')
        elif txt == '!':
            self.input_field.insert('!')
        elif txt in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'sqrt', 'ln', 'log', 'exp', 'abs']:
            self.input_field.insert(f"{txt}(")
        else:
            self.input_field.insert(txt)
        self.focus_input()

    def calculate(self):
        res = self.engine.evaluate(self.input_field.text())
        if res["status"] == "success":
            out = f"Exact Value:   {res['exact']}\nDecimal Output: {res['numeric']}"
            self.result_display.setText(out)
            self.history_list.addItem(res["history_item"])
            self.status_cb("Evaluated successfully.")
        elif res["status"] == "error":
            err = res["analysis"]
            out = f"⚠️ {err['title']}\n• Cause: {err['details']}\n• Suggestion: {err['suggestion']}"
            self.result_display.setText(out)
            self.status_cb("Evaluation Error Detected.")
        self.focus_input()

    def use_history_item(self, item):
        expr = item.text().split("=")[0].strip()
        self.input_field.setText(expr)
        self.focus_input()

    def clear_history(self):
        self.history_list.clear()
        self.engine.history.clear()

# ==========================================
# 2. UPGRADED INTELLIGENCE VIEW (NLP & Function Inspector)
# ==========================================

class IntelligenceView(QWidget):
    def __init__(self, engine: MathEngine):
        super().__init__()
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.addTab(self.create_nlp_subtab(), "Natural Language Solver")
        tabs.addTab(self.create_inspector_subtab(), "Function & Polynomial Inspector")
        layout.addWidget(tabs)

    def create_nlp_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        lbl = QLabel("Natural Language Prompt & Symbolic Solver")
        lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #00F0FF;")
        l.addWidget(lbl)

        self.nlp_input = QLineEdit()
        self.nlp_input.setObjectName("DisplayInput")
        self.nlp_input.setPlaceholderText("e.g., 'integrate x^2', 'differentiate sin(x)', 'solve x^2 - 4 = 0'")
        self.nlp_input.returnPressed.connect(self.process_nlp)

        self.nlp_output = QTextEdit()
        self.nlp_output.setObjectName("DisplayResult")
        self.nlp_output.setReadOnly(True)

        l.addWidget(self.nlp_input)
        l.addWidget(self.nlp_output)
        return w

    def create_inspector_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        l.addWidget(QLabel("Target Function f(x):"))
        self.inspect_input = QLineEdit("x**3 - 3*x")
        self.inspect_input.setObjectName("DisplayInput")
        self.inspect_input.returnPressed.connect(self.run_inspection)

        btn_inspect = QPushButton("Analyze Function Properties")
        btn_inspect.setObjectName("CalcBtnPrimary")
        btn_inspect.setFocusPolicy(Qt.NoFocus)
        btn_inspect.clicked.connect(self.run_inspection)

        l.addWidget(self.inspect_input)
        l.addWidget(btn_inspect)

        self.inspect_output = QTextEdit()
        self.inspect_output.setObjectName("DisplayResult")
        self.inspect_output.setReadOnly(True)
        l.addWidget(self.inspect_output)

        return w

    def focus_input(self):
        self.nlp_input.setFocus()

    def process_nlp(self):
        query = self.nlp_input.text().strip().lower()
        x = sp.Symbol('x')
        try:
            if "integrate" in query:
                expr_str = query.replace("integrate", "").strip()
                expr = sp.sympify(expr_str)
                res = sp.integrate(expr, x)
                explanation = f"🔍 INTEGRATION:\n∫ ({expr}) dx = {res} + C"
            elif "differentiate" in query or "derivative" in query:
                expr_str = query.replace("differentiate", "").replace("derivative of", "").strip()
                expr = sp.sympify(expr_str)
                res = sp.diff(expr, x)
                explanation = f"🔍 DIFFERENTIATION:\nd/dx ({expr}) = {res}"
            elif "solve" in query:
                expr_str = query.replace("solve", "").replace("= 0", "").strip()
                expr = sp.sympify(expr_str.split("=")[0] if "=" in expr_str else expr_str)
                res = sp.solve(expr, x)
                explanation = f"🔍 ALGEBRA SOLVER:\nRoots for {expr} = 0:\nx = {res}"
            else:
                expr = sp.sympify(query)
                explanation = f"Evaluated Expression: {expr}\nNumeric: {expr.evalf()}"
            self.nlp_output.setText(explanation)
        except Exception as e:
            err = ErrorAnalyzer.analyze(query, e)
            self.nlp_output.setText(f"⚠️ {err['title']}\n• Details: {err['details']}")

    def run_inspection(self):
        x = sp.Symbol('x')
        raw = self.inspect_input.text()
        try:
            expr = sp.sympify(raw)
            d1 = sp.diff(expr, x)
            d2 = sp.diff(d1, x)
            crit_pts = sp.solve(d1, x)
            inflect_pts = sp.solve(d2, x)
            roots = sp.solve(expr, x)

            out = (f"📊 FUNCTION ANALYSIS REPORT for f(x) = {expr}\n"
                   f"• First Derivative f'(x): {d1}\n"
                   f"• Second Derivative f''(x): {d2}\n"
                   f"• Roots / Zeros: x = {roots}\n"
                   f"• Critical Points (f' = 0): x = {crit_pts}\n"
                   f"• Inflection Points (f'' = 0): x = {inflect_pts}\n"
                   f"• Domain: R (Continuous over real domain if applicable)")
            self.inspect_output.setText(out)
        except Exception as e:
            self.inspect_output.setText(f"⚠️ Analysis Error: {str(e)}")

# ==========================================
# 3. UPGRADED MATHEMATICS SUITE VIEW
# ==========================================

class MathSuiteView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self.create_specialized_tab(), "Specialized Formulas")
        tabs.addTab(self.create_calculus_tab(), "Calculus & Integrals")
        tabs.addTab(self.create_algebra_tab(), "Algebra & Systems")
        tabs.addTab(self.create_matrix_tab(), "Linear Algebra")
        tabs.addTab(self.create_ode_tab(), "Differential Equations")
        layout.addWidget(tabs)

    def create_specialized_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        mode_box = QHBoxLayout()
        mode_box.addWidget(QLabel("Calculation Category:"))
        self.spec_mode = QComboBox()
        self.spec_mode.addItems([
            "Finance: Compound Interest",
            "Finance: Loan Amortization Monthly Payment",
            "Physics: Kinematics (v = v0 + a*t)",
            "Physics: Kinetic Energy (0.5 * m * v^2)",
            "Geometry: Sphere Volume & Surface Area",
            "Statistics: Mean, Variance & Std Dev"
        ])
        self.spec_mode.currentIndexChanged.connect(self.update_spec_inputs)
        mode_box.addWidget(self.spec_mode)
        l.addLayout(mode_box)

        self.spec_inputs_container = QWidget()
        self.spec_inputs_layout = QGridLayout(self.spec_inputs_container)
        l.addWidget(self.spec_inputs_container)

        btn_calc = QPushButton("Calculate Formula Result")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.run_specialized_calc)
        l.addWidget(btn_calc)

        self.spec_output = QTextEdit()
        self.spec_output.setObjectName("DisplayResult")
        self.spec_output.setReadOnly(True)
        l.addWidget(self.spec_output)

        self.spec_fields = {}
        self.update_spec_inputs()
        return w

    def update_spec_inputs(self):
        while self.spec_inputs_layout.count():
            item = self.spec_inputs_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.spec_fields.clear()

        mode = self.spec_mode.currentText()
        if "Compound Interest" in mode:
            labels = [("Principal (P):", "1000"), ("Annual Rate (r):", "0.05"), ("Freq/Yr (n):", "12"), ("Years (t):", "5")]
        elif "Loan Amortization" in mode:
            labels = [("Loan Principal (P):", "250000"), ("Annual Rate (r):", "0.06"), ("Term (Years):", "30")]
        elif "Kinematics" in mode:
            labels = [("Initial Vel v0:", "0"), ("Accel a:", "9.81"), ("Time t:", "5")]
        elif "Kinetic Energy" in mode:
            labels = [("Mass m:", "70"), ("Velocity v:", "15")]
        elif "Sphere" in mode:
            labels = [("Radius r:", "5")]
        elif "Statistics" in mode:
            labels = [("Comma-separated values:", "12, 15, 18, 22, 30, 35")]

        for idx, (label_text, default_val) in enumerate(labels):
            lbl = QLabel(label_text)
            field = QLineEdit(default_val)
            field.setObjectName("DisplayInput")
            self.spec_inputs_layout.addWidget(lbl, idx, 0)
            self.spec_inputs_layout.addWidget(field, idx, 1)
            self.spec_fields[label_text] = field

    def run_specialized_calc(self):
        mode = self.spec_mode.currentText()
        try:
            if "Compound Interest" in mode:
                P = float(self.spec_fields["Principal (P):"].text())
                r = float(self.spec_fields["Annual Rate (r):"].text())
                n = float(self.spec_fields["Freq/Yr (n):"].text())
                t = float(self.spec_fields["Years (t):"].text())
                A = P * ((1 + r / n) ** (n * t))
                res = f"Final Balance (A): {A:.2f}\nTotal Interest: {A - P:.2f}"
            elif "Sphere" in mode:
                r = float(self.spec_fields["Radius r:"].text())
                res = f"Volume: {(4/3)*math.pi*(r**3):.4f}\nSurface Area: {4*math.pi*(r**2):.4f}"
            elif "Statistics" in mode:
                raw = self.spec_fields["Comma-separated values:"].text()
                data = [float(x.strip()) for x in raw.split(",") if x.strip()]
                if not data: raise ValueError("Enter at least one numeric value.")
                res = f"Count: {len(data)}\nMean: {np.mean(data):.6g}\nPopulation Variance: {np.var(data):.6g}\nSample Variance: {np.var(data, ddof=1) if len(data)>1 else float('nan'):.6g}\nPopulation Std Dev: {np.std(data):.6g}\nSample Std Dev: {np.std(data, ddof=1) if len(data)>1 else float('nan'):.6g}\nMedian: {np.median(data):.6g}"
            elif "Loan Amortization" in mode:
                P = float(self.spec_fields["Loan Principal (P):"].text()); r = float(self.spec_fields["Annual Rate (r):"].text()); years = float(self.spec_fields["Term (Years):"].text())
                n = round(years * 12); rm = r / 12
                if P < 0 or n <= 0 or r < 0: raise ValueError("Principal and term must be positive; rate cannot be negative.")
                M = P / n if rm == 0 else P * rm * (1 + rm)**n / ((1 + rm)**n - 1)
                res = f"Monthly Payment: {M:,.2f}\nTotal Paid: {M*n:,.2f}\nTotal Interest: {M*n-P:,.2f}"
            elif "Kinematics" in mode:
                v0 = float(self.spec_fields["Initial Vel v0:"].text()); a = float(self.spec_fields["Accel a:"].text()); t = float(self.spec_fields["Time t:"].text())
                v = v0 + a*t; d = v0*t + 0.5*a*t*t
                res = f"Final Velocity: {v:.6g}\nDisplacement: {d:.6g}\nAcceleration: {a:.6g}\nTime: {t:.6g}"
            elif "Kinetic Energy" in mode:
                m = float(self.spec_fields["Mass m:"].text()); v = float(self.spec_fields["Velocity v:"].text())
                res = f"Kinetic Energy: {0.5*m*v*v:.6g} J\nMomentum: {m*v:.6g} kg·m/s"
            else:
                res = "Formula Computed Successfully."
            self.spec_output.setText(res)
        except Exception as e:
            self.spec_output.setText(f"⚠️ Formula Error: {str(e)}")

    def create_calculus_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        l.addWidget(QLabel("Target Expression f(x):"))
        self.calc_input = QLineEdit("sin(x)/x")
        self.calc_input.setObjectName("DisplayInput")
        l.addWidget(self.calc_input)

        # Definite Integration Controls
        box_def = QGroupBox("Definite Integration Bounds")
        def_grid = QGridLayout(box_def)
        def_grid.addWidget(QLabel("Lower Bound (a):"), 0, 0)
        self.bound_a = QLineEdit("0")
        self.bound_a.setObjectName("DisplayInput")
        def_grid.addWidget(self.bound_a, 0, 1)

        def_grid.addWidget(QLabel("Upper Bound (b):"), 0, 2)
        self.bound_b = QLineEdit("3.14159")
        self.bound_b.setObjectName("DisplayInput")
        def_grid.addWidget(self.bound_b, 0, 3)

        btn_def = QPushButton("Compute Definite Integral ∫[a,b]")
        btn_def.setObjectName("CalcBtnPrimary")
        btn_def.setFocusPolicy(Qt.NoFocus)
        btn_def.clicked.connect(self.run_definite_integral)
        def_grid.addWidget(btn_def, 1, 0, 1, 4)

        l.addWidget(box_def)

        self.calc_output = QTextEdit()
        self.calc_output.setObjectName("DisplayResult")
        self.calc_output.setReadOnly(True)
        l.addWidget(self.calc_output)

        return w

    def run_definite_integral(self):
        x = sp.Symbol('x')
        raw = self.calc_input.text()
        try:
            expr = sp.sympify(raw)
            a = sp.sympify(self.bound_a.text())
            b = sp.sympify(self.bound_b.text())
            val = sp.integrate(expr, (x, a, b))
            num_val = val.evalf()
            self.calc_output.setText(f"∫_{a}^{b} ({expr}) dx =\nExact: {val}\nNumeric: {num_val:.8f}")
        except Exception as e:
            self.calc_output.setText(f"⚠️ Integration Error: {str(e)}")

    def create_algebra_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        l.addWidget(QLabel("System of Linear Equations (2x2 or 3x3, e.g. '2*x + y = 5; x - 3*y = 2'):"))
        self.sys_input = QLineEdit("2*x + y = 5; x - 3*y = 2")
        self.sys_input.setObjectName("DisplayInput")
        l.addWidget(self.sys_input)

        btn_sys = QPushButton("Solve System of Equations")
        btn_sys.setObjectName("CalcBtnPrimary")
        btn_sys.setFocusPolicy(Qt.NoFocus)
        btn_sys.clicked.connect(self.solve_system)
        l.addWidget(btn_sys)

        self.alg_output = QTextEdit()
        self.alg_output.setObjectName("DisplayResult")
        self.alg_output.setReadOnly(True)
        l.addWidget(self.alg_output)
        return w

    def solve_system(self):
        try:
            raw = self.sys_input.text()
            eq_strings = raw.split(";")
            eqs = []
            x, y, z = sp.symbols('x y z')
            for eq_str in eq_strings:
                if "=" in eq_str:
                    lhs, rhs = eq_str.split("=")
                    eqs.append(sp.Eq(sp.sympify(lhs), sp.sympify(rhs)))
                else:
                    eqs.append(sp.Eq(sp.sympify(eq_str), 0))
            sol = sp.solve(eqs)
            self.alg_output.setText(f"System Solution:\n{sol}")
        except Exception as e:
            self.alg_output.setText(f"⚠️ System Solver Error: {str(e)}")

    def create_matrix_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.addWidget(QLabel("Matrix Input [a, b; c, d]:"))
        self.mat_input = QLineEdit("[1, 2; 3, 4]")
        self.mat_input.setObjectName("DisplayInput")
        l.addWidget(self.mat_input)

        btn_det = QPushButton("Compute Determinant & Inverse")
        btn_det.setObjectName("CalcBtnPrimary")
        btn_det.setFocusPolicy(Qt.NoFocus)
        btn_det.clicked.connect(self.run_matrix)
        l.addWidget(btn_det)

        self.mat_output = QTextEdit()
        self.mat_output.setObjectName("DisplayResult")
        self.mat_output.setReadOnly(True)
        l.addWidget(self.mat_output)
        return w

    def run_matrix(self):
        try:
            M = sp.Matrix(sp.sympify(self.mat_input.text()))
            res = f"Matrix:\n{sp.pretty(M)}\n\nDeterminant: {M.det()}\nInverse:\n{sp.pretty(M.inv())}"
            self.mat_output.setText(res)
        except Exception as e:
            self.mat_output.setText(f"⚠️ Matrix Error: {str(e)}")

    def create_ode_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.addWidget(QLabel("ODE Expression (e.g., y(x).diff(x) - y(x)):"))
        self.ode_input = QLineEdit("y(x).diff(x) - y(x)")
        self.ode_input.setObjectName("DisplayInput")
        l.addWidget(self.ode_input)

        btn_ode = QPushButton("Solve Differential Equation")
        btn_ode.setObjectName("CalcBtnPrimary")
        btn_ode.setFocusPolicy(Qt.NoFocus)
        btn_ode.clicked.connect(self.run_ode)
        l.addWidget(btn_ode)

        self.ode_output = QTextEdit()
        self.ode_output.setObjectName("DisplayResult")
        self.ode_output.setReadOnly(True)
        l.addWidget(self.ode_output)
        return w

    def run_ode(self):
        x = sp.Symbol('x')
        y = sp.Function('y')
        try:
            sol = sp.dsolve(sp.sympify(self.ode_input.text()), y(x))
            self.ode_output.setText(f"General Solution:\n{sp.pretty(sol)}")
        except Exception as e:
            self.ode_output.setText(f"⚠️ ODE Error: {str(e)}")

    def focus_input(self):
        pass

# ==========================================
# 4. ADVANCED MATHEMATICS LAB
# ==========================================

class AdvancedLabView(QWidget):
    """High-powered symbolic, numerical and scientific workspace."""
    def __init__(self):
        super().__init__()
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.z = sp.Symbol('z')
        self.init_ui()

    def _field(self, text=""):
        w = QLineEdit(text)
        w.setObjectName("DisplayInput")
        return w

    def _button(self, text, slot):
        b = QPushButton(text)
        b.setObjectName("CalcBtn")
        b.setFocusPolicy(Qt.NoFocus)
        b.clicked.connect(slot)
        return b

    def init_ui(self):
        root = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self.create_symbolic_tab(), "Symbolic Engine")
        tabs.addTab(self.create_matrix_tab(), "Matrix Lab")
        tabs.addTab(self.create_stats_tab(), "Statistics & Regression")
        tabs.addTab(self.create_number_tab(), "Number Theory")
        tabs.addTab(self.create_complex_tab(), "Complex Numbers")
        tabs.addTab(self.create_calculus_tab(), "Calculus Lab")
        tabs.addTab(self.create_constants_tab(), "Constants")
        root.addWidget(tabs)

    def output(self):
        box=QTextEdit(); box.setObjectName("DisplayResult"); box.setReadOnly(True); return box

    def create_symbolic_tab(self):
        w=QWidget(); l=QVBoxLayout(w)
        l.addWidget(QLabel("Expression / equation (use x, y, z):"))
        self.sym_expr=self._field("x**3 - 6*x**2 + 11*x - 6")
        l.addWidget(self.sym_expr)
        row=QHBoxLayout()
        for text,slot in [("Simplify",self.sym_simplify),("Expand",self.sym_expand),("Factor",self.sym_factor),("Collect",self.sym_collect),("Partial Fractions",self.sym_apart),("Solve",self.sym_solve)]:
            row.addWidget(self._button(text,slot))
        l.addLayout(row)
        l.addWidget(QLabel("System equations (one per line, e.g. x+y=5):"))
        self.sym_system=QPlainTextEdit("x + y = 5\n2*x - y = 1")
        l.addWidget(self.sym_system)
        l.addWidget(self._button("Solve System", self.sym_system_solve))
        self.sym_out=self.output(); l.addWidget(self.sym_out)
        return w

    def _parse_expr(self):
        raw=self.sym_expr.text().strip()
        if not raw: raise ValueError("Enter an expression.")
        if '=' in raw:
            a,b=raw.split('=',1); return sp.Eq(sp.sympify(a),sp.sympify(b))
        return sp.sympify(raw)
    def _show_sym(self, fn):
        try: self.sym_out.setText(sp.pretty(fn(self._parse_expr())))
        except Exception as e: self.sym_out.setText(f"Error: {e}")
    def sym_simplify(self): self._show_sym(lambda e: sp.simplify(e))
    def sym_expand(self): self._show_sym(lambda e: sp.expand(e))
    def sym_factor(self): self._show_sym(lambda e: sp.factor(e))
    def sym_collect(self): self._show_sym(lambda e: sp.collect(e,self.x))
    def sym_apart(self): self._show_sym(lambda e: sp.apart(e,self.x))
    def sym_solve(self):
        try:
            e=self._parse_expr(); eq=e.lhs-e.rhs if isinstance(e,sp.Equality) else e
            vars=sorted(eq.free_symbols,key=lambda q:q.name)
            self.sym_out.setText("Solutions:\n"+sp.pretty(sp.solve(eq,vars or [self.x], dict=True)))
        except Exception as e: self.sym_out.setText(f"Error: {e}")
    def sym_system_solve(self):
        try:
            lines=[q.strip() for q in self.sym_system.toPlainText().splitlines() if q.strip()]
            eqs=[]
            for line in lines:
                if '=' in line:
                    a,b=line.split('=',1); eqs.append(sp.Eq(sp.sympify(a),sp.sympify(b)))
                else: eqs.append(sp.sympify(line))
            vars=sorted(set().union(*(q.free_symbols for q in eqs)),key=lambda q:q.name)
            self.sym_out.setText(sp.pretty(sp.solve(eqs,vars,dict=True)))
        except Exception as e: self.sym_out.setText(f"System error: {e}")

    def create_matrix_tab(self):
        w=QWidget(); l=QVBoxLayout(w)
        l.addWidget(QLabel("Matrix A (rows separated by newline, values by spaces or commas):"))
        self.mat_a=QPlainTextEdit("1 2\n3 4"); l.addWidget(self.mat_a)
        self.mat_b=self._field("5, 11")
        l.addWidget(QLabel("Vector b (optional):")); l.addWidget(self.mat_b)
        row=QHBoxLayout()
        for text,slot in [("Analyze A",self.mat_analyze),("Solve Ax=b",self.mat_solve),("Eigenvalues",self.mat_eigen),("RREF",self.mat_rref)]: row.addWidget(self._button(text,slot))
        l.addLayout(row); self.mat_out=self.output(); l.addWidget(self.mat_out); return w
    def _matrix(self):
        rows=[]
        for line in self.mat_a.toPlainText().strip().splitlines():
            vals=[q for q in re.split(r'[ ,;]+',line.strip()) if q]
            if vals: rows.append([sp.sympify(q) for q in vals])
        if not rows or any(len(r)!=len(rows[0]) for r in rows): raise ValueError("Matrix rows must have equal length.")
        return sp.Matrix(rows)
    def mat_analyze(self):
        try:
            A=self._matrix(); lines=[f"A =\n{sp.pretty(A)}",f"Shape: {A.rows} × {A.cols}",f"Rank: {A.rank()}"]
            if A.rows==A.cols:
                lines += [f"Determinant: {A.det()}",f"Trace: {A.trace()}"]
                if A.det()!=0: lines.append(f"Inverse:\n{sp.pretty(A.inv())}")
            self.mat_out.setText('\n\n'.join(lines))
        except Exception as e:self.mat_out.setText(f"Matrix error: {e}")
    def mat_solve(self):
        try:
            A=self._matrix(); vals=[q for q in re.split(r'[ ,;]+',self.mat_b.text().strip()) if q]
            b=sp.Matrix([sp.sympify(q) for q in vals])
            if len(b)!=A.rows: raise ValueError("Vector b length must equal A row count.")
            self.mat_out.setText("Solution x:\n"+sp.pretty(A.gauss_jordan_solve(b)[0]))
        except Exception as e:self.mat_out.setText(f"Solve error: {e}")
    def mat_eigen(self):
        try:
            A=self._matrix(); self.mat_out.setText("Eigenvalues:\n"+sp.pretty(A.eigenvals()))
        except Exception as e:self.mat_out.setText(f"Eigenvalue error: {e}")
    def mat_rref(self):
        try:
            A=self._matrix(); r,piv=A.rref(); self.mat_out.setText(f"RREF:\n{sp.pretty(r)}\n\nPivot columns: {piv}")
        except Exception as e:self.mat_out.setText(f"RREF error: {e}")

    def create_stats_tab(self):
        w=QWidget(); l=QVBoxLayout(w)
        self.stat_data=self._field("12, 15, 18, 22, 30, 35, 40")
        l.addWidget(QLabel("Data (comma/space separated):")); l.addWidget(self.stat_data)
        row=QHBoxLayout(); row.addWidget(self._button("Analyze",self.stat_analyze)); row.addWidget(self._button("Linear Regression",self.stat_regression)); l.addLayout(row)
        l.addWidget(QLabel("For regression, enter x values below and y values in the second field."))
        self.reg_x=self._field("1,2,3,4,5"); self.reg_y=self._field("2,4,5,8,11")
        l.addWidget(self.reg_x); l.addWidget(self.reg_y)
        self.stat_out=self.output(); l.addWidget(self.stat_out); return w
    def _nums(self,text): return [float(q) for q in re.split(r'[ ,;]+',text.strip()) if q]
    def stat_analyze(self):
        try:
            d=np.array(self._nums(self.stat_data.text()),dtype=float)
            if len(d)==0: raise ValueError("No data.")
            q=np.percentile(d,[25,50,75]);
            mode_vals=[]
            vals,counts=np.unique(d,return_counts=True); maxc=counts.max()
            if maxc>1: mode_vals=vals[counts==maxc].tolist()
            out=(f"Count: {len(d)}\nMean: {np.mean(d):.12g}\nMedian: {np.median(d):.12g}\n"
                 f"Mode(s): {mode_vals if mode_vals else 'No repeated mode'}\nMin: {np.min(d):.12g}\nMax: {np.max(d):.12g}\n"
                 f"Range: {np.ptp(d):.12g}\nQ1: {q[0]:.12g}\nQ3: {q[2]:.12g}\nIQR: {q[2]-q[0]:.12g}\n"
                 f"Population variance: {np.var(d):.12g}\nSample variance: {np.var(d,ddof=1) if len(d)>1 else float('nan'):.12g}\n"
                 f"Population std dev: {np.std(d):.12g}\nSample std dev: {np.std(d,ddof=1) if len(d)>1 else float('nan'):.12g}")
            self.stat_out.setText(out)
        except Exception as e:self.stat_out.setText(f"Statistics error: {e}")
    def stat_regression(self):
        try:
            x=np.array(self._nums(self.reg_x.text()),float); y=np.array(self._nums(self.reg_y.text()),float)
            if len(x)!=len(y) or len(x)<2: raise ValueError("x and y must have equal length (at least 2).")
            m,b=np.polyfit(x,y,1); pred=m*x+b; ss_res=np.sum((y-pred)**2); ss_tot=np.sum((y-np.mean(y))**2); r2=1-ss_res/ss_tot if ss_tot else 1.0
            r=np.corrcoef(x,y)[0,1]
            self.stat_out.setText(f"y = {m:.12g}x + {b:.12g}\nSlope: {m:.12g}\nIntercept: {b:.12g}\nCorrelation r: {r:.12g}\nR²: {r2:.12g}")
        except Exception as e:self.stat_out.setText(f"Regression error: {e}")

    def create_number_tab(self):
        w=QWidget(); l=QVBoxLayout(w); self.num_n=self._field("360"); self.num_m=self._field("24")
        l.addWidget(QLabel("n:")); l.addWidget(self.num_n); l.addWidget(QLabel("m (optional):")); l.addWidget(self.num_m)
        row=QHBoxLayout()
        for text,slot in [("Analyze n",self.num_analyze),("gcd / lcm",self.num_gcd),("Modular Power",self.num_pow)]: row.addWidget(self._button(text,slot))
        l.addLayout(row); self.num_out=self.output(); l.addWidget(self.num_out); return w
    def num_analyze(self):
        try:
            n=int(self.num_n.text()); fac=sp.factorint(n); self.num_out.setText(f"n = {n}\nPrime: {sp.isprime(n)}\nFactorization: {fac}\nDivisors: {sp.divisors(n)}\nTotient φ(n): {sp.totient(n)}\nNumber of divisors: {sp.divisor_count(n)}")
        except Exception as e:self.num_out.setText(f"Number theory error: {e}")
    def num_gcd(self):
        try:
            a=int(self.num_n.text()); b=int(self.num_m.text()); self.num_out.setText(f"gcd({a},{b}) = {math.gcd(a,b)}\nlcm({a},{b}) = {math.lcm(a,b)}")
        except Exception as e:self.num_out.setText(f"GCD/LCM error: {e}")
    def num_pow(self):
        try:
            a=int(self.num_n.text()); m=int(self.num_m.text()); exp,ok=QInputDialog.getInt(self,"Modular exponent","Exponent:",5,0,10**9)
            if not ok: return
            self.num_out.setText(f"{a}^{exp} mod {m} = {pow(a,exp,m)}")
        except Exception as e:self.num_out.setText(f"Modular power error: {e}")

    def create_complex_tab(self):
        w=QWidget(); l=QVBoxLayout(w); self.cx_expr=self._field("3 + 4*I"); l.addWidget(QLabel("Complex expression:")); l.addWidget(self.cx_expr)
        row=QHBoxLayout()
        for text,slot in [("Analyze",self.cx_analyze),("Polar",self.cx_polar),("Conjugate",self.cx_conj)]: row.addWidget(self._button(text,slot))
        l.addLayout(row); self.cx_out=self.output(); l.addWidget(self.cx_out); return w
    def _cx(self): return sp.sympify(self.cx_expr.text().replace('i','I'))
    def cx_analyze(self):
        try:
            z=self._cx(); self.cx_out.setText(f"z = {z}\nReal: {sp.re(z)}\nImaginary: {sp.im(z)}\nMagnitude: {sp.Abs(z)}\nArgument: {sp.arg(z)} rad\nConjugate: {sp.conjugate(z)}")
        except Exception as e:self.cx_out.setText(f"Complex error: {e}")
    def cx_polar(self):
        try:
            z=self._cx(); self.cx_out.setText(f"Polar form:\n{sp.pretty(sp.expand_complex(z))}\n\nr = {sp.Abs(z)}\nθ = {sp.arg(z)} rad")
        except Exception as e:self.cx_out.setText(f"Polar error: {e}")
    def cx_conj(self):
        try:self.cx_out.setText(sp.pretty(sp.conjugate(self._cx())))
        except Exception as e:self.cx_out.setText(f"Conjugate error: {e}")

    def create_calculus_tab(self):
        w=QWidget(); l=QVBoxLayout(w); self.cal_expr=self._field("sin(x)*exp(-x)"); l.addWidget(QLabel("f(x):")); l.addWidget(self.cal_expr)
        self.cal_a=self._field("0"); self.cal_b=self._field("pi")
        g=QGridLayout(); g.addWidget(QLabel("Lower:"),0,0);g.addWidget(self.cal_a,0,1);g.addWidget(QLabel("Upper:"),0,2);g.addWidget(self.cal_b,0,3);l.addLayout(g)
        row=QHBoxLayout()
        for text,slot in [("Derivative",self.cal_deriv),("Integral",self.cal_integral),("Definite Integral",self.cal_defint),("Limit",self.cal_limit),("Taylor Series",self.cal_series)]: row.addWidget(self._button(text,slot))
        l.addLayout(row); self.cal_out=self.output(); l.addWidget(self.cal_out); return w
    def _calexpr(self): return sp.sympify(self.cal_expr.text())
    def cal_deriv(self):
        try:self.cal_out.setText(sp.pretty(sp.diff(self._calexpr(),self.x)))
        except Exception as e:self.cal_out.setText(f"Derivative error: {e}")
    def cal_integral(self):
        try:self.cal_out.setText(sp.pretty(sp.integrate(self._calexpr(),self.x))+" + C")
        except Exception as e:self.cal_out.setText(f"Integral error: {e}")
    def cal_defint(self):
        try:self.cal_out.setText(sp.pretty(sp.integrate(self._calexpr(),(self.x,sp.sympify(self.cal_a.text()),sp.sympify(self.cal_b.text())))))
        except Exception as e:self.cal_out.setText(f"Definite integral error: {e}")
    def cal_limit(self):
        try:
            point,ok=QInputDialog.getText(self,"Limit","x approaches:",text="0")
            if ok:self.cal_out.setText(sp.pretty(sp.limit(self._calexpr(),self.x,sp.sympify(point))))
        except Exception as e:self.cal_out.setText(f"Limit error: {e}")
    def cal_series(self):
        try:self.cal_out.setText(sp.pretty(sp.series(self._calexpr(),self.x,0,8)))
        except Exception as e:self.cal_out.setText(f"Series error: {e}")

    def create_constants_tab(self):
        w=QWidget(); l=QVBoxLayout(w); table=QTableWidget(); table.setColumnCount(4); table.setHorizontalHeaderLabels(["Constant","Symbol","Value","Unit"])
        data=[("Pi","π",str(sp.pi),"dimensionless"),("Euler","e",str(sp.E),"dimensionless"),("Golden ratio","φ",str((1+sp.sqrt(5))/2),"dimensionless"),("Speed of light","c","299792458","m/s"),("Planck","h","6.62607015e-34","J·s"),("Gravitational","G","6.67430e-11","m³/(kg·s²)"),("Elementary charge","e_charge","1.602176634e-19","C"),("Avogadro","N_A","6.02214076e23","1/mol"),("Boltzmann","k_B","1.380649e-23","J/K")]
        table.setRowCount(len(data))
        for r,row in enumerate(data):
            for c,val in enumerate(row): table.setItem(r,c,QTableWidgetItem(val))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); l.addWidget(table); return w

    def focus_input(self):
        if hasattr(self,'sym_expr'): self.sym_expr.setFocus()

# ==========================================
# 4. UPGRADED VISUAL PLOTTER VIEW (2D & 3D Rendering)
# ==========================================

class GraphingView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        top_controls = QHBoxLayout()
        self.plot_mode = QComboBox()
        self.plot_mode.addItems(["2D Function Comparison", "3D Surface Plot z = f(x,y)"])
        self.plot_mode.currentIndexChanged.connect(self.toggle_mode_inputs)

        top_controls.addWidget(QLabel("Plot Mode:"))
        top_controls.addWidget(self.plot_mode)

        top_controls.addWidget(QLabel("Range x:"))
        self.xmin = QLineEdit("-10")
        self.xmin.setFixedWidth(40)
        self.xmax = QLineEdit("10")
        self.xmax.setFixedWidth(40)
        top_controls.addWidget(self.xmin)
        top_controls.addWidget(QLabel("to"))
        top_controls.addWidget(self.xmax)

        layout.addLayout(top_controls)

        input_box = QHBoxLayout()
        input_box.addWidget(QLabel("f1(x) / z ="))
        self.graph_input = QLineEdit("sin(x)")
        self.graph_input.setObjectName("DisplayInput")

        input_box.addWidget(QLabel("f2(x):"))
        self.graph_input2 = QLineEdit("cos(x)")
        self.graph_input2.setObjectName("DisplayInput")

        btn_plot = QPushButton("Render Graph")
        btn_plot.setObjectName("CalcBtnPrimary")
        btn_plot.setFocusPolicy(Qt.NoFocus)
        btn_plot.clicked.connect(self.plot_graph)

        input_box.addWidget(self.graph_input)
        input_box.addWidget(self.graph_input2)
        input_box.addWidget(btn_plot)
        layout.addLayout(input_box)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#0F172A')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_graph()

    def toggle_mode_inputs(self):
        is_3d = "3D" in self.plot_mode.currentText()
        self.graph_input2.setVisible(not is_3d)

    def focus_input(self):
        self.graph_input.setFocus()

    def plot_graph(self):
        self.figure.clear()
        mode_3d = "3D" in self.plot_mode.currentText()

        try:
            x_min = float(self.xmin.text())
            x_max = float(self.xmax.text())
        except ValueError:
            x_min, x_max = -10, 10

        if mode_3d:
            ax = self.figure.add_subplot(111, projection='3d')
            ax.set_facecolor('#0F172A')
            expr_str = self.graph_input.text()
            x, y = sp.symbols('x y')
            try:
                expr = sp.sympify(expr_str)
                f = sp.lambdify((x, y), expr, "numpy")
                X = np.linspace(x_min, x_max, 50)
                Y = np.linspace(x_min, x_max, 50)
                X, Y = np.meshgrid(X, Y)
                Z = f(X, Y)

                surf = ax.plot_surface(X, Y, Z, cmap='cool', edgecolor='none')
                ax.set_title(f"3D Surface: z = {expr_str}", color='#00F0FF')
            except Exception as e:
                ax.text2D(0.5, 0.5, f"3D Plot Error: {str(e)}", color='red')
        else:
            ax = self.figure.add_subplot(111)
            ax.set_facecolor('#1E293B')
            ax.tick_params(colors='#94A3B8')
            ax.grid(True, color='#334155', linestyle='--')

            x = sp.Symbol('x')
            x_vals = np.linspace(x_min, x_max, 500)

            for idx, inp in enumerate([self.graph_input, self.graph_input2]):
                expr_str = inp.text().strip()
                if not expr_str: continue
                try:
                    expr = sp.sympify(expr_str)
                    f = sp.lambdify(x, expr, "numpy")
                    y_vals = f(x_vals)
                    color = '#00F0FF' if idx == 0 else '#38BDF8'
                    ax.plot(x_vals, y_vals, color=color, linewidth=2, label=f"y = {expr_str}")
                except Exception:
                    pass
            ax.legend(facecolor='#1E293B', edgecolor='none', labelcolor='#F8FAFC')

        self.canvas.draw()

# ==========================================
# 5. EXPANDED SPECIALIST & ELECTRONICS VIEW
# ==========================================

class SpecialistView(QWidget):
    def __init__(self):
        super().__init__()
        self.current_value = 0
        self.updating = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self.create_electronics_tab(), "Circuit Calculators")
        tabs.addTab(self.create_programmer_tab(), "Programmer & Bitwise")
        tabs.addTab(self.create_units_tab(), "Multi-Domain Units")
        tabs.addTab(self.create_financial_tab(), "Financial Suite")
        tabs.addTab(self.create_engineering_tab(), "Engineering & Constants")
        layout.addWidget(tabs)

    def focus_input(self):
        if hasattr(self, 'dec_field'):
            self.dec_field.setFocus()

    # ------------------------------------------------------------------
    # ELECTRONICS & CIRCUIT CALCULATIONS
    # ------------------------------------------------------------------
    def create_electronics_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        mode_box = QHBoxLayout()
        mode_box.addWidget(QLabel("Select Circuit Calculation:"))
        self.elec_mode = QComboBox()
        self.elec_mode.addItems([
            "Ohm's Law & Power (V, I, R, P)",
            "LED Current-Limiting Resistor",
            "Voltage Divider Output",
            "RC Circuit Time Constant & Cutoff"
        ])
        self.elec_mode.currentIndexChanged.connect(self.update_elec_inputs)
        mode_box.addWidget(self.elec_mode)
        l.addLayout(mode_box)

        self.elec_inputs_container = QWidget()
        self.elec_inputs_layout = QGridLayout(self.elec_inputs_container)
        l.addWidget(self.elec_inputs_container)

        btn_calc = QPushButton("Calculate Circuit Parameters")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.run_circuit_calc)
        l.addWidget(btn_calc)

        self.elec_output = QTextEdit()
        self.elec_output.setObjectName("DisplayResult")
        self.elec_output.setReadOnly(True)
        l.addWidget(self.elec_output)

        self.elec_fields = {}
        self.update_elec_inputs()
        return w

    def update_elec_inputs(self):
        while self.elec_inputs_layout.count():
            item = self.elec_inputs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.elec_fields.clear()

        mode = self.elec_mode.currentText()
        if "Ohm's Law" in mode:
            labels = [
                ("Voltage V (Volts):", "12.0"),
                ("Current I (Amperes, or leave 0):", "0.0"),
                ("Resistance R (Ohms, or leave 0):", "100.0")
            ]
        elif "LED Current-Limiting" in mode:
            labels = [
                ("Supply Voltage V_supply (V):", "5.0"),
                ("Forward Voltage V_f (V):", "2.0"),
                ("Forward Current I_f (mA):", "20.0")
            ]
        elif "Voltage Divider" in mode:
            labels = [
                ("Input Voltage V_in (V):", "9.0"),
                ("Resistor R1 (Ohms):", "10000.0"),
                ("Resistor R2 (Ohms):", "5000.0")
            ]
        elif "RC Circuit" in mode:
            labels = [
                ("Resistance R (Ohms):", "10000.0"),
                ("Capacitance C (uF):", "10.0")
            ]

        for idx, (label_text, default_val) in enumerate(labels):
            lbl = QLabel(label_text)
            field = QLineEdit(default_val)
            field.setObjectName("DisplayInput")
            self.elec_inputs_layout.addWidget(lbl, idx, 0)
            self.elec_inputs_layout.addWidget(field, idx, 1)
            self.elec_fields[label_text] = field

    def run_circuit_calc(self):
        mode = self.elec_mode.currentText()
        try:
            if "Ohm's Law" in mode:
                v = float(self.elec_fields["Voltage V (Volts):"].text())
                i = float(self.elec_fields["Current I (Amperes, or leave 0):"].text())
                r = float(self.elec_fields["Resistance R (Ohms, or leave 0):"].text())

                if v > 0 and r > 0 and i == 0:
                    i = v / r
                elif v > 0 and i > 0 and r == 0:
                    r = v / i
                elif i > 0 and r > 0 and v == 0:
                    v = i * r

                p = v * i
                res = (
                    f"⚡ OHM'S LAW & POWER RESULTS:\n"
                    f"• Voltage (V): {v:.4g} V\n"
                    f"• Current (I): {i:.4g} A ({i*1000:.4g} mA)\n"
                    f"• Resistance (R): {r:.4g} Ω\n"
                    f"• Power (P): {p:.4g} W ({p*1000:.4g} mW)"
                )

            elif "LED Current-Limiting" in mode:
                v_supp = float(self.elec_fields["Supply Voltage V_supply (V):"].text())
                v_f = float(self.elec_fields["Forward Voltage V_f (V):"].text())
                i_f_ma = float(self.elec_fields["Forward Current I_f (mA):"].text())
                i_f = i_f_ma / 1000.0

                if v_supp <= v_f:
                    res = "⚠️ Error: Supply voltage must be higher than LED forward voltage (V_supply > V_f)."
                else:
                    r_req = (v_supp - v_f) / i_f
                    p_res = (v_supp - v_f) * i_f
                    res = (
                        f"💡 LED LIMITING RESISTOR RESULTS:\n"
                        f"• Calculated Resistance: {r_req:.2f} Ω\n"
                        f"• Resistor Power Dissipation: {p_res:.4g} W ({p_res*1000:.2f} mW)\n"
                        f"• Recommendation: Choose a standard resistor >= {r_req:.2f} Ω rated for at least {p_res*2:.4g} W."
                    )

            elif "Voltage Divider" in mode:
                v_in = float(self.elec_fields["Input Voltage V_in (V):"].text())
                r1 = float(self.elec_fields["Resistor R1 (Ohms):"].text())
                r2 = float(self.elec_fields["Resistor R2 (Ohms):"].text())

                v_out = v_in * (r2 / (r1 + r2))
                i_draw = v_in / (r1 + r2)
                res = (
                    f"📉 VOLTAGE DIVIDER RESULTS:\n"
                    f"• Output Voltage (V_out): {v_out:.4g} V\n"
                    f"• Divider Ratio (V_out / V_in): {r2 / (r1 + r2):.4f}\n"
                    f"• Total Current Draw: {i_draw*1000:.4g} mA\n"
                    f"• Formula: V_out = V_in × [R2 / (R1 + R2)]"
                )

            elif "RC Circuit" in mode:
                r = float(self.elec_fields["Resistance R (Ohms):"].text())
                c_uf = float(self.elec_fields["Capacitance C (uF):"].text())
                c = c_uf / 1e6

                tau = r * c
                fc = 1.0 / (2.0 * math.pi * r * c)
                res = (
                    f"⏱️ RC TIME CONSTANT & FREQUENCY:\n"
                    f"• Time Constant (τ = R × C): {tau:.6g} s ({tau*1000:.4g} ms)\n"
                    f"• Cutoff Frequency (f_c = 1 / [2πRC]): {fc:.4g} Hz\n"
                    f"• Time to 99% Charge (5τ): {5 * tau:.6g} s"
                )

            self.elec_output.setText(res)
        except Exception as e:
            self.elec_output.setText(f"⚠️ Calculation Error: {str(e)}")

    # ------------------------------------------------------------------
    # 1. PROGRAMMER TOOLKIT
    # ------------------------------------------------------------------
    def create_programmer_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        top_box = QHBoxLayout()
        top_box.addWidget(QLabel("Word Size:"))
        self.word_size = QComboBox()
        self.word_size.addItems(["64-Bit (QWORD)", "32-Bit (DWORD)", "16-Bit (WORD)", "8-Bit (BYTE)"])
        self.word_size.currentIndexChanged.connect(self.rebuild_bit_visualizer)
        top_box.addWidget(self.word_size)

        btn_swap_bytes = QPushButton("Swap Endianness")
        btn_swap_bytes.setObjectName("CalcBtn")
        btn_swap_bytes.setFocusPolicy(Qt.NoFocus)
        btn_swap_bytes.clicked.connect(self.swap_endianness)
        top_box.addWidget(btn_swap_bytes)

        top_box.addStretch()
        l.addLayout(top_box)

        grid = QGridLayout()
        self.base_fields = {}
        for idx, tag in enumerate(["HEX", "DEC", "OCT", "BIN"]):
            lbl = QLabel(f"{tag}:")
            lbl.setStyleSheet("font-weight: bold; color: #00F0FF;")
            field = QLineEdit("0")
            field.setObjectName("DisplayInput")
            field.textEdited.connect(lambda text, b=tag: self.on_base_edited(b, text))
            grid.addWidget(lbl, idx, 0)
            grid.addWidget(field, idx, 1)
            self.base_fields[tag] = field

        self.dec_field = self.base_fields["DEC"]
        l.addLayout(grid)

        # Text / ASCII Representation
        ascii_box = QHBoxLayout()
        ascii_box.addWidget(QLabel("ASCII / Text Equivalent:"))
        self.ascii_disp = QLineEdit("")
        self.ascii_disp.setObjectName("DisplayInput")
        self.ascii_disp.setReadOnly(True)
        ascii_box.addWidget(self.ascii_disp)
        l.addLayout(ascii_box)

        # 32-Bit Bit Grid
        l.addWidget(QLabel("Interactive Bit Visualizer (MSB .. 0):"))
        self.bit_buttons = []
        grid_bits = QGridLayout()
        grid_bits.setSpacing(2)
        self.bit_grid_layout = grid_bits

        bit_count = 64 if "64" in self.word_size.currentText() else 32
        for bit in range(bit_count - 1, -1, -1):
            btn = QPushButton("0")
            btn.setObjectName("BitBtn")
            btn.setFixedSize(24, 24)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.clicked.connect(lambda _, b=bit: self.toggle_bit(b))
            display_index = bit_count - 1 - bit
            row, col = divmod(display_index, 16)
            grid_bits.addWidget(btn, row, col)
            self.bit_buttons.append(btn)

        self.bit_buttons.reverse()
        l.addLayout(grid_bits)

        self.update_all_displays()
        return w

    def rebuild_bit_visualizer(self):
        """Rebuild the bit grid when changing 8/16/32/64-bit mode."""
        if not hasattr(self, "bit_buttons") or not hasattr(self, "bit_grid_layout"):
            self.mask_value()
            return
        while self.bit_grid_layout.count():
            item=self.bit_grid_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.bit_buttons=[]
        bit_count=64 if "64" in self.word_size.currentText() else 32 if "32" in self.word_size.currentText() else 16 if "16" in self.word_size.currentText() else 8
        for bit in range(bit_count-1,-1,-1):
            btn=QPushButton("0"); btn.setObjectName("BitBtn"); btn.setFixedSize(24,24); btn.setFocusPolicy(Qt.NoFocus)
            btn.clicked.connect(lambda _, b=bit:self.toggle_bit(b))
            display_index=bit_count-1-bit; row,col=divmod(display_index,16)
            self.bit_grid_layout.addWidget(btn,row,col); self.bit_buttons.append(btn)
        self.bit_buttons.reverse(); self.mask_value()

    def get_max_mask(self):
        sz = self.word_size.currentText()
        if "64" in sz: return 0xFFFFFFFFFFFFFFFF
        if "32" in sz: return 0xFFFFFFFF
        if "16" in sz: return 0xFFFF
        return 0xFF

    def mask_value(self):
        self.current_value &= self.get_max_mask()
        self.update_all_displays()

    def swap_endianness(self):
        val = self.current_value
        if "64" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(8, 'little'), 'big')
        elif "32" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(4, 'little'), 'big')
        elif "16" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(2, 'little'), 'big')
        else:
            self.current_value = val
        self.update_all_displays()

    def on_base_edited(self, base, text):
        if self.updating: return
        try:
            if base == "HEX": val = int(text, 16) if text else 0
            elif base == "DEC": val = int(text, 10) if text else 0
            elif base == "OCT": val = int(text, 8) if text else 0
            elif base == "BIN": val = int(text, 2) if text else 0
            self.current_value = val & self.get_max_mask()
            self.update_all_displays(skip_base=base)
        except ValueError:
            pass

    def toggle_bit(self, bit_idx):
        self.current_value ^= (1 << bit_idx)
        self.current_value &= self.get_max_mask()
        self.update_all_displays()

    def update_all_displays(self, skip_base=None):
        self.updating = True
        val = self.current_value

        if skip_base != "HEX": self.base_fields["HEX"].setText(f"{val:X}")
        if skip_base != "DEC": self.base_fields["DEC"].setText(str(val))
        if skip_base != "OCT": self.base_fields["OCT"].setText(f"{val:o}")
        if skip_base != "BIN": self.base_fields["BIN"].setText(f"{val:b}")

        # ASCII Conversion
        try:
            bytes_val = val.to_bytes((val.bit_length() + 7) // 8 or 1, 'big')
            self.ascii_disp.setText(bytes_val.decode('ascii', errors='replace'))
        except Exception:
            self.ascii_disp.setText("N/A")

        for bit in range(len(self.bit_buttons)):
            is_set = bool(val & (1 << bit))
            btn = self.bit_buttons[bit]
            btn.setText("1" if is_set else "0")
            btn.setProperty("active", "true" if is_set else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.updating = False

    # ------------------------------------------------------------------
    # 2. MULTI-DOMAIN UNIT CONVERTER
    # ------------------------------------------------------------------
    def create_units_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        self.unit_factors = {
            "Length": {"Meter": 1.0, "Kilometer": 1000.0, "Centimeter": 0.01, "Mile": 1609.34, "Foot": 0.3048, "Inch": 0.0254},
            "Area": {"Square Meter": 1.0, "Square Km": 1e6, "Hectare": 10000.0, "Acre": 4046.86, "Square Foot": 0.092903},
            "Volume": {"Liter": 1.0, "Milliliter": 0.001, "Cubic Meter": 1000.0, "Gallon (US)": 3.78541},
            "Mass": {"Kilogram": 1.0, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
            "Data Storage": {"Byte": 1.0, "KB": 1024.0, "MB": 1048576.0, "GB": 1073741824.0, "TB": 1099511627776.0},
            "Speed": {"m/s": 1.0, "km/h": 1/3.6, "mph": 0.44704, "ft/s": 0.3048, "knot": 0.514444},
            "Pressure": {"Pa": 1.0, "kPa": 1000.0, "bar": 100000.0, "psi": 6894.757, "atm": 101325.0},
            "Energy": {"Joule": 1.0, "kJ": 1000.0, "calorie": 4.184, "kWh": 3600000.0, "BTU": 1055.056},
            "Power": {"Watt": 1.0, "kW": 1000.0, "MW": 1000000.0, "hp": 745.699872},
            "Time": {"Second": 1.0, "Millisecond": 0.001, "Minute": 60.0, "Hour": 3600.0, "Day": 86400.0, "Week": 604800.0},
            "Angle": {"Degree": 1.0, "Radian": 180/math.pi, "Gradian": 0.9},
            "Temperature": {"Celsius": 1.0, "Fahrenheit": 1.0, "Kelvin": 1.0},
            "Currency (Fixed Rates)": {"USD ($)": 1.0, "EUR (€)": 1.08, "GBP (£)": 1.27, "JPY (¥)": 0.0067, "ZAR (R)": 0.055}
        }

        mode_box = QHBoxLayout()
        mode_box.addWidget(QLabel("Category:"))
        self.unit_cat = QComboBox()
        self.unit_cat.addItems(list(self.unit_factors.keys()))
        self.unit_cat.currentIndexChanged.connect(self.populate_unit_combos)
        mode_box.addWidget(self.unit_cat)
        l.addLayout(mode_box)

        conv_grid = QGridLayout()

        self.u_input_val = QLineEdit("1.0")
        self.u_input_val.setObjectName("DisplayInput")
        self.u_input_val.textChanged.connect(self.calculate_conversion)

        self.u_from_combo = QComboBox()
        self.u_to_combo = QComboBox()
        self.u_from_combo.currentIndexChanged.connect(self.calculate_conversion)
        self.u_to_combo.currentIndexChanged.connect(self.calculate_conversion)

        conv_grid.addWidget(QLabel("From:"), 0, 0)
        conv_grid.addWidget(self.u_input_val, 0, 1)
        conv_grid.addWidget(self.u_from_combo, 0, 2)

        conv_grid.addWidget(QLabel("To:"), 1, 0)
        self.u_result_lbl = QLabel("---")
        self.u_result_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #00F0FF;")
        conv_grid.addWidget(self.u_result_lbl, 1, 1)
        conv_grid.addWidget(self.u_to_combo, 1, 2)

        l.addLayout(conv_grid)
        l.addStretch()

        self.populate_unit_combos()
        return w

    def populate_unit_combos(self):
        cat = self.unit_cat.currentText()
        self.u_from_combo.blockSignals(True)
        self.u_to_combo.blockSignals(True)

        self.u_from_combo.clear()
        self.u_to_combo.clear()

        units = list(self.unit_factors[cat].keys())
        self.u_from_combo.addItems(units)
        self.u_to_combo.addItems(units)
        if len(units) > 1: self.u_to_combo.setCurrentIndex(1)

        self.u_from_combo.blockSignals(False)
        self.u_to_combo.blockSignals(False)
        self.calculate_conversion()

    def calculate_conversion(self):
        cat = self.unit_cat.currentText()
        try:
            val = float(self.u_input_val.text())
        except ValueError:
            self.u_result_lbl.setText("Invalid Input")
            return
        u_from = self.u_from_combo.currentText(); u_to = self.u_to_combo.currentText()
        if not u_from or not u_to: return
        if cat == "Temperature":
            if u_from == "Celsius": c = val
            elif u_from == "Fahrenheit": c = (val - 32) * 5/9
            else: c = val - 273.15
            if u_to == "Celsius": res = c
            elif u_to == "Fahrenheit": res = c * 9/5 + 32
            else: res = c + 273.15
        else:
            factors = self.unit_factors[cat]
            res = (val * factors[u_from]) / factors[u_to]
        self.u_result_lbl.setText(f"{res:.10g}")


    # ------------------------------------------------------------------
    # 3. FINANCIAL SUITE
    # ------------------------------------------------------------------
    def create_financial_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        fin_tabs = QTabWidget()
        fin_tabs.addTab(self.create_growth_subtab(), "Investment Growth")
        fin_tabs.addTab(self.create_amortization_subtab(), "Loan Amortization")
        l.addWidget(fin_tabs)

        return w

    def create_growth_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        grid = QGridLayout()
        grid.addWidget(QLabel("Initial Deposit ($):"), 0, 0)
        self.inv_principal = QLineEdit("10000")
        self.inv_principal.setObjectName("DisplayInput")
        grid.addWidget(self.inv_principal, 0, 1)

        grid.addWidget(QLabel("Monthly Deposit ($):"), 0, 2)
        self.inv_monthly = QLineEdit("500")
        self.inv_monthly.setObjectName("DisplayInput")
        grid.addWidget(self.inv_monthly, 0, 3)

        grid.addWidget(QLabel("Annual Rate (%):"), 1, 0)
        self.inv_rate = QLineEdit("7.0")
        self.inv_rate.setObjectName("DisplayInput")
        grid.addWidget(self.inv_rate, 1, 1)

        grid.addWidget(QLabel("Time Horizon (Years):"), 1, 2)
        self.inv_years = QLineEdit("10")
        self.inv_years.setObjectName("DisplayInput")
        grid.addWidget(self.inv_years, 1, 3)

        btn_calc = QPushButton("Calculate Investment Projection")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.calculate_investment)
        grid.addWidget(btn_calc, 2, 0, 1, 4)

        l.addLayout(grid)

        self.growth_output = QTextEdit()
        self.growth_output.setObjectName("DisplayResult")
        self.growth_output.setReadOnly(True)
        l.addWidget(self.growth_output)

        return w

    def calculate_investment(self):
        try:
            P = float(self.inv_principal.text())
            PMT = float(self.inv_monthly.text())
            r = float(self.inv_rate.text()) / 100.0 / 12.0
            n = int(float(self.inv_years.text()) * 12)

            balance = P
            total_contributions = P

            for _ in range(n):
                balance = balance * (1 + r) + PMT
                total_contributions += PMT

            total_interest = balance - total_contributions
            res = (f"📈 FUTURE INVESTMENT VALUE REPORT:\n"
                   f"• Total Final Balance: ${balance:,.2f}\n"
                   f"• Total Principal Invested: ${total_contributions:,.2f}\n"
                   f"• Compound Interest Earned: ${total_interest:,.2f}")
            self.growth_output.setText(res)
        except Exception as e:
            self.growth_output.setText(f"⚠️ Calculation Error: {str(e)}")

    def create_amortization_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        grid = QGridLayout()
        grid.addWidget(QLabel("Loan Amount ($):"), 0, 0)
        self.fin_principal = QLineEdit("250000")
        self.fin_principal.setObjectName("DisplayInput")
        grid.addWidget(self.fin_principal, 0, 1)

        grid.addWidget(QLabel("Annual Rate (%):"), 0, 2)
        self.fin_rate = QLineEdit("5.5")
        self.fin_rate.setObjectName("DisplayInput")
        grid.addWidget(self.fin_rate, 0, 3)

        grid.addWidget(QLabel("Term (Years):"), 1, 0)
        self.fin_term = QLineEdit("30")
        self.fin_term.setObjectName("DisplayInput")
        grid.addWidget(self.fin_term, 1, 1)

        btn_calc = QPushButton("Generate Amortization Table")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.calculate_amortization)
        grid.addWidget(btn_calc, 1, 2, 1, 2)

        l.addLayout(grid)

        self.amort_table = QTableWidget()
        self.amort_table.setColumnCount(5)
        self.amort_table.setHorizontalHeaderLabels(["Month", "Payment", "Principal", "Interest", "Balance"])
        self.amort_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        l.addWidget(self.amort_table)

        return w

    def calculate_amortization(self):
        try:
            P = float(self.fin_principal.text())
            r = (float(self.fin_rate.text()) / 100.0) / 12.0
            n = int(float(self.fin_term.text()) * 12)

            M = P / n if r == 0 else P * (r * (1 + r)**n) / ((1 + r)**n - 1)
            self.amort_table.setRowCount(n)
            balance = P

            for month in range(1, n + 1):
                interest_payment = balance * r
                principal_payment = M - interest_payment
                balance -= principal_payment

                self.amort_table.setItem(month - 1, 0, QTableWidgetItem(str(month)))
                self.amort_table.setItem(month - 1, 1, QTableWidgetItem(f"${M:.2f}"))
                self.amort_table.setItem(month - 1, 2, QTableWidgetItem(f"${principal_payment:.2f}"))
                self.amort_table.setItem(month - 1, 3, QTableWidgetItem(f"${interest_payment:.2f}"))
                self.amort_table.setItem(month - 1, 4, QTableWidgetItem(f"${max(0, balance):.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ------------------------------------------------------------------
    # 4. ENGINEERING REFERENCE & RESISTOR CALCULATOR
    # ------------------------------------------------------------------
    def create_engineering_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        box_resistor = QGroupBox("4-Band Resistor Color Code Calculator")
        res_grid = QGridLayout(box_resistor)

        self.colors = ["Black (0)", "Brown (1)", "Red (2)", "Orange (3)", "Yellow (4)", 
                       "Green (5)", "Blue (6)", "Violet (7)", "Grey (8)", "White (9)"]

        self.band1 = QComboBox()
        self.band2 = QComboBox()
        self.band1.addItems(self.colors[1:]) # Skip black for band 1
        self.band2.addItems(self.colors)

        self.mult_combo = QComboBox()
        self.mult_combo.addItems(["x1 Ω", "x10 Ω", "x100 Ω", "x1k Ω", "x10k Ω", "x100k Ω", "x1M Ω"])

        self.band1.currentIndexChanged.connect(self.calc_resistor)
        self.band2.currentIndexChanged.connect(self.calc_resistor)
        self.mult_combo.currentIndexChanged.connect(self.calc_resistor)

        res_grid.addWidget(QLabel("1st Digit:"), 0, 0)
        res_grid.addWidget(self.band1, 0, 1)
        res_grid.addWidget(QLabel("2nd Digit:"), 0, 2)
        res_grid.addWidget(self.band2, 0, 3)
        res_grid.addWidget(QLabel("Multiplier:"), 1, 0)
        res_grid.addWidget(self.mult_combo, 1, 1)

        self.resistor_val_lbl = QLabel("Resistor Value: ---")
        self.resistor_val_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #00F0FF;")
        res_grid.addWidget(self.resistor_val_lbl, 1, 2, 1, 2)

        l.addWidget(box_resistor)

        # Scientific Constants Table
        l.addWidget(QLabel("Universal Constants:"))
        self.const_table = QTableWidget()
        self.const_table.setColumnCount(3)
        self.const_table.setHorizontalHeaderLabels(["Name", "Value", "Units"])
        self.const_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        constants_data = [
            ("Speed of Light (c)", "299792458", "m/s"),
            ("Planck Constant (h)", "6.62607015e-34", "J·s"),
            ("Gravitational Constant (G)", "6.67430e-11", "m³/(kg·s²)"),
            ("Elementary Charge (e)", "1.602176634e-19", "C")
        ]
        self.const_table.setRowCount(len(constants_data))
        for row, data in enumerate(constants_data):
            for col in range(3):
                self.const_table.setItem(row, col, QTableWidgetItem(data[col]))

        l.addWidget(self.const_table)

        self.calc_resistor()
        return w

    def calc_resistor(self):
        d1 = self.band1.currentIndex() + 1
        d2 = self.band2.currentIndex()
        mult = 10 ** self.mult_combo.currentIndex()

        val = (d1 * 10 + d2) * mult
        if val >= 1e6:
            str_val = f"{val/1e6:.2f} MΩ"
        elif val >= 1e3:
            str_val = f"{val/1e3:.2f} kΩ"
        else:
            str_val = f"{val} Ω"

        self.resistor_val_lbl.setText(f"Resistor Value: {str_val}")

    # ------------------------------------------------------------------
    # 1. PROGRAMMER TOOLKIT
    # ------------------------------------------------------------------
    def create_programmer_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        top_box = QHBoxLayout()
        top_box.addWidget(QLabel("Word Size:"))
        self.word_size = QComboBox()
        self.word_size.addItems(["64-Bit (QWORD)", "32-Bit (DWORD)", "16-Bit (WORD)", "8-Bit (BYTE)"])
        self.word_size.currentIndexChanged.connect(self.mask_value)
        top_box.addWidget(self.word_size)

        btn_swap_bytes = QPushButton("Swap Endianness")
        btn_swap_bytes.setObjectName("CalcBtn")
        btn_swap_bytes.setFocusPolicy(Qt.NoFocus)
        btn_swap_bytes.clicked.connect(self.swap_endianness)
        top_box.addWidget(btn_swap_bytes)

        top_box.addStretch()
        l.addLayout(top_box)

        grid = QGridLayout()
        self.base_fields = {}
        for idx, tag in enumerate(["HEX", "DEC", "OCT", "BIN"]):
            lbl = QLabel(f"{tag}:")
            lbl.setStyleSheet("font-weight: bold; color: #00F0FF;")
            field = QLineEdit("0")
            field.setObjectName("DisplayInput")
            field.textEdited.connect(lambda text, b=tag: self.on_base_edited(b, text))
            grid.addWidget(lbl, idx, 0)
            grid.addWidget(field, idx, 1)
            self.base_fields[tag] = field

        self.dec_field = self.base_fields["DEC"]
        l.addLayout(grid)

        # Text / ASCII Representation
        ascii_box = QHBoxLayout()
        ascii_box.addWidget(QLabel("ASCII / Text Equivalent:"))
        self.ascii_disp = QLineEdit("")
        self.ascii_disp.setObjectName("DisplayInput")
        self.ascii_disp.setReadOnly(True)
        ascii_box.addWidget(self.ascii_disp)
        l.addLayout(ascii_box)

        # 32-Bit Bit Grid
        l.addWidget(QLabel("Interactive Bit Visualizer (MSB .. 0):"))
        self.bit_buttons = []
        grid_bits = QGridLayout()
        grid_bits.setSpacing(2)
        self.bit_grid_layout = grid_bits

        bit_count = 64 if "64" in self.word_size.currentText() else 32
        for bit in range(bit_count - 1, -1, -1):
            btn = QPushButton("0")
            btn.setObjectName("BitBtn")
            btn.setFixedSize(24, 24)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.clicked.connect(lambda _, b=bit: self.toggle_bit(b))
            display_index = bit_count - 1 - bit
            row, col = divmod(display_index, 16)
            grid_bits.addWidget(btn, row, col)
            self.bit_buttons.append(btn)

        self.bit_buttons.reverse()
        l.addLayout(grid_bits)

        self.update_all_displays()
        return w

    def get_max_mask(self):
        sz = self.word_size.currentText()
        if "64" in sz: return 0xFFFFFFFFFFFFFFFF
        if "32" in sz: return 0xFFFFFFFF
        if "16" in sz: return 0xFFFF
        return 0xFF

    def mask_value(self):
        self.current_value &= self.get_max_mask()
        self.update_all_displays()

    def swap_endianness(self):
        val = self.current_value
        if "64" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(8, 'little'), 'big')
        elif "32" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(4, 'little'), 'big')
        elif "16" in self.word_size.currentText():
            self.current_value = int.from_bytes(val.to_bytes(2, 'little'), 'big')
        else:
            self.current_value = val
        self.update_all_displays()

    def on_base_edited(self, base, text):
        if self.updating: return
        try:
            if base == "HEX": val = int(text, 16) if text else 0
            elif base == "DEC": val = int(text, 10) if text else 0
            elif base == "OCT": val = int(text, 8) if text else 0
            elif base == "BIN": val = int(text, 2) if text else 0
            self.current_value = val & self.get_max_mask()
            self.update_all_displays(skip_base=base)
        except ValueError:
            pass

    def toggle_bit(self, bit_idx):
        self.current_value ^= (1 << bit_idx)
        self.current_value &= self.get_max_mask()
        self.update_all_displays()

    def update_all_displays(self, skip_base=None):
        self.updating = True
        val = self.current_value

        if skip_base != "HEX": self.base_fields["HEX"].setText(f"{val:X}")
        if skip_base != "DEC": self.base_fields["DEC"].setText(str(val))
        if skip_base != "OCT": self.base_fields["OCT"].setText(f"{val:o}")
        if skip_base != "BIN": self.base_fields["BIN"].setText(f"{val:b}")

        # ASCII Conversion
        try:
            bytes_val = val.to_bytes((val.bit_length() + 7) // 8 or 1, 'big')
            self.ascii_disp.setText(bytes_val.decode('ascii', errors='replace'))
        except Exception:
            self.ascii_disp.setText("N/A")

        for bit in range(len(self.bit_buttons)):
            is_set = bool(val & (1 << bit))
            btn = self.bit_buttons[bit]
            btn.setText("1" if is_set else "0")
            btn.setProperty("active", "true" if is_set else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self.updating = False

    # ------------------------------------------------------------------
    # 2. MULTI-DOMAIN UNIT CONVERTER (Expanded Domain)
    # ------------------------------------------------------------------
    def create_units_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        self.unit_factors = {
            "Length": {"Meter": 1.0, "Kilometer": 1000.0, "Centimeter": 0.01, "Mile": 1609.34, "Foot": 0.3048, "Inch": 0.0254},
            "Area": {"Square Meter": 1.0, "Square Km": 1e6, "Hectare": 10000.0, "Acre": 4046.86, "Square Foot": 0.092903},
            "Volume": {"Liter": 1.0, "Milliliter": 0.001, "Cubic Meter": 1000.0, "Gallon (US)": 3.78541},
            "Mass": {"Kilogram": 1.0, "Gram": 0.001, "Pound": 0.453592, "Ounce": 0.0283495},
            "Data Storage": {"Byte": 1.0, "KB": 1024.0, "MB": 1048576.0, "GB": 1073741824.0, "TB": 1099511627776.0},
            "Speed": {"m/s": 1.0, "km/h": 1/3.6, "mph": 0.44704, "ft/s": 0.3048, "knot": 0.514444},
            "Pressure": {"Pa": 1.0, "kPa": 1000.0, "bar": 100000.0, "psi": 6894.757, "atm": 101325.0},
            "Energy": {"Joule": 1.0, "kJ": 1000.0, "calorie": 4.184, "kWh": 3600000.0, "BTU": 1055.056},
            "Power": {"Watt": 1.0, "kW": 1000.0, "MW": 1000000.0, "hp": 745.699872},
            "Time": {"Second": 1.0, "Millisecond": 0.001, "Minute": 60.0, "Hour": 3600.0, "Day": 86400.0, "Week": 604800.0},
            "Angle": {"Degree": 1.0, "Radian": 180/math.pi, "Gradian": 0.9},
            "Temperature": {"Celsius": 1.0, "Fahrenheit": 1.0, "Kelvin": 1.0},
            "Currency (Fixed Rates)": {"USD ($)": 1.0, "EUR (€)": 1.08, "GBP (£)": 1.27, "JPY (¥)": 0.0067, "ZAR (R)": 0.055}
        }

        mode_box = QHBoxLayout()
        mode_box.addWidget(QLabel("Category:"))
        self.unit_cat = QComboBox()
        self.unit_cat.addItems(list(self.unit_factors.keys()))
        self.unit_cat.currentIndexChanged.connect(self.populate_unit_combos)
        mode_box.addWidget(self.unit_cat)
        l.addLayout(mode_box)

        conv_grid = QGridLayout()

        self.u_input_val = QLineEdit("1.0")
        self.u_input_val.setObjectName("DisplayInput")
        self.u_input_val.textChanged.connect(self.calculate_conversion)

        self.u_from_combo = QComboBox()
        self.u_to_combo = QComboBox()
        self.u_from_combo.currentIndexChanged.connect(self.calculate_conversion)
        self.u_to_combo.currentIndexChanged.connect(self.calculate_conversion)

        conv_grid.addWidget(QLabel("From:"), 0, 0)
        conv_grid.addWidget(self.u_input_val, 0, 1)
        conv_grid.addWidget(self.u_from_combo, 0, 2)

        conv_grid.addWidget(QLabel("To:"), 1, 0)
        self.u_result_lbl = QLabel("---")
        self.u_result_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #00F0FF;")
        conv_grid.addWidget(self.u_result_lbl, 1, 1)
        conv_grid.addWidget(self.u_to_combo, 1, 2)

        l.addLayout(conv_grid)
        l.addStretch()

        self.populate_unit_combos()
        return w

    def populate_unit_combos(self):
        cat = self.unit_cat.currentText()
        self.u_from_combo.blockSignals(True)
        self.u_to_combo.blockSignals(True)

        self.u_from_combo.clear()
        self.u_to_combo.clear()

        units = list(self.unit_factors[cat].keys())
        self.u_from_combo.addItems(units)
        self.u_to_combo.addItems(units)
        if len(units) > 1: self.u_to_combo.setCurrentIndex(1)

        self.u_from_combo.blockSignals(False)
        self.u_to_combo.blockSignals(False)
        self.calculate_conversion()

    def calculate_conversion(self):
        cat = self.unit_cat.currentText()
        try:
            val = float(self.u_input_val.text())
        except ValueError:
            self.u_result_lbl.setText("Invalid Input")
            return

        u_from = self.u_from_combo.currentText()
        u_to = self.u_to_combo.currentText()

        base_val = val * self.unit_factors[cat][u_from]
        res = base_val / self.unit_factors[cat][u_to]

        self.u_result_lbl.setText(f"{res:.8g}")

    # ------------------------------------------------------------------
    # 3. FINANCIAL SUITE (Amortization & Compound Deposits)
    # ------------------------------------------------------------------
    def create_financial_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        fin_tabs = QTabWidget()
        fin_tabs.addTab(self.create_growth_subtab(), "Investment Growth")
        fin_tabs.addTab(self.create_amortization_subtab(), "Loan Amortization")
        l.addWidget(fin_tabs)

        return w

    def create_growth_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        grid = QGridLayout()
        grid.addWidget(QLabel("Initial Deposit ($):"), 0, 0)
        self.inv_principal = QLineEdit("10000")
        self.inv_principal.setObjectName("DisplayInput")
        grid.addWidget(self.inv_principal, 0, 1)

        grid.addWidget(QLabel("Monthly Deposit ($):"), 0, 2)
        self.inv_monthly = QLineEdit("500")
        self.inv_monthly.setObjectName("DisplayInput")
        grid.addWidget(self.inv_monthly, 0, 3)

        grid.addWidget(QLabel("Annual Rate (%):"), 1, 0)
        self.inv_rate = QLineEdit("7.0")
        self.inv_rate.setObjectName("DisplayInput")
        grid.addWidget(self.inv_rate, 1, 1)

        grid.addWidget(QLabel("Time Horizon (Years):"), 1, 2)
        self.inv_years = QLineEdit("10")
        self.inv_years.setObjectName("DisplayInput")
        grid.addWidget(self.inv_years, 1, 3)

        btn_calc = QPushButton("Calculate Investment Projection")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.calculate_investment)
        grid.addWidget(btn_calc, 2, 0, 1, 4)

        l.addLayout(grid)

        self.growth_output = QTextEdit()
        self.growth_output.setObjectName("DisplayResult")
        self.growth_output.setReadOnly(True)
        l.addWidget(self.growth_output)

        return w

    def calculate_investment(self):
        try:
            P = float(self.inv_principal.text())
            PMT = float(self.inv_monthly.text())
            r = float(self.inv_rate.text()) / 100.0 / 12.0
            n = int(float(self.inv_years.text()) * 12)

            balance = P
            total_contributions = P

            for _ in range(n):
                balance = balance * (1 + r) + PMT
                total_contributions += PMT

            total_interest = balance - total_contributions
            res = (f"📈 FUTURE INVESTMENT VALUE REPORT:\n"
                   f"• Total Final Balance: ${balance:,.2f}\n"
                   f"• Total Principal Invested: ${total_contributions:,.2f}\n"
                   f"• Compound Interest Earned: ${total_interest:,.2f}")
            self.growth_output.setText(res)
        except Exception as e:
            self.growth_output.setText(f"⚠️ Calculation Error: {str(e)}")

    def create_amortization_subtab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        grid = QGridLayout()
        grid.addWidget(QLabel("Loan Amount ($):"), 0, 0)
        self.fin_principal = QLineEdit("250000")
        self.fin_principal.setObjectName("DisplayInput")
        grid.addWidget(self.fin_principal, 0, 1)

        grid.addWidget(QLabel("Annual Rate (%):"), 0, 2)
        self.fin_rate = QLineEdit("5.5")
        self.fin_rate.setObjectName("DisplayInput")
        grid.addWidget(self.fin_rate, 0, 3)

        grid.addWidget(QLabel("Term (Years):"), 1, 0)
        self.fin_term = QLineEdit("30")
        self.fin_term.setObjectName("DisplayInput")
        grid.addWidget(self.fin_term, 1, 1)

        btn_calc = QPushButton("Generate Amortization Table")
        btn_calc.setObjectName("CalcBtnPrimary")
        btn_calc.setFocusPolicy(Qt.NoFocus)
        btn_calc.clicked.connect(self.calculate_amortization)
        grid.addWidget(btn_calc, 1, 2, 1, 2)

        l.addLayout(grid)

        self.amort_table = QTableWidget()
        self.amort_table.setColumnCount(5)
        self.amort_table.setHorizontalHeaderLabels(["Month", "Payment", "Principal", "Interest", "Balance"])
        self.amort_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        l.addWidget(self.amort_table)

        return w

    def calculate_amortization(self):
        try:
            P = float(self.fin_principal.text())
            r = (float(self.fin_rate.text()) / 100.0) / 12.0
            n = int(float(self.fin_term.text()) * 12)

            M = P / n if r == 0 else P * (r * (1 + r)**n) / ((1 + r)**n - 1)
            self.amort_table.setRowCount(n)
            balance = P

            for month in range(1, n + 1):
                interest_payment = balance * r
                principal_payment = M - interest_payment
                balance -= principal_payment

                self.amort_table.setItem(month - 1, 0, QTableWidgetItem(str(month)))
                self.amort_table.setItem(month - 1, 1, QTableWidgetItem(f"${M:.2f}"))
                self.amort_table.setItem(month - 1, 2, QTableWidgetItem(f"${principal_payment:.2f}"))
                self.amort_table.setItem(month - 1, 3, QTableWidgetItem(f"${interest_payment:.2f}"))
                self.amort_table.setItem(month - 1, 4, QTableWidgetItem(f"${max(0, balance):.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ------------------------------------------------------------------
    # 4. ENGINEERING REFERENCE & RESISTOR CALCULATOR
    # ------------------------------------------------------------------
    def create_engineering_tab(self):
        w = QWidget()
        l = QVBoxLayout(w)

        box_resistor = QGroupBox("4-Band Resistor Color Code Calculator")
        res_grid = QGridLayout(box_resistor)

        self.colors = ["Black (0)", "Brown (1)", "Red (2)", "Orange (3)", "Yellow (4)", 
                       "Green (5)", "Blue (6)", "Violet (7)", "Grey (8)", "White (9)"]

        self.band1 = QComboBox()
        self.band2 = QComboBox()
        self.band1.addItems(self.colors[1:]) # Skip black for band 1
        self.band2.addItems(self.colors)

        self.mult_combo = QComboBox()
        self.mult_combo.addItems(["x1 Ω", "x10 Ω", "x100 Ω", "x1k Ω", "x10k Ω", "x100k Ω", "x1M Ω"])

        self.band1.currentIndexChanged.connect(self.calc_resistor)
        self.band2.currentIndexChanged.connect(self.calc_resistor)
        self.mult_combo.currentIndexChanged.connect(self.calc_resistor)

        res_grid.addWidget(QLabel("1st Digit:"), 0, 0)
        res_grid.addWidget(self.band1, 0, 1)
        res_grid.addWidget(QLabel("2nd Digit:"), 0, 2)
        res_grid.addWidget(self.band2, 0, 3)
        res_grid.addWidget(QLabel("Multiplier:"), 1, 0)
        res_grid.addWidget(self.mult_combo, 1, 1)

        self.resistor_val_lbl = QLabel("Resistor Value: ---")
        self.resistor_val_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #00F0FF;")
        res_grid.addWidget(self.resistor_val_lbl, 1, 2, 1, 2)

        l.addWidget(box_resistor)

        # Scientific Constants Table
        l.addWidget(QLabel("Universal Constants:"))
        self.const_table = QTableWidget()
        self.const_table.setColumnCount(3)
        self.const_table.setHorizontalHeaderLabels(["Name", "Value", "Units"])
        self.const_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        constants_data = [
            ("Speed of Light (c)", "299792458", "m/s"),
            ("Planck Constant (h)", "6.62607015e-34", "J·s"),
            ("Gravitational Constant (G)", "6.67430e-11", "m³/(kg·s²)"),
            ("Elementary Charge (e)", "1.602176634e-19", "C")
        ]
        self.const_table.setRowCount(len(constants_data))
        for row, data in enumerate(constants_data):
            for col in range(3):
                self.const_table.setItem(row, col, QTableWidgetItem(data[col]))

        l.addWidget(self.const_table)

        self.calc_resistor()
        return w

    def calc_resistor(self):
        d1 = self.band1.currentIndex() + 1
        d2 = self.band2.currentIndex()
        mult = 10 ** self.mult_combo.currentIndex()

        val = (d1 * 10 + d2) * mult
        if val >= 1e6:
            str_val = f"{val/1e6:.2f} MΩ"
        elif val >= 1e3:
            str_val = f"{val/1e3:.2f} kΩ"
        else:
            str_val = f"{val} Ω"

        self.resistor_val_lbl.setText(f"Resistor Value: {str_val}")

# ==========================================
# SETTINGS VIEW
# ==========================================

class SettingsView(QWidget):
    def __init__(self, engine: MathEngine, theme_cb):
        super().__init__()
        self.engine = engine
        self.theme_cb = theme_cb
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Angle Unit Mode Configuration:"))
        angle_combo = QComboBox()
        angle_combo.addItems(["DEG", "RAD", "GRAD"])
        angle_combo.setCurrentText(self.engine.angle_mode)
        angle_combo.currentTextChanged.connect(lambda m: setattr(self.engine, 'angle_mode', m))
        layout.addWidget(angle_combo)

        layout.addSpacing(15)
        layout.addWidget(QLabel("UI Appearance Theme:"))
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Theme", "Light Theme"])
        theme_combo.setCurrentText("Dark Theme" if self.theme_cb.__self__.is_dark else "Light Theme") if hasattr(self.theme_cb, "__self__") else None
        theme_combo.currentTextChanged.connect(lambda t: self.theme_cb(t == "Dark Theme"))
        layout.addWidget(theme_combo)

        layout.addStretch()

    def focus_input(self):
        pass

# ==========================================
# MAIN WINDOW WITH KEYBOARD NAVIGATION
# ==========================================

class AMCMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AMC Foundation - Advanced Calculator & Specialist Suite")
        self.resize(1200, 780)
        self.setMinimumSize(980, 650)

        self.engine = MathEngine()
        self.settings = QSettings("AMCFoundation", "AMCSuite")
        self.is_dark = self.settings.value("dark_mode", True, type=bool)
        self.engine.angle_mode = self.settings.value("angle_mode", "DEG")

        self.init_ui()
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        self.setup_shortcuts()
        self.setup_power_shortcuts()
        self.apply_theme()

        self.calc_view.focus_input()

    def init_ui(self):
        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(210)

        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(10, 20, 10, 20)

        brand = QLabel("AMC Suite V4.0")
        brand.setStyleSheet("font-size: 20px; font-weight: 800; color: #00F0FF; margin-bottom: 20px;")
        s_layout.addWidget(brand)

        self.stack = QStackedWidget()

        self.calc_view = CalculatorView(self.engine, self.update_status)
        self.intel_view = IntelligenceView(self.engine)
        self.math_view = MathSuiteView()
        self.graph_view = GraphingView()
        self.spec_view = SpecialistView()
        self.advanced_view = AdvancedLabView()
        self.settings_view = SettingsView(self.engine, self.set_theme)

        self.stack.addWidget(self.calc_view)
        self.stack.addWidget(self.intel_view)
        self.stack.addWidget(self.math_view)
        self.stack.addWidget(self.graph_view)
        self.stack.addWidget(self.spec_view)
        self.stack.addWidget(self.advanced_view)
        self.stack.addWidget(self.settings_view)

        nav_items = [
            ("Calculator (Ctrl+1)", 0),
            ("Intelligence (Ctrl+2)", 1),
            ("Mathematics (Ctrl+3)", 2),
            ("Visual Plotter (Ctrl+4)", 3),
            ("Specialist (Ctrl+5)", 4),
            ("Advanced Lab (Ctrl+6)", 5),
            ("Settings (Ctrl+7)", 6)
        ]

        self.nav_btns = []
        for name, idx in nav_items:
            btn = QPushButton(name)
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.setFocusPolicy(Qt.NoFocus)
            if idx == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda _, i=idx, b=btn: self.switch_page(i, b))
            s_layout.addWidget(btn)
            self.nav_btns.append(btn)

        s_layout.addStretch()

        layout.addWidget(sidebar)
        layout.addWidget(self.stack)

        self.status_bar = self.statusBar()
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        export_action = QAction("Export History (CSV)", self); export_action.triggered.connect(self.export_history); file_menu.addAction(export_action)
        edit_menu = menu.addMenu("Edit")
        copy_action = QAction("Copy Current Result", self); copy_action.setShortcut(QKeySequence("Ctrl+Shift+C")); copy_action.triggered.connect(self.copy_result); edit_menu.addAction(copy_action)
        clear_action = QAction("Clear Calculator History", self); clear_action.setShortcut(QKeySequence("Ctrl+Shift+H")); clear_action.triggered.connect(self.calc_view.clear_history); edit_menu.addAction(clear_action)
        self.update_status("AMC Engine Ready")

    def setup_shortcuts(self):
        for i in range(7):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda idx=i: self.switch_page(idx, self.nav_btns[idx]))

    def setup_power_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+K"), self).activated.connect(self.command_palette)
        QShortcut(QKeySequence("Ctrl+Shift+E"), self).activated.connect(self.export_history)

    def command_palette(self):
        commands = {
            "Calculator": 0, "Intelligence": 1, "Mathematics": 2, "Visual Plotter": 3,
            "Specialist": 4, "Advanced Lab": 5, "Settings": 6
        }
        choice, ok = QInputDialog.getItem(self, "AMC Command Palette", "Go to:", list(commands), 0, False)
        if ok and choice in commands:
            idx=commands[choice]
            self.switch_page(idx, self.nav_btns[idx])

    def switch_page(self, idx, target_btn):
        for b in self.nav_btns:
            b.setChecked(False)
        target_btn.setChecked(True)
        self.stack.setCurrentIndex(idx)

        current_widget = self.stack.currentWidget()
        if hasattr(current_widget, 'focus_input'):
            current_widget.focus_input()

    def update_status(self, msg):
        self.status_bar.showMessage(f" Status: {msg} | Angle Mode: {self.engine.angle_mode}")

    def set_theme(self, dark_mode):
        self.is_dark = dark_mode
        self.settings.setValue("dark_mode", dark_mode)
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

    def export_history(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Calculation History", "amc_history.csv", "CSV Files (*.csv)")
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f); writer.writerow(["Calculation", "Timestamp"])
                for item in self.calc_view.history_list.findItems("*", Qt.MatchWildcard):
                    writer.writerow([item.text(), datetime.now().isoformat(timespec="seconds")])
            self.update_status("History exported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def copy_result(self):
        text = self.calc_view.result_display.toPlainText()
        if text:
            QApplication.clipboard().setText(text); self.update_status("Result copied to clipboard.")

    def closeEvent(self, event):
        self.settings.setValue("light_mode", self.is_light)
        self.settings.setValue("angle_mode", self.engine.angle_mode)
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AMCMainWindow()
    window.show()
    sys.exit(app.exec())