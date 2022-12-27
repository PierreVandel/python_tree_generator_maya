"""
TREE GENERATOR
Auteur : Pierre Vandel
02/11/2022
PEP8 approved
"""

import imp

import maya.OpenMayaUI as openMayaUI
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QWidget
from shiboken2 import wrapInstance

import tree_generator.data.api as tree_generator_api

imp.reload(tree_generator_api)


def maya_main_window():
    main_window_ptr = openMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class MyUI(QDialog):

    def __init__(self):
        super(MyUI, self).__init__(parent=maya_main_window())

    def init_ui(self):
        self.init_layouts()
        self.init_widgets()
        self.set_layouts()
        self.set_connections()
        self.set_default()

    def init_layouts(self):
        self.mainLayout = QVBoxLayout(self)

        self.treeParameterLayout = QHBoxLayout(self)
        self.GenerateLayout = QHBoxLayout(self)
        self.SnapLayout = QHBoxLayout(self)
        self.RamifiLayout = QHBoxLayout(self)
        self.DimensionLayout = QHBoxLayout(self)

    def init_widgets(self):
        self.generateButton = QPushButton("Generate trees")
        self.cleanButton = QPushButton("Clean trees")

        self.labelNumberTree = QLabel("Number tree")
        self.spinNumber = QSpinBox()
        self.spinNumber.setRange(0, 1000)

        self.labelRamifi = QLabel("Ramifications")
        self.spinRamifi = QSpinBox()
        self.spinRamifi.setRange(0, 5)

        self.chboxSnap = QCheckBox("Snap to")

        self.labelMin = QLabel("Min")
        self.inputMin = QLineEdit()
        self.labelMax = QLabel("Max")
        self.inputMax = QLineEdit()

        self.inputGroundName = QLineEdit()

    def set_layouts(self):
        '''Main Layout'''
        self.mainLayout.addLayout(self.treeParameterLayout)
        self.mainLayout.addLayout(self.RamifiLayout)
        self.mainLayout.addLayout(self.SnapLayout)
        self.mainLayout.addLayout(self.DimensionLayout)
        self.mainLayout.addLayout(self.GenerateLayout)

        '''Tree Parameter Layout'''
        self.treeParameterLayout.addWidget(self.labelNumberTree)
        self.treeParameterLayout.addWidget(self.spinNumber)

        '''Ramification Layout'''
        self.RamifiLayout.addWidget(self.labelRamifi)
        self.RamifiLayout.addWidget(self.spinRamifi)

        '''Snap Layout'''
        self.SnapLayout.addWidget(self.chboxSnap)
        self.SnapLayout.addWidget(self.inputGroundName)

        '''Dimension Layout'''
        self.DimensionLayout.addWidget(self.labelMin)
        self.DimensionLayout.addWidget(self.inputMin)
        self.DimensionLayout.addWidget(self.labelMax)
        self.DimensionLayout.addWidget(self.inputMax)

        '''Generate Layout'''
        self.GenerateLayout.addWidget(self.generateButton)
        self.GenerateLayout.addWidget(self.cleanButton)

    def set_connections(self):
        self.generateButton.clicked.connect(
            lambda: tree_generator_api.generate_trees(
                self.spinNumber.value(),
                self.spinRamifi.value(),
                self.chboxSnap.checkState(),
                int(self.inputMin.text()),
                int(self.inputMax.text()),
                self.inputGroundName.text()
            )
        )
        self.cleanButton.clicked.connect(tree_generator_api.clean_trees)
        pass

    def set_default(self):
        self.spinNumber.setValue(3)
        self.spinRamifi.setValue(2)
        self.inputMin.setText("-10")
        self.inputMax.setText("10")
        self.inputGroundName.setText("GroundName")
        pass

    def show(self):
        self.init_ui()
        return super(MyUI, self).show()


if __name__ == '__main__':
    if "my_ui" in globals():
        globals()["my_ui"].deleteLater()
    my_ui = MyUI()
    my_ui.show()
