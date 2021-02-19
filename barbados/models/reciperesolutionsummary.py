from barbados.models.base import BarbadosModel
from sqlalchemy import Column, JSON, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID


class RecipeResolutionSummaryModel(BarbadosModel):
    __tablename__ = 'reciperesolutionsummary'

    id = Column(String, primary_key=True)
    inventory_id = Column(UUID(as_uuid=True), nullable=False)
    cocktail_slug = Column(String, nullable=False)
    spec_slug = Column(String, nullable=False)
    components = Column(JSON, nullable=False)
    component_count = Column(Integer, nullable=False)
    alpha = Column(String, nullable=False)
    construction_slug = Column(String, nullable=False)
    citations = Column(JSON, nullable=False)
    garnish = Column(JSON, nullable=False)
    status_count = Column(JSON, nullable=False)
    generated_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return "<Barbados::Models::RecipeResolutionSummaryModel[%s]>" % self.id
