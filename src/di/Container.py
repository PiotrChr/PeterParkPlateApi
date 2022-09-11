from dependency_injector import containers, providers
from src.infrastructure.db.Database import Database
from src.infrastructure.repository.PlateRepository import PlateRepository
from src.services.PlateService import PlateService
from src.delivery.mapper.PlateMapper import PlateMapper
from src.delivery.validation.PlateValidator import PlateValidator

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(modules=[
        'src.delivery.api'
    ])

    db = providers.Singleton(
        Database,
        db_host=config.db_host,
        db_name=config.db_name,
        db_user=config.db_user,
        db_pass=config.db_pass
    )

    plate_mapper = providers.Singleton(PlateMapper)

    plate_validator = providers.Singleton(PlateValidator)

    plate_repository = providers.Factory(
        PlateRepository,
        session_factory=db.provided.session
    )

    plate_service = providers.Factory(
        PlateService,
        plate_repository=plate_repository
    )


