"""Action Functions

Helper functions that perform different actions on a bridge
"""

def turn_off(bridge, groups):
    """Turn off lights

    Parameters
    ----------
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    """
    for grp in groups:
        if grp.isdigit():
            grp = int(grp)
        bridge.off(grp)

def turn_on(bridge, groups):
    """Turn on lights

    Parameters
    ----------
    bridge: mookfist_lled_controller.WifiBridge
    groups: list
    """
    for grp in groups:

        if grp.isdigit():
            grp = int(grp)

        bridge.on(int(grp))

def white(bridge, groups):
    """Turn on the white light

    Parameters
    ----------
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    """
    for grp in groups:

        if grp.isdigit():
            grp = int(grp)

        bridge.white(grp)

def transition_brightness(bridge, groups, start, end):
    """Transition the brightness of the selected groups

    Parameters
    ----------
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    start : int
    end : int
    """

    if start > end:
        cmds = list(reversed(range(end, start)))
    else:
        cmds = range(start, end)


    for cmd in cmds:
        for grp in groups:
            if grp.isdigit():
                grp = int(grp)
            bridge.brightness(cmd, grp)


def transition_color(bridge, groups, start, end):
    """Transition the color of the selected groups

    Parameters
    ----------
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    start : int
    end : int
    """
    if start > end:
        cmds = list(reversed(range(end, start)))
    else:
        cmds = range(start, end)

    for cmd in cmds:
        for grp in groups:
            if grp.isdigit():
                grp = int(grp)
            bridge.color(cmd, grp)


def set_color(bridge, groups, color):
    """Set the color of the selected groups

    Parameters:
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    color : int
    """
    for grp in groups:
        if grp.isdigit():
            grp = int(grp)
        bridge.color(color, grp)

def color_rgb(bridge, groups, r, g, b):
    """Set the color of selected groups using red/green/blue values

    Parameters:
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    r : int
    b : int
    g : int
    """
    for grp in groups:
        if grp.isdigit():
            grp = int(grp)
        bridge.color_rgb(r, g, b, grp)

def set_brightness(bridge, groups, brightness):
    """Set the brightness of the selected groups

    Parameters:
    bridge : mookfist_lled_controller.WifiBridge
    groups : list
    brightnes: int
    """
    for grp in groups:
        if grp.isdigit():
            grp = int(grp)
        bridge.brightness(brightness, grp)

