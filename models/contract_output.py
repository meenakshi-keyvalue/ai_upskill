from pydantic import BaseModel
from typing import List

class ContractInfo(BaseModel):
    Brief_Summary: str
    Start_Date: str
    Parties_Involved: List[str]
    Termination_Date: str
    Governing_Law: str
    Contract_Type: str
    Payments: str
    Penalties_on_Termination: List[str]
