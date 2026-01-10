from typing import Optional, List

from pydantic import BaseModel, Field, field_validator

from root.backend.app.models.document.conditions import Condition
from root.backend.app.models.document.diagnosis import DiagnosisParameters
from root.backend.app.models.document.operations import OperationParameters


class Source(BaseModel):
    """Цитата из текста документа"""
    section: str = Field(..., description="Раздел документа")
    page: Optional[int] = Field(None, description="Номер страницы")
    quote: str = Field(..., description="Текст цитаты")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Уверенность в извлечении")


class SurgicalTreatmentModel(BaseModel):
    """Модель хирургического лечения"""
    operation_type: str = Field(..., description="Вид операции")
    operation_condition: Optional[Condition] = Field(None, description="Условия вида операции")
    operation_parameters: OperationParameters = Field(..., description="Параметры операции")
    diagnosis_parameters: DiagnosisParameters = Field(..., description="Параметры диагноза")
    sources: List[Source] = Field(default_factory=list, description="Источники в документе")

    @field_validator('operation_type')
    def validate_operation_type(cls, v):
        if not v or not v.strip():
            raise ValueError('Operation type cannot be empty')
        return v.strip()


class DiagnosisCategory(BaseModel):
    """Категория диагнозов с общими методами лечения"""
    diagnosis: str = Field(..., description="Диагноз")
    treatment_models: List[SurgicalTreatmentModel] = Field(default_factory=list, description="Модели хирургического лечения")

    @field_validator('diagnosis')
    def validate_diagnosis(cls, v):
        if not v or not v.strip():
            raise ValueError('Diagnosis cannot be empty')
        return v.strip()