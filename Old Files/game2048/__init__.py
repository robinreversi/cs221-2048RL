from gym.envs.registration import register

register(
    id='2048-v0',
    entry_point='game2048.game2048_env:Game2048Env',
)