import ghostV2, ghostV1
def _init(level):
    ghosts = [
        ghostV2.Ghost("Spirit", [1.7], level, ["EMF5, SpiritBox, Writing"], ["doubleSafeDur"], 50, 50),
        ghostV2.Ghost("Wraith", [1.7], level, ["EMF5, SpiritBox, DOTs"], ["teleport", "noFootstep"], 50, 50),
        ghostV2.Ghost("Jinn", [1.7, 2.5], level, ["EMF5, SpiritBox, DOTs"], "doubleSafeDur", 50, 50),
    ]
