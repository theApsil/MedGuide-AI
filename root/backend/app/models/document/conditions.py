from enum import Enum
from typing import Optional, Union, Any, Dict

from pydantic import BaseModel, Field, field_validator


class LogicalOperation(str, Enum):
    """Логические операции для составных условий"""
    AND = "И"
    OR = "ИЛИ"
    XOR = "ИСКЛЮЧАЮЩЕЕ ИЛИ"
    THEN = "ТОГДА"
    IFF = "ТОГДА И ТОЛЬКО ТОГДА"
    EITHER = "ЛИБО"
    NOT = "НЕ"


class ConditionValue(BaseModel):
    """Значение условия"""
    type: str = Field(..., description="Тип значения")
    value: Union[str, int, float, bool] = Field(..., description="Значение")
    operator: Optional[str] = Field(None, description="Оператор сравнения: <, >, =, ≤, ≥")

    @field_validator('operator')
    def validate_operator(cls, v):
        if v and v not in ['<', '>', '=', '≤', '≥', '!=', '∈', '∉']:
            raise ValueError(f'Invalid operator: {v}')
        return v


class SimpleCondition(BaseModel):
    """Простое условие"""
    parameter: str = Field(..., description="Параметр для проверки")
    value: ConditionValue = Field(..., description="Значение для сравнения")

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            "parameter": self.parameter,
            "value": self.value.value,
            "operator": self.value.operator or "=",
            "type": self.value.type
        }


class CompoundCondition(BaseModel):
    """Составное условие"""
    left_condition: Union['SimpleCondition', 'CompoundCondition'] = Field(..., description="Левое условие")
    logical_operation: LogicalOperation = Field(..., description="Логическая операция")
    right_condition: Optional[Union['SimpleCondition', 'CompoundCondition']] = Field(
        None, description="Правое условие (для бинарных операций)"
    )

    @field_validator('right_condition')
    def validate_right_condition(cls, v, values):
        logical_op = values.get('logical_operation')
        # Для унарных операций правое условие не требуется
        if logical_op in [LogicalOperation.NOT]:
            if v is not None:
                raise ValueError(f'Для унарных операций правое условие не требуется: {logical_op}')
        # Для бинарных операций требуется правое условие
        elif v is None:
            raise ValueError(f'Для бинарных операций требуется правое условие: {logical_op}')
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        result = {
            "left": self.left_condition.to_dict() if hasattr(self.left_condition, 'to_dict') else self.left_condition,
            "operation": self.logical_operation.value
        }
        if self.right_condition:
            result["right"] = self.right_condition.to_dict() if hasattr(self.right_condition, 'to_dict') else self.right_condition
        return result


# Обновляем ссылки для рекурсивных типов
Condition = Union[SimpleCondition, CompoundCondition]
CompoundCondition.model_rebuild()
