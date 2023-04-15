from functools import wraps

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from pyqtgraph.parametertree import (
    Parameter,
    ParameterTree,
    RunOptions,
    InteractiveFunction,
    Interactor,
)

app = pg.mkQApp()


def printResult(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        QtWidgets.QMessageBox.information(
            QtWidgets.QApplication.activeWindow(),
            "Function Run!",
            f"Func result: {LAST_RESULT.value}",
        )

    return wrapper


host = Parameter.create(name="Interactive Parameter Use", type="group")
interactor = Interactor(parent=host, runOptions=RunOptions.ON_CHANGED)


@interactor.decorate(a=10)
@printResult
def requiredParam(a, b=10):
    return a + b


@interactor.decorate(runOptions=RunOptions.ON_ACTION)
@printResult
def runOnButton(a=10, b=20):
    return a + b


@interactor.decorate(
    runOptions=(RunOptions.ON_ACTION),
    dictionary={"type": "list", "limits": ["4x4_1000"]},
)
def runOnBtnOrChange_listOpts(dictionary="4x4_1000", cols=29, rows=21):
    return dictionary



tree = ParameterTree()
tree.setParameters(host)

tree.show()
if __name__ == "__main__":
    pg.exec()