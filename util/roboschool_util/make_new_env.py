from gym.envs.registration import register
import custom_envs.pybulletgym_custom
import gym

def make_array_env(change_variable, name):
    env, env_eval = [], []

    for i in range(len(change_variable)):

        if name == "HopperPyBulletEnv-v0":
            register(
                id='HopperPyBulletEnv-v' + str(i+1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.hopper_env:HopperBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=2500.0
            )

            env.append(gym.make('HopperPyBulletEnv-v' + str(i+1)))
            env_eval.append(gym.make('HopperPyBulletEnv-v' + str(i+1)))

            env[i].reset()
            env_eval[i].reset()

        elif name == "Walker2DPyBulletEnv-v0":

            register(
                id='Walker2DPyBulletEnv-v' + str(i+1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.walker2d_env:Walker2DBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=2500.0
            )

            env.append(gym.make('Walker2DPyBulletEnv-v' + str(i+1)))
            env_eval.append(gym.make('Walker2DPyBulletEnv-v' + str(i+1)))

            env[i].reset()
            env_eval[i].reset()

        elif name == "AntPyBulletEnv-v0":
            register(
                id='AntPyBulletEnv-v' + str(i+1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.ant_env:AntBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=2500.0
            )

            env.append(gym.make('AntPyBulletEnv-v' + str(i+1)))
            env_eval.append(gym.make('AntPyBulletEnv-v' + str(i+1)))

            env[i].reset()
            env_eval[i].reset()

        elif name == 'AtlasPyBulletEnv-v0':
            register(
                id='AtlasPyBulletEnv-v' + str(i + 1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.atlas_env:AtlasBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=2500.0
            )

            env.append(gym.make('AtlasPyBulletEnv-v' + str(i + 1)))
            env_eval.append(gym.make('AtlasPyBulletEnv-v' + str(i + 1)))

            env[i].reset()
            env_eval[i].reset()

        elif name == "HumanoidPyBulletEnv-v0":
            register(
                id="HumanoidPyBulletEnv-v" + str(i + 1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.humanoid_env:HumanoidBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=2500.0
            )

            env.append(gym.make('HumanoidPyBulletEnv-v' + str(i + 1)))
            env_eval.append(gym.make('HumanoidPyBulletEnv-v' + str(i + 1)))

            env[i].reset()
            env_eval[i].reset()

        elif name == "HalfCheetahPyBulletEnv-v0":
            register(
                id="HalfCheetahPyBulletEnv-v" + str(i + 1),
                entry_point='custom_envs.pybulletgym_custom.envs.roboschool.envs.locomotion.half_cheetah_env:HalfCheetahBulletEnv',
                kwargs={'power': change_variable[i]},
                max_episode_steps=1000,
                reward_threshold=3000.0
            )

            env.append(gym.make('HalfCheetahPyBulletEnv-v' + str(i + 1)))
            env_eval.append(gym.make('HalfCheetahPyBulletEnv-v' + str(i + 1)))

            env[i].reset()
            env_eval[i].reset()


    return  env, env_eval



