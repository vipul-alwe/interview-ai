from app.domain.competency_catalog import (
    COMPETENCY_CATALOG,
    CompetencyCatalogEntry,
)


class CompetencyRegistry:

    def __init__(self):
        self._competencies: dict[
            str,
            CompetencyCatalogEntry,
        ] = {
            competency.id: competency
            for competency in COMPETENCY_CATALOG
        }

    def get(
        self,
        competency_id: str,
    ) -> CompetencyCatalogEntry | None:

        return self._competencies.get(
            competency_id
        )

    def all(
        self,
    ) -> list[CompetencyCatalogEntry]:

        return list(
            self._competencies.values()
        )

    def ids(self) -> list[str]:

        return list(
            self._competencies.keys()
        )

    def count(self) -> int:

        return len(self._competencies)


competency_registry = CompetencyRegistry()