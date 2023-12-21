from archivesorter.database.models import FileInfo


def evaluate_category(info: FileInfo) -> str:
    cat = ''
    lower_path = info.source_path.lower()
    if any([x in lower_path for x in ['biber', 'bieber']]):
        cat += 'Biber'
    if any(
        [
            x in lower_path
            for x in ['wiwoe', 'wiwö', 'wichtel', 'wölflinge', 'woelflinge']
        ]
    ):
        cat += 'WiWö'
    if any(
        [
            x in lower_path
            for x in ['gusp', 'guide', 'spaeher', 'späher', 'geilstestufe']
        ]
    ):
        cat += 'GuSp'
    if any([x in lower_path for x in ['caex', 'cavelier', 'explorer']]):
        cat += 'CaEx'
    if any([x in lower_path for x in ['raro', 'ranger', 'rover']]):
        cat += 'RaRo'
    if cat == '':
        cat = 'Gruppe'
    cat += '/'
    if any(
        [x in lower_path for x in ['sola', 'sommerlager', 'sommerla', 'sommer lager']]
    ):
        cat += 'SoLa'
    elif any(
        [
            x in lower_path
            for x in [
                'wola',
                'wochenendla',
                'wochenendlager',
                'wochenendelager',
                'wochendend lager',
                'woela',
            ]
        ]
    ):
        cat += 'WoLa'
    elif any(
        [
            x in lower_path
            for x in ['pfila', 'pfingsten', 'pfingstlager', 'pfingst lager']
        ]
    ):
        cat += 'PfiLa'
    elif any([x in lower_path for x in ['halloweenlager', 'halloween lager']]):
        cat += 'HalloweenLager'
    elif any(
        [x in lower_path for x in ['bezirksaktion', 'bezirks aktion', 'bezirk aktion']]
    ):
        cat += 'Bezirksaktion'
    elif any(
        [
            x in lower_path
            for x in [
                'xl-heimabend',
                'xlarge-heimabend',
                'xl-heimstunde',
                'xl heimabend',
                'xl heimstunde',
            ]
        ]
    ):
        cat += 'XL-Heimstunde'
    elif any(
        [
            x in lower_path
            for x in ['heimstunde', 'heimabend', 'heim stunde', 'heim abend']
        ]
    ):
        cat += 'Heimstunden'
    else:
        cat += 'Divers'
    return cat


def compute_target_path(info: FileInfo) -> str:
    ...
