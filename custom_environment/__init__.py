import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)


register(id ='customenv-v0',
         entry_point ='custom_environment.envs:Customenv'
         )
