from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
import sys
import io
from contextlib import redirect_stdout

from Bubblesort import bubblesort
from Insertionsort import insertionsort
from Quicksort import quicksort, normalize, parse_key
from Selectionsort import selectsort


def parse_int_list(text: str) -> list[int]:
    if not text.strip():
        return []
    raw = [x.strip() for x in text.replace(";", ",").replace(" ", ",").split(",") if x.strip()]
    return [int(x) for x in raw]

def parse_card_list(text: str) -> list[str]:
    if not text.strip():
        return []
    parts = [x.strip() for x in text.split(",") if x.strip()]
    return parts

def run_bubblesort(user_input: str):
    arr = parse_int_list(user_input)
    buf = io.StringIO()
    with redirect_stdout(buf):
        bubblesort(arr)
    process = buf.getvalue().rstrip()
    result = ";".join(map(str, arr))
    return process, result

def run_insertionsort(user_input: str):
    arr = parse_card_list(user_input)
    buf = io.StringIO()
    with redirect_stdout(buf):
        insertionsort(arr)
    process = buf.getvalue().rstrip()
    result = ",".join(arr)
    return process, result

def run_quicksort(user_input: str):
    parts = parse_card_list(user_input)
    buf = io.StringIO()
    with redirect_stdout(buf):
        quicksort(parts)
    process = buf.getvalue().rstrip()

    normed = [normalize(x) for x in parts]
    final_sorted = sorted(normed, key=parse_key)
    result = ",".join(final_sorted)
    return process, result

def run_selectionsort(user_input: str):
    arr = parse_int_list(user_input)
    buf = io.StringIO()
    with redirect_stdout(buf):
        selectsort(arr)
    process = buf.getvalue().rstrip()
    result = ",".join(map(str, arr))
    return process, result

# ---- GUI ----
class SortApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Visualizer (PyQt6)")
        self.resize(900, 620)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        top_bar = QHBoxLayout()
        layout.addLayout(top_bar)

        top_bar.addWidget(QLabel("Algorithm: "))
        self.combo = QComboBox()
        self.combo.addItems([
            "Bubble Sort (Integers; separated by semicolons or commas)",
            "Insertion Sort (Cards; separated by commas, e.g. C10,D2,HQ)",
            "Quick Sort (Cards; separated by commas, e.g. D3,SK,HA)",
            "Selection Sort (Integers; separated by semicolons or commas)",
        ])
        self.combo.currentIndexChanged.connect(self.on_algo_change)
        top_bar.addWidget(self.combo, stretch=1)

        self.example_btn = QPushButton("Fill Example")
        self.example_btn.clicked.connect(self.fill_example)
        top_bar.addWidget(self.example_btn)

        # 輸入列
        input_row = QHBoxLayout()
        layout.addLayout(input_row)

        input_row.addWidget(QLabel("Test Data Input: "))
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Please refer to the prompt above or click 'Fill Example'")
        input_row.addWidget(self.input_edit, stretch=1)

        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_sort)
        input_row.addWidget(self.run_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_outputs)
        input_row.addWidget(self.clear_btn)

        # 輸出區
        self.process_view = QTextEdit()
        self.process_view.setReadOnly(True)
        self.process_view.setPlaceholderText("Sorting process (original program's print output step by step)")
        layout.addWidget(QLabel("Sorting Process:"))
        layout.addWidget(self.process_view, stretch=2)

        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setPlaceholderText("Final Result:")
        layout.addWidget(QLabel("Final Result:"))
        layout.addWidget(self.result_view, stretch=1)

        # 初始提示
        self.on_algo_change(0)

    def on_algo_change(self, idx: int):
        if idx == 0:
            self.input_edit.setPlaceholderText("For example: 3;1;4;2 or 3,1,4,2 (integers)")
        elif idx == 1:
            self.input_edit.setPlaceholderText("For example: C10,D2,HQ,SA (cards, separated by commas)")
        elif idx == 2:
            self.input_edit.setPlaceholderText("For example: D3,SK,HA,C2 (cards, separated by commas)")
        elif idx == 3:
            self.input_edit.setPlaceholderText("For example: 8;5;6;1 or 8,5,6,1 (integers)")

    def fill_example(self):
        idx = self.combo.currentIndex()
        if idx == 0:
            self.input_edit.setText("3;1;4;2;5")
        elif idx == 1:
            self.input_edit.setText("C10,C2,D12,D3,HA")
        elif idx == 2:
            self.input_edit.setText("D3,SK,HA,C2,QJ")
        elif idx == 3:
            self.input_edit.setText("8,5,6,1,9,2")

    def clear_outputs(self):
        self.process_view.clear()
        self.result_view.clear()

    def run_sort(self):
        algo_idx = self.combo.currentIndex()
        text = self.input_edit.text()

        try:
            if algo_idx == 0:
                process, result = run_bubblesort(text)
                hint = ("※ Bubble Sort: The original program outputs a line for each swap; the initial list is printed with semicolons.\n")
            elif algo_idx == 1:
                process, result = run_insertionsort(text)
                hint = ("※ Insertion Sort: A line is output only when an actual insertion occurs; cards are sorted by suit, and numbers of the same suit are sorted from high to low.\n")
            elif algo_idx == 2:
                process, result = run_quicksort(text)
                hint = ("※ Quick Sort: The original program only prints the swapping process; the GUI additionally provides the final sequence (using the same sorting key).\n")
            elif algo_idx == 3:
                process, result = run_selectionsort(text)
                hint = ("※ Selection Sort: A line is output for each swap; your original code prints the initial list with semicolons and uses commas for swaps.\n")
            else:
                raise ValueError("Unknown algorithm selected.")

            self.process_view.setPlainText(hint + ("\n" + process if process else "\n(No process output)"))
            self.result_view.setPlainText(result if result else "(No result)")

        except ValueError as e:
            QMessageBox.warning(self, "Input Format Error", f"Please check your input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"An exception occurred:\n{e}")

def main():
    app = QApplication(sys.argv)
    w = SortApp()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()