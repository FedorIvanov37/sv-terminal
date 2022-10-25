from PyQt5.QtCore import QTimer

def slot(*args):
    print(args)


timer = QTimer()
timer. singleShot(100000, slot)
print(timer.interval())
print(timer.remainingTime())
