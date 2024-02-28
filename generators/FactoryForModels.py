import generators.normalModel as normalModel

class FactoryForModels:
    def main_Factory(self, params):
        mode = params["mode"]
        nModel = normalModel.NormalModel()

        if mode == "normalModel":
            nModel = normalModel.NormalModel()