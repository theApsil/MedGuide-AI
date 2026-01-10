from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel, Field

from root.backend.app.models.document.conditions import Condition


class SurgicalMethod(str, Enum):
    """Метод хирургического вмешательства"""
    OSTEOSYNTHESIS = "Погружной остеосинтез"
    ENDOPROSTHETICS = "Эндопротезирование"


class FixationType(BaseModel):
    """Тип фиксации"""
    name: str = Field(..., description="Название типа фиксации")
    condition: Optional[Condition] = Field(None, description="Условие применения типа фиксации")


class EndoprosthesisType(BaseModel):
    """Тип эндопротеза"""
    name: str = Field(..., description="Название типа эндопротеза")
    condition: Optional[Condition] = Field(None, description="Условие применения типа эндопротеза")


class ComponentFixationType(BaseModel):
    """Тип фиксации компонента"""
    name: str = Field(..., description="Название типа фиксации компонента")
    condition: Optional[Condition] = Field(None, description="Условие применения типа фиксации компонента")


class SurgicalMethodWithCondition(BaseModel):
    """Метод хирургического вмешательства с условием"""
    method: SurgicalMethod = Field(..., description="Метод вмешательства")
    condition: Optional[Condition] = Field(None, description="Условие применения метода")


class ReferenceParameter(BaseModel):
    """Справочный параметр"""
    info_type: str = Field(..., description="Тип справочной информации")
    value: Any = Field(..., description="Значение")
    condition: Optional[Condition] = Field(None, description="Условие для справочной информации")


class OperationParameters(BaseModel):
    """Параметры операции"""
    # Общие условия на параметры операции
    general_condition: Optional[Condition] = Field(None, description="Общие условия на параметры операции")

    # Конкретные параметры с их условиями
    fixation_type: Optional[FixationType] = Field(None, description="Тип фиксации")
    endoprosthesis_type: Optional[EndoprosthesisType] = Field(None, description="Тип эндопротеза")
    component_fixation_type: Optional[ComponentFixationType] = Field(None, description="Тип фиксации компонента")
    surgical_method: Optional[SurgicalMethodWithCondition] = Field(None, description="Метод хирургического вмешательства")
    reference_parameters: List[ReferenceParameter] = Field(default_factory=list, description="Справочные параметры")