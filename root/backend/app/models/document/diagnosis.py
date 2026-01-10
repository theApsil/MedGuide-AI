from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from root.backend.app.models.document.conditions import Condition


class FractureTypeParameter(BaseModel):
    """Тип перелома с условием"""
    name: str = Field(..., description="Название типа перелома")
    condition: Optional[Condition] = Field(None, description="Условие на тип перелома")


class FractureLocationParameter(BaseModel):
    """Локализация перелома с условием"""
    description: str = Field(..., description="Описание локализации")
    condition: Optional[Condition] = Field(None, description="Условие на локализацию")


class FractureStabilityParameter(BaseModel):
    """Стабильность перелома с условием"""
    description: str = Field(..., description="Описание стабильности перелома")
    condition: Optional[Condition] = Field(None, description="Условие на стабильность перелома")


class FractureDisplacementParameter(BaseModel):
    """Смещение перелома с условием"""
    description: str = Field(..., description="Описание смещения перелома")
    condition: Optional[Condition] = Field(None, description="Условие на смещение перелома")


class MedialSupportParameter(BaseModel):
    """Состояние медиальной опоры с условием"""
    description: str = Field(..., description="Описание состояния медиальной опоры")
    condition: Optional[Condition] = Field(None, description="Условие на состояние медиальной опоры")


class CombinedTraumaParameter(BaseModel):
    """Сочетанная травма с условием"""
    name: str = Field(..., description="Название сочетанной травмы")
    condition: Optional[Condition] = Field(None, description="Условие на сочетанную травму")


class DiagnosisParameters(BaseModel):
    """Параметры диагноза согласно онтологии"""
    # Общие условия на все параметры диагноза
    general_condition: Optional[Condition] = Field(None, description="Общие условия на параметры диагноза")

    # Конкретные параметры с их условиями
    fracture_type: Optional[FractureTypeParameter] = Field(None, description="Тип перелома")
    fracture_location: Optional[FractureLocationParameter] = Field(None, description="Локализация перелома")
    fracture_stability: Optional[FractureStabilityParameter] = Field(None, description="Стабильность перелома")
    fracture_displacement: Optional[FractureDisplacementParameter] = Field(None, description="Смещение перелома")
    medial_support: Optional[MedialSupportParameter] = Field(None, description="Состояние медиальной опоры")
    combined_trauma: Optional[CombinedTraumaParameter] = Field(None, description="Сочетанная травма")

    def get_active_parameters(self) -> List[Dict[str, Any]]:
        """Получить список активных параметров (тех, которые заполнены)"""
        active_params = []

        if self.fracture_type:
            active_params.append({
                "type": "fracture_type",
                "name": self.fracture_type.name,
                "condition": self.fracture_type.condition
            })

        if self.fracture_location:
            active_params.append({
                "type": "fracture_location",
                "description": self.fracture_location.description,
                "condition": self.fracture_location.condition
            })

        if self.fracture_stability:
            active_params.append({
                "type": "fracture_stability",
                "description": self.fracture_stability.description,
                "condition": self.fracture_stability.condition
            })

        if self.fracture_displacement:
            active_params.append({
                "type": "fracture_displacement",
                "description": self.fracture_displacement.description,
                "condition": self.fracture_displacement.condition
            })

        if self.medial_support:
            active_params.append({
                "type": "medial_support",
                "description": self.medial_support.description,
                "condition": self.medial_support.condition
            })

        if self.combined_trauma:
            active_params.append({
                "type": "combined_trauma",
                "name": self.combined_trauma.name,
                "condition": self.combined_trauma.condition
            })

        return active_params
