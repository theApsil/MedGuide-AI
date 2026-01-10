from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from root.backend.app.models.document.conditions import Condition, LogicalOperation
from root.backend.app.models.document.document import DiagnosisCategory
from root.backend.app.models.document.operations import SurgicalMethod


class DecisionVariable(BaseModel):
    """Переменная для принятия решения в графе"""
    name: str = Field(..., description="Название переменной")
    type: str = Field(..., description="Тип переменной: fracture_type, location, stability и т.д.")
    possible_values: Optional[List[str]] = Field(None, description="Возможные значения")
    description: Optional[str] = Field(None, description="Описание переменной")


class DecisionNode(BaseModel):
    """Ноды, по которым идёт обход графа"""
    condition: Condition = Field(..., description="Условие на основе параметров диагноза")
    then_treatments: List[str] = Field(..., description="Рекомендуемые виды операций при выполнении условия")
    else_treatments: Optional[List[str]] = Field(None, description="Рекомендуемые виды операций при невыполнении")
    description: Optional[str] = Field(None, description="Описание узла")

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в формат if/then/else"""
        result = {
            "if": self.condition.to_dict() if hasattr(self.condition, 'to_dict') else self.condition,
            "then": self.then_treatments
        }
        if self.else_treatments:
            result["else"] = self.else_treatments
        return result


class DecisionGraph(BaseModel):
    """Граф для принятия решений"""
    variables: List[DecisionVariable] = Field(default_factory=list, description="Переменные из онтологии")
    nodes: List[DecisionNode] = Field(default_factory=list, description="Узлы графа принятия решений")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Метаданные графа")


class ExtractionResult(BaseModel):
    """Результат извлечения информации из документа"""
    title: str = Field(..., description="Название документа/рекомендаций")
    diagnosis_categories: List[DiagnosisCategory] = Field(default_factory=list, description="Категории диагнозов")
    decision_graph: Optional[DecisionGraph] = Field(None, description="Decision graph для принятия решений")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Метаданные извлечения")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            LogicalOperation: lambda v: v.value,
            SurgicalMethod: lambda v: v.value
        }
