import subprocess
import sys
from typing import Self

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon


class TrayApp:
    def __init__(self: Self) -> None:
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon("resilio_sync_tray/resources/resilio-sync-icon.png"))
        self.tray.setVisible(True)

        self.menu = QMenu()

        self.status_action = QAction(f"Status: {self.get_status()}")
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)

        self.toggle_action = QAction(self.get_toggle_text())
        self.toggle_action.triggered.connect(self.toggle_resilio)
        self.menu.addAction(self.toggle_action)

        self.menu.addSeparator()

        self.exit_action = QAction("Quit")
        self.exit_action.setIcon(QIcon.fromTheme("application-exit"))
        self.exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(self.exit_action)

        self.tray.setContextMenu(self.menu)

    def get_status(self: Self) -> bool:
        return subprocess.getoutput("systemctl is-active resilio-sync")

    def get_toggle_text(self: Self) -> str:
        return "Start Resilio Sync" if self.get_status() == "inactive" else "Stop Resilio Sync"

    def update_menu(self: Self) -> None:
        self.status_action.setText(f"Status: {self.get_status()}")
        self.toggle_action.setText(self.get_toggle_text())

    def toggle_resilio(self: Self) -> None:
        status = self.get_status()
        if status == "active":
            subprocess.run(["sudo", "systemctl", "--user", "stop", "resilio-sync"])
        else:
            subprocess.run(["sudo", "systemctl", "--user", "start", "resilio-sync"])
        self.update_menu()

    def run(self: Self) -> None:
        self.app.exec()
