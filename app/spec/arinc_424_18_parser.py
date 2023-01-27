
ARINC_FIELD_NAME=0
ARINC_FIELD_WIDTH=1
FIELD_REFERENCE=2

SECTION_CODE='section_code'
SUBSECTION_CODE='subsection_code'

IGNORE=['blank','reserved']

SQL_DEF=0
SQL_TABLE=0
ADDITIONAL_SQL_LIST=1

ARINC_424_PARSE_DEF = {
    ' ':
    [
        ('ST',1,'0'),
        ('CUST',3,'0'),
        ('section_code',1,'0'),
    ],
    'A': {
        'S': # (AS) Supported // Grid MORA
        [
            ('MORA',[]),
            ('record_type',1,'5.2'),
            ('blank',3,'0'),
            ('section_code',1,'5.4'),
            ('subsection_code',1,'5.5'),
            ('blank',7,'0'),
            ('latitude',3,'5.141'),
            ('longitude',4,'5.142'),
            ('blank',10,'0'),
            ('MORA1',3,'5.143'),
            ('MORA2',3,'5.143'),
            ('MORA3',3,'5.143'),
            ('MORA4',3,'5.143'),
            ('MORA5',3,'5.143'),
            ('MORA6',3,'5.143'),
            ('MORA7',3,'5.143'),
            ('MORA8',3,'5.143'),
            ('MORA9',3,'5.143'),
            ('MORA10',3,'5.143'),
            ('MORA11',3,'5.143'),
            ('MORA12',3,'5.143'),
            ('MORA13',3,'5.143'),
            ('MORA14',3,'5.143'),
            ('MORA15',3,'5.143'),
            ('MORA16',3,'5.143'),
            ('MORA17',3,'5.143'),
            ('MORA18',3,'5.143'),
            ('MORA19',3,'5.143'),
            ('MORA20',3,'5.143'),
            ('MORA21',3,'5.143'),
            ('MORA22',3,'5.143'),
            ('MORA23',3,'5.143'),
            ('MORA24',3,'5.143'),
            ('MORA25',3,'5.143'),
            ('MORA26',3,'5.143'),
            ('MORA27',3,'5.143'),
            ('MORA28',3,'5.143'),
            ('MORA29',3,'5.143'),
            ('MORA30',3,'5.143'),
            ('reserved',3,'0'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32')
        ]
    },
    'D':{
        ' ': # (D) Supported // VHF Navaid
        [
            ('VOR',[]),
            ('record_type',1,'5.2'), # 5.2
            ('area_code',3,'5.3'), # 5.3
            ('section_code',1,'5.4'), # 5.4
            ('subsection_code',1,'5.5'), # 5.5
            ('ICAO_id',4,'5.6'), # 5.4
            ('ICAO_region_code',2,'5.14'), # 5.14
            ('blank',1,'0'),  
            ('VOR_id',4,'5.33'), # 5.33
            ('blank',2,'0'),
            ('ICAO_region',2,'5.14'), # 5.14 
            ('continuation_number',1,'5.16'), # 5.16
            ('frequency',5,'5.34'), # 5.34
            ('NAVAID_class',5,'5.35'), # 5.35
            ('latitude',9,'5.36'), # 5.36
            ('longitude',10,'5.37'), # 5.37
            ('DME_id',4,'5.38'), # 5.38
            ('DME_latitude',9,'5.36'), # 5.36
            ('DME_longitude',10,'5.37'),  # 5.37
            ('declination',5,'5.66'), # 5.66
            ('elevation',5,'5.40'), # 5.40
            ('FOM',1,'5.149'), # 5.149
            ('ILS_DME_bias',2,'5.90'), # 5.90
            ('frequency_protection',3,'5.150'), # 5.150
            ('datum',3,'5.197'), # 5.197
            ('name',30,'5.71'), # 5.71
            ('record_number',5,'5.31'), # 5.31
            ('cycle_date',4,'5.32','2') # 5.32
        ],
        'B': # (DB) Supported // NDB Navaids
        [
            ('NDB',[]),
            ('record_type',1,'5.2'), # 5.2
            ('area_code',3,'5.3'), # 5.3
            ('section_code',1,'5.4'), # 5.4
            ('subsection_code',1,'5.5'), # 5.5
            ('airport_id',4,'5.6'), # 5.6
            ('ICAO_region_code',2,'5.14'), # 5.14
            ('blank',1,'0'), 
            ('NDB_id',4,'5.33'), # 5.33
            ('blank',2,'0'),
            ('NDB_ICAO_region',2,'5.14'), # 5.14
            ('continuation_number',1,'5.16'), # 5.16
            ('frequency',5,'5.34'), # 5.34
            ('NDB_class',5,'5.35'), # 5.35
            ('latitude',9,'5.36'), # 5.36
            ('longitude',10,'5.37'), # 5.37
            ('blank',23,'0'), 
            ('variation',5,'5.39'), # 5.39
            ('blank',6,'0'), 
            ('reserved',5,'0'),
            ('datum',3,'5.197'), # 5.197
            ('name',30,'5.71'), # 5.71
            ('record_number',5,'5.31'), # 5.31
            ('cycle_date',4 ,'5.32') # 5.32
        ]
    },
    # See pg15(30 of PDF) for clarification on repeated subsection_code
    'E':{ # Enroute
        'A': # (EA) Supported // Enroute Waypoint
        [
            ('WAYPOINT',[]),
            ('record_type',1,'5.2'), # 5.2
            ('area_code',3,'5.3'), # 5.3
            ('section_code',1,'5.4'), # 5.4
            ('subsection_code',1,'5.5'), # 5.5
            ('region_code',4,'5.41'), # 5.41
            ('ICAO_region_code',2,'5.14'), # 5.14
            ('blank_subsection_code',1,'0'),
            ('waypoint_id',5,'5.14'), # 5.14
            ('blank',1,'0'), 
            ('ICAO_region',2,'5.14'), # 5.14 
            ('continuation_number',1,'5.16'), # 5.16
            ('blank',4,'0'),
            ('type',3,'5.42'), # 5.42
            ('usage',2,'5.82'), # 5.82
            ('blank',1,'0'),
            ('latitude',9,'5.36'), # 5.36
            ('longitude',10,'5.37'), # 5.37
            ('blank',23,'0'),
            ('dynamic_mag_variation',5,'5.39'), # 5.39
            ('reserved',5,'0'),
            ('datum',3,'5.197'), # 5.197
            ('reserved',8,'0'),
            ('name_format_indicator',3,'5.196'), # 5.196
            ('description',25,'5.43'), # 5.43
            ('record_number',5,'5.31'), # 5.31
            ('cycle_date',4,'5.32','3') # 5.32
        ],
        'R': # (ER) Supeported // Airways
        [ 
            ('AIRWAY', [
                ',longitude double precision,',
                'latitude double precision,',
                'declination real,'
                'vor_id integer,',
                'waypoint_id integer,',
                'ndb_id integer,',
                
                'constraint vor_id foreign key(vor_id) '+\
                'references vor(id) '+\
                'on delete set null ',
                
                ',constraint waypoint_id foreign key(waypoint_id) '+\
                'references waypoint(id) '+\
                'on delete set null',

                ',constraint ndb_id foreign key(ndb_id) '+\
                'references ndb(id) '+\
                'on delete set null',

            ]),
            ('record_type',1,'5.2'), # 5.2
            ('area_code',3,'5.3'), # 5.3
            ('section_code',1,'5.4'), # 5.4
            ('subsection_code',1,'5.5'), # 5.5
            ('blank',7,'0'),
            ('route_id',5,'5.8'), # 5.8
            ('reserved',1,'0'), 
            ('blank',6,'0'),
            ('sequence',4,'5.12'), # 5.12
            ('fix_id',5,'5.13'), # 5.13
            ('ICAO_region_code',2,'5.14'), # 5.14
            ('fix_section_code',1,'5.4'), # 5.4
            ('fix_subsection_code',1,'5.5'), # 5.5
            ('continuation_number',1,'5.16'), # 5.16
            ('description_code',4,'5.17'), # 5.17
            ('boundary_code',1,'5.18'), # 5.18
            ('route_type',1,'5.7'), # 5.7
            ('level',1,'5.19'), # 5.19
            ('direction_restriction',1,'5.115'), # 5.115
            ('cruise_table_indicator',2,'5.134'), # 5.134
            ('EU_indicator',1,'5.164'), # 5.164
            ('recommended_navaid',4,'5.23'), # 5.23
            ('recommended_navaid_ICAO_region_code',2,'5.14'), # 5.14
            ('RNP',3,'5.211'), # 5.211
            ('blank',3,'0'), 
            ('theta',4,'5.24'), # 5.24
            ('rho',4,'5.25'), # 5.25
            ('outbound_mag_course',4,'5.26'), # 5.26
            ('route_distance_from',4,'5.27'), # 5.27
            ('inbound_mag_course',4,'5.28'), # 5.28
            ('blank',1,'0'), 
            ('minimum_altitude',5,'5.30'), # 5.30
            ('minimum_altitude1',5,'5.30'), # 5.30 
            ('maximum_altitude',5,'5.127'), # 5.127 
            ('radius_transition_indicator',3,'5.254'), # 5.254
            ('reserved',22,'0'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32','6')
        ],
    },
    'H': {
        'A': # (HA) Supported // Airports and heliport
        [
            ('HELIPORT',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('blank',1,'0'),
            ('heliport_id',4,'5.6'),
            ('facility_ICAO_region_code',2,'5.14'),
            ('subsection_code',1,'5.5'),
            ('ATAIATA_designator',3,'5.107'),
            ('PAD_id',5,'5.180'),
            ('continuation_number',1,'5.16'),
            ('speed_limit_altitude',5,'5.73'),
            ('datum',3,'5.197'),
            ('IFR_indicator',1,'5.108'),
            ('blank',1,'0'),
            ('latitude',9,'5.36'),
            ('longitude',10,'5.37'),
            ('variation',5,'5.39'),
            ('elevation',5,'5.55'),
            ('speed_limit',3,'5.72'),
            ('recommended_VHF_navaid',4,'5.23'),
            ('recommended_VHF_navaid_ICO_region_code',2,'5.23'),
            ('transition_altitude',5,'5.53'),
            ('transition_level',5,'5.53'),
            ('public_military',1,'5.177'),
            ('timezone',3,'5.178'),
            ('DST_indicator',1,'5.179'),
            ('pad_dimensions',6,'5.176'),
            ('magnetic_true_indicator',1,'5.165'),
            ('reserved',1,'0'),
            ('name',30,'5.71'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32','10')
        ],
        'C': # (HC) Supported // Terminal Waypoints
        [
            ('HELIPORT_WAYPOINT',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('blank',1,'0'),
            ('heliport_id',4,'5.6'),
            ('facility_ICAO_region_code',2,'5.14'),
            ('subsection_code',1,'5.5'),
            ('waypoint_id',5,'5.13'),
            ('blank',1,'0'),
            ('waypoint_ICAO_region_code',2,'5.14'),
            ('continuation_number',1,'5.16'),
            ('blank',4,'0'),
            ('waypoint_type',3,'5.42'),
            ('waypoint_usage',2,'5.82'),
            ('blank',1,'0'),
            ('latitude',9,'5.36'),
            ('longitude',10,'5.37'),
            ('blank',23,'0'),
            ('dynamic_mag_variation',5,'5.39'),
            ('reserved',5,'0'),
            ('datum',3,'5.197'),
            ('reserved',8,'0'),
            ('name_format_indicator',3,'5.196'),
            ('description',25,'5.43'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32','11')
        ],
        'F': # (HF) Supported // Approaches, including LOS continuation records
        [
            ('HELIPORT_APPROACH',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('blank',1,'0'),
            ('heliport_id',4,'5.6'),
            ('facility_ICAO_region_code',2,'5.14'),
            ('subsection_code',1,'5.5'),
            ('SIDSTARAPP_id',6,'5.9'),
            ('route_type',1,'5.7'),
            ('transition_id',5,'5.11'),
            ('blank',1,'0'),
            ('sequence_number',3,'5.12'),
            ('fix_id',5,'5.13'),
            ('fix_ICAO_region_code',2,'5.14'),
            ('fix_section_code',1,'5.4'),
            ('fix_subsection_code',1,'5.5'),
            ('continuation_number',1,'5.16'),
            ('waypoint_description_code1',4,'5.17'),
            ('turn_direction',1,'5.20'),
            ('RNP',3,'5.211'),
            ('path_and_termination',2,'5.21'),
            ('turn_direction_valid',1,'5.22'),
            ('recommended_navaid',4,'5.23'),
            ('recommended_navaid_ICAO_region_code',2,'5.14'),
            ('ARC_radius',6,'5.204'),
            ('theta',4,'5.24'),
            ('rho',4,'5.25'),
            ('magnetic_course',4,'5.26'),
            ('route_distance_holding_dstance_or_time',4,'5.27'),
            ('recommended_navaid_section',1,'5.4'),
            ('recommended_navaid_subsection',1,'5.5'),
            ('reservedSpacing',2,'0'),
            ('altitude_description',1,'5.29'),
            ('ATC_indicator',1,'5.81'),
            ('altitude',5,'5.30'),
            ('altitude1',5,'5.30'),
            ('transition_altitude',5,'5.53'),
            ('speed_limit',3,'5.72'),
            ('vertical_angle',4,'5.70'),
            ('center_fix_or_TAA_procedure_turn_indicator',5,'5.144'),
            ('multiple_code_or_TAA_sector_id',1,'5.130'),
            ('center_fix_or_TAA_procedure_turn_indicator_ICAO_RC',2,'5.14'),
            ('center_fix_or_TAA_procedure_turn_indicator_SC',1,'5.4'),
            ('center_fix_or_TAA_procedure_turn_Indicator_SSC',1,'5.5'),
            ('GNSS_FMS_indicator',1,'5.222'),
            ('speed_limit_description',1,'5.261'),
            ('apch_route_qualifier1',1,'5.7'),
            ('apch_route_qualifier2',1,'5.7'),
            ('blank',3,'0'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.31','14')
        ],
        'S': # (HS) Supported // MSA Records
        [
            ('HELIPORT_MSA',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('blank',1,'0'),
            ('heliport_id',4,'5.6'),
            ('facility_ICAO_region_code',2,'5.14'),
            ('subsection_code',1,'5.5'),
            ('MSA_center',5,'5.144'),
            ('MSA_center_ICAO_region_code',2,'5.14'),
            ('MSA_center_section_code',1,'5.4'),
            ('MSA_center_subsection_code',1,'5.5'),
            ('multiple_code',1,'5.130'),
            ('reserved',15,'0'),
            ('continuation_number',1,'5.16'),
            ('reserved',3,'0'),
            #---------------------------
            ('sector_bearing1',6,'5.146'),
            ('sector_altitude1',3,'5.147'),
            ('sector_radius1',2,'5.145'),
            #---------------------------
            ('sector_bearing2',6,'5.146'),
            ('sector_altitude2',3,'5.147'),
            ('sector_radius2',2,'5.145'),
            #---------------------------
            ('sector_bearing3',6,'5.146'),
            ('sector_altitude3',3,'5.147'),
            ('sector_radius3',2,'5.145'),
            #---------------------------
            ('sector_bearing4',6,'5.146'),
            ('sector_altitude4',3,'5.147'),
            ('sector_radius4',2,'5.145'),
            #---------------------------
            ('sector_bearing5',6,'5.146'),
            ('sector_altitude5',3,'5.147'),
            ('sector_radius5',2,'5.145'),
            #---------------------------
            ('sector_bearing6',6,'5.146'),
            ('sector_altitude6',3,'5.147'),
            ('sector_radius6',2,'5.145'),
            #---------------------------
            ('sector_bearing7',6,'5.146'),
            ('sector_altitude7',3,'5.147'),
            ('sector_radius7',2,'5.145'),
            #---------------------------
            ('magnetic_true_indicator',1,'5.165'),
            ('reserved',3,'0'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32','16')
        ],
    },
    'P':
    {
        'A': # (PA) Supported // Airports and heliport
        [
            ('AIRPORT',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('blank',1,'0'),
            ('airport_id',4,'5.6'),
            ('facility_ICAO_region_code',2,'5.14'),
            ('subsection_code',1,'5.5'),
            ('ATAIATA_designator',3,'5.107'),
            ('reserved',2,'0'),
            ('blank',3,'0'),
            ('continuation_number',1,'5.16'),
            ('speed_limit_altitude',5,'5.73'),
            ('longest_runway',3,'5.54'),
            ('IFR_capability',1,'5.108'),
            ('longest_runway_surface_code',1,'5.249'),
            ('airport_reference_pt_latitude',9,'5.36'),
            ('airport_reference_pt_longitude',10,'5.37'),
            ('magnetic_variation',5,'5.39'),
            ('airport_elevation',5,'5.55'),
            ('speed_limit',3,'5.72'),
            ('recommended_navaid',4,'5.23'),
            ('recommended_navaid_ICAO_region_code',2,'5.14'),
            ('transitions_altitude',5,'5.53'),
            ('transition_level',5,'5.53'),
            ('public_military_indicator',1,'5.177'),
            ('time_zone',3,'5.178'),
            ('daylight_indicator',1,'5.179'),
            ('magnetic_true_indicator',1,'5.165'),
            ('datum',3,'5.197'),
            ('reserved',4,'0'),
            ('name',30,'5.71'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32')
        ],
        'C': # (PC) Supported // Airport Waypoints
        [
            ('AIRPORT_WAYPOINT',[] ),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('subsection_code',1,'5.5'),
            ('region_code',4,'5.41'),
            ('ICAO_region_code',2,'5.14'),
            ('subsection',1,'5.5'),
            ('waypoint_id',5,'5.13'),
            ('blank',1,'0'),
            ('waypoint_ICAO_region_code',2,'5.14'),
            ('continuation_number',1,'5.16'),
            ('blank',4,'0'),
            ('waypoint_type',3,'5.42'),
            ('waypoint_usage',2,'5.82'),
            ('blank',1,'0'),
            ('latitude',9,'5.36'),
            ('longitude',10,'5.37'),
            ('blank',23,'0'),
            ('dynamic_mag_variation',5,'5.39'),
            ('reserved',5,'0'),
            ('datum',3,'5.197'),
            ('reserved',8,'0'),
            ('name_format_indicator',3,'5.196'),
            ('waypoint_name_description',25,'5.43'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32')
        ],
        'D': # (PD) Supported // SIDs
          [
              ('SID',[]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('SIDSTAR_approach_id',6,'5.9'), # 5.10 too
              ('route_type',1,'5.7'),
              ('transition_id',5,'5.11'),
              ('blank',1,'0'),
              ('sequence_number',3,'5.12'),
              ('fix_id',5,'5.13'),
              ('fix_ICAO_region_code',2,'5.14'),
              ('fix_section_code',1,'5.4'),
              ('fix_subsection_code',1,'5.5'),
              ('continuation_number',1,'5.16'),
              ('waypoint_description_code',4,'5.17'),
              ('turn_direction',1,'5.20'),
              ('RNP',3,'5.211'),
              ('path_and_termination',2,'5.21'),
              ('turn_direction_valid',1,'5.22'),
              ('recommended_navaid',4,'5.23'),
              ('recommended_navaid_ICAO_region_code',2,'5.14'),
              ('ARC_radius',6,'5.204'),
              ('theta',4,'5.24'),
              ('rho',4,'5.25'),
              ('magnetic_course',4,'5.26'),
              ('route_distance_holding_distance_or_time',4,'5.27'),
              ('recommended_NAVAID_section',1,'5.4'),
              ('recommended_NAVAID_subsection',1,'5.5'),
              ('reserved',2,'0'),
              ('altitude_description',1,'5.29'),
              ('ATC_indicator',1,'5.81'),
              ('altitude',5,'5.30'),
              ('altitude1',5,'5.30'),
              ('transition_altitude',5,'5.53'),
              ('speed_limit',3,'5.72'),
              ('vertical_angle',4,'5.70'),
              ('center_fix_or_TAA_procedure_turn_indicator',5,'5.144'), # Or 5.271
              ('multiple_code_or_TAA_Sector_id',1,'5.130'), # Or 5.272
              ('center_fix_or_TAA_procedure_turn_indicator_ICAO_RC',2,'0','5.14'),
              ('center_fix_or_TAA_procedure_turn_indicator_SC',1,'5.4'),
              ('center_fix_or_TAA_procedure_turn_indicator_SSC',1,'5.5'),
              ('GNSS_FMS_indication',1,'5.22'),
              ('speed_limit_description',1,'5.261'),
              ('apch_route_qualifier1',1,'5.7'),
              ('apch_route_qualifier2',1,'5.7'),
              ('blank',3,'0'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32','21')
          ],
        'E': # (PE) Supported // STARs
          [
              ('STAR',[]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('SIDSTAR_approach_id',6,'5.9'), # 5.10 too
              ('route_type',1,'5.7'),
              ('transition_id',5,'5.11'),
              ('blank',1,'0'),
              ('sequence_number',3,'5.12'),
              ('fix_id',5,'5.13'),
              ('fix_ICAO_region_code',2,'5.14'),
              ('fix_section_code',1,'5.4'),
              ('fix_subsection_code',1,'5.5'),
              ('continuation_number',1,'5.16'),
              ('waypoint_description_code',4,'5.17'),
              ('turn_direction',1,'5.20'),
              ('RNP',3,'5.211'),
              ('path_and_termination',2,'5.21'),
              ('turn_direction_valid',1,'5.22'),
              ('recommended_navaid',4,'5.23'),
              ('recommended_navaid_ICAO_region_code',2,'5.14'),
              ('ARC_radius',6,'5.204'),
              ('theta',4,'5.24'),
              ('rho',4,'5.25'),
              ('magnetic_course',4,'5.26'),
              ('route_distance_holding_distance_or_time',4,'5.27'),
              ('recommended_NAVAID_section',1,'5.4'),
              ('recommended_NAVAID_subsection',1,'5.5'),
              ('reserved',2,'0'),
              ('altitude_description',1,'5.29'),
              ('ATC_indicator',1,'5.81'),
              ('altitude',5,'5.30'),
              ('altitude1',5,'5.30'),
              ('transition_altitude',5,'5.53'),
              ('speed_limit',3,'5.72'),
              ('vertical_angle',4,'5.70'),
              ('center_fix_or_TAA_procedure_turn_indicator',5,'5.144'), # Or 5.271
              ('multiple_code_or_TAA_Sector_id',1,'5.130'), # Or 5.272
              ('center_fix_or_TAA_procedure_turn_indicator_ICAO_RC',2,'0','5.14'),
              ('center_fix_or_TAA_procedure_turn_indicator_SC',1,'5.4'),
              ('center_fix_or_TAA_procedure_turn_indicator_SSC',1,'5.5'),
              ('GNSS_FMS_indication',1,'5.22'),
              ('speed_limit_description',1,'5.261'),
              ('apch_route_qualifier1',1,'5.7'),
              ('apch_route_qualifier2',1,'5.7'),
              ('blank',3,'0'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32','21')
          ],
        'F': # (PF) Supported // Approaches, including LOS continuation records
          [
              ('APPROACH',[]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('approach_id',6,'5.9'), # 5.10 too
              ('route_type',1,'5.7'),
              ('transition_id',5,'5.11'),
              ('blank',1,'0'),
              ('sequence_number',3,'5.12'),
              ('fix_id',5,'5.13'),
              ('fix_ICAO_region_code',2,'5.14'),
              ('fix_section_code',1,'5.4'),
              ('fix_subsection_code',1,'5.5'),
              ('continuation_number',1,'5.16'),
              ('waypoint_description_code',4,'5.17'),
              ('turn_direction',1,'5.20'),
              ('RNP',3,'5.211'),
              ('path_and_termination',2,'5.21'),
              ('turn_direction_valid',1,'5.22'),
              ('recommended_navaid',4,'5.23'),
              ('recommended_navaid_ICAO_region_code',2,'5.14'),
              ('ARC_radius',6,'5.204'),
              ('theta',4,'5.24'),
              ('rho',4,'5.25'),
              ('magnetic_course',4,'5.26'),
              ('route_distance_holding_distance_or_time',4,'5.27'),
              ('recommended_NAVAID_section',1,'5.4'),
              ('recommended_NAVAID_subsection',1,'5.5'),
              ('reserved',2,'0'),
              ('altitude_description',1,'5.29'),
              ('ATC_indicator',1,'5.81'),
              ('altitude',5,'5.30'),
              ('altitude1',5,'5.30'),
              ('transition_altitude',5,'5.53'),
              ('speed_limit',3,'5.72'),
              ('vertical_angle',4,'5.70'),
              ('center_fix_or_TAA_procedure_turn_indicator',5,'5.144'), # Or 5.271
              ('multiple_code_or_TAA_Sector_id',1,'5.130'), # Or 5.272
              ('center_fix_or_TAA_procedure_turn_indicator_ICAO_RC',2,'0','5.14'),
              ('center_fix_or_TAA_procedure_turn_indicator_SC',1,'5.4'),
              ('center_fix_or_TAA_procedure_turn_indicator_SSC',1,'5.5'),
              ('GNSS_FMS_indication',1,'5.22'),
              ('speed_limit_description',1,'5.261'),
              ('apch_route_qualifier1',1,'5.7'),
              ('apch_route_qualifier2',1,'5.7'),
              ('blank',3,'0'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32','21')            
          ],
        'G': # (PG) Supported // Runways
          [
              ('RUNWAY',[
                  ',airport_fid integer,'+\
                  'constraint airport_fid foreign key(airport_fid) '+\
                  'references airport(id) '+\
                  'on delete set null ',
              ]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('runway_id',5,'5.46'),
              ('blank',3,'0'),
              ('continuation_number',1,'5.16'),
              ('runway_length',5,'5.57'),
              ('runway_magnetic_bearing',4,'5.58'),
              ('blank',1,'0'),
              ('latitude',9,'5.36'),
              ('longitude',10,'5.37'),
              ('runway_gradient',5,'5.212'),
              ('blank',10,'0'),
              ('landing_threshold_elevation',5,'5.68'),
              ('displaced_threshold_distance',4,'5.69'),
              ('threshold_crossing_height',2,'5.67'),
              ('runway_width',3,'5.109'),
              ('TCH_value_indicator',1,'5.270'),
              ('localizer_MLS_GLS_ref_path_id',4,'5.44'),
              ('localizer_MLS_GLS_category_class',1,'5.80'),
              ('stopway',4,'5.79'),
              ('second_localizer_MLS_GLS_ref_path_id',4,'5.44'),
              ('second_localizer_MLS_GLS_category_class',1,'5.80'),
              ('reserved',6,'0'),
              ('runway_description',22,'5.59'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32')
          ],
        'I': # (PI) Supported // Localizer and Glide Slope Records
          [
              ('LOCALIZER',[
                  ',runway_fid integer,'+\
                  'constraint runway_fid foreign key(runway_fid) '+\
                  'references runway(id) '+\
                  'on delete set null ',
              ]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('localizer_id',4,'5.44'),
              ('ILS_category',1,'5.80'),
              ('blank',3,'0'),
              ('continuation_number',1,'5.16'),
              ('frequency',5,'5.45'),
              ('runway_id',5,'5.46'),
              ('latitude',9,'5.36'),
              ('longitude',10,'5.37'),
              ('localizer_bearing',4,'5.47'),
              ('glide_slope_latitude',9,'5.36'),
              ('glide_slope_longitude',10,'5.37'),
              ('localizer_position',4,'5.50'),
              ('localizer_position_ref',1,'5.49'),
              ('glide_slope_position',4,'5.50'),
              ('localizer_width',4,'5.51'),
              ('glide_slope_angle',3,'5.52'),
              ('station_declination',5,'5.66'),
              ('glide_slope_height_at_landing_threshold',2,'5.67'),
              ('glide_slope_elevation',5,'5.74'),
              ('supporting_facility_id',4,'5.33'),
              ('supporting_facility_ICAO_region_code',2,'5.14'),
              ('supporting_facilitys_section_code',1,'5.4'),
              ('supporting_facility_subsection_code',1,'5.5'),
              ('reserved',13,'0'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32')
          ],
        'N': # (PN) Supported // Terminal Navaids
          [
              ('AIRPORT_NDB',[
                  ',airport_fid integer,'+\
                  'constraint airport_fid foreign key(airport_fid) '+\
                  'references airport(id) '+\
                  'on delete set null ',
              ]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('subsection_code',1,'5.5'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('blank',1,'0'),
              ('NDB_id',4,'5.33'),
              ('blank',2,'0'),
              ('NDB_ICAO_region_code',2,'5.14'),
              ('continuation_number',1,'5.16'),
              ('frequency',5,'5.34'),
              ('NDB_class',5,'5.35'),
              ('latitude',9,'5.36'),
              ('longitude',10,'5.37'),
              ('blank',23,'0'),
              ('magnetic_variation',5,'5.39'),
              ('blank',6,'0'),
              ('reserved',5,'0'),
              ('datum',3,'5.197'),
              ('name',30,'5.71'),
              ('record_number',5,'5.31'),
              ('CycleData',4,'5.32'),
          ],
        'P': # (PP) Supported // Path Point Records, Primary and Continuation
          [
              ('AIRPORT_WAYPOINT',[
                  ',airport_fid integer,'+\
                  'constraint airport_fid foreign key(airport_fid) '+\
                  'references airport(id) '+\
                  'on delete set null ',
              ]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('LandingFacilityIcaoRegionCode',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('approach_id',6,'5.10'),
              ('runway_id',5,'5.46'), # Could be 5.180
              ('OperationType',2,'5.223'),
              ('continuation_number',1,'5.16'),
              ('route_id',1,'5.224'),
              ('SBASServiceProviderIdentifier',2,'5.255'),
              ('ReferencePathDataSelector',2,'5.256'),
              ('ReferencePathIdentifier',4,'5.257'),
              ('ApproachPerformanceDesignator',1,'5.258'),
              ('LandingThresholdPointLatitude',11,'5.267'),
              ('LandingThresholdPointLongitude',12,'5.267'),
              ('LTPEllipsoidHeight',6,'5.225'),
              ('GlidePathAngle',4,'5.226'),
              ('FlightPathAlignmentPointLatitude',11,'5.267'),
              ('FlightPathAlignmentPointLongitude',12,'5.268'),
              ('CourseWidthatThreshold',5,'5.228'),
              ('LengthOffset',4,'5.259'),
              ('PathPointTCH',6,'5.265'),
              ('TCHUnitsIndicator',1,'5.266'),
              ('HAL',3,'5.263'),
              ('VAL',3,'5.264'),
              ('SBASFASDataCRCRemainder',8,'5.229'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32')
          ],
        'S': # (PS) Supported // MSA Records 
          [
              ('AIRPORT_MSA',[
                  ',airport_fid integer,'+\
                  'constraint airport_fid foreign key(airport_fid) '+\
                  'references airport(id) '+\
                  'on delete set null ',
              ]),
              ('record_type',1,'5.2'),
              ('area_code',3,'5.3'),
              ('section_code',1,'5.4'),
              ('blank',1,'0'),
              ('airport_id',4,'5.6'),
              ('facility_ICAO_region_code',2,'5.14'),
              ('subsection_code',1,'5.5'),
              ('MSA_center',5,'5.144'),
              ('MSA_center_ICAO_region_code',2,'5.14'),
              ('MSA_center_section_code',1,'5.4'),
              ('MSA_center_subsection_code',1,'5.5'),
              ('multiple_code',1,'5.130'),
              ('reserved',15,'0'),
              ('continuation_number',1,'5.16'),
              ('reserved',3,'0'),
              ('sector_bearing1',6,'5.146'),
              ('sector_altitude1',3,'5.147'),
              ('sector_radius1',2,'5.145'),
              ('sector_bearing2',6,'5.146'),
              ('sector_altitude2',3,'5.147'),
              ('sector_radius2',2,'5.145'),
              ('sector_bearing3',6,'5.146'),
              ('sector_altitude3',3,'5.147'),
              ('sector_radius3',2,'5.145'),
              ('sector_bearing4',6,'5.146'),
              ('sector_altitude4',3,'5.147'),
              ('sector_radius4',2,'5.145'),
              ('sector_bearing5',6,'5.146'),
              ('sector_altitude5',3,'5.147'),
              ('sector_radius5',2,'5.145'),
              ('sector_bearing6',6,'5.146'),
              ('sector_altitude6',3,'5.147'),
              ('sector_radius6',2,'5.145'),
              ('sector_bearing7',6,'5.146'),
              ('sector_altitude7',3,'5.147'),
              ('sector_radius7',2,'5.145'),
              ('magnetic_true_indicator',1,'5.165'),
              ('reserved',3,'0'),
              ('record_number',5,'5.31'),
              ('cycle_date',4,'5.32')
          ],
      },
    'U':{
        'C': # (UC) Supported // Class B,C and D Airspace
        [
            ('CONTROLLED_AIRSPACE',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('subsection_code',1,'5.5'),
            ('ICAO_region_code',2,'5.14'),
            ('airspace_type',1,'5.213'),
            ('airspace_center',5,'5.214'),
            ('airspace_center_section_code',1,'5.4'),
            ('airspace_center_subsection_code',1,'5.5'),
            ('airspace_classification',1,'5.215'),
            ('reserved',2,'0'),
            ('multiple_code',1,'5.130'),
            ('sequenc_number',4,'5.12'),
            ('continuation_number',1,'5.16'),
            ('level',1,'5.19'),
            ('time_code',1,'5.131'),
            ('NOTAM',1,'5.132'),
            ('blank',2,'0'),
            ('boundary_Via',2,'5.118'),
            ('latitude',9,'5.36'),
            ('longitude',10,'5.37'),
            ('arc_origin_latitude',9,'5.36'),
            ('arc_origin_longitude',10,'5.37'),
            ('arc_distance',4,'5.119'),
            ('arc_bearing',4,'5.120'),
            ('RNP',3,'5.211'),
            ('lower_limit',5,'5.121'),
            ('unit_indicator_L',1,'5.133'),
            ('upper_limit',5,'5.121'),
            ('unit_Indicator_U',1,'5.133'),
            ('name',30,'5.216'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32')
        ],
        'R': # (UR) Supported // Special Use Airspace, Primary and Continuation
        [
            ('SPECIAL_AIRSPACE',[]),
            ('record_type',1,'5.2'),
            ('area_code',3,'5.3'),
            ('section_code',1,'5.4'),
            ('subsection_code',1,'5.5'),
            ('ICAO_region_code',2,'5.14'),
            ('restrictive_type',1,'5.128'),
            ('restrictive_airspace_designation',10,'5.129'),
            ('multiple_code',1,'5.130'),
            ('sequence_number',4,'5.12'),
            ('continuation_number',1,'5.16'),
            ('level',1,'5.19'),
            ('time_code',1,'5.131'),
            ('NOTAM',1,'5.132'),
            ('blank',2,'0'),
            ('boundary_via',2,'5.118'),
            ('latitude',9,'5.36'),
            ('longitude',10,'5.37'),
            ('arc_origin_latitude',9,'5.36'),
            ('arc_origin_longitude',10,'5.37'),
            ('arc_distance',4,'5.119'),
            ('arc_bearing',4,'5.120'),
            ('blank',3,'0'),
            ('lower_limit',5,'5.121'),
            ('unit_indicator_L',1,'5.133'),
            ('upper_limit',5,'5.121'),
            ('unit_indicator_U',1,'5.133'),
            ('name',30,'5.126'),
            ('record_number',5,'5.31'),
            ('cycle_date',4,'5.32')
        ]
    }
}
if __name__ == '__main__':
    for k in PARSE_DEF.keys():
        print(k,end=' ')
        for kk in PARSE_DEF[k].keys():
            print(kk,end=' ')
            total_fields = 0
            for tup in PARSE_DEF[k][kk]:
                total_fields = total_fields + tup[1]
            if total_fields != 132:
                print('err',k,kk,total_fields)
        print('\n')
