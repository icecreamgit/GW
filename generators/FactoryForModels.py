import generators.normalModel as normalModel
import generators.cauchyModel as cauchyModel
import generators.exponentModel as exponentModel

class FactoryForModels:
    def main_Factory(self, mode):

        if mode == "normalModel":
            return normalModel.NormalModel()
        elif mode == "cauchyModel":
            return cauchyModel.cauchyModel()
        elif mode == "exponentModel":
            return exponentModel.exponentModel()
