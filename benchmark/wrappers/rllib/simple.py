# MIT License
#
# Copyright (C) 2021. Huawei Technologies Co., Ltd. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from benchmark.wrappers.rllib.wrapper import Wrapper


class Simple(Wrapper):
    def __init__(self, config):
        super(Simple, self).__init__(config)
        print(f"init simple")
        self.observation_adapter = config["observation_adapter"]
        self.info_adapter = config.get("info_adapter")
        self.reward_adapter = config["reward_adapter"]

    def _get_rewards(self, last_observation, observation, reward):
        print(f"in _get_rewards, simple class")
        res = {}
        for k in observation:
            # print("1714")
            res[k] = self.reward_adapter(last_observation[k], observation[k], reward[k])
            # print("1715")
        return res

    def _get_observations(self, observations):
        print(f"in _get_observations, simple class")
        res = {}
        for k, _obs in observations.items():
            res[k] = self.observation_adapter(_obs)
        return res

    def step(self, agent_actions):
        print(f"in step, simple class")
        observations, rewards, dones, infos = self.env.step(agent_actions)
        # End the episode if agent_actions not valid.
        # Target position behind the current position. x < x_{ego}
        # ego_pos = observations.ego_vehicle_state.position
        #
        # TODO:
        #   Current version supports handling only one agent
        #   done sets to True except for '__all__' in this situation
        action = [
            action
            for _, action in agent_actions.items()
        ]
        pos = [
            obs.ego_vehicle_state.position
            for _, obs in observations.items()
        ]
        cur_position = pos
        anchor_point = action[0]

        assert anchor_point[0]>=0, "anchor point x <0"

        # print(f"cur pos {cur_position}")
        # print(f"anchor point {anchor_point}")

        # dis: [x, y, heading(arc)]
        dis = (anchor_point - cur_position)[0]

        new_dones = dones
        buffer = 0
        # buffer = -10
        if dis[0] < buffer:
            print(f"End episode in advance, ego_position {cur_position}; anchor point {anchor_point}")
            new_dones = {
                    # key: True
                    key: True if val != '__all__' else False
                    for key, val in dones.items()
                }
            print(new_dones)

        infos = self._get_infos(observations, rewards, infos)
        print("start call reward in common")
        rewards = self._get_rewards(self._last_observations, observations, rewards)
        self._update_last_observation(observations)  # it is environment observation
        observations = self._get_observations(observations)
        # return observations, rewards, dones, infos
        return observations, rewards, new_dones, infos

    def reset(self):
        print(f"in reset, simple class")
        obs = self.env.reset()
        self._update_last_observation(obs)
        return self._get_observations(obs)
