from PyQt6 import QtWidgets, uic


class MainView(QtWidgets.QMainWindow):
    def __init__(self, parent, orderView, controlView, graphView, transactionsView):
        super(MainView, self).__init__(parent)
        # Load the UI from the .ui file located in the same folder.
        uic.loadUi("view/main_view.ui", self)

        self.orderView = orderView
        self.controlView = controlView
        self.graphView = graphView
        self.transactionsView = transactionsView

        # Set the subviews’ parent to this main window.
        self.orderView.setParent(self)
        self.controlView.setParent(self)
        self.graphView.setParent(self)
        self.transactionsView.setParent(self)

        # Add the subviews to the appropriate layouts defined in the UI.
        # (Ensure that 'patientTabLayout' and 'medicineTabLayout' exist in MainView.ui.)
        self.orderLayout.addWidget(self.orderView)
        self.controlLayout.addWidget(self.controlView)
        self.graphLayout.addWidget(self.graphView)
        self.transactionsLayout.addWidget(self.transactionsView)
