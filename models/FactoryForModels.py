import models.normal as normalModel
import models.cauchy as cauchyModel
import models.exponent as exponentModel
import models.cauchy_Mod as cauchy_Mod
import models.normal_Mod as normal_Mod
import models.exponent_Mod as exponent_Mod


class FactoryForModels:
    def main_Factory(self, mode):

        if mode == "normal":
            return normalModel.NormalModel()
        elif mode == "cauchy":
            return cauchyModel.cauchyModel()
        elif mode == "exponent":
            return exponentModel.exponentModel()
        elif mode == "normal_Mod":
            return normal_Mod.NormalModel()
        elif mode == "cauchy_Mod":
            return cauchy_Mod.cauchyModel()
        elif mode == "exponent_Mod":
            return exponent_Mod.exponentModel()
