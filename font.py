import pygame as pg
from settings import that_final_thingy, font


def get_numbers_on_a_special_tablet_so_it_looks_cool_sorry_for_the_bad_name(n):
    try:
        n = str(int(n) if n > 0 else 0)
    except (ValueError, TypeError):
        pass

    left_part = that_final_thingy.subsurface(pg.Rect(80, 0, 9, 16))
    middle_part = that_final_thingy.subsurface(pg.Rect(90, 0, 1, 16))
    right_part = that_final_thingy.subsurface(pg.Rect(92, 0, 9, 16))

    total_width = 0
    nums = []

    for c in n:
        img = get_char_in_font(c)
        total_width += img.get_width()
        nums.append(img)

    tablet = pg.Surface((total_width+12, 16), pg.SRCALPHA)

    tablet.blit(left_part, (0, 0))
    tablet.blit(right_part, (total_width+3, 0))

    for i in range(total_width-4):
        tablet.blit(middle_part, (9+i, 0))

    pos = [6, 6]
    for n in nums:
        tablet.blit(n, pos)
        pos[0] += n.get_width()

    return tablet



def get_char_in_font(n):
    if n == "1":
        return font.subsurface(0, 0, 4, 5)
    elif n == "2":
        return font.subsurface(5, 0, 5, 5)
    elif n == "3":
        return font.subsurface(11, 0, 5, 5)
    elif n == "4":
        return font.subsurface(17, 0, 5, 5)
    elif n == "5":
        return font.subsurface(23, 0, 5, 5)
    elif n == "6":
        return font.subsurface(29, 0, 5, 5)
    elif n == "7":
        return font.subsurface(35, 0, 5, 5)
    elif n == "8":
        return font.subsurface(41, 0, 5, 5)
    elif n == "9":
        return font.subsurface(47, 0, 5, 5)
    elif n == "0":
        return font.subsurface(53, 0, 5, 5)
    elif n == ".":
        return font.subsurface(59, 0, 2, 5)
    elif n == "d":
        return font.subsurface(62, 0, 5, 5)
    elif n == "h":
        return font.subsurface(68, 0, 5, 5)
    elif n == "m":
        return font.subsurface(74, 0, 6, 5)
    elif n == "s":
        return font.subsurface(81, 0, 5, 5)
    elif n == " ":
        return pg.Surface((5, 5), pg.SRCALPHA)


def get_time_str(sec):
    if sec > (60*60*24*10) + (60*60*12) + (60*30) + 30:  # my time limit
        sec = (60*60*24*10) + (60*60*12) + (60*30) + 30

    minutes = sec//60
    sec = round(sec - minutes*60, 2)

    hours = minutes//60
    minutes = round(minutes - hours*60)

    days = hours//24
    hours = round(hours - days*24)

    time = (" ".join([i for i in [(str(days)+"d") if days > 0 else "",
                     (str(hours)+"h") if hours > 0 else "",
                     (str(minutes)+"m") if minutes > 0 else "",
                     (str(sec)+"s") if sec > 0 else ""] if i != ""]))

    if time == "":
        time = "0s"

    return time
