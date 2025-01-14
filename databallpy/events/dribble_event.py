from dataclasses import dataclass

import numpy as np
import pandas as pd

from databallpy.events.base_event import BaseOnBallEvent


@dataclass
class DribbleEvent(BaseOnBallEvent):
    """Class for dribble events

    Args:
        event_id (int): distinct id of the event
        period_id (int): id of the period
        minutes (int): minute in which the event occurs
        seconds (int): seconds within the aforementioned minute where the event occurs
        datetime (pd.Timestamp): datetime at which the event occured
        start_x (float): x coordinate of the start location of the event
        start_y (float): y coordinate of the start location of the event
        pitch_size (tuple): size of the pitch in meters.
        team_side (str): side of the team that performed the event, either
            ["home", "away"]
        team_id (int): id of the team that performed the event
        player_id (int): id of the player that performed the event
        related_event_id (int): id of the event that the dribble is related to
        duel_type (str): type of duel that the dribble is related to, either
            ["offensive", "defensive"].
        outcome (bool): whether the dribble was successful or not
        has_opponent (bool): whether the dribble has an opponent in the area or not

    Attributes:
        xT (float): expected threat of the event. This is calculated using a model
            that is trained on the distance and angle to the goal, and the distance
            times the angle to the goal. See the notebook in the notebooks folder for
            more information on the model.
        df_attributes (list[str]): list of attributes that are used to create a
            DataFrame

    Raises:
        TypeError: when one of the input arguments is of the wrong type

    Returns:
        DribbleEvent: Dribble event
    """

    player_id: int
    related_event_id: int
    duel_type: str
    outcome: bool
    has_opponent: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._check_datatypes()
        _ = self._xt

    def __eq__(self, other):
        if not isinstance(other, DribbleEvent):
            return False
        else:
            result = [
                super().__eq__(other),
                self.player_id == other.player_id,
                self.related_event_id == other.related_event_id,
                self.duel_type == other.duel_type
                if not pd.isnull(self.duel_type)
                else pd.isnull(other.duel_type),
                self.outcome == other.outcome,
                self.has_opponent == other.has_opponent,
            ]
            return all(result)

    @property
    def df_attributes(self) -> list[str]:
        base_attributes = super().base_df_attributes
        return base_attributes + [
            "player_id",
            "related_event_id",
            "duel_type",
            "outcome",
            "has_opponent",
        ]

    def copy(self):
        return DribbleEvent(
            event_id=self.event_id,
            period_id=self.period_id,
            minutes=self.minutes,
            seconds=self.seconds,
            datetime=self.datetime,
            start_x=self.start_x,
            start_y=self.start_y,
            pitch_size=self.pitch_size,
            team_side=self.team_side,
            _xt=self._xt,
            team_id=self.team_id,
            player_id=self.player_id,
            related_event_id=self.related_event_id,
            duel_type=self.duel_type,
            outcome=self.outcome,
            has_opponent=self.has_opponent,
        )

    def _check_datatypes(self):
        if not isinstance(self.player_id, (int, np.integer, str)):
            raise TypeError(
                f"player_id should be int, got {type(self.player_id)} instead"
            )
        if not isinstance(self.related_event_id, (int, np.integer)):
            raise TypeError(
                f"related_event_id should be int, got {type(self.related_event_id)} "
                "instead"
            )
        if not isinstance(self.duel_type, (str, type(None))):
            raise TypeError(
                f"duel_type should be str, got {type(self.duel_type)} instead"
            )
        if not isinstance(self.outcome, (bool, type(None))):
            raise TypeError(f"outcome should be bool, got {type(self.outcome)} instead")
