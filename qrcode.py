import qrmvc.controller

if __name__ == '__main__':
    controller = qrmvc.controller.QRGenerator()
    controller.model.delete_temp()
