from enum import Enum
from src.common.enums.piece_names_enum import PieceNamesEnum
from src.common.enums.mode_enum import ModeEnum

class DefaultPriceEnum(float, Enum):
    """
    Enum containing default prices of all services
    """
    PAYROLL_PRICE = 250.0
    SIGNUPS_SIGNOFFS = 300.0
    EXECUTIONS = 880.0
    BY_HAND_NO_DPH = 20.0
    BY_HAND_EVIDENCE = 25.0
    BY_HAND_UCTO = 35.0
    CREATE_VFA_DPH = 50.0
    CREATE_VFA_NO_DPH = 20.0
    CREATE_PFA_EVIDENCE = 25.0
    CREATE_PFA_UCTO = 35.0
    CREDIT_CARD_EVIDENCE = 35.0
    CREDIT_CARD_UCTO = 35.0
    CREDIT_CARD_NO_DPH = 20.0
    REGISTER_EVIDENCE = 25.0
    REGISTER_UCTO = 35.0
    REGISTER_NO_DPH = 20.0
    DPPO_DPFO = 1500.0
    SEND_DOCS = 300.0
    BANK = 10.0

    @classmethod
    def get_by_mode(cls, mode: ModeEnum, variable: PieceNamesEnum) -> float:
        mapping = {
            ModeEnum.EVIDENCE: {
                PieceNamesEnum.BY_HAND      : cls.BY_HAND_EVIDENCE,
                PieceNamesEnum.PFA          : cls.CREATE_PFA_EVIDENCE,
                PieceNamesEnum.CREDIT_CARD  : cls.CREDIT_CARD_EVIDENCE,
                PieceNamesEnum.REGISTER     : cls.REGISTER_EVIDENCE,
                PieceNamesEnum.VFA          : cls.CREATE_VFA_DPH
            },

            ModeEnum.UCTO: {
                PieceNamesEnum.BY_HAND      : cls.BY_HAND_UCTO,
                PieceNamesEnum.PFA          : cls.CREATE_PFA_UCTO,
                PieceNamesEnum.CREDIT_CARD  : cls.CREDIT_CARD_UCTO,
                PieceNamesEnum.REGISTER     : cls.REGISTER_UCTO,
                PieceNamesEnum.VFA          : cls.CREATE_VFA_DPH
            },

            ModeEnum.NO_DPH: {
                PieceNamesEnum.BY_HAND      : cls.BY_HAND_NO_DPH,
                PieceNamesEnum.VFA          : cls.CREATE_VFA_NO_DPH,
                PieceNamesEnum.CREDIT_CARD  : cls.CREDIT_CARD_NO_DPH,
            }
        }

        return mapping[mode][variable]