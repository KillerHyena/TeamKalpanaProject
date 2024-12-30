import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTabWidget, QLabel,
    QPushButton, QWidget, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Load data from CSV
csv_file_path = r"C:\Users\Aaryan\OneDrive\Desktop\TeamKalpanaProject\trial_data.csv"
data = pd.read_csv(csv_file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Team Kalpana - CanSat Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Set Main Window Background Color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #3f3d56;  /* Dark blue-gray */
            }
        """)

        # Header Section
        self.header_layout = QVBoxLayout()
        self.layout.addLayout(self.header_layout)

        # Title Layout
        self.title_layout = QHBoxLayout()
        self.header_layout.addLayout(self.title_layout)

        # Title Label
        self.title_label = QLabel("TEAM KALPANA : 2024-CANSAT-ASI-023")
        self.title_label.setStyleSheet("font-size: 16pt; font-weight: bold; color: white; background-color: #6c63ff; padding: 10px; border-radius: 8px;")
        self.title_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Sub Header Layout
        self.sub_header_layout = QGridLayout()
        self.header_layout.addLayout(self.sub_header_layout)

        # Software State Label
        self.state_label = QLabel("SOFTWARE STATE")
        self.state_label.setStyleSheet("font-size: 12pt; color: white;")
        self.sub_header_layout.addWidget(self.state_label, 0, 0, alignment=Qt.AlignLeft)

        # Rounded Rectangle Below Software State
        self.launch_pad_label = QLabel("Launch_Pad")
        self.launch_pad_label.setStyleSheet("""
            font-size: 12pt;
            background-color: #b7b5e4;  /* Light purple */
            border: 2px solid gray;
            border-radius: 10px;
            padding: 5px;
        """)
        self.sub_header_layout.addWidget(self.launch_pad_label, 1, 0, alignment=Qt.AlignLeft)

        # Logo
        logo_path = r"C:\Users\Aaryan\OneDrive\Desktop\TeamKalpanaProject\Team Kalpana Logo.png"
        self.logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.sub_header_layout.addWidget(self.logo_label, 0, 1, 2, 1, alignment=Qt.AlignCenter)

        # Time and Packet Count
        self.time_packet_layout = QHBoxLayout()

        # Time Layout
        self.time_layout = QVBoxLayout()
        self.time_label = QLabel("Time:")
        self.time_label.setStyleSheet("font-size: 12pt; color: white;")
        self.time_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        self.time_rectangle_label = QLabel("0")  # The "0" will appear in the rectangle
        self.time_rectangle_label.setStyleSheet("""
            font-size: 12pt;
            background-color: #b7b5e4;  /* Light purple */
            border: 2px solid gray;
            border-radius: 10px;
            padding: 5px;
        """)
        self.time_layout.addWidget(self.time_rectangle_label, alignment=Qt.AlignCenter)

        # Packet Count Layout
        self.packet_layout = QVBoxLayout()
        self.packet_count_label = QLabel("Packet Count:")
        self.packet_count_label.setStyleSheet("font-size: 12pt; color: white;")
        self.packet_layout.addWidget(self.packet_count_label, alignment=Qt.AlignCenter)

        self.packet_rectangle_label = QLabel("0")  # The "0" will appear in the rectangle
        self.packet_rectangle_label.setStyleSheet("""
            font-size: 12pt;
            background-color: #b7b5e4;  /* Light purple */
            border: 2px solid gray;
            border-radius: 10px;
            padding: 5px;
        """)
        self.packet_layout.addWidget(self.packet_rectangle_label, alignment=Qt.AlignCenter)

        # Add Time and Packet Layouts to the Horizontal Layout
        self.time_packet_layout.addLayout(self.time_layout)
        self.time_packet_layout.addSpacing(20)
        self.time_packet_layout.addLayout(self.packet_layout)

        # Add the horizontal layout to the sub-header grid layout
        self.sub_header_layout.addLayout(self.time_packet_layout, 0, 2, 2, 1)

        # Tabs Section
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
                width: 280px;
                background-color: #6c63ff;  /* Medium purple */
                color: white;
                border-radius: 15px;
            }
            QTabBar::tab:selected {
                background-color: #b7b5e4;  /* Lighter purple for selected tab */
                font-size: 14pt;
                color: black;
            }
            QTabWidget::pane {
                border: 1px solid gray;
                background-color: #f5f5f5;
            }
        """)
        self.layout.addWidget(self.tabs)

        # Add Tabs
        self.telemetry_tab = QWidget()
        self.graphs_tab = QWidget()
        self.location_tab = QWidget()
        self.live_tab = QWidget()

        self.tabs.addTab(self.telemetry_tab, "Telemetry Data")
        self.tabs.addTab(self.graphs_tab, "Graphs")
        self.tabs.addTab(self.location_tab, "Location and 3D Plotting")
        self.tabs.addTab(self.live_tab, "Live Telecast")

        # Create Graphs
        self.create_graphs()

        # Buttons Section
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        buttons = ["BOOT", "Set Time", "Calibrate", "ON / OFF", "CX", "SIM Enable", "SIM Activate", "SIM Disable"]
        for btn in buttons:
            button = QPushButton(btn)
            button.setStyleSheet("""
                background-color: #6c63ff;  /* Medium purple */
                color: white;
                font-size: 10pt;
                border: 2px solid #4b478e;
                border-radius: 5px;
                padding: 8px;
            """)
            self.button_layout.addWidget(button)

    def create_graphs(self):
        # Graphs Layout
        graphs_layout = QVBoxLayout(self.graphs_tab)

        # Matplotlib Figure
        fig, axs = plt.subplots(2, 3, figsize=(10, 6))
        fig.subplots_adjust(hspace=0.5, wspace=0.4)

        # Plotting data
        axs[0, 0].plot(data['ALTITUDE'], label='Altitude', color='blue')
        axs[0, 0].set_title('Altitude vs Time')
        axs[0, 0].set_xlabel('Time')
        axs[0, 0].set_ylabel('Altitude')
        axs[0, 0].legend()

        axs[0, 1].plot(data['PRESSURE'], label='Pressure', color='green')
        axs[0, 1].set_title('Pressure vs Time')
        axs[0, 1].set_xlabel('Time')
        axs[0, 1].set_ylabel('Pressure')
        axs[0, 1].legend()

        axs[0, 2].plot(data['VOLTAGE'], label='Voltage', color='orange')
        axs[0, 2].set_title('Voltage vs Time')
        axs[0, 2].set_xlabel('Time')
        axs[0, 2].set_ylabel('Voltage')
        axs[0, 2].legend()

        axs[1, 0].plot(data['GYRO_P'], label='Gyro', color='purple')
        axs[1, 0].set_title('Gyro vs Time')
        axs[1, 0].set_xlabel('Time')
        axs[1, 0].set_ylabel('Gyro')
        axs[1, 0].legend()

        axs[1, 1].plot(data['ACC_R'], label='Accel', color='red')
        axs[1, 1].set_title('Accel vs Time')
        axs[1, 1].set_xlabel('Time')
        axs[1, 1].set_ylabel('Accel')
        axs[1, 1].legend()

        axs[1, 2].plot(data['ALTITUDE'], label='Velocity', color='cyan')
        axs[1, 2].set_title('Velocity vs Time')
        axs[1, 2].set_xlabel('Time')
        axs[1, 2].set_ylabel('Velocity')
        axs[1, 2].legend()

        # Embedding Matplotlib into PyQt
        canvas = FigureCanvas(fig)
        graphs_layout.addWidget(canvas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
