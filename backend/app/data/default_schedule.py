# Default schedule blocks - migrated from scheduler.py
# All times are in America/New_York timezone

DEFAULT_BLOCKS = {
    "monday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "pause.py"),
        ],
        "DAY": [
            ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "65fm.py"), ("12:45", "65sm.py"),
            ("13:00", "75TIGS.py"), ("13:15", "65sm.py"), ("13:30", "70fm.py"), ("13:45", "70sm.py"),
            ("14:00", "70parking.py"), ("14:15", "75TIGS.py"), ("14:30", "70fm.py"), ("14:45", "70sm.py"),
            ("15:00", "75fm.py"), ("15:15", "75sm.py"), ("15:30", "75fm.py"), ("15:45", "75TIGS.py"),
            ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75fm.py"), ("16:45", "75sm.py"),
            ("17:00", "75parking.py"), ("17:15", "75sm.py"), ("17:30", "75fm.py"),
        ],
        "PM_FIRE": [
            ("17:45", "75fireparking.py"), ("18:00", "75fireparking.py"), ("18:50", "75adfire.py"),
            ("19:00", "75fireparking.py"), ("19:50", "75adfire.py"),
            ("20:00", "75fireparking.py"), ("20:50", "75adfire.py"),
            ("21:00", "75fireparking.py"), ("21:50", "75adfire.py"),
            ("22:00", "75fireparking.py"), ("22:50", "75adfire.py"),
            ("23:00", "75fireparking.py"),
        ],
    },

    "tuesday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "65fm.py"), ("11:15", "65sm.py"), ("11:30", "65fm.py"), ("11:45", "65sm.py"),
            ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "65fm.py"), ("12:45", "65sm.py"),
            ("13:00", "65parking.py"), ("13:15", "75TIGS.py"), ("13:30", "65fm.py"), ("13:45", "65sm.py"),
            ("14:00", "65parking.py"), ("14:15", "65sm.py"), ("14:30", "70fm.py"), ("14:45", "70sm.py"),
            ("15:00", "70parking.py"), ("15:15", "70sm.py"), ("15:30", "75TIGS.py"), ("15:45", "70sm.py"),
            ("16:00", "75parking.py"), ("16:15", "75sm.py"), ("16:30", "75TIGS.py"), ("16:45", "75sm.py"),
            ("17:00", "75parking.py"), ("17:15", "75sm.py"), ("17:30", "75TIGS.py"),
        ],
        "PM_FIRE": [
            ("17:45", "75fireparking.py"), ("18:00", "75fireparking.py"), ("18:50", "75adfire.py"),
            ("19:00", "75fireparking.py"), ("19:50", "75adfire.py"),
            ("20:00", "75fireparking.py"), ("20:50", "75adfire.py"),
            ("21:00", "75fireparking.py"), ("21:50", "75adfire.py"),
            ("22:00", "75fireparking.py"), ("22:50", "75adfire.py"),
            ("23:00", "75fireparking.py"),
        ],
    },

    "wednesday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "65fm.py"), ("11:15", "65sm.py"), ("11:30", "75TIGS.py"), ("11:45", "65sm.py"),
            ("12:00", "65fm.py"), ("12:15", "65sm.py"), ("12:30", "75TIGS.py"), ("12:45", "65sm.py"),
            ("13:00", "65parking.py"), ("13:15", "65sm.py"), ("13:30", "65fm.py"), ("13:45", "65sm.py"),
            ("14:00", "75TIGS.py"), ("14:15", "65sm.py"), ("14:30", "65fm.py"), ("14:45", "70sm.py"),
            ("15:00", "70parking.py"), ("15:15", "70sm.py"), ("15:30", "75TIGS.py"), ("15:45", "70sm.py"),
            ("16:00", "70parking.py"), ("16:15", "70sm.py"), ("16:30", "75TIGS.py"), ("16:45", "75sm.py"),
            ("17:00", "80parking.py"), ("17:15", "80sm.py"), ("17:30", "80fm.py"),
        ],
        "PM_FIRE": [
            ("17:45", "75fireparking.py"), ("18:00", "75fireparking.py"), ("18:50", "75adfire.py"),
            ("19:00", "75fireparking.py"), ("19:50", "75adfire.py"),
            ("20:00", "75fireparking.py"), ("20:50", "75adfire.py"),
            ("21:00", "75fireparking.py"), ("21:50", "75adfire.py"),
            ("22:00", "75fireparking.py"), ("22:50", "75adfire.py"),
            ("23:00", "75fireparking.py"),
        ],
    },

    "thursday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "75TIGS.py"), ("11:15", "75sm.py"), ("11:30", "75fm.py"), ("11:45", "75sm.py"),
            ("12:00", "75parking.py"), ("12:15", "75TIGS.py"), ("12:30", "75fm.py"), ("12:45", "75sm.py"),
            ("13:00", "75TIGS.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
            ("14:00", "75parking.py"), ("14:15", "75sm.py"), ("14:30", "75TIGS.py"), ("14:45", "75sm.py"),
            ("15:00", "80parking.py"), ("15:15", "80sm.py"), ("15:30", "80fm.py"), ("15:45", "80sm.py"),
            ("16:00", "80parking.py"), ("16:15", "80sm.py"), ("16:30", "80fm.py"), ("16:45", "80sm.py"),
            ("17:00", "80parking.py"), ("17:15", "80ad.py"), ("17:30", "80fm.py"),
        ],
        "PM_FIRE": [
            ("17:45", "85fireparking.py"), ("18:00", "85fireparking.py"), ("18:50", "85adfire.py"),
            ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
            ("20:00", "85fireparking.py"), ("20:50", "85adfire.py"),
            ("21:00", "85fireparking.py"), ("21:50", "85adfire.py"),
            ("22:00", "85fireparking.py"), ("22:50", "85adfire.py"),
            ("23:00", "85fireparking.py"),
        ],
    },

    "friday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "65parking.py"), ("02:15", "50sm.py"), ("02:30", "50sm.py"), ("02:45", "50sm.py"),
            ("03:00", "65parking.py"), ("03:15", "50sm.py"), ("03:30", "50sm.py"), ("03:45", "50sm.py"),
            ("04:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "75fm.py"), ("11:15", "75sm.py"), ("11:30", "75TIGS.py"), ("11:45", "75sm.py"),
            ("12:00", "75fm.py"), ("12:15", "75sm.py"), ("12:30", "75fm.py"), ("12:45", "75TIGS.py"),
            ("13:00", "75parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
            ("14:00", "75parking.py"), ("14:15", "75TIGS.py"), ("14:30", "75fm.py"), ("14:45", "75sm.py"),
            ("15:00", "80parking.py"), ("15:15", "80sm.py"), ("15:30", "80fm.py"), ("15:45", "80sm.py"),
            ("16:00", "90parking.py"), ("16:15", "90ad.py"), ("16:30", "90fm.py"), ("16:45", "90sm.py"),
            ("17:00", "90parking.py"), ("17:15", "90ad.py"), ("17:30", "90fm.py"),
        ],
        "PM_FIRE": [
            ("17:45", "85fireparking.py"), ("18:00", "85fireparking.py"), ("18:50", "85adfire.py"),
            ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
            ("20:00", "85fireparking.py"), ("20:50", "85adfire.py"),
            ("21:00", "85fireparking.py"), ("21:50", "85adfire.py"),
            ("22:00", "85fireparking.py"), ("22:50", "85adfire.py"),
            ("23:00", "85fireparking.py"),
        ],
    },

    "saturday": {
        "AM": [
            ("00:00", "70parking.py"),
            ("00:15", "70sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "65sm.py"), ("02:15", "65sm.py"), ("02:30", "65sm.py"), ("02:45", "65sm.py"),
            ("03:00", "65parking.py"), ("03:15", "65sm.py"), ("03:30", "65sm.py"), ("03:45", "65sm.py"),
            ("04:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "75fm.py"), ("11:15", "75sm.py"), ("11:30", "75parking.py"), ("11:45", "75sm.py"),
            ("12:00", "75parking.py"), ("12:15", "75sm.py"), ("12:30", "75fm.py"), ("12:45", "75sm.py"),
            ("13:00", "75parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
            ("14:00", "75parking.py"), ("14:15", "75sm.py"), ("14:30", "75ad.py"), ("14:45", "75sm.py"),
            ("15:00", "75parking.py"), ("15:15", "75sm.py"), ("15:30", "75ad.py"), ("15:45", "75sm.py"),
        ],
        "PM_FIRE": [
            ("16:10", "85fireparking.py"), ("18:00", "85fireparking.py"), ("18:50", "85adfire.py"),
            ("19:00", "85fireparking.py"), ("19:50", "85adfire.py"),
            ("20:00", "85fireparking.py"), ("20:50", "85adfire.py"),
            ("21:00", "85fireparking.py"), ("21:50", "85adfire.py"),
            ("22:00", "85fireparking.py"), ("22:50", "85adfire.py"),
            ("23:00", "85fireparking.py"),
        ],
    },

    "sunday": {
        "AM": [
            ("00:00", "65parking.py"), ("00:15", "65sm.py"), ("00:30", "65sm.py"), ("00:45", "65sm.py"),
            ("01:00", "65parking.py"), ("01:15", "65sm.py"), ("01:30", "65sm.py"), ("01:45", "65sm.py"),
            ("02:00", "pause.py"),
        ],
        "DAY": [
            ("11:00", "70fm.py"), ("11:15", "70sm.py"), ("11:30", "70parking.py"), ("11:45", "70sm.py"),
            ("12:00", "70fm.py"), ("12:15", "70sm.py"), ("12:30", "70fm.py"), ("12:45", "70sm.py"),
            ("13:00", "70parking.py"), ("13:15", "75sm.py"), ("13:30", "75fm.py"), ("13:45", "75sm.py"),
            ("14:00", "75parking.py"), ("14:15", "80sm.py"), ("14:30", "80fm.py"), ("14:45", "80sm.py"),
            ("15:00", "85parking.py"), ("15:15", "85ad.py"), ("15:30", "85fm.py"), ("15:45", "85fm.py"),
            ("16:00", "85parking.py"), ("16:15", "85sm.py"), ("16:30", "85sm.py"), ("16:45", "85ad.py"),
            ("17:00", "85parking.py"), ("17:15", "85sm.py"), ("17:30", "85sm.py"),
        ],
        "PM_FIRE": [
            ("17:45", "85fireparking.py"), ("18:00", "85fireparking.py"), ("18:50", "80adfire.py"),
            ("19:00", "85fireparking.py"), ("19:50", "80adfire.py"),
            ("20:00", "75fireparking.py"), ("20:50", "75adfire.py"),
            ("21:00", "75fireparking.py"), ("21:50", "75adfire.py"),
            ("22:00", "75fireparking.py"), ("22:50", "75adfire.py"),
            ("23:00", "75fireparking.py"),
        ],
    },
}
