unique_floor_map = [    {'name': 'u1_0', 'number': -1.0, 'letter': 'U1'},
                        {'name': '0_0', 'number': 0.0, 'letter': 'EG'},
                        {'name': '1_0', 'number': 1.0, 'letter': '01'},
                        {'name': '2_0', 'number': 2.0, 'letter': '02'},
                        {'name': '9999_0', 'number': 9999.0, 'letter': 'DG'}]

def get_floor_float(name):
    """
    assuming input name is like "DA_EG_03_2019.dxf"
    :param name: dxf file name like "DA_EG_03_2019.dxf"
    :return: float value of floor
    """

    floor_names_odd = ['ZD', 'ZE', 'ZU', 'DG', 'EG', 'SO', 'SOU']
    floor_names_u = ['U1', 'U2', 'U3', 'U4']
    floor_names_z = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']
    floor_names_int = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    if not name:
        return name
    # floor = name.split("_")[-3]

    floor = name.upper()

    if floor in floor_names_odd:
        if floor == "EG":
            floor = 0.0
        elif floor == "SO":
            floor = -0.5
        elif floor == "SOU":
            floor = -0.5
        elif floor == "ZE":
            floor = 0.5
        elif floor == "ZU":
            floor = -1.5
        elif floor == "ZD":
            floor = 7777
        elif floor == "DG":
            floor = 9999.0
        else:
            floor = 8888.0
    elif floor in floor_names_z:
        # zwischen stock
        floor = float(floor[1])*1.0 + 0.5

    elif floor in floor_names_int:
        floor = float(floor)*1.0

    elif floor.upper().startswith("U"):
        # underground
        floor = float(floor[1]) * -1.0
    else:
        floor = 4444.0

    return floor*1.0
