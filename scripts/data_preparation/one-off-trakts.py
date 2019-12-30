import pandas as pd


def read_campus_csv_list():
    df = pd.read_csv('gebauede-tu-juli-2019.csv', header=None,
                     names=["CAMPUS", "TRAKT", "TRAKTBEZEICHNUNG", "ADRESSE", "PLZ", "ORT", "GESCHOSS"], delimiter=";")
    # print(df.groupby('TRAKT').groups)

    grouped_campus = df.groupby('CAMPUS')
    grouped_trakt = df.groupby('TRAKT')
    grouped_adresse = df.groupby('ADRESSE')
    grouped_floors = df.groupby('GESCHOSS')

    campuses = [name for name, group in grouped_campus]
    print(campuses)
    trakts = [name for name, group in grouped_trakt]
    adresse = [name for name, group in grouped_adresse]
    floors = [name for name, group in grouped_floors]

    # print("floors", len(floors), floors)
    # print("campuses", len(campuses))
    print("trakts", len(trakts))
    # print("adresse", len(adresse))

    m = []



    for floor in floors:
        c = df[df['GESCHOSS'].str.contains(floor)]
        f = {}
        trak = c.groupby('TRAKT')
        trakts = [name for name, group in trak]
        print("Floor;", floor, ";TRACKTS;", trakts, ";count;", len(trakts))
        f['floor'] = floor
        f['traks'] = trakts
        m.append(f)

    print(m)

read_campus_csv_list()

ftraks = [{'floor': '01', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HL', 'MG', 'MH', 'OA', 'OB', 'OC', 'OY', 'OZ', 'QA', 'ZA', 'ZB', 'ZC']}, {'floor': '02', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AP', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'OA', 'OB', 'OY', 'OZ', 'QA', 'WA', 'WB', 'WC', 'WD']}, {'floor': '03', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HK', 'OB', 'OY', 'OZ', 'WB', 'WC', 'WD']}, {'floor': '04', 'traks': ['AA', 'AB', 'AC', 'AD', 'AK', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'FB', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HK', 'HL']}, {'floor': '05', 'traks': ['BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'CA', 'CB', 'CD', 'CG', 'DA', 'DB', 'DC', 'DD', 'DF', 'EA', 'FB', 'HA', 'HB', 'HC', 'HD', 'HF', 'HG']}, {'floor': '06', 'traks': ['BA', 'BB', 'BD', 'BE', 'BI', 'CA', 'CB', 'CD', 'CG', 'DA', 'DB', 'DC', 'DD', 'DF']}, {'floor': '07', 'traks': ['BA', 'BD', 'BI', 'DA', 'DB', 'DC', 'DD', 'GA']}, {'floor': '08', 'traks': ['BA', 'BI', 'DA', 'DB', 'DC']}, {'floor': '09', 'traks': ['BA', 'BI', 'DA', 'DB']}, {'floor': '10', 'traks': ['BA', 'BI', 'DB']}, {'floor': '11', 'traks': ['BA', 'DB']}, {'floor': '12', 'traks': ['DB']}, {'floor': 'DG', 'traks': ['AB', 'AC', 'AF', 'AG', 'BA', 'BD', 'BE', 'BI', 'BZ', 'CF', 'CG', 'CI', 'DD', 'DE', 'EA', 'EB', 'EC', 'GA', 'ZA', 'ZB', 'ZC']}, {'floor': 'EG', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AK', 'AP', 'AQ', 'AS', 'AT', 'BA', 'BB', 'BC', 'BD', 'BE', 'BH', 'BI', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'FC', 'GA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HK', 'MA', 'MB', 'MC', 'MD', 'MG', 'MH', 'MI', 'OA', 'OB', 'OC', 'OY', 'OZ', 'PF', 'QA', 'WA', 'WB', 'WD', 'ZA', 'ZB', 'ZC', 'ZD']}, {'floor': 'SO', 'traks': ['CF']}, {'floor': 'U1', 'traks': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AI', 'AK', 'AP', 'AQ', 'AS', 'BA', 'BB', 'BC', 'BD', 'BE', 'BG', 'BH', 'BI', 'BK', 'BL', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CF', 'CG', 'CH', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'EA', 'EB', 'EC', 'FA', 'FB', 'FC', 'GA', 'MD', 'OA', 'OB', 'OC', 'OY', 'OZ', 'QA', 'WA', 'WB', 'WC', 'WD', 'ZA', 'ZB', 'ZC', 'ZD']}, {'floor': 'U2', 'traks': ['AE', 'BA', 'BC', 'BD', 'BG', 'BI', 'BK', 'BL', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'DA', 'DB', 'DC', 'DD', 'DE', 'EB', 'GA', 'OY', 'OZ', 'WA', 'ZA', 'ZB']}, {'floor': 'U3', 'traks': ['DA', 'DB', 'DC', 'DD', 'DE']}, {'floor': 'U4', 'traks': ['DA', 'DB', 'DC']}, {'floor': 'Z1', 'traks': ['AA', 'AC', 'AE']}, {'floor': 'Z2', 'traks': ['AC', 'AF', 'AG', 'CF']}, {'floor': 'Z3', 'traks': ['AA', 'AC', 'AE']}, {'floor': 'Z4', 'traks': ['AC', 'BB']}, {'floor': 'Z5', 'traks': ['BB']}, {'floor': 'ZD', 'traks': ['AF']}, {'floor': 'ZE', 'traks': ['AA', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AK', 'CD', 'DE', 'EA', 'FA', 'FB', 'FC', 'OC', 'QA']}, {'floor': 'ZU', 'traks': ['AE', 'AP', 'BA', 'ZD']}]


    # for campus in campuses:
    #     if campus != 'CAMPUS':
    #         c = df[df['CAMPUS'].str.contains(campus)]
    #         print(campus, len(c))
    #
    #         trak = c.groupby('TRAKT')
    #         trakts = [name for name, group in trak]
    #         print("TRACKTS ", trakts, " count: ", len(trakts))
    #
    #         gp_floors = c.groupby('GESCHOSS')
    #         floors = [name for name, group in gp_floors]
    #         print(f"FLOORS on {campus} campus ", floors, " count: ", len(floors))
    #
    #         address = c.groupby('ADRESSE')
    #         adresses = [name for name, group in address]
    #         print("adresses ", " count : ", len(adresses), " adresses ", adresses)
    #
    #         for a in adresses:
    #             t = df[df['ADRESSE'].str.contains(a)]
    #
    #             gp2_floors = t.groupby('GESCHOSS')
    #             floors2 = [name for name, group in gp2_floors]
    #
    #             x = t.groupby('TRAKT')
    #             tt = [name for name, group in x]
    #             print("address-new ", a, " tracks at this address ", tt, " floors ", floors2)
