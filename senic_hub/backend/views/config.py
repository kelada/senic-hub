from time import sleep

from cornice.service import Service

from ..commands import create_nuimo_app_cfg
from ..config import path
from ..supervisor import stop_program
from .api_descriptions import descriptions as desc
from cornice.validators import colander_body_validator
import subprocess
import logging

logger = logging.getLogger(__name__)

configuration_service = Service(
    name='configuration',
    path=path('config'),
    description=desc.get('configuration_service'),
    renderer='json',
    accept='application/json',
)


@configuration_service.post(validators=(colander_body_validator,))
def post_configuration(request):

    logger.info("Stopping device discovery")
    stop_program('device_discovery')

    create_nuimo_app_cfg(request.registry.settings)

    # Wait for Nuimo App to restart and connect to Nuimo
    # TODO: Add D-Bus interface to Nuimo and wait for its ready signal
    sleep(10.0)


@configuration_service.delete()
def delete_configuration(request):
    subprocess.Popen(['/usr/bin/senic_hub_factory_reset'])
