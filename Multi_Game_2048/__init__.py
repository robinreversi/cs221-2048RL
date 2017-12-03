from gym.envs.registration import register

register(
    id='Multi2048-v0',
    entry_point='Multi_Game_2048.Multi_Game_2048_env:MultiGame2048Env',
)