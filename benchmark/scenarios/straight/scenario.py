from pathlib import Path
import random
from smarts.sstudio import types as t
from smarts.sstudio import gen_scenario

# trajectory_boid_agent = t.BoidAgentActor(
#     name="trajectory-boid",
#     agent_locator="scenarios.straight.agent_prefabs:trajectory-boid-agent-v0",
# )
#
# pose_boid_agent = t.BoidAgentActor(
#     name="pose-boid",
#     agent_locator="scenarios.straight.agent_prefabs:pose-boid-agent-v0",
# )

act1 = t.TrafficActor(name="car1", speed = t.Distribution(mean=2, sigma=5), min_gap = t.Distribution(mean=2.5, sigma=0),
                      vehicle_type=random.choice(["passenger", "bus", "coach", "truck", "trailer"]))
act2 = t.TrafficActor(name="car2", speed = t.Distribution(mean=2, sigma=1), min_gap = t.Distribution(mean=2.5, sigma=0.2),
                      vehicle_type=random.choice(["passenger", "bus", "coach", "truck", "trailer"]))

traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("west", lane_idx, "random"), end=("east", lane_idx, "max"),),
            # route=t.Route(begin=("west", lane_idx, 10), end=("east", lane_idx, "max"),),
            # route=t.RandomRoute(),
            # rate=50,
            # end = 10 * 60 * 60,
            end = 1001,
            rate= 10,
            # actors={t.TrafficActor("car"): 1},
            actors={act1: 0.5, act2: 0.5},
            # actors={t.TrafficActor(name="car", speed = t.Distribution(mean=1.0, sigma=0), min_gap = t.Distribution(mean=2.5, sigma=0)): 1},
        )
        for lane_idx in range(3)
    ]
)

missions = [
    # t.Mission(t.Route(begin=("west", 1, 10), end=("east", 1, 90))),
    t.Mission(t.Route(begin=("west", 1, 5), end=("east", 0, "max"))),
]

scenario = t.Scenario(
    traffic={"all": traffic},
    ego_missions=missions,
    # bubbles=[
    #     t.Bubble(
    #         zone=t.PositionalZone(pos=(50, 0), size=(40, 20)),
    #         margin=5,
    #         actor=trajectory_boid_agent,
    #     ),
    #     t.Bubble(
    #         zone=t.PositionalZone(pos=(150, 0), size=(50, 20)),
    #         margin=5,
    #         actor=pose_boid_agent,
    #         keep_alive=True,
    #     ),
    # ],
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent))
